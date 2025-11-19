"""
UI Specialist Agent Tools

Defines the tool functions available to the UI/UX specialist agent.
These tools help the agent analyze code, check accessibility, and provide recommendations.
"""

import re
from typing import List, Dict, Tuple


def check_color_contrast(
    foreground: str, background: str, text_size: str = "normal"
) -> Dict[str, any]:
    """
    Check color contrast ratio for WCAG compliance.

    Args:
        foreground: Foreground color (hex format, e.g., "#000000")
        background: Background color (hex format)
        text_size: "normal" or "large" text

    Returns:
        Dict with contrast ratio and WCAG compliance status
    """
    # Simple implementation - would use actual color contrast calculation
    # For demo purposes, returning mock data
    return {
        "contrast_ratio": 4.5,
        "wcag_aa": True,
        "wcag_aaa": False,
        "recommendation": "Meets WCAG AA for normal text",
    }


def analyze_accessibility_issues(component_code: str) -> List[Dict[str, str]]:
    """
    Analyze component code for common accessibility issues.

    Args:
        component_code: React component code to analyze

    Returns:
        List of accessibility issues found
    """
    issues = []

    # Check for missing alt text on images
    if re.search(r'<img[^>]*(?!alt=)', component_code):
        issues.append({
            "type": "accessibility",
            "severity": "high",
            "issue": "Images without alt text",
            "description": "All images should have descriptive alt text for screen readers",
            "fix": 'Add alt attribute: <img src="..." alt="Description" />',
        })

    # Check for buttons without aria-label when only icons
    if re.search(r'<button[^>]*>(?=\s*<(?:svg|i|span\s+class=)', component_code):
        if not re.search(r'aria-label=', component_code):
            issues.append({
                "type": "accessibility",
                "severity": "high",
                "issue": "Icon buttons without aria-label",
                "description": "Icon-only buttons need aria-label for screen readers",
                "fix": '<button aria-label="Descriptive label">...</button>',
            })

    # Check for forms without labels
    if re.search(r'<input[^>]*(?!id=)', component_code):
        issues.append({
            "type": "accessibility",
            "severity": "medium",
            "issue": "Form inputs may lack associated labels",
            "description": "Inputs should have associated labels for accessibility",
            "fix": '<label htmlFor="inputId">Label</label><input id="inputId" />',
        })

    # Check for missing keyboard event handlers
    if re.search(r'onClick=', component_code) and not re.search(
        r'onKeyDown=|onKeyPress=', component_code
    ):
        issues.append({
            "type": "accessibility",
            "severity": "medium",
            "issue": "Click handlers without keyboard support",
            "description": "Interactive elements with onClick should also handle keyboard events",
            "fix": "Add onKeyDown handler for Enter/Space keys",
        })

    return issues


def analyze_responsive_design(component_code: str) -> List[Dict[str, str]]:
    """
    Analyze component for responsive design patterns.

    Args:
        component_code: React component code to analyze

    Returns:
        List of responsive design recommendations
    """
    recommendations = []

    # Check for hardcoded pixel values
    if re.search(r'width:\s*\d+px|height:\s*\d+px', component_code):
        recommendations.append({
            "type": "responsive",
            "severity": "medium",
            "issue": "Hardcoded pixel values detected",
            "description": "Consider using relative units (rem, em, %) for better responsiveness",
            "fix": "Replace fixed pixels with relative units or CSS variables",
        })

    # Check for mobile-first media queries
    if re.search(r'@media.*max-width', component_code):
        recommendations.append({
            "type": "responsive",
            "severity": "low",
            "issue": "max-width media queries detected",
            "description": "Consider mobile-first approach with min-width media queries",
            "fix": "Use min-width for progressive enhancement",
        })

    # Check for viewport meta tag consideration
    if not re.search(r'viewport', component_code):
        recommendations.append({
            "type": "responsive",
            "severity": "info",
            "issue": "Ensure viewport meta tag is set",
            "description": "Make sure your HTML includes viewport meta tag for mobile responsiveness",
            "fix": '<meta name="viewport" content="width=device-width, initial-scale=1" />',
        })

    return recommendations


