# LLM Message Chain And Toolcalling

## Source: experience/best-practice-routes/backend/docs/llms_how_to.md

## General Requirements

### Message Chain Construction

**Rule**: Always preserve reasoning data in multi-turn conversations.

**Why**: Models with extended thinking (Claude 3.7+, GPT-o1+, etc.) require reasoning signatures to validate message chain integrity. Missing signatures cause API errors.

**Critical**: Use `TextPartWithReasoning()` even if `Content` is empty. The reasoning block and signature must be preserved for API validation.

### Tool Call ID Format Compatibility

**Rule**: Each provider uses a specific format for tool call IDs that must be validated when switching providers.

**Why**: Different providers have different validation rules for tool call IDs. For example:
- **OpenAI/Gemini**: Accept alphanumeric IDs like `call_abc123def456ghi789jkl0`
- **Anthropic**: Require base62 IDs matching pattern `^[a-zA-Z0-9_-]+$` like `toolu_A1b2C3d4E5f6G7h8I9j0K1l2`

**Problem**: When restoring a message chain that was created with one provider (e.g., Gemini) and using it with another provider (e.g., Anthropic), the API will reject tool call IDs that don't match its expected format.

**Solution**: Use `ChainAST.NormalizeToolCallIDs()` to convert incompatible tool call IDs:

**How it works**:
1. Validates each tool call ID against the new template using `ValidatePattern`
2. Generates new IDs only for those that don't match
3. Preserves IDs that already match to avoid unnecessary changes
4. Updates both tool calls and their corresponding responses

**Common Templates**:

| Provider | Template | Example |
|----------|----------|---------|
| OpenAI | `call_{r:24:x}` | `call_abc123def456ghi789jkl0` |
| Gemini | `call_{r:24:x}` | `call_xyz789abc012def345ghi6` |
| Anthropic | `toolu_{r:24:b}` | `toolu_A1b2C3d4E5f6G7h8I9j0K1l2` |

### Reasoning Content Cleanup

**Rule**: Clear reasoning content when switching between providers.

**Why**: Reasoning content contains provider-specific data that causes API errors with different providers:
- **Cryptographic signatures**: Anthropic's extended thinking uses signatures that other providers reject
- **Reasoning metadata**: Provider-specific formatting and validation

**Problem**: When restoring a chain created with Anthropic (with reasoning signatures) and sending to Gemini, the API will reject the request.

**What gets cleared**:
- `TextContent.Reasoning` - Extended thinking signatures and content
- `ToolCall.Reasoning` - Per-tool reasoning data

**What stays preserved**:
- All text content
- Tool call IDs (after normalization)
- Function names and arguments
- Tool responses

## Provider Conflicts & Multi-Provider Code

### 1. Signature Support Conflict

| Provider | Signature Support | Requirement |
|----------|------------------|-------------|
| **Anthropic** | Yes (cryptographic) | MANDATORY for roundtrip |
| **Gemini** | Yes (thought signature) | MANDATORY for tool calls, RECOMMENDED for text |
| **OpenAI** | No | N/A (not supported) |

**Solution**: Universal signature preservation (safe for all)

```go
func buildAIMessage(choice *llms.ContentChoice) llms.MessageContent {
    var parts []llms.ContentPart

    if choice.Reasoning != nil {
        parts = append(parts,
            llms.TextPartWithReasoning(choice.Content, choice.Reasoning),
        )
    } else {
        parts = append(parts, llms.TextPart(choice.Content))
    }

    parts = append(parts, choice.ToolCalls...)

    return llms.MessageContent{
        Role:  llms.ChatMessageTypeAI,
        Parts: parts,
    }
}
```

### 2. Reasoning Location Conflict

| Provider | Text Response | Tool Call Response |
|----------|--------------|-------------------|
| **Anthropic** | `choice.Reasoning` | `choice.Reasoning` |
| **Gemini** | `choice.Reasoning` | `ToolCall[0].Reasoning` |
| **OpenAI** | `choice.Reasoning` | `choice.Reasoning` |

**Solution**: Provider-aware reasoning extraction

```go
func extractReasoning(resp *llms.ContentResponse, provider string) *reasoning.ContentReasoning {
    choice := resp.Choices[0]

    switch provider {
    case "anthropic", "openai":
        return choice.Reasoning

    case "gemini":
        if len(choice.ToolCalls) > 0 {
            return choice.ToolCalls[0].Reasoning
        }
        return choice.Reasoning

    default:
        if choice.Reasoning != nil {
            return choice.Reasoning
        }
        if len(choice.ToolCalls) > 0 && choice.ToolCalls[0].Reasoning != nil {
            return choice.ToolCalls[0].Reasoning
        }
        return nil
    }
}
```

### 5. Message Construction Conflict

**Solution**: Universal pattern (works for all)

```go
func buildUniversalAIMessage(choice *llms.ContentChoice) llms.MessageContent {
    var parts []llms.ContentPart

    if choice.Content != "" || choice.Reasoning != nil {
        parts = append(parts,
            llms.TextPartWithReasoning(choice.Content, choice.Reasoning),
        )
    }

    parts = append(parts, choice.ToolCalls...)

    return llms.MessageContent{
        Role:  llms.ChatMessageTypeAI,
        Parts: parts,
    }
}
```

