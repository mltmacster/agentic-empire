"""
Sovereign Forge Platform - Core Pydantic Schemas
=================================================

This module defines the type-safe data models that form the "Ironclad Governance"
layer of the Sovereign Forge platform. All agent communications, journal entries,
and data exchanges must conform to these validated schemas.

Philosophy: "Real recognize real" - No hallucinations, no loose strings, only
validated objects that ensure the integrity of the entire agentic ecosystem.
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, SecretStr, SecretBytes, validator, field_validator
from pydantic import ConfigDict


# ============================================================================
# ENUMERATIONS
# ============================================================================

class AgentStatus(str, Enum):
    """Status of an agent in the system"""
    ACTIVE = "active"
    IDLE = "idle"
    PROCESSING = "processing"
    ERROR = "error"
    OFFLINE = "offline"


class TaskStatus(str, Enum):
    """Status of a task or story shard"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    FAILED = "failed"
    ARCHIVED = "archived"


class SecurityLevel(int, Enum):
    """Security clearance levels for agents and operations"""
    PUBLIC = 1
    INTERNAL = 2
    CONFIDENTIAL = 3
    SECRET = 4
    TOP_SECRET = 5


class AgentRole(str, Enum):
    """Roles of Guru Agents in the system"""
    ARCHITECTURAL_SOVEREIGN = "architectural_sovereign"
    CODE_GENERATION_MAESTRO = "code_generation_maestro"
    SECURITY_SENTINEL = "security_sentinel"
    DEVOPS_AUTOMATOR = "devops_automator"
    PROJECT_COORDINATOR = "project_coordinator"
    FRONTEND_ENGINEER = "reactive_frontend_engineer"
    BACKEND_ENGINEER = "backend_systems_engineer"
    DATA_SCIENCE_SHAPER = "data_science_shaper"
    PERFORMANCE_OPTIMIZER = "performance_optimizer"
    TEST_AUTOMATION_DIRECTOR = "test_automation_director"
    DOCUMENTATION_SYNTHESIZER = "documentation_synthesizer"
    UX_UI_DESIGNER = "ux_ui_designer"


# ============================================================================
# CORE DATA MODELS
# ============================================================================

class AgenticJournalEntry(BaseModel):
    """
    The fundamental unit of agent communication and memory.
    
    Every action taken by an agent MUST be recorded as a journal entry
    to ensure "No Content Left Behind" and maintain full context continuity.
    """
    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)
    
    task_id: str = Field(
        ...,
        description="Unique ID for the story shard (e.g., 'SHARD-001-INIT')",
        min_length=5,
        max_length=50
    )
    
    guru_agent: AgentRole = Field(
        ...,
        description="The Master Controller in charge of this task"
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="UTC timestamp of the journal entry"
    )
    
    logic_summary: str = Field(
        ...,
        description="The 'Journal' entry explaining what happened and why",
        min_length=10,
        max_length=5000
    )
    
    sub_agents_engaged: List[str] = Field(
        default_factory=list,
        description="List of sub-agents that participated in this task"
    )
    
    git_commit_hash: Optional[str] = Field(
        None,
        description="Git commit hash if code was committed",
        pattern=r'^[a-f0-9]{7,40}$'
    )
    
    artifacts_created: List[str] = Field(
        default_factory=list,
        description="Paths to artifacts (code, docs, media) created"
    )
    
    security_clearance: SecurityLevel = Field(
        default=SecurityLevel.INTERNAL,
        description="Security level required to access this journal entry"
    )
    
    parent_context_id: Optional[str] = Field(
        None,
        description="ID of parent workflow or context for traceability"
    )
    
    next_steps: List[str] = Field(
        default_factory=list,
        description="Recommended next actions for subsequent agents"
    )
    
    status: TaskStatus = Field(
        default=TaskStatus.IN_PROGRESS,
        description="Current status of the task"
    )


class CodeUpdate(BaseModel):
    """
    Represents a code change or generation event.
    
    Used by the Code Generation Maestro to document all code synthesis
    activities with full validation and security compliance.
    """
    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)
    
    file_path: str = Field(
        ...,
        description="Relative path to the file being created or modified",
        min_length=1
    )
    
    language: str = Field(
        ...,
        description="Programming language (e.g., 'python', 'javascript', 'typescript')"
    )
    
    code_snippet: str = Field(
        ...,
        description="The actual code content",
        min_length=1
    )
    
    tests_passed: bool = Field(
        default=False,
        description="Whether automated tests passed for this code"
    )
    
    test_coverage_percent: Optional[float] = Field(
        None,
        ge=0.0,
        le=100.0,
        description="Test coverage percentage if available"
    )
    
    dependency_audit: Optional[SecretStr] = Field(
        None,
        description="Sensitive dependency information (masked for security)"
    )
    
    security_scan_passed: bool = Field(
        default=False,
        description="Whether security scanning passed"
    )
    
    linting_passed: bool = Field(
        default=False,
        description="Whether code linting passed"
    )
    
    created_by: AgentRole = Field(
        default=AgentRole.CODE_GENERATION_MAESTRO,
        description="Agent responsible for this code"
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="When this code was generated"
    )


