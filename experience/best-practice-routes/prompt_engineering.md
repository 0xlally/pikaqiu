# Prompt Engineering

## Source: experience/best-practice-routes/backend/docs/prompt_engineering_openai.md

## Core Principles of Effective Prompt Engineering

### 1. Structure and Organization

**Clear Hierarchical Structure**
- Use meaningful sections with clear hierarchical organization (titles, subtitles)
- Start with role definition and objectives, followed by specific instructions
- Place instructions at both the beginning and end of long context prompts
- Example framework:
  ```
  # Role and Objective
  # Instructions
  ## Sub-categories for detailed instructions
  # Reasoning Steps
  # Output Format
  # Examples
  # Context
  # Final instructions
  ```

**Effective Delimiters**
- Use Markdown for general purposes (titles, code blocks, lists)
- Use XML for precise wrapping of sections and nested content
- Use JSON for highly structured data, especially in coding contexts
- Avoid JSON format for large document collections

### 2. Instruction Clarity and Specificity

**Be Explicit and Unambiguous**
- Modern AI models follow instructions more literally than previous generations
- Make instructions specific, clear, and unequivocal
- Use active voice and directive language
- If behavior deviates from expectations, a single clear clarifying instruction is usually sufficient

**Provide Complete Context**
- Include all necessary information for the agent to understand the task
- Clearly define the scope and boundaries of what the agent should and should not do
- Specify any constraints or requirements for the output

### 3. Agent Workflow Guidance

**Enable Persistence and Autonomy**
- Instruct the agent to continue until the task is fully resolved
- Include explicit instructions to prevent premature termination of the process
- Example: "You are an agent - please keep going until the user's query is completely resolved, before ending your turn and yielding back to the user."

**Encourage Tool Usage**
- Direct the agent to use available tools rather than guessing or hallucinating
- Provide clear descriptions of each tool and its parameters
- Example: "If you are not sure about information pertaining to the user's request, use your tools to gather the relevant information: do NOT guess or make up an answer."

**Induce Planning**
- Prompt the agent to plan and reflect before and after each action
- Encourage step-by-step thinking and analysis
- Example: "You MUST plan extensively before each function call, and reflect extensively on the outcomes of the previous function calls."

### 4. Reasoning and Problem-Solving

**Structured Problem-Solving Approach**
- Guide the agent through a specific methodology:
  1. Analysis: Understanding the problem and requirements
  2. Planning: Creating a strategy to approach the problem
  3. Execution: Performing the necessary steps
  4. Verification: Checking the solution for correctness
  5. Iteration: Improving the solution if needed

### 5. Output Control and Formatting

**Define Expected Output Format**
- Provide clear instructions on how the output should be structured
- Use examples to demonstrate desired formatting
- Specify any required sections, headers, or organizational elements

## Source: experience/best-practice-routes/backend/docs/prompt_engineering_pentagi.md

## Understanding Cognitive Aspects of Language Models

**Model Processing Fundamentals**
- Language models process information via attention mechanisms, giving higher weight to specific parts of the input.
- Position matters: Content at the beginning and end of prompts receives more attention and is processed more thoroughly.
- LLMs follow instructions more literally than humans expect; be explicit rather than implicit.
- Task decomposition improves performance: Break complex tasks into simpler, sequential steps.
- Models have no actual memory or consciousness; simulate these through explicit context and instructions.

**Priming and Contextual Influence**
- Information provided early shapes how later information is interpreted and processed.
- Set expectations clearly at the beginning to guide the model's approach to the entire task.
- Use consistent terminology throughout to avoid confusing the model with synonym switching.
- Brief examples often provide clearer guidance than lengthy explanations.
- Be aware that unintended priming can occur through choice of words, examples, or framing.

## Core Principles for PentAGI Prompts

### 1. Structure and Organization