**Why this works**:
- Anthropic: Gets required `TextPartWithReasoning` + tool calls
- Gemini: Library auto-deduplicates - skips empty text if tool call has signature
- OpenAI: Ignores reasoning in parts, uses tool calls normally

### Provider Detection

**Recommendation**: Explicitly track provider type rather than inferring from model name.

```go
type ProviderType string

const (
    ProviderAnthropic ProviderType = "anthropic"
    ProviderGemini    ProviderType = "gemini"
    ProviderOpenAI    ProviderType = "openai"
)

type Config struct {
    Provider ProviderType
    Model    string
}
```

### Critical Actions (All Providers)

1. **Always** use `TextPartWithReasoning()` when `choice.Reasoning != nil` (universal pattern)
2. **Always** check provider-specific reasoning location (Gemini differs for tool calls)
3. **Never** assume signature presence - OpenAI doesn't support signatures
4. **Never** hardcode temperature for reasoning - let library handle it OR use provider-specific logic

### Universal Best Practices

**For maximum compatibility across all providers**:

1. **Always preserve reasoning** (library handles deduplication):
```go
llms.TextPartWithReasoning(choice.Content, choice.Reasoning)
```

2. **Check reasoning in both locations**:
```go
reasoning := choice.Reasoning
if reasoning == nil && len(choice.ToolCalls) > 0 {
    reasoning = choice.ToolCalls[0].Reasoning
}
```

3. **Don't set temperature for reasoning** (let library handle):
```go
llms.WithReasoning(llms.ReasoningMedium, 2048)
```

4. **Monitor cache via standard metrics**:
```go
cachedTokens := genInfo["PromptCachedTokens"].(int)
reasoningTokens := genInfo["ReasoningTokens"].(int)
```

5. **Handle missing reasoning content gracefully**:
```go
if choice.Reasoning != nil && choice.Reasoning.Content != "" {
    // Process reasoning (Anthropic, Gemini)
} else if reasoningTokens, ok := genInfo["ReasoningTokens"].(int); ok && reasoningTokens > 0 {
    // Reasoning used but content unavailable (OpenAI)
}
```

## Source: experience/best-practice-routes/backend/docs/chain_ast.md

## Common Validation Rules

When `force=false`, NewChainAST enforces these rules:
1. First message must be System or Human
2. No consecutive Human messages
3. Tool calls must have matching responses
4. Tool responses must reference valid tool calls
5. System messages can't appear in the middle of a chain
6. AI messages with tool calls must have responses before another AI message
7. Summarization body pairs must have exactly one tool message

## Provider-Specific Requirements

### Reasoning Signatures

Different LLM providers have specific requirements for reasoning content in function calls:

#### Gemini (Google AI)

Gemini requires **thought signatures** (`thought_signature`) for function calls, especially in multi-turn conversations with tool use. These signatures:

- Are cryptographic representations of the model's internal reasoning process
- Are strictly validated only for the **current turn** (defined as all messages after the last user message with text content)
- Must be preserved when summarizing content that contains them
- Can use fake signatures when creating summarized content: `"skip_thought_signature_validator"`

#### Anthropic (Claude)

Anthropic uses **extended thinking** with cryptographic signatures that:

- Are automatically removed from previous turns (not counted in context window)
- Are only required for the current tool use loop

#### Kimi/Moonshot (OpenAI-compatible)

Kimi reasoning models require **reasoning_content in TextContent** before ToolCall:

- Reasoning must be present in a TextContent part before any ToolCall when thinking is enabled
- Error: "thinking is enabled but reasoning_content is missing in assistant tool call message"
- Use `ExtractReasoningMessage()` to preserve reasoning TextContent when summarizing
- Combine with fake ToolCall signatures for full multi-provider compatibility

**Critical Rule:** Never summarize the last body pair in a section, as this preserves reasoning signatures required by Gemini, Anthropic, and Kimi.

## Best Practices

1. **Validation First**: Use `NewChainAST` with `force=false` to validate chains before processing
2. **Defensive Programming**: Always check for errors from ChainAST functions
3. **Complete Tool Calls**: Ensure all tool calls have corresponding responses before sending to an LLM
4. **Section Management**: Use sections to organize conversation turns logically
5. **Testing**: Use the provided generators to test code that manipulates message chains
6. **Size Management**: Leverage size tracking to maintain efficient context windows
7. **Reasoning Preservation**:
   - Use `ContainsToolCallReasoning()` to check if fake signatures are needed (checks only ToolCall.Reasoning)
   - Use `ExtractReasoningMessage()` to preserve reasoning TextContent for Kimi/Moonshot
8. **Last Pair Protection**: Never summarize the last (most recent) body pair in a section to preserve reasoning signatures
9. **Multi-Provider Support**: When summarizing for current turn, preserve both ToolCall and TextContent reasoning for maximum compatibility

