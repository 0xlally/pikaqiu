# Observability And Runtime

## Source: experience/okk/backend/docs/flow_execution.md

## Advanced Agent Supervision

PentAGI implements a sophisticated multi-layered agent supervision system to ensure efficient task execution, prevent infinite loops, and provide intelligent recovery from stuck states.

### Execution Monitoring System

**ExecutionMonitorDetector** continuously monitors agent tool call patterns and automatically invokes the Adviser agent for progress reviews:

**Trigger Conditions**:
- **Same Tool Threshold**: Triggered after 5 consecutive calls to the same tool (configurable via `EXECUTION_MONITOR_SAME_TOOL_LIMIT`)
- **Total Tool Threshold**: Triggered after 10 total tool calls regardless of variety (configurable via `EXECUTION_MONITOR_TOTAL_TOOL_LIMIT`)
- **Reset Behavior**: Counters reset after adviser intervention or when different tools are used

**Monitoring Process**:
1. **Pattern Detection**: `execToolCall` method checks detector before executing each tool
2. **Context Collection**: Gathers recent messages, executed tool calls, subtask description, and agent prompt
3. **Mentor Invocation**: Calls `performMentor` with comprehensive execution context
4. **Enhanced Response**: Mentor analysis is formatted as `<mentor_analysis>` alongside `<original_result>`
5. **Counter Reset**: Monitor state resets after successful intervention

**Mentor Analysis Provides**:
- **Progress Assessment**: Evaluation of whether agent is advancing toward subtask objective
- **Issue Identification**: Detection of loops, inefficiencies, or incorrect approaches
- **Alternative Strategies**: Recommendations for different approaches when current strategy fails
- **Information Retrieval Guidance**: Suggestions to search for established solutions instead of reinventing
- **Termination Guidance**: Clear indication if task is impossible or should be completed with completion function call

### Enhanced Reflector Integration

**Automatic Reflector on Generation Failures**:

When LLM fails to generate valid tool calls after 3 attempts in `callWithRetries`, the system now automatically invokes the Reflector agent instead of failing:

**Invocation Process**:
1. **Failure Detection**: `callWithRetries` reaches `maxRetriesToCallAgentChain` (3 attempts)
2. **Context Preparation**: Builds reflector message describing all failed attempts and errors
3. **Reflector Call**: Invokes `performReflector` to analyze situation and provide guidance
4. **Recovery Options**: Reflector guides agent to either:
   - Fix the issue with specific corrective instructions
   - Use barrier tool to report completion or request assistance

**Benefits**:
- Prevents premature task termination due to transient LLM issues
- Provides contextual guidance based on specific failure patterns
- Maintains conversation flow rather than hard errors
- Enables graceful degradation and adaptive recovery

### Hard Limit Graceful Termination

**Max Tool Calls Per Agent Execution**:

To prevent runaway executions, each agent has a hard limit on tool calls. The limit varies by agent type to balance capabilities with efficiency:

**Agent Types and Limits**:
- **General Agents** (Assistant, Primary Agent, Pentester, Coder, Installer):
  - Default: 100 tool calls
  - Configurable via `MAX_GENERAL_AGENT_TOOL_CALLS`
  - Designed for complex, multi-step workflows requiring extensive tool usage

- **Limited Agents** (Searcher, Enricher, Memorist, Generator, Reporter, Adviser, Reflector, Planner):
  - Default: 20 tool calls
  - Configurable via `MAX_LIMITED_AGENT_TOOL_CALLS`
  - Designed for focused, specific tasks with limited scope

**Termination Process**:
1. **Limit Check**: Before each `callWithRetries` in `performAgentChain`, system checks `iteration` against agent-specific limit
2. **Reflector Invocation**: When approaching limit (within 3 iterations), reflector is called with termination context
3. **Graceful Completion**: Reflector guides agent to use barrier tool (`done` or `ask`) to:
   - Report successful completion if objective was achieved
   - Report partial progress with clear blocker explanation
   - Request user assistance if critical information is missing
4. **Forced Exit**: After reflector guidance, execution terminates gracefully

### Intelligent Task Planning (Planner)

**Planner-Generated Execution Plans**:

When specialist agents (Pentester, Coder, Installer) are invoked, the Planner (adviser in planning mode) optionally generates a structured execution plan before task execution:

**Planning Process**:
1. **Context Analysis**: Planner analyzes full execution context via enricher agent
2. **Plan Generation**: Creates 3-7 specific, actionable steps via `PromptTypeQuestionTaskPlanner` template
3. **Scope Limitation**: Ensures plan focuses only on current subtask objective
4. **Plan Wrapping**: Original task question is wrapped in `<task_assignment>` structure with plan
5. **Agent Execution**: Specialist receives both original request and decomposed execution plan