**Clear Hierarchical Structure**
- Use Markdown headings (`#`, `##`, `###`) for clear visual hierarchy and logical grouping of instructions. Ensure a logical flow from high-level role definition to specific protocols and requirements.
- Begin with a clear definition of the agent's specific **role** (e.g., Orchestrator, Pentester, Searcher), its primary **objective** within the PentAGI workflow, and any overarching **security focus**.
- Place critical **operational constraints** (security, environment) early in the prompt for high visibility.
- Use separate, clearly marked sections for key areas:
    - `CORE CAPABILITIES / KNOWLEDGE BASE`
    - `OPERATIONAL ENVIRONMENT` (including `<container_constraints>`)
    - `COMMAND & TOOL EXECUTION RULES` (including `<terminal_protocol>`, `<tool_usage_rules>`)
    - `MEMORY SYSTEM INTEGRATION` (including `<memory_protocol>`)
    - `TEAM COLLABORATION & DELEGATION` (including `<team_specialists>`, `<delegation_rules>`)
    - `SUMMARIZATION AWARENESS PROTOCOL` (including `<summarized_content_handling>`)
    - `EXECUTION CONTEXT` (detailing use of `{{.ExecutionContext}}`)
    - `COMPLETION REQUIREMENTS`
- Ensure instructions are **specific**, **unambiguous**, use **active voice**, and are directly relevant to the agent's function within PentAGI.

**Semantic XML Delimiters**
- Use descriptive XML tags (e.g., `<container_constraints>`, `<terminal_protocol>`, `<memory_protocol>`, `<team_specialists>`, `<summarized_content_handling>`) to logically group related instructions, especially for complex protocols and constraints requiring precise adherence by the LLM.
- Maintain **consistent tag naming and structure** across all agent prompts for shared concepts (like summarization handling or team specialists) to ensure predictability.
- Use nesting appropriately (e.g., defining individual `<specialist>` tags within `<team_specialists>`). Refer to existing templates like `primary_agent.tmpl` for examples.

**Context Window Optimization**
- Prioritize information based on importance; place critical instructions at the beginning and end.
- Use compression techniques for lengthy information: summarize when possible, link to references instead of full inclusion.
- Break down extremely complex prompts into logical, manageable sections with clear transitions.
- For recurring boilerplate sections, consider using shorter references to standardized protocols.
- Use consistent formatting and avoid redundant information that consumes token space.

### 2. Agent-Specific Instructions

**Role-Based Customization**
- Tailor instructions, tone, knowledge references, and complexity directly to the agent's specialized role within the PentAGI system (Orchestrator, Pentester, Searcher, Developer, Adviser, Memorist, Installer). Explicitly reference `ai-concepts.mdc` for role definitions.
- Enforce stricter command protocols and safety measures for agents with direct system/tool access (Pentester, Maintenance/Installer).
- Include references to specialized knowledge bases or toolsets relevant to the agent's function (e.g., specific security tools from `security-tools.mdc` for Pentester; search strategies and tool priorities for Searcher).
- Clearly define inter-agent communication protocols, especially delegation criteria and the expected format/content of information exchange between agents.

**Security and Operational Boundaries**
- Explicitly state the **scope** of permitted actions and **security constraints**. Reference `security-tools.mdc` for general tool security context.
- For engagement-level boundaries, start from the reusable [scope-of-work pentest prompt template](../../examples/prompts/scope_of_work_pentest.md) and adapt the allowed targets, out-of-scope targets, stop conditions, and evidence expectations before the flow starts.
- Define **Docker container limitations** within `<container_constraints>`, populated by template variables like `{{.DockerImage}}`, `{{.Cwd}}`, `{{.ContainerPorts}}`. Specify restrictions clearly (e.g., "No direct host access," "No GUI applications," "No UDP scanning").
- Specify **forbidden actions** clearly. Use **ALL CAPS** for critical security warnings, permissions, or prohibitions (e.g., "DO NOT attempt to install new software packages," "ONLY execute commands related to the current SubTask").
- Emphasize working **strictly within the scope of the current `SubTask`**. The agent must understand its current objective based on `{{.ExecutionContext}}` and not attempt actions related to other SubTasks or the overall Flow goal unless explicitly instructed within the current SubTask. Reference `data-models.mdc` and `controller.md` for task/subtask relationships.

