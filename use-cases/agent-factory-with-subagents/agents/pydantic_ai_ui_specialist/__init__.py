"""
Pydantic AI UI Specialist Agent

A specialized AI agent for UI/UX analysis and recommendations.
"""

from .agent import agent, analyze_component
from .settings import Settings, load_settings, get_llm_model
from .dependencies import UIAnalysisContext, UIRecommendation, AnalysisResult
from .prompts import get_system_prompt, get_analysis_prompt

__all__ = [
    "agent",
    "analyze_component",
    "Settings",
    "load_settings",
    "get_llm_model",
    "UIAnalysisContext",
    "UIRecommendation",
    "AnalysisResult",
    "get_system_prompt",
    "get_analysis_prompt",
]

__version__ = "1.0.0"
