"""
Test Suite for Inter-Agent Communication
==========================================

This test suite validates that agents can communicate effectively through
the journal system and orchestrator, ensuring the Git-as-Memory architecture
functions correctly.
"""

import pytest
import json
from pathlib import Path
from datetime import datetime

import sys
sys.path.insert(0, '..')

from schemas import (
    AgenticJournalEntry,
    StoryShardSpec,
    AgentRole,
    TaskStatus,
    SecurityLevel
)
from orchestrator import AgentOrchestrator, OrchestratorMode


class TestOrchestrator:
    """Test suite for the Agent Orchestrator"""
    
    def test_orchestrator_initialization(self):
        """Test that the orchestrator initializes correctly"""
        orchestrator = AgentOrchestrator(repo_path=".", mode=OrchestratorMode.TESTING)
        
        assert orchestrator.repo_path.exists()
        assert orchestrator.manifest is not None
        assert len(orchestrator.manifest['guru_agents']) == 12
    
    def test_list_active_agents(self):
        """Test listing active Guru Agents"""
        orchestrator = AgentOrchestrator(repo_path=".", mode=OrchestratorMode.TESTING)
        
        active_agents = orchestrator.list_guru_agents(status="active")
        
        # Should have 5 active agents from Phase 1
        assert len(active_agents) >= 5
        
        # Verify the core 5 are present
        agent_names = [a['name'] for a in active_agents]
        assert "Architectural Sovereign" in agent_names
        assert "Code Generation Maestro" in agent_names
        assert "Security Sentinel" in agent_names
    
    def test_get_agent_by_role(self):
        """Test retrieving a specific agent by role"""
        orchestrator = AgentOrchestrator(repo_path=".", mode=OrchestratorMode.TESTING)
        
        agent = orchestrator.get_agent_by_role(AgentRole.ARCHITECTURAL_SOVEREIGN)
        
        assert agent is not None
        assert agent['name'] == "Architectural Sovereign"
        assert agent['role'] == "System Design & Pattern Governance"


class TestStoryShardManagement:
    """Test suite for story shard creation and management"""
    
    def test_create_story_shard(self):
        """Test creating a new story shard"""
        orchestrator = AgentOrchestrator(repo_path=".", mode=OrchestratorMode.TESTING)
        
        shard = orchestrator.create_story_shard(
            shard_id="SHARD-001-TEST",
            title="Test Story Shard Creation",
            description="This is a test shard to validate the creation process.",
            owner_agent=AgentRole.PROJECT_COORDINATOR,
            priority="high"
        )
        
        assert shard.shard_id == "SHARD-TEST-001"
        assert shard.title == "Test Story Shard Creation"
        assert shard.owner_agent == AgentRole.PROJECT_COORDINATOR
        assert shard.status == TaskStatus.PENDING
    
    def test_assign_shard_to_agent(self):
        """Test assigning a story shard to an agent"""
        orchestrator = AgentOrchestrator(repo_path=".", mode=OrchestratorMode.TESTING)
        
        # Create a shard
        shard = orchestrator.create_story_shard(
            shard_id="SHARD-002-TEST",
            title="Test Shard Assignment",
            description="Testing shard assignment to agents.",
            owner_agent=AgentRole.SECURITY_SENTINEL,
            priority="medium"
        )
        
        # Assign it
        agent = orchestrator.assign_shard_to_agent("SHARD-002-TEST")
        
        assert agent is not None
        assert agent['name'] == "Security Sentinel"
    
    def test_complete_shard(self):
        """Test marking a story shard as completed"""
        orchestrator = AgentOrchestrator(repo_path=".", mode=OrchestratorMode.TESTING)
        
        # Create a shard
        orchestrator.create_story_shard(
            shard_id="SHARD-003-TEST",
            title="Test Shard Completion",
            description="Testing shard completion workflow.",
            owner_agent=AgentRole.CODE_GENERATION_MAESTRO,
            priority="low"
        )
        
        # Complete it
        result = orchestrator.complete_shard("SHARD-003-TEST")
        
        assert result is True


