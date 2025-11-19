"""
UI Specialist Agent Dependencies

Defines the dependency classes and context for the UI/UX specialist agent.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class UIAnalysisContext:
    """
    Context information for UI/UX analysis.

    This class holds the context needed by the agent to perform
    UI/UX analysis, including component code, project settings,
    and analysis focus areas.
    """

    # Component code to analyze
    component_code: str

    # Analysis focus (general, accessibility, responsive, performance, ux)
    analysis_focus: str = "general"

    # Project configuration
    project_framework: str = "React"  # React, Vue, Angular, etc.
    typescript_enabled: bool = True
    styling_approach: Optional[str] = None  # Tailwind, CSS-in-JS, CSS Modules, etc.

    # Design system information
    design_system_tokens: Dict[str, any] = field(default_factory=dict)
    component_library: Optional[str] = None  # MUI, Ant Design, custom, etc.

    # Accessibility requirements
    wcag_level: str = "AA"  # AA or AAA
    required_aria_support: bool = True
    keyboard_nav_required: bool = True

    # Target devices and breakpoints
    target_breakpoints: List[int] = field(
        default_factory=lambda: [320, 768, 1024, 1440]
    )
    mobile_first: bool = True

    # Performance considerations
    performance_budget_ms: int = 3000  # Time to interactive budget
    code_splitting_enabled: bool = True
    lazy_loading_enabled: bool = True

    # Additional context
    existing_patterns: List[str] = field(default_factory=list)
    known_issues: List[str] = field(default_factory=list)
    user_preferences: Dict[str, any] = field(default_factory=dict)

    def get_context_summary(self) -> str:
        """
        Generate a summary of the analysis context.

        Returns:
            str: Human-readable context summary
        """
        summary_parts = [
            f"Framework: {self.project_framework}",
            f"TypeScript: {'Enabled' if self.typescript_enabled else 'Disabled'}",
            f"Focus: {self.analysis_focus}",
            f"WCAG Level: {self.wcag_level}",
            f"Mobile First: {'Yes' if self.mobile_first else 'No'}",
        ]

        if self.styling_approach:
            summary_parts.append(f"Styling: {self.styling_approach}")

        if self.component_library:
            summary_parts.append(f"Component Library: {self.component_library}")

        return " | ".join(summary_parts)


@dataclass
class UIRecommendation:
    """
    Represents a UI/UX recommendation from the agent.
    """

    category: str  # accessibility, responsive, performance, ux, consistency
    severity: str  # critical, high, medium, low, suggestion
    title: str
    description: str
    code_example: Optional[str] = None
    rationale: Optional[str] = None
    resources: List[str] = field(default_factory=list)


@dataclass
class AnalysisResult:
    """
    Complete analysis result from the UI specialist agent.
    """

    summary: str
    recommendations: List[UIRecommendation]
    accessibility_score: Optional[int] = None  # 0-100
    performance_score: Optional[int] = None  # 0-100
    ux_score: Optional[int] = None  # 0-100
    overall_grade: Optional[str] = None  # A, B, C, D, F
    additional_notes: List[str] = field(default_factory=list)
