export type NodeType = "info" | "test";

export type NodeStatus = "todo" | "doing" | "done" | "failed";

export type RunStatus = "running" | "completed" | "failed";

export type RunStage =
  | "bootstrap"
  | "act:info"
  | "parsing:info"
  | "reasoning:feature-mapping"
  | "act:test"
  | "parsing:test";

export type EventType =
  | "agent_step_started"
  | "agent_step_finished"
  | "tool_call_started"
  | "tool_call_finished"
  | "parsing_completed"
  | "reasoning_completed"
  | "node_created"
  | "node_updated"
  | "error"
  | "retry";

export type EventActor = "reasoning" | "act" | "parsing" | "tool" | "system";

export type EventStatus = "running" | "success" | "failed" | "retry" | "info";

export type ParsingSectionKey =
  | "discovered_pages"
  | "discovered_endpoints"
  | "discovered_fields"
  | "discovered_objects"
  | "discovered_actions"
  | "discovered_flows"
  | "discovered_roles"
  | "discovered_render_points"
  | "discovered_upload_points"
  | "discovered_callback_points";

export type JsonPrimitive = string | number | boolean | null;

export type JsonValue = JsonPrimitive | JsonValue[] | { [key: string]: JsonValue };

export interface DebugError {
  code: string;
  message: string;
  details?: string;
}

export interface TaskNode {
  id: string;
  title: string;
  nodeType: NodeType;
  status: NodeStatus;
  parentId: string | null;
  source: string;
  sourceFeatureId: string | null;
  familyIds: string[];
  primaryFamilyId: string | null;
  notes: string[];
  evidenceRefs: string[];
  createdAt: string;
  updatedAt: string;
}

export interface TimelineEvent {
  id: string;
  stepIndex: number;
  eventType: EventType;
  actor: EventActor;
  title: string;
  summary: string;
  status: EventStatus;
  startedAt: string;
  finishedAt: string | null;
  durationMs: number | null;
  relatedNodeId: string | null;
  relatedToolCallId: string | null;
  rawInput: unknown | null;
  rawOutput: unknown | null;
  parsedOutput: unknown | null;
  error: DebugError | null;
}

export interface ToolCallRecord {
  id: string;
  toolName: string;
  title: string;
  summary: string;
  status: "running" | "success" | "failed";
  startedAt: string;
  finishedAt: string | null;
  durationMs: number | null;
  request: unknown;
  response: unknown | null;
  error: DebugError | null;
  relatedNodeId: string | null;
  relatedEventId: string | null;
}

export interface ParsingFact {
  id: string;
  text: string;
  sourceEventId: string;
  sourceToolCallId: string | null;
  evidenceRefs: string[];
}

export interface ParsingNote {
  id: string;
  text: string;
  sourceEventId: string;
  evidenceRefs: string[];
}

export interface ParsingResult {
  id: string;
  eventId: string;
  relatedNodeId: string;
  summary: string;
  factsByType: Record<ParsingSectionKey, ParsingFact[]>;
  notes: ParsingNote[];
}

export interface FeatureRecord {
  featureId: string;
  title: string;
  summary: string;
  evidenceRefs: string[];
  facts: string[];
}

export interface FamilyMappingRecord {
  featureId: string;
  familyIds: string[];
  primaryFamilyId: string;
  confidence: number;
  reasons: string[];
  familyNames: string[];
  familyScores: Record<string, number>;
}

export interface TestNodeProposal {
  title: string;
  nodeType: "test";
  sourceFeatureId: string;
  familyIds: string[];
  primaryFamilyId: string;
  rationale: string;
  priority: number;
  createdNodeId: string | null;
}

export interface ReasoningResult {
  id: string;
  eventId: string;
  relatedNodeId: string;
  identifiedFeatures: FeatureRecord[];
  familyMapping: FamilyMappingRecord[];
  proposedTestNodes: TestNodeProposal[];
  createdNodeIds: string[];
}

export interface StateItem {
  id: string;
  title: string;
  content: string;
  refs: string[];
  source: string;
  updatedInEventId: string;
  isNew: boolean;
}

export interface StateNoteRecord {
  id: string;
  text: string;
  updatedInEventId: string;
  isNew: boolean;
}

export interface StateTable {
  identities: StateItem[];
  sessionMaterials: StateItem[];
  keyEntrypoints: StateItem[];
  workflowPrerequisites: StateItem[];
  reusableArtifacts: StateItem[];
  sessionRisks: StateItem[];
  notes: StateNoteRecord[];
  latestUpdateEventId: string;
}

export interface RunSummary {
  runId: string;
  target: string;
  goal: string;
  status: RunStatus;
  currentStage: RunStage;
  startedAt: string;
  updatedAt: string;
  currentNodeId: string | null;
  currentActor: EventActor | null;
  nodes: TaskNode[];
  timeline: TimelineEvent[];
  toolCalls: ToolCallRecord[];
  parsingResults: ParsingResult[];
  reasoningResults: ReasoningResult[];
  stateTable: StateTable;
}