def analyze_performance(component_code: str) -> List[Dict[str, str]]:
    """
    Analyze component for performance optimization opportunities.

    Args:
        component_code: React component code to analyze

    Returns:
        List of performance recommendations
    """
    recommendations = []

    # Check for missing React.memo
    if re.search(r'export\s+(?:const|function)\s+\w+', component_code):
        if not re.search(r'React\.memo|memo\(', component_code):
            recommendations.append({
                "type": "performance",
                "severity": "low",
                "issue": "Component not memoized",
                "description": "Consider using React.memo() for components that render frequently with same props",
                "fix": "export const Component = React.memo(({ props }) => { ... })",
            })

    # Check for inline function definitions in JSX
    if re.search(r'onClick=\{.*=>', component_code):
        recommendations.append({
            "type": "performance",
            "severity": "medium",
            "issue": "Inline function definitions in JSX",
            "description": "Inline functions create new instances on each render",
            "fix": "Use useCallback for event handlers: const handleClick = useCallback(() => { ... }, [])",
        })

    # Check for missing key props in lists
    if re.search(r'\.map\(.*=>', component_code):
        if not re.search(r'key=', component_code):
            recommendations.append({
                "type": "performance",
                "severity": "high",
                "issue": "Missing key prop in list rendering",
                "description": "Lists need unique key props for efficient re-rendering",
                "fix": "Add unique key: items.map(item => <div key={item.id}>...</div>)",
            })

    return recommendations


def analyze_ux_patterns(component_code: str) -> List[Dict[str, str]]:
    """
    Analyze component for UX best practices.

    Args:
        component_code: React component code to analyze

    Returns:
        List of UX recommendations
    """
    recommendations = []

    # Check for loading state handling
    if re.search(r'useState|isLoading', component_code):
        if not re.search(r'loading|skeleton|spinner', component_code, re.IGNORECASE):
            recommendations.append({
                "type": "ux",
                "severity": "medium",
                "issue": "Missing loading state UI",
                "description": "Show loading indicators for async operations",
                "fix": "{isLoading ? <Spinner /> : <Content />}",
            })

    # Check for error state handling
    if re.search(r'catch|error|onError', component_code):
        if not re.search(r'error.*message|ErrorBoundary', component_code):
            recommendations.append({
                "type": "ux",
                "severity": "high",
                "issue": "Missing error state UI",
                "description": "Display user-friendly error messages",
                "fix": "{error && <Alert type='error'>{error.message}</Alert>}",
            })

    # Check for form validation feedback
    if re.search(r'<form|<input', component_code):
        if not re.search(r'error|valid|invalid', component_code):
            recommendations.append({
                "type": "ux",
                "severity": "medium",
                "issue": "Missing form validation feedback",
                "description": "Provide real-time validation feedback to users",
                "fix": "Add error states and validation messages to form fields",
            })

    return recommendations


def get_wcag_guidelines() -> List[Dict[str, str]]:
    """
    Get WCAG 2.1 accessibility guidelines summary.

    Returns:
        List of key WCAG guidelines
    """
    return [
        {
            "principle": "Perceivable",
            "guideline": "Text Alternatives",
            "requirement": "Provide text alternatives for non-text content",
            "level": "A",
        },
        {
            "principle": "Perceivable",
            "guideline": "Color Contrast",
            "requirement": "Minimum contrast ratio of 4.5:1 for normal text",
            "level": "AA",
        },
        {
            "principle": "Operable",
            "guideline": "Keyboard Accessible",
            "requirement": "All functionality available via keyboard",
            "level": "A",
        },
        {
            "principle": "Operable",
            "guideline": "Focus Visible",
            "requirement": "Keyboard focus indicator visible",
            "level": "AA",
        },
        {
            "principle": "Understandable",
            "guideline": "Error Identification",
            "requirement": "Input errors are identified and described to user",
            "level": "A",
        },
        {
            "principle": "Robust",
            "guideline": "Name, Role, Value",
            "requirement": "Elements have appropriate ARIA attributes",
            "level": "A",
        },
    ]