class StoryShardSpec(BaseModel):
    """
    Specification for a task shard in the BMAD workflow.
    
    Breaks down complex projects into atomic, executable units that
    maintain context and prevent agent "trippin'."
    """
    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)
    
    shard_id: str = Field(
        ...,
        description="Unique identifier for this story shard",
        pattern=r'^SHARD-\d{3}-[A-Z]+$'
    )
    
    title: str = Field(
        ...,
        description="Human-readable title of the task",
        min_length=5,
        max_length=200
    )
    
    description: str = Field(
        ...,
        description="Detailed description of what needs to be accomplished",
        min_length=20
    )
    
    owner_agent: AgentRole = Field(
        ...,
        description="Primary Guru Agent responsible for this shard"
    )
    
    contributing_agents: List[AgentRole] = Field(
        default_factory=list,
        description="Additional agents that will contribute"
    )
    
    priority: str = Field(
        default="medium",
        description="Priority level: critical, high, medium, low"
    )
    
    status: TaskStatus = Field(
        default=TaskStatus.PENDING,
        description="Current status of this shard"
    )
    
    dependencies: List[str] = Field(
        default_factory=list,
        description="List of shard IDs that must complete before this one"
    )
    
    estimated_complexity: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Complexity score from 1 (simple) to 10 (complex)"
    )
    
    acceptance_criteria: List[str] = Field(
        default_factory=list,
        description="Specific criteria that define 'done'"
    )
    
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="When this shard was created"
    )
    
    target_completion: Optional[datetime] = Field(
        None,
        description="Target completion date"
    )


class SecurityAuditReport(BaseModel):
    """
    Security audit report generated by the Security Sentinel.
    
    Ensures all code, configurations, and operations meet the
    "Ironclad Governance" security standards.
    """
    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)
    
    audit_id: str = Field(
        ...,
        description="Unique identifier for this audit",
        pattern=r'^AUDIT-\d{8}-[A-Z0-9]+$'
    )
    
    target_path: str = Field(
        ...,
        description="Path to file or directory being audited"
    )
    
    audit_type: str = Field(
        ...,
        description="Type of audit: vulnerability_scan, compliance_check, secret_detection"
    )
    
    vulnerabilities_found: int = Field(
        default=0,
        ge=0,
        description="Number of vulnerabilities detected"
    )
    
    critical_issues: List[str] = Field(
        default_factory=list,
        description="List of critical security issues"
    )
    
    warnings: List[str] = Field(
        default_factory=list,
        description="List of security warnings"
    )
    
    recommendations: List[str] = Field(
        default_factory=list,
        description="Recommended actions to improve security"
    )
    
    pydantic_validation_passed: bool = Field(
        default=False,
        description="Whether all Pydantic schemas are properly used"
    )
    
    secrets_properly_masked: bool = Field(
        default=False,
        description="Whether SecretStr/SecretBytes are used for sensitive data"
    )
    
    compliance_standards: List[str] = Field(
        default_factory=list,
        description="Compliance standards checked (e.g., 'GDPR', 'HIPAA')"
    )
    
    overall_security_score: float = Field(
        default=0.0,
        ge=0.0,
        le=100.0,
        description="Overall security score (0-100)"
    )
    
    audited_by: AgentRole = Field(
        default=AgentRole.SECURITY_SENTINEL,
        description="Agent that performed the audit"
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="When the audit was performed"
    )


class ArchitecturalSpec(BaseModel):
    """
    Architectural specification generated by the Architectural Sovereign.
    
    Represents the validated PRD and technical blueprint that guides
    all subsequent development work.
    """
    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)
    
    spec_id: str = Field(
        ...,
        description="Unique identifier for this specification",
        pattern=r'^SPEC-\d{8}-[A-Z0-9]+$'
    )
    
    project_name: str = Field(
        ...,
        description="Name of the project or application",
        min_length=3,
        max_length=100
    )
    
    project_description: str = Field(
        ...,
        description="Detailed description of the project",
        min_length=50
    )
    
    tech_stack: Dict[str, str] = Field(
        ...,
        description="Technology stack (e.g., {'frontend': 'React', 'backend': 'FastAPI'})"
    )
    
    architectural_patterns: List[str] = Field(
        default_factory=list,
        description="Architectural patterns to be used (e.g., 'microservices', 'event-driven')"
    )
    
    constraints: Dict[str, Any] = Field(
        default_factory=dict,
        description="Technical constraints (performance, security, cost, etc.)"
    )
    
    system_components: List[Dict[str, str]] = Field(
        default_factory=list,
        description="List of system components and their responsibilities"
    )
    
    data_models: List[str] = Field(
        default_factory=list,
        description="Core data models required"
    )
    
    api_endpoints: List[Dict[str, str]] = Field(
        default_factory=list,
        description="API endpoints specification"
    )
    
    security_requirements: List[str] = Field(
        default_factory=list,
        description="Security requirements and protocols"
    )
    
    deployment_strategy: str = Field(
        default="docker_compose",
        description="Deployment strategy (docker, kubernetes, serverless, etc.)"
    )
    
    estimated_timeline_weeks: int = Field(
        default=4,
        ge=1,
        description="Estimated timeline in weeks"
    )
    
    validated_by_pattern_matcher: bool = Field(
        default=False,
        description="Whether validated against 1000+ architectural patterns"
    )
    
    created_by: AgentRole = Field(
        default=AgentRole.ARCHITECTURAL_SOVEREIGN,
        description="Agent that created this specification"
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="When this spec was created"
    )


