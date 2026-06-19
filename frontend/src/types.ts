export type Status = "queued" | "running" | "done" | "stopped" | "error" | "timeout" | string;

export type Bootstrap = {
  llm_mode: string;
  model: string;
  sandbox_container: string;
  sandbox_containers: string[];
  sandbox_workdir: string;
  agent_capacity: number;
  agent_slots: AgentSlot[];
  knowledge: KnowledgeStats;
  skills: SkillStats;
  defaults: {
    max_rounds: number;
    max_commands: number;
    command_timeout_sec: number;
  };
};

export type AgentSlot = {
  slot: number;
  agent_id: string;
  container: string;
  status: "idle" | "running" | string;
  status_reason: "not_started" | "flag_captured" | "not_running" | "running" | string;
  allocated: boolean;
  mission_id: string;
  mission_name: string;
  target: string;
  mission_status: string;
  captured_flag_count: number;
  thread_alive: boolean;
};

export type KnowledgeStats = {
  available?: boolean;
  status?: string;
  search_backend?: string;
  total_docs?: number;
  total_chunks?: number;
  domains?: Record<string, number>;
  cve_poc_entries?: number;
  rag?: {
    available?: boolean;
    error?: string;
    total_chunks?: number;
  };
  error?: string;
};

export type SkillStats = {
  status?: string;
  skills_dir?: string;
  total?: number;
  enabled?: number;
  errors?: string[];
};

export type Skill = {
  id: string;
  name: string;
  description: string;
  tags: string[];
  path: string;
  enabled: boolean;
  metadata?: Record<string, unknown>;
};

export type Mission = {
  id: string;
  name: string;
  target: string;
  goal: string;
  scope: string;
  domains: string[];
  status: Status;
  max_rounds: number;
  max_commands: number;
  command_timeout_sec: number;
  model: string;
  expected_flags: number;
  skills: string[];
  activated_skills: string[];
  human_collab_enabled: boolean;
  error_message: string;
  stop_requested: boolean;
  captured_flags: string[];
  captured_flag_count: number;
  created_at: string;
  updated_at: string;
};

export type Round = {
  round_no: number;
  worker_role: string;
  prompt_excerpt: string;
  raw_response: string;
  decision: Record<string, unknown>;
  created_at: string;
};

export type Event = {
  id: number;
  round_no: number;
  type: string;
  title: string;
  content: string;
  command: string;
  exit_code: number;
  metadata: Record<string, unknown>;
  started_at: string;
  ended_at: string;
};

export type MemoryState = {
  summary: string;
  findings: unknown[];
  leads: unknown[];
  dead_ends: unknown[];
  credentials: unknown[];
  next_focus: unknown[];
  nodes: Record<string, unknown>;
  topology: unknown[];
  idea_board: Record<string, unknown>;
  memory_board: Record<string, unknown>;
  highest_value_lead: string;
  blocked_reason: string;
  next_one_command: string;
  primary_hypothesis: string;
  next_verification: string;
  failure_boundary: string;
  blocked_prerequisite: string;
  required_next_evidence: string;
  observer_enforcement_state: string;
  agent_override_reason: string;
  updated_at: string;
};

export type ObserverMessage = {
  id: number;
  observer_id: string;
  mission_id: string;
  round_no: number;
  type: string;
  direction: string;
  title: string;
  content: string;
  metadata: Record<string, unknown>;
  created_at: string;
};

export type ObserverSummary = {
  agent: Record<string, unknown> | null;
  status: string;
  latest_decision: Record<string, unknown>;
  latest_message: ObserverMessage | null;
  messages: ObserverMessage[];
  stats: {
    messages: number;
    decisions: number;
    warn_critical: number;
    steers: number;
    memory_patches: number;
    skill_signals: number;
  };
};

export type ExperimentRecord = {
  mission_id: string;
  mission_name: string;
  mission_status: string;
  challenge_code: string;
  target: string;
  goal: string;
  difficulty: string;
  outcome: string;
  failure_reason: string;
  key_parameters: string;
  notes: string;
  started_at: string;
  ended_at: string;
  duration_sec: number | null;
  selected_skills: string[];
  activated_skills: string[];
  event_count: number;
  command_count: number;
  error_count: number;
  flag_count: number;
  captured_flags: string[];
  captured_flag_count: number;
  updated_at: string;
};

export type HumanGuidance = {
  id: number;
  mission_id: string;
  content: string;
  status: string;
  created_at: string;
  consumed_at: string;
};

export type MissionDetail = {
  mission: Mission;
  memory: MemoryState;
  rounds: Round[];
  events: Event[];
  observer: ObserverSummary;
  experiment: ExperimentRecord | null;
  captured_flags: string[];
  captured_flag_count: number;
  human_guidance: HumanGuidance[];
  thread_alive: boolean;
};

export type KnowledgeItem = {
  id: number;
  source: string;
  domain: string;
  title: string;
  path: string;
  snippet?: string;
  body?: string;
};

export type ExperienceCraft = {
  id: string;
  path: string;
  source: "craft" | string;
  status: "pending_review" | "approved" | "rejected" | string;
  source_mission_id: string;
  mission_name: string;
  target: string;
  created_at: string;
  reviewed_at: string;
  reviewer: string;
  distilled_path: string;
  snippet: string;
};

export type ExperienceCraftDetail = ExperienceCraft & {
  ok: boolean;
  truncated: boolean;
  content: string;
};

export type Config = Record<string, string | number | boolean | null>;

export type ConfigResponse = {
  config: Config;
};

export type ConfigSaveResponse = {
  ok: boolean;
  config: Config;
  errors?: Record<string, string>;
};

export type AppTab = "overview" | "timeline" | "observer" | "memory" | "evidence" | "knowledge";
