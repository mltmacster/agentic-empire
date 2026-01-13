"""
Sovereign Forge - Agent Runtime Orchestrator
=============================================

This module implements the core orchestration system that manages the lifecycle
of Guru Agents and Sub-Agents, handles task distribution, and ensures proper
communication through the Git-as-Memory architecture.

Philosophy: This is the "Agentic Conductor" - the maestro that coordinates
the entire swarm while maintaining the BMAD principles.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Any
from enum import Enum

from schemas import (
    AgenticJournalEntry,
    StoryShardSpec,
    AgentRole,
    TaskStatus,
    SecurityLevel
)


class OrchestratorMode(str, Enum):
    """Operating modes for the orchestrator"""
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"


class AgentOrchestrator:
    """
    The Agentic Conductor - orchestrates all agent activities.
    
    This class manages:
    - Loading and parsing the conductor manifest
    - Distributing story shards to appropriate agents
    - Managing the Git-Loop workflow
    - Ensuring journal entries are created
    - Coordinating inter-agent communication
    """
    
    def __init__(self, repo_path: str = ".", mode: OrchestratorMode = OrchestratorMode.DEVELOPMENT):
        """
        Initialize the orchestrator.
        
        Args:
            repo_path: Path to the Sovereign Forge repository
            mode: Operating mode (development, testing, production)
        """
        self.repo_path = Path(repo_path)
        self.mode = mode
        self.manifest = self._load_manifest()
        self.active_shards = self._load_active_shards()
        
        print(f"🎭 Agent Orchestrator initialized in {mode.value} mode")
        print(f"📂 Repository: {self.repo_path.absolute()}")
        print(f"🤖 Active Guru Agents: {len([a for a in self.manifest['guru_agents'] if a['status'] == 'active'])}")
    
    def _load_manifest(self) -> Dict[str, Any]:
        """Load the conductor manifest"""
        manifest_path = self.repo_path / ".agentic" / "manifests" / "conductor_manifest.json"
        
        if not manifest_path.exists():
            raise FileNotFoundError(f"Conductor manifest not found at {manifest_path}")
        
        with open(manifest_path, 'r') as f:
            return json.load(f)
    
    def _load_active_shards(self) -> Dict[str, Any]:
        """Load active story shards"""
        shards_path = self.repo_path / ".agentic" / "manifests" / "active_story_shards.json"
        
        if not shards_path.exists():
            return {"active_shards": [], "completed_shards": [], "archived_shards": []}
        
        with open(shards_path, 'r') as f:
            return json.load(f)
    
    def list_guru_agents(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List all Guru Agents, optionally filtered by status.
        
        Args:
            status: Filter by status ('active', 'planned', 'offline')
        
        Returns:
            List of Guru Agent definitions
        """
        agents = self.manifest['guru_agents']
        
        if status:
            agents = [a for a in agents if a['status'] == status]
        
        return agents
    
    def get_agent_by_role(self, role: AgentRole) -> Optional[Dict[str, Any]]:
        """
        Get a specific Guru Agent by role.
        
        Args:
            role: The AgentRole enum value
        
        Returns:
            Agent definition or None if not found
        """
        for agent in self.manifest['guru_agents']:
            if agent['name'].lower().replace(' ', '_') == role.value:
                return agent
        return None
    
    def create_story_shard(
        self,
        shard_id: str,
        title: str,
        description: str,
        owner_agent: AgentRole,
        priority: str = "medium",
        dependencies: List[str] = None
    ) -> StoryShardSpec:
        """
        Create a new story shard and add it to active tracking.
        
        Args:
            shard_id: Unique shard identifier (e.g., "SHARD-003-BUILD")
            title: Human-readable title
            description: Detailed description
            owner_agent: Primary Guru Agent responsible
            priority: Priority level (critical, high, medium, low)
            dependencies: List of shard IDs that must complete first
        
        Returns:
            Validated StoryShardSpec instance
        """
        shard = StoryShardSpec(
            shard_id=shard_id,
            title=title,
            description=description,
            owner_agent=owner_agent,
            priority=priority,
            status=TaskStatus.PENDING,
            dependencies=dependencies or [],
            estimated_complexity=5
        )
        
        # Add to active shards
        shard_dict = {
            "shard_id": shard.shard_id,
            "title": shard.title,
            "status": shard.status.value,
            "priority": shard.priority,
            "owner_agent": shard.owner_agent.value,
            "created_at": shard.created_at.isoformat(),
            "dependencies": shard.dependencies
        }
        
        self.active_shards["active_shards"].append(shard_dict)
        self._save_active_shards()
        
        print(f"✅ Created story shard: {shard_id}")
        print(f"   Owner: {owner_agent.value}")
        print(f"   Priority: {priority}")
        
        return shard
    
    def assign_shard_to_agent(self, shard_id: str) -> Optional[Dict[str, Any]]:
        """
        Assign a story shard to its owner agent for execution.
        
        Args:
            shard_id: The shard to assign
        
        Returns:
            Agent definition or None if shard not found
        """
        # Find the shard
        shard = None
        for s in self.active_shards["active_shards"]:
            if s["shard_id"] == shard_id:
                shard = s
                break
        
        if not shard:
            print(f"❌ Shard {shard_id} not found")
            return None
        
        # Get the owner agent
        owner_role = shard["owner_agent"]
        agent = None
        for a in self.manifest['guru_agents']:
            if a['name'].lower().replace(' ', '_') == owner_role:
                agent = a
                break
        
        if not agent:
            print(f"❌ Agent {owner_role} not found")
            return None
        
        # Update shard status
        shard["status"] = TaskStatus.IN_PROGRESS.value
        self._save_active_shards()
        
        print(f"📋 Assigned {shard_id} to {agent['name']}")
        print(f"   Status: {shard['status']}")
        
        return agent
    
    def create_journal_entry(
        self,
        task_id: str,
        guru_agent: AgentRole,
        logic_summary: str,
        sub_agents_engaged: List[str] = None,
        artifacts_created: List[str] = None,
        status: TaskStatus = TaskStatus.IN_PROGRESS
    ) -> AgenticJournalEntry:
        """
        Create a journal entry for an agent action.
        
        Args:
            task_id: The story shard ID
            guru_agent: The Guru Agent creating the entry
            logic_summary: Explanation of what was done and why
            sub_agents_engaged: List of sub-agents that participated
            artifacts_created: List of artifact paths created
            status: Current task status
        
        Returns:
            Validated AgenticJournalEntry instance
        """
        entry = AgenticJournalEntry(
            task_id=task_id,
            guru_agent=guru_agent,
            logic_summary=logic_summary,
            sub_agents_engaged=sub_agents_engaged or [],
            artifacts_created=artifacts_created or [],
            security_clearance=SecurityLevel.INTERNAL,
            status=status
        )
        
        # Save to journal directory
        journal_dir = self.repo_path / "journal"
        journal_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
        filename = f"{timestamp}-{task_id.lower()}.md"
        filepath = journal_dir / filename
        
        # Create markdown journal entry
        content = f"""---
task_id: "{entry.task_id}"
status: "{entry.status.value}"
owner_agent: "{entry.guru_agent.value}"
contributing_agents: {json.dumps(entry.sub_agents_engaged)}
last_sync: "{entry.timestamp.isoformat()}"
security_clearance: {entry.security_clearance.value}
---

# Journal Entry: {entry.task_id}

**Date:** {entry.timestamp.strftime("%Y-%m-%d %H:%M:%S")}  
**Agent:** {entry.guru_agent.value.replace('_', ' ').title()}  
**Status:** {entry.status.value.upper()}

## Summary

{entry.logic_summary}

## Sub-Agents Engaged

{chr(10).join(f"- {agent}" for agent in entry.sub_agents_engaged) if entry.sub_agents_engaged else "None"}

## Artifacts Created

{chr(10).join(f"- `{artifact}`" for artifact in entry.artifacts_created) if entry.artifacts_created else "None"}

## Next Steps

{chr(10).join(f"- {step}" for step in entry.next_steps) if entry.next_steps else "To be determined"}

---

*Generated by Agent Orchestrator*
"""
        
        with open(filepath, 'w') as f:
            f.write(content)
        
        print(f"📝 Journal entry created: {filename}")
        
        return entry
    
    def complete_shard(self, shard_id: str) -> bool:
        """
        Mark a story shard as completed and move it to completed list.
        
        Args:
            shard_id: The shard to complete
        
        Returns:
            True if successful, False otherwise
        """
        # Find and remove from active
        shard = None
        for i, s in enumerate(self.active_shards["active_shards"]):
            if s["shard_id"] == shard_id:
                shard = self.active_shards["active_shards"].pop(i)
                break
        
        if not shard:
            print(f"❌ Shard {shard_id} not found in active shards")
            return False
        
        # Update status and move to completed
        shard["status"] = TaskStatus.COMPLETED.value
        shard["completed_at"] = datetime.now().isoformat()
        self.active_shards["completed_shards"].append(shard)
        
        # Update metrics
        self.active_shards["metrics"]["total_completed"] += 1
        
        self._save_active_shards()
        
        print(f"✅ Shard {shard_id} marked as COMPLETED")
        
        return True
    
    def _save_active_shards(self):
        """Save active shards to file"""
        shards_path = self.repo_path / ".agentic" / "manifests" / "active_story_shards.json"
        
        with open(shards_path, 'w') as f:
            json.dump(self.active_shards, f, indent=2)
    
    def get_status_report(self) -> Dict[str, Any]:
        """
        Generate a status report of the entire platform.
        
        Returns:
            Dictionary containing platform status
        """
        active_agents = [a for a in self.manifest['guru_agents'] if a['status'] == 'active']
        active_shards = self.active_shards["active_shards"]
        completed_shards = self.active_shards["completed_shards"]
        
        return {
            "platform": self.manifest['platform']['name'],
            "mode": self.mode.value,
            "guru_agents": {
                "total": len(self.manifest['guru_agents']),
                "active": len(active_agents),
                "planned": len([a for a in self.manifest['guru_agents'] if a['status'] == 'planned'])
            },
            "story_shards": {
                "active": len(active_shards),
                "completed": len(completed_shards),
                "total": len(active_shards) + len(completed_shards)
            },
            "last_updated": datetime.now().isoformat()
        }
    
    def print_status(self):
        """Print a formatted status report"""
        status = self.get_status_report()
        
        print("\n" + "="*60)
        print(f"🎭 {status['platform']} - Status Report")
        print("="*60)
        print(f"\n📊 Mode: {status['mode'].upper()}")
        print(f"\n🤖 Guru Agents:")
        print(f"   Total: {status['guru_agents']['total']}")
        print(f"   Active: {status['guru_agents']['active']}")
        print(f"   Planned: {status['guru_agents']['planned']}")
        print(f"\n📋 Story Shards:")
        print(f"   Active: {status['story_shards']['active']}")
        print(f"   Completed: {status['story_shards']['completed']}")
        print(f"   Total: {status['story_shards']['total']}")
        print(f"\n⏰ Last Updated: {status['last_updated']}")
        print("="*60 + "\n")


# Example usage and testing
if __name__ == "__main__":
    # Initialize orchestrator
    orchestrator = AgentOrchestrator(repo_path=".", mode=OrchestratorMode.TESTING)
    
    # Print status
    orchestrator.print_status()
    
    # List active agents
    print("\n🤖 Active Guru Agents:")
    active_agents = orchestrator.list_guru_agents(status="active")
    for agent in active_agents:
        print(f"   - {agent['name']} ({agent['role']})")
    
    # Create a test journal entry
    print("\n📝 Creating test journal entry...")
    entry = orchestrator.create_journal_entry(
        task_id="SHARD-002-TEST-VALIDATION",
        guru_agent=AgentRole.SECURITY_SENTINEL,
        logic_summary="Completed comprehensive Pydantic validation testing. All 23 tests passed successfully.",
        sub_agents_engaged=["Vulnerability Scanner", "Compliance Auditor"],
        artifacts_created=["tests/test_schemas.py", "journal/2026-01-13-validation-tests-complete.md"],
        status=TaskStatus.COMPLETED
    )
    
    print("\n✅ Orchestrator test complete!")