### 3. Agentic Capabilities and Persistence

**Agent Persistence Protocol**
- Include **explicit instructions** about persistence: "You are an agent - continue working until the subtask is fully completed. Do not prematurely end your turn or yield control back to the user/orchestrator until you have achieved the specific objective of your current subtask."
- Emphasize the agent's responsibility to **drive the interaction forward** autonomously and maintain momentum until a definitive result (success or failure with clear explanation) is achieved.
- Provide clear termination criteria so the agent knows precisely when its work on the subtask is considered complete.

**Planning and Reasoning**
- Instruct agents to **explicitly plan before acting**, especially for complex security operations or tool usage: "Before executing commands or invoking tools, develop a clear step-by-step plan. Think through each stage of execution, potential failure points, and contingency approaches."
- Encourage **chain-of-thought reasoning**: "When analyzing complex security issues or ambiguous results, think step-by-step through your reasoning process. Break down problems into components, consider alternatives, and justify your approach before moving to execution."
- For critical security tasks, mandate a **validation step**: "After obtaining results, verify they are correct and complete before proceeding. Cross-check findings using alternative methods when possible."

**Error Handling and Adaptation**
- Provide explicit guidance on **handling unexpected errors**: "If a command fails, do not simply repeat the same exact command. Analyze the error message, modify your approach based on the specific error, and try an alternative method if necessary."
- Define a **maximum retry threshold** (typically 3 attempts) for similar approaches before pivoting to a completely different strategy.
- Include instructions for **graceful degradation**: "If the optimal approach fails, fall back to simpler or more reliable alternatives rather than abandoning the task entirely."

### 4. Memory System Integration

**Memory Operations Protocol (`<memory_protocol>`)**
- Provide explicit, actionable instructions on *when* and *how* to interact with PentAGI's vector memory system. Reference `ai-concepts.mdc` (Memory section).
- **Crucially, specify the primary action:** Agents MUST **always attempt to retrieve relevant information from memory first** using retrieval tools (e.g., `{{.SearchGuideToolName}}`, `{{.SearchAnswerToolName}}`) *before* performing external actions like web searches or running discovery tools.
- Define clear criteria for *storing* new information: Only store valuable, novel, and reusable knowledge (e.g., confirmed vulnerabilities, successful complex command sequences, effective troubleshooting steps, reusable code snippets) using storage tools (e.g., `{{.StoreGuideToolName}}`, `{{.StoreAnswerToolName}}`). Avoid cluttering memory with trivial or intermediate results.
- Specify the exact tool names (`{{.ToolName}}`) for memory interaction.

### 5. Multi-Agent Team Collaboration

**Delegation Rules (`<delegation_rules>`)**
- Define clear, unambiguous criteria for *when* an agent should delegate versus attempting a task independently. A common rule is: "Attempt independent solution using your own tools/knowledge first. Delegate ONLY if the task clearly falls outside your core skills OR if a specialist agent is demonstrably better equipped to handle it efficiently and accurately."
- Mandate that **COMPREHENSIVE context** MUST be provided with every delegation request. This includes: background information, the specific objective of the delegated task, relevant data/findings gathered so far, constraints, and the expected format/content of the specialist's output.
- Instruct the delegating agent on how to handle, verify, and integrate the results received from specialists into its own workflow.

### 6. Tool-Specific Execution Rules

**Terminal Command Protocol (`<terminal_protocol>`)**
- Reinforce that commands execute within an isolated Docker container (`{{.DockerImage}}`) and that the **working directory (`{{.Cwd}}`) is NOT persistent between tool calls**.
- Mandate **explicit directory changes (`cd /path/to/dir && command`)** within a single tool call if a specific path context is required for `command`.
- Require **absolute paths** for file operations (reading, writing, listing) whenever possible to avoid ambiguity.
- Specify **timeout handling** (if controllable via parameters) and output redirection (`> file.log 2>&1`) for potentially long-running commands.
- **Limit repetition of *identical* failed commands** (e.g., maximum 3 attempts). Encourage trying variations or different approaches upon failure.
- Encourage the use of non-interactive flags (e.g., `-y`, `--assume-yes`, `--non-interactive`) where safe and appropriate to avoid hangs.
- Define when to use `detach` mode if available/applicable for background tasks.