**Benefits**:
- **Prevents scope creep**: Keeps agents focused on current subtask only
- **Reduces redundancy**: Leverages enriched context to avoid duplicate work
- **Improves success rate**: Breaks complex tasks into manageable steps
- **Provides guardrails**: Highlights potential pitfalls and verification points

### Mentor Supervision Protocol

All agents with adviser handler access (Primary, Pentester, Coder, Installer, Assistant) now include explicit awareness of mentor supervision in their system prompts:

**Enhanced Response Format**:
Agents are instructed to expect tool responses containing both:
- `<original_result>`: Actual tool execution output
- `<mentor_analysis>`: Mentor's evaluation with progress assessment, identified issues, alternative approaches, information retrieval suggestions, and next steps

**Agent Instructions**:
- Agents must read and integrate BOTH sections into decision-making
- Mentor analysis should guide next actions when provided
- Agents can explicitly request advice via `advice` tool
- Automatic mentor reviews occur at configured thresholds (not revealed to agents)

## Source: experience/okk/backend/docs/docker.md

## Security and Isolation

### Container Security Model

PentAGI implements a multi-layered security approach for container isolation:

#### Network Isolation
- **Custom Networks**: Containers run in dedicated Docker networks
- **Port Control**: Only specific ports are exposed to the host
- **Host Protection**: Container cannot access host network by default

#### File System Isolation
- **Read-Only Root**: Base container filesystem is immutable
- **Controlled Mounts**: Only specific directories are writable
- **Volume Separation**: Each flow gets isolated storage space

#### Capability Management
```go
hostConfig := &container.HostConfig{
    CapAdd: []string{"NET_RAW"},  // Required for network scanning tools
    // Other dangerous capabilities are not granted
}
```

#### Process Isolation
- **User Namespaces**: Containers run with isolated user space
- **PID Isolation**: Container processes are isolated from host
- **Resource Limits**: Memory and CPU usage are controlled

### Security Best Practices Implemented

1. **Image Validation**: All images are pulled and verified before use
2. **Fallback Strategy**: Safe default image used if custom image fails
3. **State Tracking**: All container operations are logged and monitored
4. **Automatic Cleanup**: Failed or abandoned containers are automatically removed
5. **Socket Security**: Docker socket is only mounted when explicitly required

## Best Practices

### Resource Management
- Always use the `Cleanup()` method on application startup
- Monitor container resource usage through observability tools
- Set appropriate timeouts for long-running operations
- Use deterministic port allocation to avoid conflicts

### Security Considerations
- Regularly update base images used for containers
- Minimize capabilities granted to containers
- Use dedicated networks for container communication
- Monitor and audit all container operations

### Development and Debugging
- Use structured logging for all Docker operations
- Implement comprehensive error handling with context
- Test container operations in isolated environments
- Use the ftester utility for debugging specific operations

### Performance Optimization
- Reuse containers when possible instead of creating new ones
- Implement efficient cleanup to prevent resource leaks
- Use appropriate container restart policies
- Monitor container startup times and optimize configurations

### Integration Guidelines
- Always use the DockerClient interface instead of direct Docker SDK calls
- Integrate with PentAGI's database for state management
- Use the provided logging and observability infrastructure
- Follow the established naming conventions for containers

## Source: experience/okk/backend/docs/observability.md

### Context-Aware Logging

For proper trace correlation, logs should include the request context. This allows the observability system to associate logs with the correct trace and span:

```go
// WithContext is critical for associating logs with the correct trace
logrus.WithContext(ctx).Info("Operation completed")

// Without context, logs may not be associated with the correct trace
logrus.Info("This log may not be properly correlated") // Avoid this

// Example with error and fields
logrus.WithContext(ctx).WithFields(logrus.Fields{
    "user_id": userID,
    "action": "login",
}).WithError(err).Error("Authentication failed")
```

When a log entry includes a context, the observability system will:

1. Extract the active span from the context
2. Associate the log with that span
3. Include trace and span IDs in the log record
4. Ensure the log appears in the trace timeline in Jaeger

If a log entry does not include a context (or the context has no active span), the system will:

1. Create a new span for the log entry
2. Associate the log with this new span
3. This creates a "span island" that isn't connected to other parts of the trace

### Context Propagation in Tracing

Context propagation is critical for maintaining trace continuity:

```go
// Create a span in function A
ctx, span := obs.Observer.NewSpan(ctx, obs.SpanKindInternal, "function-a")
defer span.End()

// Pass the context to function B
resultB := functionB(ctx, param1, param2)

// Inside function B, create a child span
func functionB(ctx context.Context, param1, param2 string) Result {
    // This will be a child span of the span in function A
    ctx, span := obs.Observer.NewSpan(ctx, obs.SpanKindInternal, "function-b")
    defer span.End()

    // ...function logic...
}
```

Always use the *updated context* returned from `NewSpan()`:

