"""
ArthaMind AI — Voice Assistant Module
=======================================
Speech-to-text (AssemblyAI) and text-to-speech (Murf AI / gTTS)
pipeline for multilingual voice interaction.
"""

import os
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from config import ASSETS_DIR, settings
from utils import logger, timer


# ═══════════════════════════════════════════════════════════════
#  SPEECH-TO-TEXT
# ═══════════════════════════════════════════════════════════════

class SpeechToText:
    """Transcribes audio using AssemblyAI with automatic language detection."""

    def __init__(self):
        self._client = None
        self._available = False
        self._initialize()

    def _initialize(self) -> None:
        """Initialize the AssemblyAI client if API key is available."""
        if not settings.ASSEMBLYAI_API_KEY:
            logger.info("AssemblyAI API key not configured — STT disabled")
            return

        try:
            import assemblyai as aai
            aai.settings.api_key = settings.ASSEMBLYAI_API_KEY
            self._client = aai
            self._available = True
            logger.info("AssemblyAI STT initialized")
        except ImportError:
            logger.warning("assemblyai package not installed")
        except Exception as exc:
            logger.error(f"AssemblyAI initialization failed: {exc}")

    @timer
    def transcribe(self, audio_path: str) -> dict[str, Any]:
        """Transcribe an audio file to text with language detection.

        Args:
            audio_path: Path to the audio file (wav, mp3, webm, etc.).

        Returns:
            Dictionary with 'text', 'language', 'confidence', and 'status'.
        """
        if not self._available:
            return {
                "text": "",
                "language": "unknown",
                "status": "error",
                "error": "Speech-to-text service is not configured. Please add ASSEMBLYAI_API_KEY to your .env file.",
            }

        try:
            aai = self._client

            config = aai.TranscriptionConfig(
                language_detection=True,
            )

            transcriber = aai.Transcriber(config=config)
            transcript = transcriber.transcribe(audio_path)

            if transcript.status == aai.TranscriptStatus.error:
                return {
                    "text": "",
                    "language": "unknown",
                    "status": "error",
                    "error": f"Transcription failed: {transcript.error}",
                }

            detected_language = "en"
            try:
                lang_code = transcript.json_response.get("language_code", "en")
                detected_language = lang_code
            except Exception:
                pass

            return {
                "text": transcript.text or "",
                "language": detected_language,
                "status": "success",
            }

        except Exception as exc:
            logger.error(f"Transcription error: {exc}")
            return {
                "text": "",
                "language": "unknown",
                "status": "error",
                "error": f"Transcription failed: {str(exc)}",
            }

    @property
    def is_available(self) -> bool:
        """Check if speech-to-text is available."""
        return self._available


# ═══════════════════════════════════════════════════════════════
#  TEXT-TO-SPEECH
# ═══════════════════════════════════════════════════════════════

