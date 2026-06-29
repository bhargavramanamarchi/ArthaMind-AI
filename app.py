"""
ArthaMind AI — Main Application
=================================
Production-grade Gradio Blocks UI with 7 professional tabs:
💬 AI Assistant | 🎙️ Voice | 📈 Market | 🧮 Calculators | 📚 Learning | 📊 Health | ℹ️ About
"""

import os
import time
from typing import Any, Optional

import gradio as gr

from config import settings
from utils import (
    format_currency,
    format_indian_number,
    get_language_code,
    logger,
    timer,
)
from prompts import (
    SYSTEM_PROMPT,
    RAG_PROMPT_TEMPLATE,
    CONTEXTUALIZER_PROMPT,
    LANGUAGE_INSTRUCTIONS,
    SUGGESTED_PROMPTS,
    FINANCIAL_HEALTH_PROMPT,
)
from calculators import (
    calculate_emi,
    calculate_sip,
    calculate_compound_interest,
    calculate_gst,
    calculate_budget,
    calculate_savings_goal,
    calculate_financial_health,
)
from learning import learning_hub
from rag import knowledge_base
from market import MarketDataFetcher
from voice import voice_assistant


# ═══════════════════════════════════════════════════════════════
#  CUSTOM CSS
# ═══════════════════════════════════════════════════════════════