class TestJournalCommunication:
    """Test suite for journal-based communication"""
    
    def test_create_journal_entry(self):
        """Test creating a journal entry"""
        orchestrator = AgentOrchestrator(repo_path=".", mode=OrchestratorMode.TESTING)
        
        entry = orchestrator.create_journal_entry(
            task_id="SHARD-004-TEST",
            guru_agent=AgentRole.DEVOPS_AUTOMATOR,
            logic_summary="Testing journal entry creation for inter-agent communication validation.",
            sub_agents_engaged=["Pipeline Architect", "Infrastructure Provisioner"],
            artifacts_created=["test_artifact.yml"],
            status=TaskStatus.IN_PROGRESS
        )
        
        assert entry.task_id == "SHARD-004-TEST"
        assert entry.guru_agent == AgentRole.DEVOPS_AUTOMATOR
        assert len(entry.sub_agents_engaged) == 2
        assert entry.status == TaskStatus.IN_PROGRESS
    
    def test_journal_entry_file_creation(self):
        """Test that journal entries are written to files"""
        orchestrator = AgentOrchestrator(repo_path=".", mode=OrchestratorMode.TESTING)
        
        # Create a journal entry
        orchestrator.create_journal_entry(
            task_id="SHARD-005-TEST",
            guru_agent=AgentRole.ARCHITECTURAL_SOVEREIGN,
            logic_summary="Testing that journal entries are persisted to the filesystem.",
            status=TaskStatus.COMPLETED
        )
        
        # Check that a file was created in the journal directory
        journal_dir = Path("journal")
        assert journal_dir.exists()
        
        # Find the most recent journal entry
        journal_files = list(journal_dir.glob("*.md"))
        assert len(journal_files) > 0
        
        # Verify the file contains the task_id
        latest_file = max(journal_files, key=lambda p: p.stat().st_mtime)
        content = latest_file.read_text()
        assert "SHARD-005-TEST" in content


class TestStatusReporting:
    """Test suite for platform status reporting"""
    
    def test_get_status_report(self):
        """Test generating a status report"""
        orchestrator = AgentOrchestrator(repo_path=".", mode=OrchestratorMode.TESTING)
        
        status = orchestrator.get_status_report()
        
        assert status['platform'] == "Sovereign Forge"
        assert status['mode'] == "testing"
        assert 'guru_agents' in status
        assert 'story_shards' in status
        assert status['guru_agents']['total'] == 12


class TestAgentCoordination:
    """Test suite for multi-agent coordination"""
    
    def test_multi_agent_workflow(self):
        """Test a complete multi-agent workflow"""
        orchestrator = AgentOrchestrator(repo_path=".", mode=OrchestratorMode.TESTING)
        
        # Step 1: Project Coordinator creates a story shard
        shard = orchestrator.create_story_shard(
            shard_id="SHARD-006-WORKFLOW",
            title="Multi-Agent Workflow Test",
            description="Testing coordination between multiple agents.",
            owner_agent=AgentRole.ARCHITECTURAL_SOVEREIGN,
            priority="critical"
        )
        
        # Step 2: Assign to Architectural Sovereign
        agent = orchestrator.assign_shard_to_agent("SHARD-006-WORKFLOW")
        assert agent['name'] == "Architectural Sovereign"
        
        # Step 3: Architectural Sovereign creates a journal entry
        entry1 = orchestrator.create_journal_entry(
            task_id="SHARD-006-WORKFLOW",
            guru_agent=AgentRole.ARCHITECTURAL_SOVEREIGN,
            logic_summary="Analyzed requirements and created architectural specification.",
            sub_agents_engaged=["Pattern Matcher", "Constraint Validator"],
            artifacts_created=["specs/workflow_test_spec.md"],
            status=TaskStatus.IN_PROGRESS
        )
        
        # Step 4: Code Generation Maestro picks up the spec and generates code
        entry2 = orchestrator.create_journal_entry(
            task_id="SHARD-006-WORKFLOW",
            guru_agent=AgentRole.CODE_GENERATION_MAESTRO,
            logic_summary="Generated code based on architectural specification from Architectural Sovereign.",
            sub_agents_engaged=["Syntax Specialist"],
            artifacts_created=["src/workflow_test.py"],
            status=TaskStatus.IN_PROGRESS
        )
        
        # Step 5: Security Sentinel audits the code
        entry3 = orchestrator.create_journal_entry(
            task_id="SHARD-006-WORKFLOW",
            guru_agent=AgentRole.SECURITY_SENTINEL,
            logic_summary="Performed security audit on generated code. No vulnerabilities found.",
            sub_agents_engaged=["Vulnerability Scanner"],
            status=TaskStatus.COMPLETED
        )
        
        # Step 6: Mark shard as completed
        result = orchestrator.complete_shard("SHARD-006-WORKFLOW")
        assert result is True
        
        # Verify all journal entries were created
        journal_dir = Path("journal")
        journal_files = list(journal_dir.glob("*shard-006-workflow*.md"))
        assert len(journal_files) >= 3


# Run tests if executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
