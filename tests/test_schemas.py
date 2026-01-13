"""
Comprehensive Test Suite for Sovereign Forge Pydantic Schemas
===============================================================

This test suite validates all Pydantic models to ensure type safety,
security compliance, and data integrity across the agentic ecosystem.
"""

import pytest
from datetime import datetime
from pydantic import ValidationError

import sys
sys.path.insert(0, '..')

from schemas import (
    AgenticJournalEntry,
    CodeUpdate,
    StoryShardSpec,
    SecurityAuditReport,
    ArchitecturalSpec,
    DeploymentManifest,
    AgentStatus,
    TaskStatus,
    SecurityLevel,
    AgentRole,
    validate_journal_entry,
    validate_code_update
)


class TestAgenticJournalEntry:
    """Test suite for AgenticJournalEntry model"""
    
    def test_valid_journal_entry(self):
        """Test creating a valid journal entry"""
        entry = AgenticJournalEntry(
            task_id="SHARD-001-TEST",
            guru_agent=AgentRole.ARCHITECTURAL_SOVEREIGN,
            logic_summary="This is a test journal entry to validate the schema.",
            sub_agents_engaged=["Pattern Matcher", "Constraint Validator"],
            artifacts_created=["test_file.py"],
            security_clearance=SecurityLevel.INTERNAL,
            status=TaskStatus.COMPLETED
        )
        
        assert entry.task_id == "SHARD-001-TEST"
        assert entry.guru_agent == AgentRole.ARCHITECTURAL_SOVEREIGN
        assert len(entry.sub_agents_engaged) == 2
        assert entry.status == TaskStatus.COMPLETED
        assert validate_journal_entry(entry) is True
    
    def test_journal_entry_with_git_commit(self):
        """Test journal entry with git commit hash"""
        entry = AgenticJournalEntry(
            task_id="SHARD-002-GIT",
            guru_agent=AgentRole.CODE_GENERATION_MAESTRO,
            logic_summary="Generated code and committed to repository.",
            git_commit_hash="a1b2c3d",
            status=TaskStatus.COMPLETED
        )
        
        assert entry.git_commit_hash == "a1b2c3d"
        assert len(entry.git_commit_hash) == 7
    
    def test_invalid_task_id(self):
        """Test that invalid task_id format is rejected"""
        with pytest.raises(ValidationError):
            AgenticJournalEntry(
                task_id="BAD",  # Too short
                guru_agent=AgentRole.SECURITY_SENTINEL,
                logic_summary="This should fail."
            )
    
    def test_invalid_logic_summary(self):
        """Test that too-short logic summary is rejected"""
        with pytest.raises(ValidationError):
            AgenticJournalEntry(
                task_id="SHARD-003-SHORT",
                guru_agent=AgentRole.DEVOPS_AUTOMATOR,
                logic_summary="Too short"  # Less than 10 chars
            )
    
    def test_security_clearance_levels(self):
        """Test different security clearance levels"""
        for level in SecurityLevel:
            entry = AgenticJournalEntry(
                task_id=f"SHARD-SEC-{level.value}",
                guru_agent=AgentRole.SECURITY_SENTINEL,
                logic_summary="Testing security clearance levels.",
                security_clearance=level
            )
            assert entry.security_clearance == level


class TestCodeUpdate:
    """Test suite for CodeUpdate model"""
    
    def test_valid_code_update(self):
        """Test creating a valid code update"""
        update = CodeUpdate(
            file_path="src/main.py",
            language="python",
            code_snippet="def hello():\n    return 'Hello, World!'",
            tests_passed=True,
            security_scan_passed=True,
            linting_passed=True,
            test_coverage_percent=95.5
        )
        
        assert update.file_path == "src/main.py"
        assert update.language == "python"
        assert update.tests_passed is True
        assert update.test_coverage_percent == 95.5
        assert validate_code_update(update) is True
    
    def test_code_update_validation_failure(self):
        """Test that code update fails validation when tests don't pass"""
        update = CodeUpdate(
            file_path="src/buggy.py",
            language="python",
            code_snippet="def buggy(): pass",
            tests_passed=False,  # Tests failed
            security_scan_passed=True,
            linting_passed=True
        )
        
        assert validate_code_update(update) is False
    
    def test_invalid_coverage_percentage(self):
        """Test that invalid coverage percentage is rejected"""
        with pytest.raises(ValidationError):
            CodeUpdate(
                file_path="src/test.py",
                language="python",
                code_snippet="pass",
                test_coverage_percent=150.0  # Invalid: > 100
            )
    
    def test_code_update_with_security_scan_failure(self):
        """Test code update with failed security scan"""
        update = CodeUpdate(
            file_path="src/vulnerable.py",
            language="python",
            code_snippet="import os; os.system('rm -rf /')",
            tests_passed=True,
            security_scan_passed=False,  # Security issue detected
            linting_passed=True
        )
        
        assert validate_code_update(update) is False


