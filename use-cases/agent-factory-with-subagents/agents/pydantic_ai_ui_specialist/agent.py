"""
UI Specialist Pydantic AI Agent

Main agent implementation for UI/UX analysis and recommendations.
"""

from pydantic_ai import Agent, RunContext
from .settings import get_llm_model
from .prompts import get_system_prompt, get_analysis_prompt
from .dependencies import UIAnalysisContext
from .tools import (
    check_color_contrast,
    analyze_accessibility_issues,
    analyze_responsive_design,
    analyze_performance,
    analyze_ux_patterns,
    get_wcag_guidelines,
)

# Initialize the UI Specialist agent
agent = Agent(
    get_llm_model(),
    deps_type=UIAnalysisContext,
    system_prompt=get_system_prompt(),
)


@agent.tool
def analyze_accessibility(ctx: RunContext[UIAnalysisContext]) -> str:
    """
    Analyze component code for accessibility issues.

    Args:
        ctx: Agent run context with component code

    Returns:
        JSON string of accessibility issues found
    """
    issues = analyze_accessibility_issues(ctx.deps.component_code)

    if not issues:
        return "No accessibility issues found. Component follows WCAG guidelines."

    result = "Accessibility Issues Found:\n\n"
    for i, issue in enumerate(issues, 1):
        result += f"{i}. [{issue['severity'].upper()}] {issue['issue']}\n"
        result += f"   {issue['description']}\n"
        result += f"   Fix: {issue['fix']}\n\n"

    return result


@agent.tool
def analyze_responsive_patterns(ctx: RunContext[UIAnalysisContext]) -> str:
    """
    Analyze component for responsive design patterns.

    Args:
        ctx: Agent run context with component code

    Returns:
        JSON string of responsive design recommendations
    """
    recommendations = analyze_responsive_design(ctx.deps.component_code)

    if not recommendations:
        return "Component follows responsive design best practices."

    result = "Responsive Design Recommendations:\n\n"
    for i, rec in enumerate(recommendations, 1):
        result += f"{i}. [{rec['severity'].upper()}] {rec['issue']}\n"
        result += f"   {rec['description']}\n"
        result += f"   Recommendation: {rec['fix']}\n\n"

    return result


@agent.tool
def analyze_performance_optimizations(ctx: RunContext[UIAnalysisContext]) -> str:
    """
    Analyze component for performance optimization opportunities.

    Args:
        ctx: Agent run context with component code

    Returns:
        JSON string of performance recommendations
    """
    recommendations = analyze_performance(ctx.deps.component_code)

    if not recommendations:
        return "Component is well-optimized for performance."

    result = "Performance Optimization Opportunities:\n\n"
    for i, rec in enumerate(recommendations, 1):
        result += f"{i}. [{rec['severity'].upper()}] {rec['issue']}\n"
        result += f"   {rec['description']}\n"
        result += f"   Optimization: {rec['fix']}\n\n"

    return result


@agent.tool
def analyze_ux_best_practices(ctx: RunContext[UIAnalysisContext]) -> str:
    """
    Analyze component for UX best practices.

    Args:
        ctx: Agent run context with component code

    Returns:
        JSON string of UX recommendations
    """
    recommendations = analyze_ux_patterns(ctx.deps.component_code)

    if not recommendations:
        return "Component follows UX best practices."

    result = "UX Pattern Recommendations:\n\n"
    for i, rec in enumerate(recommendations, 1):
        result += f"{i}. [{rec['severity'].upper()}] {rec['issue']}\n"
        result += f"   {rec['description']}\n"
        result += f"   Best Practice: {rec['fix']}\n\n"

    return result


@agent.tool_plain
def get_wcag_reference() -> str:
    """
    Get WCAG 2.1 accessibility guidelines reference.

    Returns:
        Summary of key WCAG guidelines
    """
    guidelines = get_wcag_guidelines()

    result = "WCAG 2.1 Key Guidelines:\n\n"
    for guideline in guidelines:
        result += f"• {guideline['principle']} - {guideline['guideline']}\n"
        result += f"  Requirement: {guideline['requirement']}\n"
        result += f"  Level: {guideline['level']}\n\n"

    return result


@agent.tool_plain
def check_contrast_ratio(foreground: str, background: str, text_size: str = "normal") -> str:
    """
    Check color contrast ratio for WCAG compliance.

    Args:
        foreground: Foreground color (hex format, e.g., "#000000")
        background: Background color (hex format)
        text_size: "normal" or "large" text

    Returns:
        Contrast ratio analysis
    """
    result = check_color_contrast(foreground, background, text_size)

    output = f"Color Contrast Analysis:\n"
    output += f"  Foreground: {foreground}\n"
    output += f"  Background: {background}\n"
    output += f"  Text Size: {text_size}\n"
    output += f"  Contrast Ratio: {result['contrast_ratio']}:1\n"
    output += f"  WCAG AA: {'✓ Pass' if result['wcag_aa'] else '✗ Fail'}\n"
    output += f"  WCAG AAA: {'✓ Pass' if result['wcag_aaa'] else '✗ Fail'}\n"
    output += f"  Recommendation: {result['recommendation']}\n"

    return output


async def analyze_component(
    component_code: str,
    analysis_focus: str = "general",
    **context_kwargs,
) -> str:
    """
    Analyze a React component for UI/UX issues and recommendations.

    Args:
        component_code: The React component code to analyze
        analysis_focus: Focus area (general, accessibility, responsive, performance, ux)
        **context_kwargs: Additional context parameters

    Returns:
        Analysis results and recommendations
    """
    # Create analysis context
    deps = UIAnalysisContext(
        component_code=component_code,
        analysis_focus=analysis_focus,
        **context_kwargs,
    )

    # Generate analysis prompt
    prompt = get_analysis_prompt(component_code, analysis_focus)

    # Run agent with context
    result = await agent.run(prompt, deps=deps)

    return result.data


async def main():
    """Example usage of the UI Specialist agent."""
    example_component = """
import { FC, useState } from 'react'

export const LoginForm: FC = () => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  return (
    <form>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
      />
      <button onClick={() => console.log('Submit')}>Login</button>
    </form>
  )
}
"""

    print("Analyzing LoginForm component...")
    print("-" * 80)

    result = await analyze_component(
        component_code=example_component,
        analysis_focus="general",
        typescript_enabled=True,
        wcag_level="AA",
    )

    print(result)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
