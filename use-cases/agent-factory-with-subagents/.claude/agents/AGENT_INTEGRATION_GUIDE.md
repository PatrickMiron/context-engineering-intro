# Pydantic AI Agent Integration Guide

This guide explains how to integrate Pydantic AI agents from this factory into your own projects. You can use these agents either as **Claude Code subagents** (invoked by the main Claude Code agent) or as **standalone CLI tools**.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Integration Overview](#integration-overview)
3. [Method 1: Claude Code Subagent Integration](#method-1-claude-code-subagent-integration)
4. [Method 2: Standalone CLI Usage](#method-2-standalone-cli-usage)
5. [CLAUDE.md Integration](#claudemd-integration)
6. [Complete Example: pydantic_ai_ui_specialist](#complete-example-pydantic_ai_ui_specialist)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before integrating any Pydantic AI agent, ensure you have:

- **Python 3.10+** installed
- **Virtual environment** (recommended)
- **Claude Code** installed (if using as subagent)
- **API keys** for the LLM provider (OpenAI, Anthropic, etc.)
- **Git** (for version control)

---

## Integration Overview

Each Pydantic AI agent consists of two parts:

### 1. **Agent Definition File** (`.md`)
- **Location**: `.claude/agents/pydantic-ai-[agent-name].md`
- **Purpose**: Tells Claude Code HOW to invoke the agent as a subagent
- **Contains**: Description, trigger conditions, examples, system prompt
- **Used by**: Claude Code main agent

### 2. **Agent Implementation** (Python package)
- **Location**: `agents/pydantic_ai_[agent_name]/`
- **Purpose**: The actual Pydantic AI agent code
- **Contains**: agent.py, tools.py, settings.py, dependencies.py, etc.
- **Used by**: Both Claude Code (via subprocess) AND standalone CLI

---

## Method 1: Claude Code Subagent Integration

Use this method when you want Claude Code to automatically invoke the agent based on user requests.

### Step 1: Copy the Agent Definition File

Copy the `.md` file from the factory to your project:

```bash
# From the agent factory project
cp .claude/agents/pydantic-ai-ui-specialist.md /path/to/your-project/.claude/agents/

# Verify it's there
ls /path/to/your-project/.claude/agents/
```

### Step 2: Copy the Agent Implementation

Copy the Python package to your project:

```bash
# From the agent factory project
cp -r agents/pydantic_ai_ui_specialist /path/to/your-project/agents/

# Verify the structure
ls /path/to/your-project/agents/pydantic_ai_ui_specialist/
```

### Step 3: Install Dependencies

In your project's virtual environment:

```bash
cd /path/to/your-project
source venv/bin/activate  # or venv_linux/bin/activate

# Install agent dependencies
pip install -r agents/pydantic_ai_ui_specialist/requirements.txt
```

### Step 4: Configure Environment Variables

Create or update your `.env` file:

```bash
# Copy the example
cp agents/pydantic_ai_ui_specialist/.env.example .env

# Edit .env with your API keys
nano .env
```

Add the required variables:
```env
LLM_PROVIDER=openai
LLM_API_KEY=sk-your-api-key-here
LLM_MODEL=gpt-4
LLM_BASE_URL=https://api.openai.com/v1
```

### Step 5: Verify Claude Code Integration

Start Claude Code and test the agent:

```bash
# In your project directory
claude-code

# Then in Claude Code, ask:
# "Can you analyze this React component for accessibility issues?"

# Claude Code should automatically invoke the pydantic-ai-ui-specialist agent
```

**How it works:**
1. Claude Code reads `.claude/agents/pydantic-ai-ui-specialist.md`
2. When user request matches the description/examples, Claude Code invokes the agent
3. Claude Code runs the Python agent as a subprocess
4. Results are returned to the main conversation

---

## Method 2: Standalone CLI Usage

Use this method to run the agent directly from the command line without Claude Code.

### Step 1: Copy Agent Implementation Only

You only need the Python package (not the .md file):

```bash
# Copy the agent
cp -r agents/pydantic_ai_ui_specialist /path/to/your-project/agents/

# Install dependencies
cd /path/to/your-project
pip install -r agents/pydantic_ai_ui_specialist/requirements.txt
```

### Step 2: Configure Environment

```bash
# Copy and edit .env
cp agents/pydantic_ai_ui_specialist/.env.example .env
nano .env
```

### Step 3: Run the Agent

**Option A: Using the agent module directly**

```bash
# Run the agent with the example
python -m agents.pydantic_ai_ui_specialist.agent

# This will run the built-in example from agent.py's main() function
```

**Option B: Create a custom script**

Create `run_ui_specialist.py`:

```python
import asyncio
from agents.pydantic_ai_ui_specialist import analyze_component

async def main():
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

    result = await analyze_component(
        component_code=component_code,
        analysis_focus="accessibility",
        wcag_level="AA",
        typescript_enabled=True
    )

    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

Run it:
```bash
python run_ui_specialist.py
```

**Option C: Interactive CLI**

Create `cli_ui_specialist.py`:

```python
import asyncio
import sys
from agents.pydantic_ai_ui_specialist import analyze_component

async def main():
    if len(sys.argv) < 2:
        print("Usage: python cli_ui_specialist.py <path-to-component.tsx>")
        sys.exit(1)

    file_path = sys.argv[1]

    with open(file_path, 'r') as f:
        component_code = f.read()

    print(f"Analyzing {file_path}...")
    print("-" * 80)

    result = await analyze_component(
        component_code=component_code,
        analysis_focus="general",
        typescript_enabled=True,
        wcag_level="AA"
    )

    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

Run it:
```bash
python cli_ui_specialist.py path/to/MyComponent.tsx
```

---

## CLAUDE.md Integration

To ensure your CLAUDE.md file properly utilizes Pydantic AI agents, follow these patterns:

### 1. Reference Agents in Workflow Sections

Add agent-specific instructions to your CLAUDE.md:

```markdown
# Your Project CLAUDE.md

## UI/UX Development Workflow

When working on frontend components:
- **ALWAYS** use the pydantic-ai-ui-specialist agent for component analysis
- Run accessibility checks before considering any component complete
- Follow the design system patterns recommended by the agent

### Using the UI Specialist Agent

The pydantic-ai-ui-specialist agent provides:
- Accessibility analysis (WCAG 2.1 AA/AAA compliance)
- Responsive design review
- Performance optimization suggestions
- UX pattern validation

**When to invoke:**
- After creating a new React component
- When refactoring existing components
- Before committing component changes
- When user requests UI/UX feedback
```

### 2. Add Agent-Specific Rules

```markdown
## Code Quality Standards

### Frontend Components

Before delivering any React component:
1. **Run pydantic-ai-ui-specialist analysis**
   - Ensure WCAG AA compliance
   - Verify responsive design across breakpoints
   - Check performance optimizations
2. **Apply all recommendations** from the agent
3. **Document any skipped recommendations** with rationale
```

### 3. Integration with Task Management

```markdown
## Task Workflow

### Frontend Development Tasks

When a task involves UI component work:
1. Implement the component
2. **Invoke pydantic-ai-ui-specialist** for analysis
3. Apply recommended fixes
4. Re-analyze until all critical issues are resolved
5. Mark task as complete only after agent approval
```

### 4. Proactive Agent Usage

Instruct Claude Code to use agents proactively:

```markdown
## AI Behavior Rules

### Proactive Agent Invocation

- **When creating React components**: Automatically invoke pydantic-ai-ui-specialist after implementation
- **When modifying forms**: Automatically check accessibility and validation patterns
- **When adding animations**: Verify prefers-reduced-motion support
- **When implementing file uploads**: Validate drag-and-drop accessibility

**DO NOT wait for user to request agent analysis** - invoke proactively for quality assurance.
```

### 5. Example CLAUDE.md Section

Here's a complete example section for your CLAUDE.md:

```markdown
# Frontend Development with Pydantic AI Agents

## Available Agents

### pydantic-ai-ui-specialist
**Purpose**: UI/UX analysis and recommendations for React components
**Location**: `agents/pydantic_ai_ui_specialist/`
**Invocation**: Claude Code automatically invokes based on UI/UX work

**Capabilities:**
- Accessibility analysis (WCAG 2.1 AA/AAA)
- Responsive design validation
- Performance optimization
- UX pattern recommendations
- Color contrast checking
- Design system consistency

## Workflow Integration

### Component Development Cycle

1. **Design Phase**
   - Define component requirements
   - Sketch component structure

2. **Implementation Phase**
   - Write TypeScript component
   - Implement styles (CSS/Tailwind)
   - Add tests

3. **Analysis Phase** ⚠️ **MANDATORY**
   - **Invoke pydantic-ai-ui-specialist**
   - Review all findings
   - Apply critical and high-severity fixes

4. **Refinement Phase**
   - Re-analyze after fixes
   - Iterate until quality gates pass

5. **Completion Phase**
   - Final analysis shows no critical issues
   - Mark task complete

## Quality Gates

A component is NOT complete until:
- ✅ pydantic-ai-ui-specialist analysis shows 0 critical issues
- ✅ WCAG AA compliance verified
- ✅ Responsive design tested across breakpoints (320px, 768px, 1024px, 1440px)
- ✅ Performance optimizations applied
- ✅ All interactive elements keyboard-accessible

## Usage Examples

### Example 1: New Component Analysis

```
User: "I've created a new Button component in src/components/Button.tsx"

Claude Code: "I'll analyze your Button component for accessibility and UX best practices."

[Invokes pydantic-ai-ui-specialist with component code]

[Receives analysis with 3 accessibility issues, 2 performance recommendations]

Claude Code: "Analysis complete. I found 3 accessibility issues:
1. [HIGH] Missing aria-label for icon-only variant
2. [MEDIUM] Focus indicator too subtle (1px vs recommended 2px)
3. [LOW] Loading state not announced to screen readers

Shall I apply these fixes?"
```

### Example 2: Proactive Analysis

```
[User creates a LoginForm component]

Claude Code: "I notice you've created a form component. Let me automatically
analyze it for accessibility and UX best practices using the UI specialist agent."

[Invokes agent without being asked]

Claude Code: "Analysis complete. The form needs improvements:
- Missing labels for inputs (WCAG violation)
- No error handling UI
- Password visibility toggle recommended
- Submit button should disable during submission

I'll apply these fixes now."
```
```

---

## Complete Example: pydantic_ai_ui_specialist

Let's walk through a complete integration of the UI specialist agent.

### Scenario

You're building a React application and want Claude Code to automatically analyze your components for accessibility and UX issues.

### Step-by-Step Integration

#### 1. **Copy Files to Your Project**

```bash
# Your project structure before:
your-project/
├── .claude/
│   └── agents/
│       └── (other agents)
├── src/
├── .env
└── CLAUDE.md

# Copy the agent
cd /path/to/agent-factory
cp .claude/agents/pydantic-ai-ui-specialist.md /path/to/your-project/.claude/agents/
cp -r agents/pydantic_ai_ui_specialist /path/to/your-project/agents/

# Your project structure after:
your-project/
├── .claude/
│   └── agents/
│       ├── pydantic-ai-ui-specialist.md  ✅ NEW
│       └── (other agents)
├── agents/
│   └── pydantic_ai_ui_specialist/        ✅ NEW
│       ├── agent.py
│       ├── tools.py
│       ├── settings.py
│       ├── dependencies.py
│       ├── prompts.py
│       ├── __init__.py
│       ├── requirements.txt
│       └── .env.example
├── src/
├── .env
└── CLAUDE.md
```

#### 2. **Install Dependencies**

```bash
cd /path/to/your-project
source venv/bin/activate  # or your virtual environment

pip install -r agents/pydantic_ai_ui_specialist/requirements.txt
```

#### 3. **Configure Environment**

```bash
# Add to your .env file
echo "LLM_PROVIDER=openai" >> .env
echo "LLM_API_KEY=sk-your-key-here" >> .env
echo "LLM_MODEL=gpt-4" >> .env
echo "LLM_BASE_URL=https://api.openai.com/v1" >> .env
```

#### 4. **Update CLAUDE.md**

Add to your project's CLAUDE.md:

```markdown
## Frontend Component Quality Standards

### Pydantic AI UI Specialist Integration

All React components MUST be analyzed by the pydantic-ai-ui-specialist agent before being considered complete.

**Automatic Invocation Triggers:**
- Creating a new component
- Modifying an existing component's structure
- Implementing forms or interactive elements
- Adding animations or transitions
- User explicitly requests UI/UX review

**Quality Requirements:**
- Zero critical accessibility issues (WCAG AA)
- All interactive elements keyboard-navigable
- Responsive design verified across breakpoints
- Performance optimizations applied
- Color contrast meets minimum 4.5:1 ratio

**Workflow:**
1. Implement component
2. Agent automatically analyzes
3. Apply recommended fixes
4. Re-analyze to verify
5. Complete task only after passing
```

#### 5. **Test Claude Code Integration**

Start Claude Code and test:

```bash
cd /path/to/your-project
claude-code
```

In Claude Code:
```
You: "I need to create a Button component with primary and secondary variants"

Claude Code: "I'll create a Button component for you with proper TypeScript types and accessibility features."

[Creates Button.tsx]

Claude Code: "I've created the Button component. Let me now analyze it with the UI specialist agent to ensure it meets accessibility and UX standards."

[Automatically invokes pydantic-ai-ui-specialist]

Claude Code: "Analysis complete! The component looks good overall. I found 2 recommendations:
1. [MEDIUM] Add focus-visible indicator of at least 2px
2. [LOW] Consider adding a loading state variant

Shall I apply these improvements?"
```

#### 6. **Test Standalone CLI Usage**

Create `test_ui_specialist.py`:

```python
import asyncio
from agents.pydantic_ai_ui_specialist import analyze_component

async def main():
    # Read your component
    with open('src/components/Button.tsx', 'r') as f:
        component_code = f.read()

    # Analyze it
    result = await analyze_component(
        component_code=component_code,
        analysis_focus="general",
        typescript_enabled=True,
        wcag_level="AA"
    )

    print("=== UI Specialist Analysis ===")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

Run it:
```bash
python test_ui_specialist.py
```

Expected output:
```
=== UI Specialist Analysis ===

Accessibility Issues Found:

1. [HIGH] Missing aria-label for icon buttons
   Icon-only buttons must have accessible labels for screen readers.
   Fix: Add aria-label="Button description" to icon buttons

2. [MEDIUM] Focus indicator too subtle
   Current focus outline is 1px, WCAG recommends minimum 2px for visibility.
   Fix: Update CSS to use outline: 2px solid var(--color-secondary)

Responsive Design Recommendations:

1. [LOW] Touch target size on mobile
   Ensure buttons are minimum 44x44px on mobile viewports.
   Fix: Add min-height: 44px for sm breakpoint

Performance Optimization Opportunities:

No performance issues found. Component is well-optimized.

UX Pattern Recommendations:

1. [MEDIUM] Loading state feedback
   Consider adding visual loading indicator when isLoading is true.
   Fix: Add spinner or loading animation inside button
```

---

## Troubleshooting

### Issue: "Module not found: pydantic_ai"

**Solution:**
```bash
pip install pydantic-ai==0.0.14
```

### Issue: "LLM_API_KEY is required"

**Solution:**
```bash
# Ensure .env file exists and has the key
cat .env | grep LLM_API_KEY

# If missing, add it:
echo "LLM_API_KEY=sk-your-key-here" >> .env
```

### Issue: Claude Code doesn't invoke the agent

**Solution:**
1. Verify `.claude/agents/pydantic-ai-ui-specialist.md` exists
2. Check that the description/examples match your use case
3. Try explicitly asking: "Use the pydantic-ai-ui-specialist to analyze this component"

### Issue: Agent runs but returns errors

**Solution:**
```bash
# Test the agent standalone first
python -m agents.pydantic_ai_ui_specialist.agent

# Check for errors in the output
# Common issues:
# - Missing dependencies
# - Invalid API key
# - Network issues
```

### Issue: "ImportError: cannot import name 'analyze_component'"

**Solution:**
```bash
# Verify __init__.py exports the function
cat agents/pydantic_ai_ui_specialist/__init__.py | grep analyze_component

# Should see:
# from .agent import agent, analyze_component
```

---

## Best Practices

1. **Always use virtual environments** to avoid dependency conflicts
2. **Keep .env file secure** - never commit API keys to git
3. **Test agents standalone first** before integrating with Claude Code
4. **Update CLAUDE.md** to document agent usage patterns
5. **Version control** - commit agent files to git (except .env)
6. **Monitor API costs** - Pydantic AI agents make LLM calls that incur costs
7. **Use TestModel for development** - Switch to real models for production

---

## Next Steps

- Explore other agents in the factory (pydantic-ai-validator, pydantic-ai-react-ui-builder, etc.)
- Create custom agents using the agent factory workflow
- Build agent compositions (agents that call other agents)
- Integrate with CI/CD pipelines for automated analysis

---

**For more information:**
- Pydantic AI Documentation: https://ai.pydantic.dev
- Agent Factory CLAUDE.md: See the main CLAUDE.md in this repository
- Claude Code Documentation: https://github.com/anthropics/claude-code

---

*Last Updated: 2025-11-18*
