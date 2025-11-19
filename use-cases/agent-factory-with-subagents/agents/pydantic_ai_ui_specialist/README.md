# Pydantic AI UI Specialist - Pydantic AI Agent

An elite UI/UX Specialist agent built with Pydantic AI that analyzes React components and provides comprehensive recommendations for accessibility, responsive design, performance, and user experience.

## Features

- **Accessibility Analysis**: WCAG 2.1 AA/AAA compliance checking
- **Responsive Design Review**: Mobile-first best practices validation
- **Performance Optimization**: Component performance analysis and recommendations
- **UX Pattern Validation**: User experience best practices checking
- **Color Contrast Checking**: WCAG contrast ratio validation
- **Comprehensive Reporting**: Detailed analysis with actionable recommendations

## Installation

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and configure your settings:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
LLM_PROVIDER=openai
LLM_API_KEY=your-openai-api-key
LLM_MODEL=gpt-4
LLM_BASE_URL=https://api.openai.com/v1
```

## Usage

### Basic Usage

```python
from pydantic_ai_ui_specialist import analyze_component

# Example React component
component_code = """
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

# Analyze the component
result = await analyze_component(
    component_code=component_code,
    analysis_focus="general",  # or "accessibility", "responsive", "performance", "ux"
    typescript_enabled=True,
    wcag_level="AA"
)

print(result)
```

### Focused Analysis

```python
# Focus on accessibility only
accessibility_result = await analyze_component(
    component_code=component_code,
    analysis_focus="accessibility",
    wcag_level="AAA",
    required_aria_support=True,
    keyboard_nav_required=True
)

# Focus on performance
performance_result = await analyze_component(
    component_code=component_code,
    analysis_focus="performance",
    code_splitting_enabled=True,
    lazy_loading_enabled=True,
    performance_budget_ms=3000
)

# Focus on responsive design
responsive_result = await analyze_component(
    component_code=component_code,
    analysis_focus="responsive",
    mobile_first=True,
    target_breakpoints=[320, 768, 1024, 1440]
)
```

### Using the Agent Directly

```python
from pydantic_ai_ui_specialist import agent
from pydantic_ai_ui_specialist.dependencies import UIAnalysisContext

# Create analysis context
deps = UIAnalysisContext(
    component_code=component_code,
    analysis_focus="general",
    typescript_enabled=True,
    styling_approach="Tailwind",
    wcag_level="AA"
)

# Run agent
result = await agent.run(
    "Analyze this component for UI/UX issues",
    deps=deps
)

print(result.data)
```

## Analysis Focus Areas

### General Analysis
Comprehensive review covering all areas:
- Accessibility compliance
- Responsive design patterns
- Performance optimizations
- UX best practices

### Accessibility Focus
- WCAG 2.1 compliance checking
- ARIA attribute validation
- Keyboard navigation support
- Screen reader compatibility
- Color contrast ratios
- Semantic HTML structure

### Responsive Design Focus
- Mobile-first approach validation
- Breakpoint strategy review
- Fluid layout analysis
- Touch target size checking
- Viewport configuration

### Performance Focus
- Component memoization opportunities
- Code splitting suggestions
- Lazy loading recommendations
- Re-render optimization
- Key prop validation

### UX Focus
- Loading state handling
- Error state management
- Form validation feedback
- User feedback mechanisms
- Optimistic UI patterns

## Available Tools

The agent has access to several specialized tools:

### `analyze_accessibility`
Analyzes component for accessibility issues based on WCAG guidelines.

### `analyze_responsive_patterns`
Reviews responsive design patterns and mobile-first implementation.

### `analyze_performance_optimizations`
Identifies performance optimization opportunities.

### `analyze_ux_best_practices`
Validates UX patterns and user feedback mechanisms.

### `check_contrast_ratio`
Checks color contrast ratios for WCAG compliance.

### `get_wcag_reference`
Provides WCAG 2.1 guideline reference information.

## Configuration Options

### UIAnalysisContext Parameters

```python
UIAnalysisContext(
    component_code: str,                    # Required: Component code to analyze
    analysis_focus: str = "general",        # Focus area
    project_framework: str = "React",       # Framework (React, Vue, Angular)
    typescript_enabled: bool = True,        # TypeScript usage
    styling_approach: str = None,           # Tailwind, CSS-in-JS, CSS Modules, etc.
    wcag_level: str = "AA",                # WCAG compliance level (AA or AAA)
    required_aria_support: bool = True,     # Require ARIA attributes
    keyboard_nav_required: bool = True,     # Require keyboard navigation
    target_breakpoints: List[int] = [320, 768, 1024, 1440],
    mobile_first: bool = True,              # Mobile-first approach
    performance_budget_ms: int = 3000,      # Performance budget (TTI)
    code_splitting_enabled: bool = True,    # Code splitting support
    lazy_loading_enabled: bool = True,      # Lazy loading support
)
```

## Output Structure

The agent provides detailed analysis with:

- **Summary**: Overall assessment
- **Issues Found**: Categorized by type and severity
- **Recommendations**: Specific, actionable suggestions
- **Code Examples**: Implementation examples for fixes
- **Rationale**: Explanation of why changes are recommended
- **Resources**: Links to relevant documentation

## Examples

### Example 1: Accessibility Analysis

```python
result = await analyze_component(
    component_code="""
    <button onClick={handleClick}>
      <svg>...</svg>
    </button>
    """,
    analysis_focus="accessibility"
)

# Output includes:
# - Missing aria-label for icon button
# - Keyboard navigation recommendations
# - Screen reader compatibility suggestions
```

### Example 2: Performance Analysis

```python
result = await analyze_component(
    component_code="""
    export const UserList = ({ users }) => {
      return users.map(user => <UserCard key={user.id} {...user} />)
    }
    """,
    analysis_focus="performance"
)

# Output includes:
# - React.memo recommendation for UserCard
# - Code splitting suggestions
# - Virtualization recommendations for large lists
```

## Command Line Usage

Run the agent from the command line:

```bash
python -m pydantic_ai_ui_specialist.agent
```

This will run the example analysis included in `agent.py`.

## Testing

Create test files for your components and analyze them:

```python
import asyncio
from pydantic_ai_ui_specialist import analyze_component

async def test_my_component():
    with open('MyComponent.tsx', 'r') as f:
        component_code = f.read()

    result = await analyze_component(
        component_code=component_code,
        analysis_focus="general",
        typescript_enabled=True
    )

    print(result)

if __name__ == "__main__":
    asyncio.run(test_my_component())
```

## Best Practices

1. **Start with General Analysis**: Get a comprehensive overview first
2. **Focus Deep Dives**: Use focused analysis for specific concerns
3. **Iterate**: Apply recommendations and re-analyze
4. **Document Decisions**: Keep track of accepted trade-offs
5. **Accessibility First**: Always prioritize accessibility in decision-making

## Troubleshooting

### API Key Issues
Ensure your `.env` file contains a valid API key:
```env
LLM_API_KEY=sk-...your-actual-key...
```

### Module Import Errors
Make sure you've installed all dependencies:
```bash
pip install -r requirements.txt
```

### Analysis Not Working
Check that:
- Component code is valid TypeScript/JavaScript
- LLM model has sufficient context length
- API quota is not exceeded

## Contributing

To extend the agent with new tools or analysis capabilities:

1. Add new tool functions in `tools.py`
2. Register tools in `agent.py` using `@agent.tool` decorator
3. Update prompts in `prompts.py` if needed
4. Add tests for new functionality

## License

MIT License - See LICENSE file for details

## Support

For issues or questions:
- Check the documentation
- Review example code
- Ensure environment is properly configured
- Verify API credentials

## Version

Current version: 1.0.0

## Changelog

### 1.0.0 (Initial Release)
- Complete UI/UX analysis agent
- Accessibility checking (WCAG 2.1)
- Responsive design validation
- Performance optimization suggestions
- UX pattern recommendations
- Color contrast checking
- Comprehensive tooling for React components