class DeploymentManifest(BaseModel):
    """
    Deployment manifest created by the DevOps Automator.
    
    Contains all information needed to deploy and operate the system
    in production environments.
    """
    model_config = ConfigDict(str_strip_whitespace=True, validate_assignment=True)
    
    manifest_id: str = Field(
        ...,
        description="Unique identifier for this deployment manifest",
        pattern=r'^DEPLOY-\d{8}-[A-Z0-9]+$'
    )
    
    application_name: str = Field(
        ...,
        description="Name of the application being deployed"
    )
    
    environment: str = Field(
        ...,
        description="Target environment: development, staging, production"
    )
    
    infrastructure_type: str = Field(
        ...,
        description="Infrastructure type: docker, kubernetes, serverless, vm"
    )
    
    container_images: List[Dict[str, str]] = Field(
        default_factory=list,
        description="Container images and their versions"
    )
    
    environment_variables: Dict[str, str] = Field(
        default_factory=dict,
        description="Non-sensitive environment variables"
    )
    
    secrets: List[str] = Field(
        default_factory=list,
        description="List of secret names (values stored securely)"
    )
    
    resource_requirements: Dict[str, str] = Field(
        default_factory=dict,
        description="CPU, memory, storage requirements"
    )
    
    networking: Dict[str, Any] = Field(
        default_factory=dict,
        description="Network configuration (ports, domains, load balancers)"
    )
    
    health_checks: List[Dict[str, str]] = Field(
        default_factory=list,
        description="Health check endpoints and configurations"
    )
    
    backup_strategy: str = Field(
        default="automated_daily",
        description="Backup and disaster recovery strategy"
    )
    
    monitoring_enabled: bool = Field(
        default=True,
        description="Whether monitoring is enabled"
    )
    
    ci_cd_pipeline: str = Field(
        default="github_actions",
        description="CI/CD pipeline being used"
    )
    
    created_by: AgentRole = Field(
        default=AgentRole.DEVOPS_AUTOMATOR,
        description="Agent that created this manifest"
    )
    
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="When this manifest was created"
    )


# ============================================================================
# VALIDATION UTILITIES
# ============================================================================

def validate_journal_entry(entry: AgenticJournalEntry) -> bool:
    """
    Validate a journal entry for completeness and security compliance.
    
    Returns True if the entry meets all "Ironclad Governance" standards.
    """
    if not entry.task_id or not entry.logic_summary:
        return False
    
    if entry.security_clearance == SecurityLevel.TOP_SECRET:
        # Top secret entries require additional validation
        if not entry.git_commit_hash:
            return False
    
    return True


def validate_code_update(update: CodeUpdate) -> bool:
    """
    Validate a code update for quality and security standards.
    
    Returns True if the code meets minimum quality gates.
    """
    if not update.tests_passed:
        return False
    
    if not update.security_scan_passed:
        return False
    
    if not update.linting_passed:
        return False
    
    return True


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # Example: Creating a journal entry
    journal = AgenticJournalEntry(
        task_id="SHARD-001-INIT",
        guru_agent=AgentRole.ARCHITECTURAL_SOVEREIGN,
        logic_summary="Initialized the Sovereign Forge repository structure. Created all core directories and manifest files. The foundation is now ready for agent activation.",
        sub_agents_engaged=["Pattern Matcher", "Constraint Validator"],
        artifacts_created=[
            ".agentic/manifests/conductor_manifest.json",
            "mcp_config.json"
        ],
        security_clearance=SecurityLevel.INTERNAL,
        status=TaskStatus.COMPLETED,
        next_steps=[
            "Generate system prompts for five core Guru Agents",
            "Implement GitHub Actions workflows"
        ]
    )
    
    print("✅ Journal Entry Validated:", validate_journal_entry(journal))
    print("\n📝 Journal Entry:")
    print(journal.model_dump_json(indent=2))