CUSTOM_CSS = """
/* ── ArthaMind AI Premium Fintech Theme ──────────────────────── */

/* Font Import */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --bg-dark: #020617;
    --bg-midnight: #090d1f;
    --card-bg: rgba(15, 23, 42, 0.45) !important;
    --card-bg-hover: rgba(20, 30, 58, 0.6) !important;
    --border-color: rgba(255, 255, 255, 0.08) !important;
    --border-color-hover: rgba(255, 255, 255, 0.15) !important;
    
    --color-primary: #3b82f6; /* Royal Blue */
    --color-secondary: #8b5cf6; /* Purple */
    --color-emerald: #10b981; /* Emerald */
    --color-gold: #fbbf24; /* Gold */
    --color-danger: #f43f5e;
    
    --text-primary: #f8fafc;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    
    --glass-blur: blur(16px);
    --card-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    --card-radius: 20px;
}

/* Global Container Override */
body {
    background-color: var(--bg-dark) !important;
    background-image: 
        radial-gradient(at 0% 0%, rgba(59, 130, 246, 0.12) 0px, transparent 50%),
        radial-gradient(at 50% 0%, rgba(139, 92, 246, 0.1) 0px, transparent 50%),
        radial-gradient(at 100% 0%, rgba(16, 185, 129, 0.08) 0px, transparent 50%) !important;
    background-attachment: fixed !important;
    color: var(--text-primary) !important;
}

.gradio-container {
    max-width: 1400px !important;
    margin: 0 auto !important;
    padding: 24px 16px !important;
    font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
}

/* Glassmorphism utility card */
.glass-panel {
    background: var(--card-bg) !important;
    backdrop-filter: var(--glass-blur) !important;
    -webkit-backdrop-filter: var(--glass-blur) !important;
    border: 1px solid var(--border-color) !important;
    box-shadow: var(--card-shadow) !important;
    border-radius: var(--card-radius) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    padding: 24px !important;
}

.glass-panel:hover {
    border-color: var(--border-color-hover) !important;
    box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.45) !important;
}

/* Sticky Premium Navigation Bar */
.tabs > .tab-nav {
    background: rgba(15, 23, 42, 0.75) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 16px !important;
    padding: 8px !important;
    margin-bottom: 32px !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25) !important;
    display: flex !important;
    justify-content: center !important;
    gap: 8px !important;
    position: sticky !important;
    top: 12px !important;
    z-index: 1000 !important;
    border-bottom: none !important;
}

.tabs > .tab-nav button {
    color: var(--text-secondary) !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    border: none !important;
    background: transparent !important;
    border-radius: 12px !important;
    padding: 12px 22px !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    cursor: pointer !important;
    border-bottom: none !important;
}

.tabs > .tab-nav button.selected {
    background: rgba(59, 130, 246, 0.15) !important;
    color: #f8fafc !important;
    box-shadow: inset 0 0 12px rgba(59, 130, 246, 0.15), 0 0 8px rgba(59, 130, 246, 0.2) !important;
    border: 1px solid rgba(59, 130, 246, 0.3) !important;
    border-bottom: none !important;
}

.tabs > .tab-nav button:hover:not(.selected) {
    background: rgba(255, 255, 255, 0.04) !important;
    color: #f8fafc !important;
}

/* Premium Dashboard Landing Page Elements */
.dashboard-hero {
    text-align: center;
    padding: 48px 24px !important;
    background: linear-gradient(185deg, rgba(15, 23, 42, 0.6) 0%, rgba(9, 13, 31, 0.9) 100%) !important;
    border-radius: var(--card-radius) !important;
    border: 1px solid var(--border-color) !important;
    box-shadow: var(--card-shadow) !important;
    margin-bottom: 32px !important;
    position: relative;
    overflow: hidden;
}

.dashboard-hero::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(139, 92, 246, 0.07) 0%, transparent 60%);
    animation: rotate-bg 20s linear infinite;
    z-index: 0;
}

@keyframes rotate-bg {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.dashboard-hero-content {
    position: relative;
    z-index: 1;
}

.dashboard-hero h1 {
    font-family: 'Outfit', sans-serif !important;
    font-weight: 800 !important;
    font-size: 3.5rem !important;
    margin: 0 0 8px 0 !important;
    background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 50%, #64748b 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -1px;
}

.dashboard-hero p.subtitle {
    font-size: 1.25rem !important;
    color: var(--text-secondary) !important;
    margin: 0 0 24px 0 !important;
    font-weight: 400 !important;
}

/* Tech Badges */
.hero-badges {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 12px;
}

.tech-badge {
    background: rgba(255, 255, 255, 0.03) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 99px !important;
    padding: 6px 16px !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    color: var(--text-secondary) !important;
    display: flex;
    align-items: center;
    gap: 6px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.2) !important;
    transition: all 0.25s ease !important;
}

.tech-badge:hover {
    background: rgba(255, 255, 255, 0.07) !important;
    border-color: rgba(255, 255, 255, 0.15) !important;
    transform: translateY(-1px) !important;
}

.tech-badge.gemini { border-color: rgba(59, 130, 246, 0.3) !important; color: #60a5fa !important; }
.tech-badge.rag { border-color: rgba(16, 185, 129, 0.3) !important; color: #34d399 !important; }
.tech-badge.voice { border-color: rgba(139, 92, 246, 0.3) !important; color: #a78bfa !important; }
.tech-badge.market { border-color: rgba(245, 158, 11, 0.3) !important; color: #fbbf24 !important; }

/* Grid for Market Cards */
.market-watch-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 20px;
    margin-bottom: 32px;
}

.dashboard-market-card {
    background: rgba(15, 23, 42, 0.45);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: var(--card-radius);
    padding: 20px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 180px;
    text-align: left !important;
}

.dashboard-market-card:hover {
    border-color: rgba(255, 255, 255, 0.15);
    transform: translateY(-4px);
    box-shadow: 0 12px 24px rgba(0,0,0,0.4);
    background: rgba(20, 30, 58, 0.6);
}

.dashboard-market-card::after {
    content: '';
    position: absolute;
    top: 0; right: 0; bottom: 0; left: 0;
    background: linear-gradient(135deg, transparent 60%, rgba(255, 255, 255, 0.02) 100%);
    pointer-events: none;
}

.card-header-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
}

.card-title {
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.card-icon {
    font-size: 1.25rem;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    background: rgba(255, 255, 255, 0.04);
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.06);
}

.card-value {
    font-family: 'Outfit', sans-serif;
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: 0;
}

.card-change-row {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.82rem;
    margin-top: 8px;
}

.trend-badge {
    padding: 2px 8px;
    border-radius: 99px;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 3px;
}

.trend-badge.up {
    background: rgba(16, 185, 129, 0.12);
    color: var(--color-emerald);
}

.trend-badge.down {
    background: rgba(244, 63, 94, 0.12);
    color: var(--color-danger);
}

.card-time {
    font-size: 0.72rem;
    color: var(--text-muted);
    margin-left: auto;
}

/* Quick Action Premium Buttons */
.quick-actions-section {
    margin-bottom: 40px;
    text-align: left !important;
}

.quick-actions-section h2 {
    font-family: 'Outfit', sans-serif !important;
    font-size: 1.5rem !important;
    font-weight: 700 !important;
    margin-bottom: 20px !important;
    color: var(--text-primary) !important;
}

.quick-actions-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 16px;
}

/* Target gradio button inside quick action columns */
.quick-action-btn button {
    display: flex !important;
    flex-direction: column !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;
    background: rgba(15, 23, 42, 0.45) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37) !important;
    border-radius: 16px !important;
    padding: 24px !important;
    height: 140px !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    cursor: pointer !important;
}

.quick-action-btn button:hover {
    border-color: var(--color-primary) !important;
    box-shadow: 0 8px 24px rgba(59, 130, 246, 0.25) !important;
    transform: translateY(-4px) !important;
    background: rgba(20, 30, 58, 0.6) !important;
}

.quick-action-btn button span {
    font-family: 'Outfit', sans-serif !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    margin-top: 12px !important;
    color: var(--text-primary) !important;
}

/* Premium News Grid */
.news-section {
    background: rgba(15, 23, 42, 0.45) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: var(--card-radius) !important;
    padding: 24px !important;
    margin-bottom: 32px !important;
    text-align: left !important;
}

.news-section h2 {
    font-family: 'Outfit', sans-serif !important;
    font-size: 1.4rem !important;
    font-weight: 700 !important;
    margin-top: 0 !important;
    margin-bottom: 20px !important;
    color: var(--text-primary) !important;
}

.news-list {
    display: grid;
    grid-template-columns: 1fr;
    gap: 16px;
}

.news-item {
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    padding-bottom: 16px;
    transition: all 0.2s ease;
}

.news-item:last-child {
    border-bottom: none;
    padding-bottom: 0;
}

.news-item:hover {
    padding-left: 6px;
}

.news-meta {
    display: flex;
    gap: 12px;
    font-size: 0.75rem;
    color: var(--color-primary);
    font-weight: 600;
    margin-bottom: 6px;
}

.news-title {
    font-size: 1rem;
    font-weight: 600;
    color: var(--text-primary);
    text-decoration: none;
    margin: 0;
    line-height: 1.4;
    transition: color 0.2s ease;
}

.news-title:hover {
    color: var(--color-primary);
}

/* Premium Chat Interface Styling */
#chatbot {
    background: rgba(15, 23, 42, 0.3) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: var(--card-radius) !important;
    overflow: hidden !important;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37) !important;
}

/* Message Styles */
#chatbot .message-wrap .message {
    padding: 16px 20px !important;
    border-radius: 16px !important;
    font-size: 0.95rem !important;
    line-height: 1.6 !important;
    margin-bottom: 16px !important;
    max-width: 85% !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
}

#chatbot .message-wrap .user-message {
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%) !important;
    border: 1px solid rgba(59, 130, 246, 0.3) !important;
    color: #f8fafc !important;
    align-self: flex-end !important;
}

#chatbot .message-wrap .bot-message {
    background: rgba(255, 255, 255, 0.04) !important;
    border: 1px solid rgba(255, 255, 255, 0.06) !important;
    color: #f1f5f9 !important;
    align-self: flex-start !important;
}

/* Citations display style */
.citation-box {
    background: rgba(15, 23, 42, 0.5) !important;
    border: 1px solid rgba(255, 255, 255, 0.06) !important;
    border-radius: 12px !important;
    padding: 16px !important;
    font-size: 0.88rem !important;
    color: var(--text-secondary) !important;
    margin-top: 16px !important;
    text-align: left !important;
}

/* Prompt chips style */
.prompt-btn {
    background: rgba(255, 255, 255, 0.03) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 12px !important;
    padding: 10px 18px !important;
    font-size: 0.88rem !important;
    color: var(--text-secondary) !important;
    font-weight: 500 !important;
    transition: all 0.25s ease !important;
}

.prompt-btn:hover {
    border-color: var(--color-primary) !important;
    background: rgba(59, 130, 246, 0.1) !important;
    color: #f8fafc !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15) !important;
}

/* Send Button, Clear Button styles */
.primary-btn {
    background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-secondary) 100%) !important;
    border: none !important;
    color: #ffffff !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important;
    border-radius: 12px !important;
    padding: 12px 24px !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3) !important;
    cursor: pointer !important;
}

.primary-btn:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(59, 130, 246, 0.45) !important;
}

/* Secondary Button styles */
button.secondary {
    background: rgba(255, 255, 255, 0.03) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    color: var(--text-secondary) !important;
    font-weight: 600 !important;
    border-radius: 12px !important;
    padding: 12px 24px !important;
    transition: all 0.25s ease !important;
}

button.secondary:hover {
    background: rgba(255, 255, 255, 0.06) !important;
    color: #ffffff !important;
    border-color: rgba(255, 255, 255, 0.15) !important;
}

/* Voice Mic Pulse effect */
.voice-record-card {
    text-align: center;
    padding: 32px 24px !important;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.voice-mic-container {
    position: relative;
    width: 90px;
    height: 90px;
    margin: 20px auto !important;
}

.voice-mic-outer {
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(139, 92, 246, 0.15);
    border-radius: 50%;
    animation: mic-pulse 2s infinite;
}

@keyframes mic-pulse {
    0% { transform: scale(1); opacity: 0.8; }
    50% { transform: scale(1.3); opacity: 0.3; }
    100% { transform: scale(1.6); opacity: 0; }
}

/* Waveform visual simulation */
.audio-waveform {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 4px;
    height: 40px;
    margin: 16px 0 !important;
}

.waveform-bar {
    width: 3px;
    background: linear-gradient(to top, var(--color-primary), var(--color-secondary));
    border-radius: 99px;
    animation: wave-bounce 1s ease-in-out infinite alternate;
}

@keyframes wave-bounce {
    0% { height: 5px; }
    100% { height: 35px; }
}

.waveform-bar:nth-child(2) { animation-delay: 0.15s; }
.waveform-bar:nth-child(3) { animation-delay: 0.3s; }
.waveform-bar:nth-child(4) { animation-delay: 0.45s; }
.waveform-bar:nth-child(5) { animation-delay: 0.6s; }
.waveform-bar:nth-child(6) { animation-delay: 0.35s; }
.waveform-bar:nth-child(7) { animation-delay: 0.2s; }
.waveform-bar:nth-child(8) { animation-delay: 0.1s; }

/* Bloomberg Terminal Live Market look */
.market-status-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(16, 185, 129, 0.1);
    color: var(--color-emerald);
    padding: 4px 10px;
    border-radius: 99px;
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    border: 1px solid rgba(16, 185, 129, 0.2);
}

.market-status-dot {
    width: 6px;
    height: 6px;
    background-color: var(--color-emerald);
    border-radius: 50%;
    box-shadow: 0 0 8px var(--color-emerald);
    animation: led-glow 1.5s infinite alternate;
}

@keyframes led-glow {
    0% { opacity: 0.4; }
    100% { opacity: 1; }
}

/* Calculator specific results cards */
.calc-result-box {
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.08) 0%, rgba(16, 185, 129, 0.05) 100%) !important;
    border: 1px solid rgba(59, 130, 246, 0.15) !important;
    border-radius: 16px !important;
    padding: 24px !important;
    text-align: left !important;
}

/* Financial Health circular grade design */
.health-grade-ring {
    width: 140px;
    height: 140px;
    border-radius: 50%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin: 0 auto 20px !important;
    background: radial-gradient(circle, rgba(9, 13, 31, 0.9) 0%, rgba(13, 20, 38, 0.6) 100%);
    border: 6px solid var(--color-emerald);
    box-shadow: 0 0 24px rgba(16, 185, 129, 0.25), inset 0 0 16px rgba(16, 185, 129, 0.15);
}

.health-grade-ring.grade-a { border-color: var(--color-emerald); box-shadow: 0 0 24px rgba(16, 185, 129, 0.25); }
.health-grade-ring.grade-b { border-color: var(--color-primary); box-shadow: 0 0 24px rgba(59, 130, 246, 0.25); }
.health-grade-ring.grade-c { border-color: var(--color-gold); box-shadow: 0 0 24px rgba(245, 158, 11, 0.25); }
.health-grade-ring.grade-d { border-color: var(--color-danger); box-shadow: 0 0 24px rgba(244, 63, 94, 0.25); }

/* Learning Hub premium cards */
.learning-card {
    background: rgba(15, 23, 42, 0.45) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 16px !important;
    padding: 20px !important;
    transition: all 0.3s ease !important;
    display: flex;
    flex-direction: column;
    height: 100%;
    text-align: left !important;
}

.learning-card:hover {
    border-color: var(--color-secondary) !important;
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 24px rgba(139, 92, 246, 0.2) !important;
}

.learning-badge {
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    padding: 3px 8px;
    border-radius: 6px;
    margin-right: 6px;
}

.learning-badge.beginner { background: rgba(16, 185, 129, 0.12); color: var(--color-emerald); }
.learning-badge.intermediate { background: rgba(59, 130, 246, 0.12); color: var(--color-primary); }
.learning-badge.advanced { background: rgba(139, 92, 246, 0.12); color: var(--color-secondary); }

/* Custom Scrollbar */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: var(--bg-dark);
}
::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 99px;
}
::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.25);
}

/* Hide Gradio default footer */
footer { display: none !important; }
"""