```go
// CORRECT: Using the updated context
ctx, span := obs.Observer.NewSpan(ctx, obs.SpanKindInternal, "operation")
// Pass the updated ctx to subsequent operations

// INCORRECT: Not using the updated context
_, span := obs.Observer.NewSpan(ctx, obs.SpanKindInternal, "operation")
// Subsequent operations won't be part of the same trace
```

## Best Practices

### Context Propagation

Always propagate context through your application to maintain trace continuity:

```go
// Pass context to functions and methods
func ProcessRequest(ctx context.Context, req Request) {
    // Use the context for spans, logs, etc.
    logrus.WithContext(ctx).Info("Processing request")

    // Pass the context to downstream functions
    result, err := fetchData(ctx, req.ID)
}
```

### Structured Logging

Use structured logging with consistent field names:

```go
// Define common field names
const (
    FieldUserID     = "user_id"
    FieldRequestID  = "request_id"
    FieldComponent  = "component"
)

// Use them consistently
logrus.WithFields(logrus.Fields{
    FieldUserID:    user.ID,
    FieldRequestID: reqID,
    FieldComponent: "auth-service",
}).Info("User authenticated")
```

### Meaningful Spans

Create spans that represent logical operations:

```go
// Good: spans represent logical operations
ctx, span := obs.Observer.NewSpan(ctx, obs.SpanKindInternal, "validate-user-input")
defer span.End()

// Bad: spans are too fine-grained or too coarse
ctx, span := obs.Observer.NewSpan(ctx, obs.SpanKindInternal, "process-entire-request")
defer span.End()
```

### Useful Metrics

Design metrics to answer specific questions:

```go
// Good: metrics that help troubleshoot
cacheHitCounter, _ := obs.Observer.NewInt64Counter("cache.hits")
cacheMissCounter, _ := obs.Observer.NewInt64Counter("cache.misses")

// Good: metrics with dimensions
requestCounter.Add(ctx, 1,
    attribute.String("status", status),
    attribute.String("endpoint", endpoint),
)
```

## Source: experience/okk/backend/docs/analytics_api.md

## Understanding Metric Differences

### Execution Stats vs Toolcalls Stats

These two metric types measure different aspects of system performance:

**Execution Stats (`flowsExecutionStatsByPeriod`):**
- **Purpose:** Measure real wall-clock time for flows/tasks/subtasks
- **Duration calculation:** Linear time (start -> end timestamp)
- **What it shows:** How long a flow/task/subtask actually ran
- **Use for:** Performance analysis, SLA monitoring, user-facing progress
- **Example:** Subtask ran for 100 seconds (even if it made 10 toolcalls)

**Toolcalls Stats (`toolcallsStatsByPeriod`, `toolcallsStatsByFunction`):**
- **Purpose:** Measure individual tool execution metrics
- **Duration calculation:** Sum of toolcall durations (each toolcall's created_at -> updated_at)
- **What it shows:** Aggregate time spent in specific tools
- **Use for:** Tool optimization, identifying slow functions, resource attribution
- **Example:** 50 terminal toolcalls totaling 300 seconds

**Key difference:**
```
Flow execution time = 100 seconds (wall-clock)
Toolcalls total time = 150 seconds (sum of all toolcalls)

Why different?
- Flow time is LINEAR (real time elapsed)
- Toolcalls time INCLUDES OVERLAPS (nested agent calls counted in parent time)
```

**When to use which:**
- User wants to know "how long did my pentest take?" -> Use **Execution Stats**
- Developer wants to optimize slow tools -> Use **Toolcalls Stats**
- Manager wants to see system utilization -> Use **Toolcalls Stats**
- SLA monitoring -> Use **Execution Stats**

## Source: experience/okk/backend/docs/installer/processor-logic-implementation.md

## Key Principles

1. **State-Driven Operations**: All operations based on comparing current and target state
2. **Stack Independence**: Each stack (observability, langfuse, pentagi) managed independently
3. **Force Mode**: Aggressive state correction ignoring warnings
4. **Idempotency**: Repeated operation calls do not cause side effects
5. **User-Facing Automation**: Installer automates manual Docker/file operations with real-time feedback

## Error Handling Strategy

### Fail-Fast Principle
- Each phase can interrupt execution
- Partial state preserved (no rollback)
- Errors bubbled up with context

### Recovery Scenarios
- User can repeat operation with force=true
- Partial installation can be completed
- Remove/Purge operations for complete cleanup

## Source: experience/okk/backend/docs/installer/checker.md

### Core Design Principles

1. **Delegation Pattern**: Uses a `CheckHandler` interface to delegate information gathering logic, allowing for flexible implementations and testing
2. **Parallel Information Gathering**: Collects information from multiple sources (Docker, filesystem, network) concurrently
3. **Fail-Safe Approach**: Returns sensible defaults when checks cannot be performed, avoiding false negatives
4. **Context-Aware**: All operations support context for cancellation and timeouts