class TestStoryShardSpec:
    """Test suite for StoryShardSpec model"""
    
    def test_valid_story_shard(self):
        """Test creating a valid story shard"""
        shard = StoryShardSpec(
            shard_id="SHARD-001-INIT",
            title="Initialize Platform Foundation",
            description="Set up the core infrastructure for the Sovereign Forge platform.",
            owner_agent=AgentRole.PROJECT_COORDINATOR,
            contributing_agents=[AgentRole.ARCHITECTURAL_SOVEREIGN, AgentRole.SECURITY_SENTINEL],
            priority="critical",
            status=TaskStatus.COMPLETED,
            estimated_complexity=8,
            acceptance_criteria=[
                "Repository structure created",
                "Pydantic schemas implemented",
                "GitHub Actions configured"
            ]
        )
        
        assert shard.shard_id == "SHARD-001-INIT"
        assert shard.priority == "critical"
        assert len(shard.contributing_agents) == 2
        assert shard.estimated_complexity == 8
    
    def test_invalid_shard_id_format(self):
        """Test that invalid shard ID format is rejected"""
        with pytest.raises(ValidationError):
            StoryShardSpec(
                shard_id="INVALID-ID",  # Doesn't match pattern
                title="Test Shard",
                description="This should fail due to invalid ID format.",
                owner_agent=AgentRole.PROJECT_COORDINATOR
            )
    
    def test_complexity_bounds(self):
        """Test that complexity is bounded between 1 and 10"""
        with pytest.raises(ValidationError):
            StoryShardSpec(
                shard_id="SHARD-999-TEST",
                title="Test Complexity",
                description="Testing complexity validation.",
                owner_agent=AgentRole.ARCHITECTURAL_SOVEREIGN,
                estimated_complexity=15  # Invalid: > 10
            )


class TestSecurityAuditReport:
    """Test suite for SecurityAuditReport model"""
    
    def test_valid_security_audit(self):
        """Test creating a valid security audit report"""
        report = SecurityAuditReport(
            audit_id="AUDIT-20260113-ABC123",
            target_path="src/",
            audit_type="vulnerability_scan",
            vulnerabilities_found=2,
            critical_issues=["SQL Injection in user_input.py"],
            warnings=["Deprecated library usage"],
            recommendations=["Update dependencies", "Add input validation"],
            pydantic_validation_passed=True,
            secrets_properly_masked=True,
            compliance_standards=["GDPR", "SOC2"],
            overall_security_score=85.5,
            audited_by=AgentRole.SECURITY_SENTINEL
        )
        
        assert report.vulnerabilities_found == 2
        assert len(report.critical_issues) == 1
        assert report.overall_security_score == 85.5
        assert report.pydantic_validation_passed is True
    
    def test_invalid_audit_id(self):
        """Test that invalid audit ID format is rejected"""
        with pytest.raises(ValidationError):
            SecurityAuditReport(
                audit_id="INVALID",  # Doesn't match pattern
                target_path="src/",
                audit_type="compliance_check"
            )
    
    def test_security_score_bounds(self):
        """Test that security score is bounded between 0 and 100"""
        with pytest.raises(ValidationError):
            SecurityAuditReport(
                audit_id="AUDIT-20260113-TEST01",
                target_path="src/",
                audit_type="secret_detection",
                overall_security_score=150.0  # Invalid: > 100
            )