## Source: experience/best-practice-routes/backend/docs/chain_summary.md

Key features of the enhanced algorithm:

- **Size-aware processing** - Tracks byte size of all content to make optimal retention decisions
- **Section summarization** - Ensures all sections except the last `KeepQASections` ones consist of a header and a single body pair
- **Last section rotation** - Intelligently manages active conversation sections with size limits
- **QA pair summarization** - Focuses on question-answer sections when enabled, **preserving last `KeepQASections` sections unconditionally**
- **Body pair type preservation** - Maintains appropriate type for summarized content based on original types
- **Keep QA Sections** - Preserves a configurable number of recent QA sections without summarization, **even if they exceed `MaxQABytes`** (critical for agent state preservation)
- **Concurrent processing** - Uses goroutines for efficient parallel summarization of sections and body pairs
- **Idempotent operation** - Multiple consecutive calls do not modify already summarized content
- **Last BodyPair protection** - The last BodyPair in a section is never summarized to preserve reasoning signatures

## Algorithm Operation

The enhanced algorithm operates in these sequential phases:

1. Convert input chain to ChainAST with size tracking
2. Apply section summarization to all sections except the last `KeepQASections` sections (with concurrent processing)
3. Apply last section rotation to multiple recent sections if enabled and size limits are exceeded
4. Apply QA pair summarization if enabled and limits are exceeded, **preserving the last `KeepQASections` sections**
5. Return the modified chain if it saves space

**Critical Guarantees:**
- The last `KeepQASections` sections are **NEVER** summarized by section or QA summarization, even if they exceed `MaxQABytes`
- The last BodyPair in a section is **NEVER** summarized by `summarizeOversizedBodyPairs` or `summarizeLastSection` to preserve reasoning signatures
- **Idempotent**: calling `SummarizeChain` multiple times on already summarized content does not change it further

## Edge Cases and Handling

| Edge Case | Handling Strategy |
|-----------|-------------------|
| Empty chain | Return unchanged immediately without processing |
| Very short chains | Return unchanged after section count check |
| Single section chains | Return unchanged after section count check |
| Empty sections to process | Skip summarization |
| Last section over size limit | Create a new section with summary pair followed by recent pairs |
| QA pairs over limit | Create summary section and keep most recent sections |
| KeepQASections larger than number of sections | No summarization performed, preserves all sections |
| Last KeepQASections sections exceed MaxQABytes | Sections are kept anyway to preserve reasoning and agent state |
| Summary generation fails | Keep the most recent content and log the error |
| Chain with already summarized content | Detected during processing and handled appropriately (idempotent) |
| Multiple consecutive summarization calls | Idempotent - no changes after first summarization |

## Source: experience/best-practice-routes/backend/pkg/templates/prompts/toolcall_fixer.tmpl

## OPERATIONAL GUIDELINES

<repair_rules>
<primary_rule>Maintain original content integrity while fixing only problematic elements</primary_rule>
<modification>Make minimal changes required to resolve the identified error</modification>
<validation>Ensure final output conforms to the provided JSON schema</validation>
<formatting>Return a single line of properly escaped JSON without additional formatting</formatting>
<follow_instructions>Always follow the specific instructions provided in the instruction tag</follow_instructions>
</repair_rules>

## PROCESS WORKFLOW

<execution_steps>
<review_instructions>First, carefully read and understand the provided instructions for this specific repair task</review_instructions>
<analysis>Examine the error message to identify specific issues in the arguments</analysis>
<comparison>Compare arguments against the provided schema for structural validation</comparison>
<correction>Apply necessary fixes while preserving original intent and content</correction>
<verification>Validate final JSON against schema requirements before submission</verification>
</execution_steps>

## Source: experience/best-practice-routes/backend/pkg/templates/prompts/tool_call_id_detector.tmpl

<pattern_format>
The pattern template uses the following format:
- Literal parts: fixed text that appears in all samples (e.g., "toolu_", "call_")
- Random parts: {r:LENGTH:CHARSET} where:
  - LENGTH: exact number of random characters
  - CHARSET: character set type
    - d or digit: [0-9]
    - l or lower: [a-z]
    - u or upper: [A-Z]
    - a or alpha: [a-zA-Z]
    - x or alnum: [a-zA-Z0-9]
    - h or hex: [0-9a-f]
    - H or HEX: [0-9A-F]
    - b or base62: [0-9A-Za-z]
- Function placeholder: {f}
  - Represents the function/tool name
  - Used when tool call IDs contain the function name
  - The function name varies but follows the same pattern structure

Examples:
- "toolu_013wc5CxNCjWGN2rsAR82rJK" -> "toolu_{r:24:b}"
- "call_Z8ofZnYOCeOnpu0h2auwOgeR" -> "call_{r:24:x}"
- "chatcmpl-tool-23c5c0da71854f9bbd8774f7d0113a69" -> "chatcmpl-tool-{r:32:h}"
- "get_number:0", "submit_pattern:0" -> "{f}:{r:1:d}"
</pattern_format>
