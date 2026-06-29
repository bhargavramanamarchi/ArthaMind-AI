"""
ArthaMind AI — RAG (Retrieval Augmented Generation) Module
============================================================
Knowledge base management using ChromaDB and sentence-transformers.
Handles document ingestion, semantic search, and source citations.
"""

import os
from pathlib import Path
from typing import Any, Optional

from config import CHROMA_DIR, DATA_DIR, settings
from utils import logger, timer


# ═══════════════════════════════════════════════════════════════
#  KNOWLEDGE BASE
# ═══════════════════════════════════════════════════════════════

class KnowledgeBase:
    """RAG knowledge base using ChromaDB for vector storage and
    sentence-transformers for embeddings.

    Attributes:
        embeddings: HuggingFace embedding model.
        vectorstore: ChromaDB vector store instance.
        retriever: LangChain retriever for semantic search.
    """

    def __init__(self):
        """Initialize the knowledge base with embeddings and vector store."""
        self.embeddings = None
        self.vectorstore = None
        self.retriever = None
        self._initialized = False

    @timer
    def initialize(self) -> bool:
        """Load embeddings, initialize ChromaDB, and ingest documents if needed.

        Returns:
            True if initialization succeeded.
        """
        if self._initialized:
            return True

        try:
            from langchain_huggingface import HuggingFaceEmbeddings
            from langchain_chroma import Chroma

            logger.info("Initializing embeddings model...")
            self.embeddings = HuggingFaceEmbeddings(
                model_name=settings.EMBEDDING_MODEL,
                model_kwargs={"device": settings.EMBEDDING_DEVICE},
                encode_kwargs={"normalize_embeddings": True},
            )

            # Check if vectorstore already has data
            chroma_path = str(CHROMA_DIR)
            self.vectorstore = Chroma(
                collection_name=settings.CHROMA_COLLECTION,
                embedding_function=self.embeddings,
                persist_directory=chroma_path,
            )

            # If empty, ingest the knowledge base documents
            collection = self.vectorstore._collection
            if collection.count() == 0:
                logger.info("Empty knowledge base — ingesting documents...")
                self._ingest_documents()
            else:
                logger.info(f"Knowledge base loaded with {collection.count()} chunks")

            # Create retriever
            self.retriever = self.vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={"k": settings.RAG_TOP_K},
            )

            self._initialized = True
            logger.info("Knowledge base initialized successfully")
            return True

        except Exception as exc:
            logger.error(f"Knowledge base initialization failed: {exc}")
            self._initialized = False
            return False

    def _ingest_documents(self) -> None:
        """Ingest all markdown documents from the data directory."""
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        from langchain_core.documents import Document

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.RAG_CHUNK_SIZE,
            chunk_overlap=settings.RAG_CHUNK_OVERLAP,
            separators=["\n## ", "\n### ", "\n\n", "\n", ". ", " "],
        )

        all_chunks: list[Document] = []
        data_files = list(DATA_DIR.glob("*.md"))

        if not data_files:
            logger.warning(f"No .md files found in {DATA_DIR}")
            return

        for filepath in data_files:
            try:
                content = filepath.read_text(encoding="utf-8")
                doc_name = filepath.stem.replace("_", " ").title()

                # Extract metadata from header comments
                source_url = self._extract_metadata(content, "URL")
                source_org = self._extract_metadata(content, "Source")

                # Split into chunks
                chunks = text_splitter.create_documents(
                    texts=[content],
                    metadatas=[{
                        "source": doc_name,
                        "file": filepath.name,
                        "url": source_url or "",
                        "organization": source_org or "",
                    }],
                )

                # Add section info to each chunk
                for i, chunk in enumerate(chunks):
                    chunk.metadata["chunk_index"] = i
                    chunk.metadata["section"] = self._extract_section(chunk.page_content)

                all_chunks.extend(chunks)
                logger.info(f"Processed {filepath.name}: {len(chunks)} chunks")

            except Exception as exc:
                logger.error(f"Failed to process {filepath.name}: {exc}")

        if all_chunks:
            logger.info(f"Adding {len(all_chunks)} chunks to vector store...")
            self.vectorstore.add_documents(all_chunks)
            logger.info("Document ingestion complete")

    @staticmethod
    def _extract_metadata(content: str, key: str) -> str:
        """Extract metadata value from document header comments.

        Args:
            content: Document text.
            key: Metadata key to search for (e.g. 'Source', 'URL').

        Returns:
            Extracted value or empty string.
        """
        for line in content.split("\n")[:10]:
            if line.startswith("#") and key + ":" in line:
                return line.split(key + ":")[1].strip()
        return ""

    @staticmethod
    def _extract_section(text: str) -> str:
        """Extract the nearest section heading from a text chunk.

        Args:
            text: Chunk text.

        Returns:
            Section heading or 'General'.
        """
        for line in text.split("\n"):
            stripped = line.strip()
            if stripped.startswith("## "):
                return stripped.replace("## ", "").strip()
            if stripped.startswith("### "):
                return stripped.replace("### ", "").strip()
        return "General"

    @timer
    def search(self, query: str, top_k: Optional[int] = None) -> list[dict[str, Any]]:
        """Search the knowledge base for relevant documents.

        Args:
            query: Search query string.
            top_k: Number of results to return (overrides default).

        Returns:
            List of result dictionaries with content, metadata, and relevance score.
        """
        if not self._initialized:
            logger.warning("Knowledge base not initialized, attempting initialization...")
            if not self.initialize():
                return []

        try:
            k = top_k or settings.RAG_TOP_K
            results = self.vectorstore.similarity_search_with_relevance_scores(query, k=k)

            formatted_results = []
            for doc, score in results:
                formatted_results.append({
                    "content": doc.page_content,
                    "source": doc.metadata.get("source", "Unknown"),
                    "section": doc.metadata.get("section", "General"),
                    "url": doc.metadata.get("url", ""),
                    "file": doc.metadata.get("file", ""),
                    "relevance_score": round(score, 4),
                })

            logger.info(f"Search for '{query[:50]}...' returned {len(formatted_results)} results")
            return formatted_results

        except Exception as exc:
            logger.error(f"Search failed: {exc}")
            return []

    def format_context(self, results: list[dict[str, Any]]) -> str:
        """Format search results as context for the LLM prompt.

        Args:
            results: List of search result dictionaries.

        Returns:
            Formatted context string with source citations.
        """
        if not results:
            return "No relevant documents found in the knowledge base."

        context_parts = []
        for i, r in enumerate(results, 1):
            part = (
                f"[Document {i}]\n"
                f"Source: {r['source']}\n"
                f"Section: {r['section']}\n"
                f"Content: {r['content']}\n"
            )
            context_parts.append(part)

        return "\n---\n".join(context_parts)

    def format_citations(self, results: list[dict[str, Any]]) -> str:
        """Format source citations as markdown for display.

        Args:
            results: List of search result dictionaries.

        Returns:
            Markdown-formatted citation block.
        """
        if not results:
            return ""

        seen_sources = set()
        citations = []

        for r in results:
            source_key = f"{r['source']}|{r['section']}"
            if source_key in seen_sources:
                continue
            seen_sources.add(source_key)

            citation = f"📄 **{r['source']}** — {r['section']}"
            if r.get("url"):
                citation += f" | [Link]({r['url']})"
            citations.append(citation)

        return "\n\n---\n**📚 Sources:**\n" + "\n".join(f"- {c}" for c in citations)

    @property
    def document_count(self) -> int:
        """Return the number of document chunks in the knowledge base."""
        if self.vectorstore:
            try:
                return self.vectorstore._collection.count()
            except Exception:
                return 0
        return 0

    @property
    def is_ready(self) -> bool:
        """Check if the knowledge base is initialized and ready."""
        return self._initialized


# ── Module-level singleton ──────────────────────────────────
knowledge_base = KnowledgeBase()