class TestArchitecturalSpec:
    """Test suite for ArchitecturalSpec model"""
    
    def test_valid_architectural_spec(self):
        """Test creating a valid architectural specification"""
        spec = ArchitecturalSpec(
            spec_id="SPEC-20260113-CHOICEWRIDE",
            project_name="Choice Wride",
            project_description="A JEPA-inspired logistics platform for the Greater Atlanta region.",
            tech_stack={
                "frontend": "React + TypeScript",
                "backend": "FastAPI + Python",
                "database": "DuckDB",
                "mapping": "Overture Maps"
            },
            architectural_patterns=["microservices", "event-driven", "CQRS"],
            constraints={
                "max_latency_ms": 200,
                "budget_monthly": 500,
                "compliance": ["GDPR"]
            },
            system_components=[
                {"name": "API Gateway", "responsibility": "Request routing"},
                {"name": "Semantic Engine", "responsibility": "World modeling"}
            ],
            security_requirements=["OAuth2", "TLS 1.3", "Rate limiting"],
            deployment_strategy="docker_compose",
            estimated_timeline_weeks=12,
            validated_by_pattern_matcher=True
        )
        
        assert spec.project_name == "Choice Wride"
        assert len(spec.tech_stack) == 4
        assert spec.estimated_timeline_weeks == 12
        assert spec.validated_by_pattern_matcher is True
    
    def test_invalid_spec_id(self):
        """Test that invalid spec ID format is rejected"""
        with pytest.raises(ValidationError):
            ArchitecturalSpec(
                spec_id="BAD-SPEC",  # Doesn't match pattern
                project_name="Test Project",
                project_description="This should fail due to invalid spec ID.",
                tech_stack={"frontend": "React"}
            )


class TestDeploymentManifest:
    """Test suite for DeploymentManifest model"""
    
    def test_valid_deployment_manifest(self):
        """Test creating a valid deployment manifest"""
        manifest = DeploymentManifest(
            manifest_id="DEPLOY-20260113-PROD01",
            application_name="sovereign-forge",
            environment="production",
            infrastructure_type="kubernetes",
            container_images=[
                {"name": "api-server", "version": "1.0.0"},
                {"name": "worker", "version": "1.0.0"}
            ],
            environment_variables={
                "LOG_LEVEL": "info",
                "API_VERSION": "v1"
            },
            secrets=["DATABASE_URL", "API_KEY"],
            resource_requirements={
                "cpu": "2 cores",
                "memory": "4GB",
                "storage": "50GB"
            },
            networking={
                "ports": [80, 443],
                "domain": "sovereignforge.ai"
            },
            health_checks=[
                {"endpoint": "/health", "interval": "30s"}
            ],
            monitoring_enabled=True,
            ci_cd_pipeline="github_actions"
        )
        
        assert manifest.environment == "production"
        assert manifest.infrastructure_type == "kubernetes"
        assert len(manifest.container_images) == 2
        assert manifest.monitoring_enabled is True
    
    def test_invalid_manifest_id(self):
        """Test that invalid manifest ID format is rejected"""
        with pytest.raises(ValidationError):
            DeploymentManifest(
                manifest_id="INVALID",  # Doesn't match pattern
                application_name="test-app",
                environment="staging",
                infrastructure_type="docker"
            )


class TestEnumerations:
    """Test suite for enumeration types"""
    
    def test_agent_status_enum(self):
        """Test AgentStatus enumeration"""
        assert AgentStatus.ACTIVE.value == "active"
        assert AgentStatus.OFFLINE.value == "offline"
    
    def test_task_status_enum(self):
        """Test TaskStatus enumeration"""
        assert TaskStatus.PENDING.value == "pending"
        assert TaskStatus.COMPLETED.value == "completed"
    
    def test_security_level_enum(self):
        """Test SecurityLevel enumeration"""
        assert SecurityLevel.PUBLIC.value == 1
        assert SecurityLevel.TOP_SECRET.value == 5
    
    def test_agent_role_enum(self):
        """Test AgentRole enumeration"""
        assert AgentRole.ARCHITECTURAL_SOVEREIGN.value == "architectural_sovereign"
        assert AgentRole.CODE_GENERATION_MAESTRO.value == "code_generation_maestro"


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