class TextToSpeech:
    """Text-to-speech with Murf AI primary and gTTS fallback."""

    def __init__(self):
        self._murf_available = False
        self._gtts_available = False
        self._initialize()

    def _initialize(self) -> None:
        """Initialize TTS engines."""
        # Try Murf AI
        if settings.MURF_API_KEY:
            try:
                import requests as _req  # noqa: F401
                self._murf_available = True
                logger.info("Murf AI TTS available")
            except Exception as exc:
                logger.warning(f"Murf AI initialization failed: {exc}")

        # Try gTTS (fallback, always available)
        try:
            from gtts import gTTS as _gTTS  # noqa: F401
            self._gtts_available = True
            logger.info("gTTS fallback TTS available")
        except ImportError:
            logger.warning("gTTS not installed — TTS disabled")

    @timer
    def synthesize(self, text: str, language: str = "en") -> Optional[str]:
        """Convert text to speech audio file.

        Args:
            text: Text to speak.
            language: ISO language code (en, hi, te, ta, kn, ml).

        Returns:
            Path to the generated audio file, or None on failure.
        """
        if not text.strip():
            return None

        # Truncate very long text for TTS
        if len(text) > 3000:
            text = text[:3000] + "..."

        # Try Murf AI first
        if self._murf_available:
            result = self._synthesize_murf(text, language)
            if result:
                return result

        # Fallback to gTTS
        if self._gtts_available:
            return self._synthesize_gtts(text, language)

        logger.warning("No TTS engine available")
        return None

    def _synthesize_murf(self, text: str, language: str) -> Optional[str]:
        """Synthesize speech using Murf AI API.

        Args:
            text: Text to speak.
            language: ISO language code.

        Returns:
            Path to audio file or None.
        """
        try:
            import requests

            # Map language codes to Murf AI locales
            locale_map = {
                "en": "en-IN",
                "hi": "hi-IN",
                "te": "te-IN",
                "ta": "ta-IN",
                "kn": "kn-IN",
                "ml": "ml-IN",
            }
            locale = locale_map.get(language, "en-IN")

            url = "https://api.murf.ai/v1/speech/generate"
            headers = {
                "Authorization": f"Bearer {settings.MURF_API_KEY}",
                "Content-Type": "application/json",
            }
            payload = {
                "text": text,
                "voiceId": f"{locale}-default",
                "format": "MP3",
                "sampleRate": 22050,
            }

            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()

            audio_url = data.get("audioFile")
            if audio_url:
                # Download the audio file
                audio_response = requests.get(audio_url, timeout=30)
                output_path = os.path.join(
                    tempfile.gettempdir(),
                    f"arthamind_tts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
                )
                with open(output_path, "wb") as f:
                    f.write(audio_response.content)
                return output_path

        except Exception as exc:
            logger.warning(f"Murf AI TTS failed, falling back to gTTS: {exc}")

        return None

    def _synthesize_gtts(self, text: str, language: str) -> Optional[str]:
        """Synthesize speech using Google TTS (free fallback).

        Args:
            text: Text to speak.
            language: ISO language code.

        Returns:
            Path to audio file or None.
        """
        try:
            from gtts import gTTS

            tts_lang = settings.GTTS_LANGUAGE_MAP.get(language, "en")
            tts = gTTS(text=text, lang=tts_lang, slow=False)

            output_path = os.path.join(
                tempfile.gettempdir(),
                f"arthamind_tts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
            )
            tts.save(output_path)
            logger.info(f"gTTS audio saved: {output_path}")
            return output_path

        except Exception as exc:
            logger.error(f"gTTS synthesis failed: {exc}")
            return None

    @property
    def is_available(self) -> bool:
        """Check if any TTS engine is available."""
        return self._murf_available or self._gtts_available


# ═══════════════════════════════════════════════════════════════
#  VOICE ASSISTANT (Orchestrator)
# ═══════════════════════════════════════════════════════════════

class VoiceAssistant:
    """End-to-end voice interaction pipeline.

    Pipeline: Audio → STT → Process → TTS → Audio Response
    """

    def __init__(self):
        self.stt = SpeechToText()
        self.tts = TextToSpeech()

    def process_audio(
        self,
        audio_path: str,
        process_fn: callable,
        language: str = "en",
    ) -> dict[str, Any]:
        """Process an audio input through the full voice pipeline.

        Args:
            audio_path: Path to input audio file.
            process_fn: Function that takes (text, language) and returns an AI response string.
            language: Target language for the response.

        Returns:
            Dictionary with transcription, response text, and audio output path.
        """
        # Step 1: Speech to Text
        logger.info(f"Voice pipeline started — audio: {audio_path}")
        stt_result = self.stt.transcribe(audio_path)

        if stt_result["status"] != "success":
            return {
                "transcription": "",
                "detected_language": "unknown",
                "response_text": f"❌ {stt_result.get('error', 'Speech recognition failed')}",
                "audio_output": None,
                "status": "stt_error",
            }

        transcribed_text = stt_result["text"]
        detected_language = stt_result.get("language", language)

        logger.info(f"Transcribed ({detected_language}): {transcribed_text[:100]}...")

        # Step 2: Process with AI
        try:
            response_text = process_fn(transcribed_text, language)
        except Exception as exc:
            logger.error(f"AI processing failed: {exc}")
            response_text = "I encountered an error while processing your question. Please try again."

        # Step 3: Text to Speech
        audio_output = self.tts.synthesize(response_text, language)

        return {
            "transcription": transcribed_text,
            "detected_language": detected_language,
            "response_text": response_text,
            "audio_output": audio_output,
            "status": "success",
        }

    @property
    def stt_available(self) -> bool:
        """Check if speech-to-text is available."""
        return self.stt.is_available

    @property
    def tts_available(self) -> bool:
        """Check if text-to-speech is available."""
        return self.tts.is_available


# ── Module-level singleton ──────────────────────────────────
voice_assistant = VoiceAssistant()