# ═══════════════════════════════════════════════════════════════
#  AI ENGINE
# ═══════════════════════════════════════════════════════════════

class ArthaMindEngine:
    """Core AI engine handling LLM, RAG, and tool integration."""

    def __init__(self):
        self.llm = None
        self.chain = None
        self._initialized = False
        self.market_fetcher = MarketDataFetcher()

    def initialize(self) -> bool:
        """Initialize the LLM and RAG pipeline."""
        if self._initialized:
            return True

        try:
            # Initialize knowledge base
            logger.info("Initializing ArthaMind Engine...")
            kb_ready = knowledge_base.initialize()
            if kb_ready:
                logger.info(f"Knowledge base ready with {knowledge_base.document_count} chunks")
            else:
                logger.warning("Knowledge base initialization failed — running without RAG")

            # Initialize LLM
            if settings.GOOGLE_API_KEY:
                os.environ["GOOGLE_API_KEY"] = settings.GOOGLE_API_KEY
                from langchain_google_genai import ChatGoogleGenerativeAI

                self.llm = ChatGoogleGenerativeAI(
                    model=settings.LLM_MODEL,
                    temperature=settings.LLM_TEMPERATURE,
                    max_output_tokens=settings.LLM_MAX_TOKENS,
                )
                logger.info(f"LLM initialized: {settings.LLM_MODEL}")
                self._initialized = True
            else:
                logger.warning("GOOGLE_API_KEY not set — LLM disabled")

            return self._initialized

        except Exception as exc:
            logger.error(f"Engine initialization failed: {exc}")
            return False

    @timer
    def chat(self, message: str, history: list[dict], language: str = "en") -> tuple[str, str]:
        """Process a chat message with RAG and return response + citations.

        Args:
            message: User's message.
            history: Chat history in messages format.
            language: Target language code.

        Returns:
            Tuple of (response_text, citations_text).
        """
        if not self._initialized:
            return (
                "⚠️ AI engine is not initialized. Please check your GOOGLE_API_KEY in the .env file.",
                ""
            )

        try:
            # Step 1: Search knowledge base
            rag_results = knowledge_base.search(message) if knowledge_base.is_ready else []
            context = knowledge_base.format_context(rag_results)
            citations = knowledge_base.format_citations(rag_results)

            # Step 2: Build language instruction
            lang_name = "English"
            for name, code in settings.SUPPORTED_LANGUAGES.items():
                if code == language:
                    lang_name = name.split("(")[0].strip()
                    break

            lang_instruction = LANGUAGE_INSTRUCTIONS.get(language, LANGUAGE_INSTRUCTIONS["en"])

            # Step 3: Build prompt with context
            chat_history_text = ""
            for msg in history[-10:]:  # Last 10 messages for context
                role = "User" if msg.get("role") == "user" else "Assistant"
                chat_history_text += f"{role}: {msg.get('content', '')}\n"

            prompt = RAG_PROMPT_TEMPLATE.format(
                context=context,
                language=lang_name,
                chat_history=chat_history_text,
                input=message,
            )

            # Step 4: Invoke LLM
            full_prompt = f"{SYSTEM_PROMPT}\n\n{lang_instruction}\n\n{prompt}"
            response = self.llm.invoke(full_prompt)
            response_text = response.content

            return response_text, citations

        except Exception as exc:
            logger.error(f"Chat error: {exc}")
            return (
                f"❌ An error occurred while processing your request. Please try again.\n\nError: {str(exc)}",
                ""
            )

    def process_voice(self, audio_path: str, language: str = "en") -> dict[str, Any]:
        """Process voice input through the full pipeline.

        Args:
            audio_path: Path to audio file.
            language: Target language code.

        Returns:
            Dictionary with transcription, response, and audio output.
        """
        def process_fn(text: str, lang: str) -> str:
            response, _ = self.chat(text, [], lang)
            return response

        return voice_assistant.process_audio(audio_path, process_fn, language)


# ── Global engine singleton ─────────────────────────────────
engine = ArthaMindEngine()


# ═══════════════════════════════════════════════════════════════
#  DASHBOARD UTILITIES
# ═══════════════════════════════════════════════════════════════

def get_dashboard_market_html(market_data: dict) -> str:
    gold = market_data.get("gold", {})
    silver = market_data.get("silver", {})
    currency = market_data.get("currency", {})
    
    gold_price_str = "₹" + format_currency(gold.get("price_per_gram_24k", 7250.0)) if gold.get("price_per_gram_24k") else "₹7,250"
    gold_source = gold.get("source", "Live")
    
    silver_price_str = "₹" + format_currency(silver.get("price_per_gram", 88.50)) if silver.get("price_per_gram") else "₹88.50"
    silver_source = silver.get("source", "Live")
    
    usd_inr_val = 83.45
    rates = currency.get("rates", {})
    if rates.get("USD"):
        usd_inr_val = round(1.0 / rates["USD"], 2)
    currency_source = currency.get("source", "Live")
    
    html = f"""
    <div class="market-watch-grid">
        <div class="dashboard-market-card">
            <div class="card-header-row">
                <span class="card-title">Gold 24K (Per g)</span>
                <span class="card-icon">🥇</span>
            </div>
            <h3 class="card-value">{{gold_price_str}}</h3>
            <div class="card-change-row">
                <span class="trend-badge up">▲ Live</span>
                <span class="card-time">{{gold_source}}</span>
            </div>
        </div>
        <div class="dashboard-market-card">
            <div class="card-header-row">
                <span class="card-title">Silver (Per g)</span>
                <span class="card-icon">🥈</span>
            </div>
            <h3 class="card-value">{{silver_price_str}}</h3>
            <div class="card-change-row">
                <span class="trend-badge up">▲ Live</span>
                <span class="card-time">{{silver_source}}</span>
            </div>
        </div>
        <div class="dashboard-market-card">
            <div class="card-header-row">
                <span class="card-title">USD / INR</span>
                <span class="card-icon">💵</span>
            </div>
            <h3 class="card-value">₹{{usd_inr_val}}</h3>
            <div class="card-change-row">
                <span class="trend-badge up">▲ Live</span>
                <span class="card-time">{{currency_source}}</span>
            </div>
        </div>
        <div class="dashboard-market-card">
            <div class="card-header-row">
                <span class="card-title">BSE Sensex</span>
                <span class="card-icon">📈</span>
            </div>
            <h3 class="card-value">77,201</h3>
            <div class="card-change-row">
                <span class="trend-badge up">▲ +0.35%</span>
                <span class="card-time">Simulated</span>
            </div>
        </div>
        <div class="dashboard-market-card">
            <div class="card-header-row">
                <span class="card-title">NSE Nifty</span>
                <span class="card-icon">📈</span>
            </div>
            <h3 class="card-value">23,500</h3>
            <div class="card-change-row">
                <span class="trend-badge up">▲ +0.42%</span>
                <span class="card-time">Simulated</span>
            </div>
        </div>
        <div class="dashboard-market-card">
            <div class="card-header-row">
                <span class="card-title">Bitcoin</span>
                <span class="card-icon">🪙</span>
            </div>
            <h3 class="card-value">$64,320</h3>
            <div class="card-change-row">
                <span class="trend-badge down">▼ -0.85%</span>
                <span class="card-time">Simulated</span>
            </div>
        </div>
        <div class="dashboard-market-card">
            <div class="card-header-row">
                <span class="card-title">Ethereum</span>
                <span class="card-icon">🪙</span>
            </div>
            <h3 class="card-value">$3,450</h3>
            <div class="card-change-row">
                <span class="trend-badge up">▲ +1.12%</span>
                <span class="card-time">Simulated</span>
            </div>
        </div>
    </div>
    """
    return html

def on_dashboard_load():
    data = engine.market_fetcher.get_all_market_data()
    return get_dashboard_market_html(data)


# ═══════════════════════════════════════════════════════════════
#  EVENT HANDLERS
# ═══════════════════════════════════════════════════════════════