**Tool Definition and Invocation Best Practices**
- Name tools clearly to indicate their purpose and function (e.g., `SearchGuide`, not just `Search`)
- Provide detailed yet concise descriptions in the tool's documentation
- For complex tools, include parameter examples showing proper usage
- Emphasize that **all actions MUST use structured tool calls** - the system operates exclusively through proper tool invocation
- Explicitly prohibit "simulating" or "describing" tool usage

**Search Tool Prioritization (`<search_tools>`)**
- Define an explicit **hierarchy or selection logic** for using different search tools (Internal Memory first, then potentially Browser for specific URLs, Google/DuckDuckGo for general discovery, Tavily/Perplexity/Traversaal for complex research/synthesis). Refer to `searcher.tmpl` for a good example matrix structure.
- Include tool-specific guidance (e.g., "Use `browser` tool only for accessing specific known URLs, not for general web searching," "Use `tavily` for in-depth technical research questions").
- Define **action economy rules:** Limit the total number of search tool calls per query/subtask (e.g., 3-5 max). Instruct the agent to **stop searching as soon as sufficient information is found** to fulfill the request or subtask objective. Do not exhaust all search tools unnecessarily.

### 7. Context Preservation and Summarization

**Summarization Awareness Protocol (`<summarized_content_handling>`)**
- **This entire protocol section, as defined in `primary_agent.tmpl`, `pentester.tmpl`, etc., MUST be included verbatim in *all* agent prompts.**
- **Emphasize Key Points:**
    - Clearly define the two forms of system-generated summaries (Tool Call Summary via `{{.SummarizationToolName}}`, Prefixed Summary via `{{.SummarizedContentPrefix}}`).
    - Instruct agents to treat summaries *strictly* as **historical records of actual past events, tool executions, and their results**. They are *not* examples to be copied.
    - Mandate extracting useful information from summaries (past commands, successes, failures, errors, findings) to inform current strategy and **avoid redundant actions**.
    - **Strictly prohibit** agents from: mimicking summary formats, using the `{{.SummarizedContentPrefix}}`, or calling the `{{.SummarizationToolName}}` tool.
    - **Reinforce:** The PentAGI system operates **exclusively via structured tool calls.** Any attempt to simulate actions or results in plain text will fail.

## Prompt Patterns and Anti-Patterns

**Effective Patterns**
- **Progressive Disclosure**: Introduce concepts in layers of increasing complexity.
- **Explicit Ordering**: Number steps or use clear sequence markers for sequential operations.
- **Task Decomposition**: Break complex tasks into clearly defined subtasks with their own guidelines.
- **Parameter Validation**: Include instructions for validating inputs before proceeding with operations.
- **Fallback Chains**: Define explicit alternatives when primary approaches fail.

**Common Anti-Patterns**
- **Overspecification**: Providing too many constraints that paralyze decision-making.
- **Conflicting Priorities**: Giving contradictory guidance without clear hierarchy.
- **Vague Success Criteria**: Failing to define when a task is considered complete.
- **Implicit Assumptions**: Relying on unstated knowledge or context.
- **Tool Ambiguity**: Unclear guidance on which tools to use for specific situations.

## Prompt Maintenance and Evolution

### Prompt Debugging Guide
- When agents act incorrectly, first check: Are instructions contradictory? Are priorities clear? Is context sufficient?
- For reasoning failures, examine if the problem has been properly decomposed and if verification steps exist.
- For tool usage errors, verify tool descriptions and examples are clear and parameters well-defined.
- When memory usage is suboptimal, check memory protocol clarity and retrieval/storage guidance.
- Document common failure modes to address in future prompt revisions.