def on_chat_submit(message: str, history: list[dict], language: str) -> tuple:
    """Handle chat message submission.

    Returns:
        Tuple of (cleared_input, updated_history, citations_markdown).
    """
    if not message.strip():
        return "", history, ""

    lang_code = get_language_code(language)
    history.append({"role": "user", "content": message})

    response_text, citations = engine.chat(message, history, lang_code)
    history.append({"role": "assistant", "content": response_text})

    return "", history, citations


def on_suggested_prompt(prompt_text: str, history: list[dict], language: str) -> tuple:
    """Handle clicking a suggested prompt."""
    return on_chat_submit(prompt_text, history, language)


def on_clear_chat() -> tuple:
    """Clear chat history."""
    return [], "", ""


def on_voice_submit(audio_path: Optional[str], language: str) -> tuple:
    """Handle voice input submission.

    Returns:
        Tuple of (transcription, response_text, audio_output).
    """
    if not audio_path:
        return "No audio recorded.", "Please record or upload an audio file.", None

    lang_code = get_language_code(language)
    result = engine.process_voice(audio_path, lang_code)

    return (
        result.get("transcription", "Transcription failed."),
        result.get("response_text", "Processing failed."),
        result.get("audio_output"),
    )


def on_refresh_market() -> tuple:
    """Refresh market data.

    Returns:
        Tuple of (gold_md, silver_md, currency_md).
    """
    data = engine.market_fetcher.refresh()

    # Format gold
    gold = data.get("gold", {})
    if gold.get("status") == "live":
        gold_md = (
            f"### 🥇 Gold Prices (Live)\n\n"
            f"| Purity | Per Gram | Per 10g |\n"
            f"|--------|----------|---------|\n"
            f"| **24K** | {format_currency(gold['price_per_gram_24k'])} | {format_currency(gold['price_per_10g_24k'])} |\n"
            f"| **22K** | {format_currency(gold['price_per_gram_22k'])} | {format_currency(gold['price_per_10g_22k'])} |\n\n"
            f"*📡 {gold['source']} — {gold['timestamp']}*"
        )
    else:
        gold_md = "### 🥇 Gold Prices\n\n⚠️ Live data unavailable. Configure `GOLDAPI_KEY` in `.env` for live prices."

    # Format silver
    silver = data.get("silver", {})
    if silver.get("status") == "live":
        silver_md = (
            f"### 🥈 Silver Prices (Live)\n\n"
            f"| Unit | Price |\n"
            f"|------|-------|\n"
            f"| **Per Gram** | {format_currency(silver['price_per_gram'])} |\n"
            f"| **Per Kg** | {format_currency(silver['price_per_kg'])} |\n\n"
            f"*📡 {silver['source']} — {silver['timestamp']}*"
        )
    else:
        silver_md = "### 🥈 Silver Prices\n\n⚠️ Live data unavailable. Configure `GOLDAPI_KEY` in `.env` for live prices."

    # Format currency
    currency = data.get("currency", {})
    if currency.get("status") == "live":
        rates = currency.get("rates", {})
        rows = "\n".join(f"| {code} | {rate:.4f} |" for code, rate in sorted(rates.items()))
        currency_md = (
            f"### 💱 Exchange Rates (Base: INR)\n\n"
            f"| Currency | Rate |\n"
            f"|----------|------|\n"
            f"{rows}\n\n"
            f"*📡 {currency['source']} — {currency['date']}*"
        )
    else:
        currency_md = "### 💱 Exchange Rates\n\n⚠️ Currency data unavailable. Check your internet connection."

    return gold_md, silver_md, currency_md


# ── Calculator Handlers ─────────────────────────────────────

def on_gst_calculate(base_amount: float, gst_rate: float, is_interstate: bool) -> str:
    """Calculate GST and return formatted result."""
    if not base_amount or base_amount <= 0:
        return "⚠️ Please enter a valid base amount."
    result = calculate_gst(base_amount, gst_rate, is_interstate)
    tx_type = "Inter-State (IGST)" if is_interstate else "Intra-State (CGST + SGST)"
    output = f"### 🧾 GST Calculation Result\n\n"
    output += f"| Item | Amount |\n|------|--------|\n"
    output += f"| Base Amount | {format_currency(result.base_amount)} |\n"
    output += f"| GST Rate | {result.gst_rate}% |\n"
    output += f"| Transaction | {tx_type} |\n"
    if is_interstate:
        output += f"| IGST | {format_currency(result.igst)} |\n"
    else:
        output += f"| CGST ({result.gst_rate/2}%) | {format_currency(result.cgst)} |\n"
        output += f"| SGST ({result.gst_rate/2}%) | {format_currency(result.sgst)} |\n"
    output += f"| **Total GST** | **{format_currency(result.total_gst)}** |\n"
    output += f"| **Final Price** | **{format_currency(result.total_amount)}** |"
    return output


def on_emi_calculate(principal: float, rate: float, tenure: int) -> str:
    """Calculate EMI and return formatted result."""
    if not principal or principal <= 0 or not rate or rate <= 0 or not tenure or tenure <= 0:
        return "⚠️ Please enter valid loan amount, interest rate, and tenure."
    result = calculate_emi(principal, rate, tenure)
    output = f"### 🏦 EMI Calculation Result\n\n"
    output += f"| Parameter | Value |\n|-----------|-------|\n"
    output += f"| Loan Amount | {format_currency(result.principal)} |\n"
    output += f"| Interest Rate | {result.annual_rate}% p.a. |\n"
    output += f"| Tenure | {result.tenure_years} years ({result.tenure_years*12} months) |\n"
    output += f"| **Monthly EMI** | **{format_currency(result.monthly_emi)}** |\n"
    output += f"| Total Payment | {format_currency(result.total_payment)} |\n"
    output += f"| Total Interest | {format_currency(result.total_interest)} |\n"
    output += f"\n\n**Yearly Breakdown (first 5 years):**\n\n"
    output += f"| Year | Principal | Interest | Balance |\n|------|-----------|----------|---------|\n"
    for row in result.yearly_breakdown[:5]:
        output += f"| {row['year']} | {format_currency(row['principal_paid'])} | {format_currency(row['interest_paid'])} | {format_currency(row['balance'])} |\n"
    return output


def on_sip_calculate(monthly: float, rate: float, years: int) -> str:
    """Calculate SIP and return formatted result."""
    if not monthly or monthly <= 0 or not rate or not years or years <= 0:
        return "⚠️ Please enter valid SIP amount, return rate, and tenure."
    result = calculate_sip(monthly, rate, years)
    output = f"### 📈 SIP Projection\n\n"
    output += f"| Parameter | Value |\n|-----------|-------|\n"
    output += f"| Monthly SIP | {format_currency(result.monthly_investment)} |\n"
    output += f"| Expected Return | {result.annual_return_rate}% p.a. |\n"
    output += f"| Duration | {result.tenure_years} years |\n"
    output += f"| Total Invested | {format_currency(result.total_invested)} |\n"
    output += f"| **Expected Corpus** | **{format_currency(result.future_value)}** |\n"
    output += f"| Wealth Gained | {format_currency(result.wealth_gained)} |"
    return output


def on_ci_calculate(principal: float, rate: float, years: int, frequency: str) -> str:
    """Calculate compound interest and return formatted result."""
    if not principal or principal <= 0 or not rate or not years or years <= 0:
        return "⚠️ Please enter valid principal, rate, and tenure."
    result = calculate_compound_interest(principal, rate, years, frequency)
    output = f"### 💰 Compound Interest Result\n\n"
    output += f"| Parameter | Value |\n|-----------|-------|\n"
    output += f"| Principal | {format_currency(result.principal)} |\n"
    output += f"| Interest Rate | {result.annual_rate}% p.a. |\n"
    output += f"| Tenure | {result.tenure_years} years |\n"
    output += f"| Compounding | {result.compounding_frequency} |\n"
    output += f"| **Maturity Amount** | **{format_currency(result.final_amount)}** |\n"
    output += f"| Interest Earned | {format_currency(result.total_interest)} |"
    return output


def on_budget_calculate(income: float) -> str:
    """Calculate budget and return formatted result."""
    if not income or income <= 0:
        return "⚠️ Please enter a valid monthly income."
    result = calculate_budget(income)
    output = f"### 📋 Your Budget Plan (50-30-20 Rule)\n\n"
    output += f"**Monthly Income:** {format_currency(result.monthly_income)}\n\n"
    output += f"| Category | Allocation | Amount |\n|----------|------------|--------|\n"
    output += f"| 🔵 Needs (50%) | Essentials | {format_currency(result.needs)} |\n"
    output += f"| 🟡 Wants (30%) | Lifestyle | {format_currency(result.wants)} |\n"
    output += f"| 🟢 Savings (20%) | Investments | {format_currency(result.savings)} |\n"
    output += f"\n\n**Suggested Allocation:**\n\n"
    output += f"| Category | Amount |\n|----------|--------|\n"
    for cat, amt in result.breakdown.items():
        output += f"| {cat} | {format_currency(amt)} |\n"
    return output


def on_savings_goal_calculate(target: float, current: float, rate: float, years: int) -> str:
    """Calculate savings goal and return formatted result."""
    if not target or target <= 0 or not years or years <= 0:
        return "⚠️ Please enter valid target amount and tenure."
    result = calculate_savings_goal(target, current or 0, rate or 10, years)
    output = f"### 🎯 Savings Goal Plan\n\n"
    output += f"| Parameter | Value |\n|-----------|-------|\n"
    output += f"| Target Amount | {format_currency(result['target_amount'])} |\n"
    output += f"| Current Savings | {format_currency(result['current_savings'])} |\n"
    output += f"| Time Horizon | {result.get('tenure_years', years)} years |\n"
    output += f"| Expected Return | {result.get('annual_return_rate', rate)}% p.a. |\n"
    output += f"| **Monthly Savings Needed** | **{format_currency(result['monthly_savings_needed'])}** |"
    if result.get("message"):
        output += f"\n\n✨ {result['message']}"
    return output


# ── Financial Health Handler ────────────────────────────────

def on_health_calculate(
    income: float, savings: float, debt: float, expenses: float, emergency: float
) -> tuple:
    """Calculate financial health and return formatted results with charts.

    Returns:
        Tuple of (score_md, details_md, pie_chart, bar_chart).
    """
    if not income or income <= 0:
        empty = "⚠️ Please enter a valid monthly income."
        return empty, empty, None, None

    result = calculate_financial_health(
        income, savings or 0, debt or 0, expenses or 0, emergency or 0
    )

    # Score display
    grade_class = (
        "grade-a" if result.score >= 75 else
        "grade-b" if result.score >= 50 else
        "grade-c" if result.score >= 35 else "grade-d"
    )
    score_color_hex = (
        "#10b981" if result.score >= 75 else
        "#3b82f6" if result.score >= 50 else
        "#fbbf24" if result.score >= 35 else "#f43f5e"
    )

    score_md = f"""
    <div class="health-grade-ring {grade_class}">
        <span style="font-size: 2.5rem; font-weight: 800; color: {score_color_hex};">{result.score}</span>
        <span style="font-size: 0.9rem; color: #94a3b8; font-weight: 600; text-transform: uppercase; margin-top: 4px;">Grade {result.grade}</span>
    </div>
    """

    # Category details
    details_md = "### 📊 Category Breakdown\n\n"
    details_md += "| Dimension | Score | Status |\n|-----------|-------|--------|\n"
    for dim, score in result.category_scores.items():
        bar = "█" * score + "░" * (25 - score)
        status = "🟢" if score >= 22 else "🟡" if score >= 17 else "🟠" if score >= 12 else "🔴"
        details_md += f"| {dim} | {score}/25 {status} | `{bar}` |\n"

    details_md += "\n\n### 📈 Key Ratios\n\n"
    details_md += "| Metric | Your Value | Ideal |\n|--------|-----------|-------|\n"
    details_md += f"| Savings Rate | {result.savings_ratio:.0%} | ≥ 20% |\n"
    details_md += f"| Debt-to-Income | {result.debt_to_income:.0%} | ≤ 30% |\n"
    details_md += f"| Expense Ratio | {result.expense_ratio:.0%} | ≤ 70% |\n"
    details_md += f"| Emergency Fund | {result.emergency_months:.1f} months | ≥ 6 months |\n"

    details_md += "\n\n### 💡 Personalized Suggestions\n\n"
    for s in result.suggestions:
        details_md += f"- {s}\n"

    # Pie chart
    try:
        import plotly.graph_objects as go

        pie_fig = go.Figure(data=[go.Pie(
            labels=list(result.category_scores.keys()),
            values=list(result.category_scores.values()),
            hole=0.45,
            marker=dict(colors=["#22c55e", "#3b82f6", "#f59e0b", "#ef4444"]),
            textinfo="label+value",
            textfont=dict(size=13),
        )])
        pie_fig.update_layout(
            title=dict(text="Category Score Distribution", font=dict(size=16)),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#f1f5f9"),
            height=350,
            margin=dict(t=50, b=20, l=20, r=20),
            showlegend=True,
            legend=dict(font=dict(size=12)),
        )

        # Bar chart
        bar_fig = go.Figure(data=[go.Bar(
            x=list(result.category_scores.keys()),
            y=list(result.category_scores.values()),
            marker=dict(
                color=["#22c55e", "#3b82f6", "#f59e0b", "#ef4444"],
                line=dict(width=0),
            ),
            text=[f"{v}/25" for v in result.category_scores.values()],
            textposition="outside",
            textfont=dict(size=13),
        )])
        bar_fig.update_layout(
            title=dict(text="Score by Dimension", font=dict(size=16)),
            yaxis=dict(range=[0, 30], title="Score", gridcolor="rgba(255,255,255,0.1)"),
            xaxis=dict(title=""),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#f1f5f9"),
            height=350,
            margin=dict(t=50, b=20, l=50, r=20),
        )

        return score_md, details_md, pie_fig, bar_fig

    except ImportError:
        return score_md, details_md, None, None


# ═══════════════════════════════════════════════════════════════
#  BUILD UI
# ═══════════════════════════════════════════════════════════════

def create_app() -> gr.Blocks:
    """Build and return the full Gradio Blocks application."""

    with gr.Blocks(
        title="ArthaMind AI — Personal Finance Advisor",
    ) as app:

        # ── Header ───────────────────────────────────────────
        gr.HTML("""
        <div id="app-header">
            <h1>🧠 ArthaMind AI</h1>
            <p>Your Intelligent Personal Finance Advisor for Indian Citizens</p>
        </div>
        """)

        # ── Tabs ─────────────────────────────────────────────
        with gr.Tabs(elem_id="main-tabs") as main_tabs:

            # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            #  TAB 0: DASHBOARD
            # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            with gr.Tab("📊 Dashboard", id="dashboard_tab"):
                # Hero HTML
                gr.HTML(f"""
                <div class="dashboard-hero">
                    <div class="dashboard-hero-content">
                        <h1>🧠 ArthaMind AI</h1>
                        <p class="subtitle">India's Intelligent Personal Finance Platform</p>
                        <div class="hero-badges">
                            <div class="tech-badge gemini"><i class="lucide-sparkles"></i> Gemini 2.5 Flash</div>
                            <div class="tech-badge rag"><i class="lucide-database"></i> Hybrid RAG</div>
                            <div class="tech-badge voice"><i class="lucide-mic"></i> Voice AI</div>
                            <div class="tech-badge market"><i class="lucide-line-chart"></i> Live Markets</div>
                            <div class="tech-badge"><i class="lucide-git-branch"></i> LangChain</div>
                        </div>
                    </div>
                </div>
                """)
                
                # Market Watch Grid HTML
                dashboard_market_html = gr.HTML(value="""
                <div class="market-watch-grid">
                    <div class="dashboard-market-card">
                        <div class="card-header-row">
                            <span class="card-title">Gold 24K</span>
                            <span class="card-icon">🥇</span>
                        </div>
                        <h3 class="card-value">₹7,250</h3>
                        <div class="card-change-row">
                            <span class="trend-badge up">▲ Live</span>
                            <span class="card-time">Loading...</span>
                        </div>
                    </div>
                    <div class="dashboard-market-card">
                        <div class="card-header-row">
                            <span class="card-title">Silver</span>
                            <span class="card-icon">🥈</span>
                        </div>
                        <h3 class="card-value">₹88.50</h3>
                        <div class="card-change-row">
                            <span class="trend-badge up">▲ Live</span>
                            <span class="card-time">Loading...</span>
                        </div>
                    </div>
                    <div class="dashboard-market-card">
                        <div class="card-header-row">
                            <span class="card-title">USD / INR</span>
                            <span class="card-icon">💵</span>
                        </div>
                        <h3 class="card-value">₹83.45</h3>
                        <div class="card-change-row">
                            <span class="trend-badge up">▲ Live</span>
                            <span class="card-time">Loading...</span>
                        </div>
                    </div>
                    <div class="dashboard-market-card">
                        <div class="card-header-row">
                            <span class="card-title">BSE Sensex</span>
                            <span class="card-icon">📈</span>
                        </div>
                        <h3 class="card-value">77,201</h3>
                        <div class="card-change-row">
                            <span class="trend-badge up">▲ +0.35%</span>
                            <span class="card-time">Simulated</span>
                        </div>
                    </div>
                    <div class="dashboard-market-card">
                        <div class="card-header-row">
                            <span class="card-title">NSE Nifty</span>
                            <span class="card-icon">📈</span>
                        </div>
                        <h3 class="card-value">23,500</h3>
                        <div class="card-change-row">
                            <span class="trend-badge up">▲ +0.42%</span>
                            <span class="card-time">Simulated</span>
                        </div>
                    </div>
                    <div class="dashboard-market-card">
                        <div class="card-header-row">
                            <span class="card-title">Bitcoin</span>
                            <span class="card-icon">🪙</span>
                        </div>
                        <h3 class="card-value">$64,320</h3>
                        <div class="card-change-row">
                            <span class="trend-badge down">▼ -0.85%</span>
                            <span class="card-time">Simulated</span>
                        </div>
                    </div>
                    <div class="dashboard-market-card">
                        <div class="card-header-row">
                            <span class="card-title">Ethereum</span>
                            <span class="card-icon">🪙</span>
                        </div>
                        <h3 class="card-value">$3,450</h3>
                        <div class="card-change-row">
                            <span class="trend-badge up">▲ +1.12%</span>
                            <span class="card-time">Simulated</span>
                        </div>
                    </div>
                </div>
                """)
                
                # Quick Actions Grid
                gr.Markdown("## ⚡ Financial Quick Actions")
                with gr.Row():
                    with gr.Column(scale=1, min_width=120, elem_classes=["quick-action-btn"]):
                        tax_btn = gr.Button("💰\nSave Income Tax")
                    with gr.Column(scale=1, min_width=120, elem_classes=["quick-action-btn"]):
                        loan_btn = gr.Button("🏡\nHome Loan EMI")
                    with gr.Column(scale=1, min_width=120, elem_classes=["quick-action-btn"]):
                        sip_btn = gr.Button("📈\nStart SIP")
                    with gr.Column(scale=1, min_width=120, elem_classes=["quick-action-btn"]):
                        gold_btn = gr.Button("🪙\nGold Rates")
                    with gr.Column(scale=1, min_width=120, elem_classes=["quick-action-btn"]):
                        score_btn = gr.Button("💳\nCheck Score")
                
                with gr.Row():
                    with gr.Column(scale=1, min_width=120, elem_classes=["quick-action-btn"]):
                        budget_btn = gr.Button("💸\nBudget Planner")
                    with gr.Column(scale=1, min_width=120, elem_classes=["quick-action-btn"]):
                        portfolio_btn = gr.Button("📊\nMarket Indices")
                    with gr.Column(scale=1, min_width=120, elem_classes=["quick-action-btn"]):
                        retirement_btn = gr.Button("🏦\nCI Calculator")
                    with gr.Column(scale=1, min_width=120, elem_classes=["quick-action-btn"]):
                        forex_btn = gr.Button("🌍\nCurrency Converter")
                    with gr.Column(scale=1, min_width=120, elem_classes=["quick-action-btn"]):
                        learn_btn = gr.Button("📚\nLearning Hub")
                
                # News Feed
                gr.HTML("""
                <div class="news-section">
                    <h2>📰 Live Financial Intelligence Feed</h2>
                    <div class="news-list">
                        <div class="news-item">
                            <div class="news-meta"><span>MARKET</span><span>•</span><span>10 mins ago</span></div>
                            <h4 class="news-title">RBI MPC keeps Repo Rate unchanged at 6.50% to align inflation with target.</h4>
                        </div>
                        <div class="news-item">
                            <div class="news-meta"><span>TAXATION</span><span>•</span><span>2 hours ago</span></div>
                            <h4 class="news-title">Finance Ministry hints at further simplification of the New Income Tax Regime for next fiscal.</h4>
                        </div>
                        <div class="news-item">
                            <div class="news-meta"><span>MUTUAL FUNDS</span><span>•</span><span>5 hours ago</span></div>
                            <h4 class="news-title">AMFI data reveals SIP contributions in India cross record monthly milestone of ₹20,000 crores.</h4>
                        </div>
                        <div class="news-item">
                            <div class="news-meta"><span>GOLD</span><span>•</span><span>1 day ago</span></div>
                            <h4 class="news-title">Gold prices hit historic peaks in Indian retail markets tracking international geopolitical cues.</h4>
                        </div>
                    </div>
                </div>
                """)

            # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            #  TAB 1: AI ASSISTANT
            # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            with gr.Tab("💬 AI Advisor", id="ai_advisor_tab"):
                with gr.Row():
                    with gr.Column(scale=4):
                        chatbot = gr.Chatbot(
                            elem_id="chatbot",
                            label="ArthaMind AI",
                            height=520,
                            avatar_images=(None, None),
                            placeholder="Ask me anything about Indian personal finance... 💰",
                        )

                        with gr.Row():
                            chat_input = gr.Textbox(
                                placeholder="Type your finance question here... (e.g., 'How to save tax under new regime?')",
                                show_label=False,
                                scale=6,
                                container=False,
                                autofocus=True,
                            )
                            send_btn = gr.Button("Send ➤", elem_classes=["primary-btn"], scale=1)

                        # Suggestions Row
                        with gr.Row(elem_classes=["suggested-questions-row"]):
                            prompt_buttons = []
                            for prompt in SUGGESTED_PROMPTS[:6]:
                                btn = gr.Button(
                                    f"{prompt['icon']} {prompt['text']}",
                                    elem_classes=["prompt-btn"],
                                    size="sm",
                                )
                                prompt_buttons.append((btn, prompt['text']))

                        citations_display = gr.Markdown(
                            value="",
                            label="Sources",
                            elem_classes=["citation-box"],
                        )

                    with gr.Column(scale=1, min_width=200):
                        language_selector = gr.Dropdown(
                            choices=list(settings.SUPPORTED_LANGUAGES.keys()),
                            value="English",
                            label="🌐 Language",
                            interactive=True,
                        )

                        clear_btn = gr.Button("🗑️ Clear Chat", variant="secondary")

                # ── Chat Event Handlers ──────────────────────
                chat_outputs = [chat_input, chatbot, citations_display]

                send_btn.click(
                    on_chat_submit,
                    inputs=[chat_input, chatbot, language_selector],
                    outputs=chat_outputs,
                )

                chat_input.submit(
                    on_chat_submit,
                    inputs=[chat_input, chatbot, language_selector],
                    outputs=chat_outputs,
                )

                clear_btn.click(
                    on_clear_chat,
                    outputs=[chatbot, chat_input, citations_display],
                )

                for btn, prompt_text in prompt_buttons:
                    btn.click(
                        on_suggested_prompt,
                        inputs=[gr.State(prompt_text), chatbot, language_selector],
                        outputs=chat_outputs,
                    )

            # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            #  TAB 2: VOICE ASSISTANT
            # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            with gr.Tab("🎙️ Voice Assistant", id="voice_assistant_tab"):
                gr.HTML("""
                <div class="glass-panel voice-record-card" style="margin-bottom: 24px;">
                    <div class="voice-mic-container">
                        <div class="voice-mic-outer"></div>
                        <div class="card-icon" style="width: 90px; height: 90px; border-radius: 50%; font-size: 2.5rem; background: rgba(139, 92, 246, 0.2); border: 2px solid rgba(139, 92, 246, 0.4); margin: 0 auto; display: flex; align-items: center; justify-content: center; position: relative; z-index: 2;">🎙️</div>
                    </div>
                    <div class="audio-waveform">
                        <div class="waveform-bar"></div>
                        <div class="waveform-bar"></div>
                        <div class="waveform-bar"></div>
                        <div class="waveform-bar"></div>
                        <div class="waveform-bar"></div>
                        <div class="waveform-bar"></div>
                        <div class="waveform-bar"></div>
                        <div class="waveform-bar"></div>
                    </div>
                    <p style="color: var(--text-secondary); font-size: 0.95rem; margin-top: 8px; font-weight: 500;">Speak your financial question. ArthaMind will transcribe, analyze, and reply with voice.</p>
                </div>
                """)

                with gr.Row():
                    with gr.Column(scale=1, elem_classes=["glass-panel"]):
                        audio_input = gr.Audio(
                            sources=["upload", "microphone"],
                            type="filepath",
                            label="🎤 Record or Upload Audio",
                        )
                        voice_language = gr.Dropdown(
                            choices=list(settings.SUPPORTED_LANGUAGES.keys()),
                            value="English",
                            label="🌐 Response Language",
                        )
                        voice_submit_btn = gr.Button(
                            "🚀 Process Audio",
                            elem_classes=["primary-btn"],
                        )

                    with gr.Column(scale=2, elem_classes=["glass-panel"]):
                        voice_transcription = gr.Textbox(
                            label="📝 Transcription",
                            lines=3,
                            interactive=False,
                        )
                        voice_response = gr.Markdown(
                            label="💬 AI Response",
                        )
                        voice_audio_output = gr.Audio(
                            label="🔊 Audio Response",
                            type="filepath",
                            interactive=False,
                        )

                stt_status = "✅ Ready" if voice_assistant.stt_available else "❌ Not configured (add ASSEMBLYAI_API_KEY)"
                tts_status = "✅ Ready" if voice_assistant.tts_available else "❌ Not configured"
                gr.Markdown(f"*Speech-to-Text: {stt_status} | Text-to-Speech: {tts_status}*")

                voice_submit_btn.click(
                    on_voice_submit,
                    inputs=[audio_input, voice_language],
                    outputs=[voice_transcription, voice_response, voice_audio_output],
                )

            # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            #  TAB 3: LIVE MARKET
            # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            with gr.Tab("📈 Live Market", id="live_market_tab"):
                gr.Markdown("### 📈 Live Market Data\n*Real-time gold, silver, and currency exchange rates.*")

                refresh_btn = gr.Button("🔄 Refresh Prices", elem_classes=["primary-btn"])

                with gr.Row():
                    with gr.Column(elem_classes=["glass-panel"]):
                        gold_display = gr.Markdown("*Click 'Refresh Prices' to load gold data...*")
                    with gr.Column(elem_classes=["glass-panel"]):
                        silver_display = gr.Markdown("*Click 'Refresh Prices' to load silver data...*")

                with gr.Column(elem_classes=["glass-panel"]):
                    currency_display = gr.Markdown("*Click 'Refresh Prices' to load exchange rates...*")

                refresh_btn.click(
                    on_refresh_market,
                    outputs=[gold_display, silver_display, currency_display],
                )

            # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            #  TAB 4: FINANCIAL CALCULATORS
            # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            with gr.Tab("🧮 Financial Calculators", id="calculators_tab"):
                gr.Markdown("### 🧮 Smart Financial Calculators\n*Professional tools for everyday financial planning.*")

                with gr.Tabs():
                    # GST Calculator
                    with gr.Tab("🧾 GST"):
                        with gr.Row():
                            with gr.Column():
                                gst_amount = gr.Number(label="Base Amount (₹)", value=10000)
                                gst_rate = gr.Dropdown(
                                    choices=["5", "12", "18", "28"],
                                    value="18",
                                    label="GST Rate (%)",
                                )
                                gst_interstate = gr.Checkbox(label="Inter-State Transaction (IGST)?", value=False)
                                gst_btn = gr.Button("Calculate GST", elem_classes=["primary-btn"])
                            with gr.Column(elem_classes=["calc-result-box"]):
                                gst_result = gr.Markdown()

                        gst_btn.click(
                            on_gst_calculate,
                            inputs=[gst_amount, gst_rate, gst_interstate],
                            outputs=gst_result,
                        )

                    # EMI Calculator
                    with gr.Tab("🏦 EMI"):
                        with gr.Row():
                            with gr.Column():
                                emi_principal = gr.Number(label="Loan Amount (₹)", value=5000000)
                                emi_rate = gr.Number(label="Annual Interest Rate (%)", value=8.5)
                                emi_tenure = gr.Slider(1, 30, value=20, step=1, label="Tenure (Years)")
                                emi_btn = gr.Button("Calculate EMI", elem_classes=["primary-btn"])
                            with gr.Column(elem_classes=["calc-result-box"]):
                                emi_result = gr.Markdown()

                        emi_btn.click(
                            on_emi_calculate,
                            inputs=[emi_principal, emi_rate, emi_tenure],
                            outputs=emi_result,
                        )

                    # SIP Calculator
                    with gr.Tab("📈 SIP"):
                        with gr.Row():
                            with gr.Column():
                                sip_monthly = gr.Number(label="Monthly SIP Amount (₹)", value=5000)
                                sip_rate = gr.Number(label="Expected Annual Return (%)", value=12)
                                sip_years = gr.Slider(1, 40, value=20, step=1, label="Investment Period (Years)")
                                sip_btn = gr.Button("Calculate SIP", elem_classes=["primary-btn"])
                            with gr.Column(elem_classes=["calc-result-box"]):
                                sip_result = gr.Markdown()

                        sip_btn.click(
                            on_sip_calculate,
                            inputs=[sip_monthly, sip_rate, sip_years],
                            outputs=sip_result,
                        )

                    # Compound Interest
                    with gr.Tab("💰 Compound Interest"):
                        with gr.Row():
                            with gr.Column():
                                ci_principal = gr.Number(label="Principal Amount (₹)", value=100000)
                                ci_rate = gr.Number(label="Annual Interest Rate (%)", value=7.1)
                                ci_years = gr.Slider(1, 30, value=15, step=1, label="Tenure (Years)")
                                ci_freq = gr.Dropdown(
                                    choices=["Annual", "Semi-Annual", "Quarterly", "Monthly", "Daily"],
                                    value="Annual",
                                    label="Compounding Frequency",
                                )
                                ci_btn = gr.Button("Calculate", elem_classes=["primary-btn"])
                            with gr.Column(elem_classes=["calc-result-box"]):
                                ci_result = gr.Markdown()

                        ci_btn.click(
                            on_ci_calculate,
                            inputs=[ci_principal, ci_rate, ci_years, ci_freq],
                            outputs=ci_result,
                        )

                    # Budget Planner
                    with gr.Tab("📋 Budget Planner"):
                        with gr.Row():
                            with gr.Column():
                                budget_income = gr.Number(label="Monthly Income (₹)", value=50000)
                                budget_btn = gr.Button("Plan My Budget", elem_classes=["primary-btn"])
                            with gr.Column(elem_classes=["calc-result-box"]):
                                budget_result = gr.Markdown()

                        budget_btn.click(
                            on_budget_calculate,
                            inputs=[budget_income],
                            outputs=budget_result,
                        )

                    # Savings Goal
                    with gr.Tab("🎯 Savings Goal"):
                        with gr.Row():
                            with gr.Column():
                                sg_target = gr.Number(label="Target Amount (₹)", value=1000000)
                                sg_current = gr.Number(label="Current Savings (₹)", value=100000)
                                sg_rate = gr.Number(label="Expected Annual Return (%)", value=10)
                                sg_years = gr.Slider(1, 30, value=5, step=1, label="Time Horizon (Years)")
                                sg_btn = gr.Button("Calculate", elem_classes=["primary-btn"])
                            with gr.Column(elem_classes=["calc-result-box"]):
                                sg_result = gr.Markdown()

                        sg_btn.click(
                            on_savings_goal_calculate,
                            inputs=[sg_target, sg_current, sg_rate, sg_years],
                            outputs=sg_result,
                        )

            # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            #  TAB 5: LEARNING HUB
            # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            with gr.Tab("📚 Learning Hub", id="learning_hub_tab"):
                gr.Markdown(learning_hub.get_topic_summary_cards())

                with gr.Row():
                    for topic in learning_hub.get_all_topics()[:5]:
                        with gr.Column(elem_classes=["learning-card"], min_width=250):
                            with gr.Accordion(f"{topic.icon} {topic.title}", open=False):
                                gr.Markdown(f"*{topic.subtitle}* — **Category:** {topic.category}")
                                gr.Markdown(topic.content)
                with gr.Row():
                    for topic in learning_hub.get_all_topics()[5:]:
                        with gr.Column(elem_classes=["learning-card"], min_width=250):
                            with gr.Accordion(f"{topic.icon} {topic.title}", open=False):
                                gr.Markdown(f"*{topic.subtitle}* — **Category:** {topic.category}")
                                gr.Markdown(topic.content)

            # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            #  TAB 6: FINANCIAL HEALTH
            # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            with gr.Tab("📊 Financial Health", id="financial_health_tab"):
                gr.Markdown(
                    "### 📊 Financial Health Dashboard\n"
                    "*Get a comprehensive assessment of your financial well-being. "
                    "Enter your financial details below.*"
                )

                with gr.Row():
                    with gr.Column(scale=1, elem_classes=["glass-panel"]):
                        health_income = gr.Number(label="Monthly Income (₹)", value=50000)
                        health_savings = gr.Number(label="Monthly Savings (₹)", value=10000)
                        health_debt = gr.Number(label="Total Debt (₹)", value=500000)
                        health_expenses = gr.Number(label="Monthly Expenses (₹)", value=30000)
                        health_emergency = gr.Number(label="Emergency Fund (₹)", value=100000)
                        health_btn = gr.Button("🔍 Analyze My Finances", elem_classes=["primary-btn"])

                    with gr.Column(scale=2, elem_classes=["glass-panel"]):
                        health_score_display = gr.HTML()
                        health_details_display = gr.Markdown()

                with gr.Row(elem_classes=["glass-panel"]):
                    health_pie = gr.Plot(label="Score Distribution")
                    health_bar = gr.Plot(label="Dimension Scores")

                health_btn.click(
                    on_health_calculate,
                    inputs=[health_income, health_savings, health_debt, health_expenses, health_emergency],
                    outputs=[health_score_display, health_details_display, health_pie, health_bar],
                )

            # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            #  TAB 7: ABOUT
            # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            with gr.Tab("ℹ️ About", id="about_tab"):
                with gr.Column(elem_classes=["glass-panel"]):
                    gr.Markdown("""
# 🧠 ArthaMind AI

**Your Intelligent Personal Finance Advisor for Indian Citizens**

---

## 🎯 Project Overview

ArthaMind AI is a **production-grade, multilingual AI-powered personal finance assistant** 
built specifically for Indian citizens. It combines cutting-edge AI technologies with 
deep domain knowledge of Indian finance to help users make better financial decisions.

The name "Artha" (अर्थ) means **wealth/finance** in Sanskrit, and "Mind" represents 
the **AI intelligence** that powers the platform.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│              Gradio Blocks UI                   │
│  (Chat, Voice, Market, Calculators, Learning)   │
├─────────────────────────────────────────────────┤
│            Business Logic Layer                 │
│  (prompts.py, calculators.py, learning.py)      │
├─────────────────────────────────────────────────┤
│         LLM Agent Layer (LangChain)             │
│  (Google Gemini 2.5 Flash + Tool Calling)       │
├─────────────────────────────────────────────────┤
│              Tool Layer                         │
│  (tools.py, market.py, voice.py)                │
├─────────────────────────────────────────────────┤
│         Vector Database (ChromaDB)              │
│  (sentence-transformers/all-MiniLM-L6-v2)       │
├─────────────────────────────────────────────────┤
│           External APIs                         │
│  (Gemini, AssemblyAI, Murf AI, GoldAPI)         │
└─────────────────────────────────────────────────┘
```

---

## ⚡ Technology Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Gradio Blocks (Professional Dark UI) |
| **LLM** | Google Gemini 2.5 Flash |
| **AI Framework** | LangChain (LCEL) |
| **Vector Database** | ChromaDB |
| **Embeddings** | sentence-transformers/all-MiniLM-L6-v2 |
| **Speech-to-Text** | AssemblyAI |
| **Text-to-Speech** | Murf AI / gTTS |
| **Market Data** | GoldAPI, Frankfurter API |
| **Charts** | Plotly |
| **Deployment** | Hugging Face Spaces |

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 💬 **AI Chat Assistant** | Context-aware financial Q&A with RAG |
| 🎙️ **Voice Assistant** | Speak your questions in 6 Indian languages |
| 📈 **Live Market Data** | Real-time gold, silver, and currency prices |
| 🧮 **Smart Calculators** | GST, EMI, SIP, Compound Interest, Budget |
| 📚 **Learning Hub** | 10+ financial education modules |
| 📊 **Health Dashboard** | Multi-dimensional financial health scoring |
| 🌐 **Multilingual** | English, Hindi, Telugu, Tamil, Kannada, Malayalam |
| 📄 **Source Citations** | Every answer backed by verified sources |
| 🔒 **Anti-Hallucination** | Strict guardrails against fabricated data |

---

## 📁 Project Structure

```
ArthaMind-AI/
├── app.py              # Main Gradio application
├── config.py           # Configuration & environment variables
├── rag.py              # RAG pipeline (ChromaDB + embeddings)
├── voice.py            # Voice assistant (STT + TTS)
├── market.py           # Live market data fetching
├── tools.py            # LangChain tool definitions
├── prompts.py          # System prompts & templates
├── calculators.py      # Financial calculator functions
├── learning.py         # Financial education content
├── utils.py            # Shared utilities & helpers
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variable template
├── README.md           # Project documentation
├── LICENSE             # MIT License
├── assets/             # Static assets
├── data/               # Knowledge base documents
└── logs/               # Application logs
```

---

## 🚀 Future Scope

- 📊 **Stock Market Integration** — Real-time NSE/BSE data via yfinance
- 🤖 **Agentic Workflows** — Multi-step reasoning with LangGraph
- 📱 **Mobile App** — React Native companion app
- 🔐 **User Authentication** — Persistent profiles and history
- 📈 **Portfolio Tracker** — Track mutual fund and stock investments
- 🧠 **Fine-tuned Models** — Domain-specific model for Indian finance
- 🌍 **More Languages** — Bengali, Marathi, Gujarati, Punjabi
- 📄 **Custom PDF Upload** — Upload your own financial documents for RAG

---

## 👨‍💻 Developer

Built with ❤️ as a showcase of AI/ML engineering capabilities.

| | |
|---|---|
| **Built with** | Python, LangChain, Gemini AI, Gradio |
| **Architecture** | Clean Architecture, Modular Design, Production-Ready |
| **License** | MIT — Open Source |

---

                """)

        # ── Dashboard & Quick Action Click Handlers ─────────
        tax_btn.click(lambda: gr.Tabs(selected="calculators_tab"), outputs=main_tabs)
        loan_btn.click(lambda: gr.Tabs(selected="calculators_tab"), outputs=main_tabs)
        sip_btn.click(lambda: gr.Tabs(selected="calculators_tab"), outputs=main_tabs)
        gold_btn.click(lambda: gr.Tabs(selected="live_market_tab"), outputs=main_tabs)
        score_btn.click(lambda: gr.Tabs(selected="financial_health_tab"), outputs=main_tabs)
        budget_btn.click(lambda: gr.Tabs(selected="calculators_tab"), outputs=main_tabs)
        portfolio_btn.click(lambda: gr.Tabs(selected="live_market_tab"), outputs=main_tabs)
        retirement_btn.click(lambda: gr.Tabs(selected="calculators_tab"), outputs=main_tabs)
        forex_btn.click(lambda: gr.Tabs(selected="live_market_tab"), outputs=main_tabs)
        learn_btn.click(lambda: gr.Tabs(selected="learning_hub_tab"), outputs=main_tabs)

        # Page load event to populate dashboard
        app.load(on_dashboard_load, outputs=dashboard_market_html)

        # ── Footer ───────────────────────────────────────────
        gr.HTML("""
        <div id="app-footer" class="glass-panel" style="margin-top: 40px; padding: 20px !important; text-align: center;">
            <p style="margin: 0 0 10px 0; font-weight: 600; color: var(--text-primary);">🧠 ArthaMind AI v1.0 — Made with ❤️ in India</p>
            <p style="margin: 0; font-size: 0.8rem; color: var(--text-muted); line-height: 1.6;">
                Powered by: Gemini 2.5 Flash • LangChain • ChromaDB • AssemblyAI • Murf AI • Gradio • Hugging Face • GoldAPI • Frankfurter API
            </p>
            <p style="margin: 8px 0 0 0; font-size: 0.75rem; color: var(--text-muted); font-style: italic;">
                ⚠️ Disclaimer: This is an educational tool. Always consult a certified financial advisor for important financial decisions.
            </p>
        </div>
        """)

    return app


# ═══════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("ArthaMind AI — Starting Application")
    logger.info("=" * 60)

    # Validate configuration
    service_status = settings.get_available_services()
    logger.info(f"Service Status:\n{service_status}")

    # Initialize AI engine
    engine.initialize()

    # Build and launch app
    app = create_app()
    theme = gr.themes.Base(
        primary_hue=gr.themes.colors.sky,
        secondary_hue=gr.themes.colors.purple,
        neutral_hue=gr.themes.colors.slate,
        font=gr.themes.GoogleFont("Inter"),
    )
    app.launch(
        server_port=settings.GRADIO_SERVER_PORT,
        share=settings.GRADIO_SHARE,
        show_error=True,
        theme=theme,
        css=CUSTOM_CSS,
        head="""<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/lucide-static@0.321.0/font/lucide.min.css">""",
    )
