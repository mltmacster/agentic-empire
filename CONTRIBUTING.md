# Contributing to Sovereign Forge

Welcome to the Sovereign Forge contributor guide. Whether you're a human developer or an AI agent, this document will help you understand how to contribute effectively to the ecosystem.

## The Philosophy: BMAD

All contributions to Sovereign Forge follow the **Breakthrough Method of Agile AI-Driven Development (BMAD)**. This means:

1. **Spec-Driven Development:** Never write code without a validated spec
2. **No Content Left Behind:** All actions must be journaled
3. **Git-as-Memory:** The repository is the source of truth
4. **Pydantic Validation:** All data must conform to schemas

## How to Contribute

### For Human Developers

1. **Fork the Repository**
   ```bash
   gh repo fork d3vgurus/agentic-empire
   ```

2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Follow the BMAD Process**
   - Create or update a Story Shard in `story-files/`
   - Implement your changes
   - Create a journal entry in `journal/` documenting your work
   - Ensure all Pydantic schemas are followed

4. **Run Quality Checks**
   ```bash
   # Format code
   black .
   
   # Lint code
   ruff check .
   
   # Run tests
   pytest
   
   # Validate schemas
   python schemas.py
   ```

5. **Submit a Pull Request**
   - Reference the Story Shard ID in your PR title
   - Include a detailed description of changes
   - Ensure all CI/CD checks pass

### For AI Agents

If you are an AI agent contributing to this ecosystem:

1. **Authenticate via MCP**
   - Consult `mcp_config.json` for your permissions
   - Verify you have the required access level

2. **Follow the Git-Loop Protocol**
   - PULL: Read latest journal entries and specs
   - PROCESS: Execute your specialized function
   - JOURNAL: Create an `AgenticJournalEntry`
   - PUSH: Commit your work with proper metadata

3. **Use Pydantic Models**
   - All data exchanges must use validated schemas
   - Use `SecretStr` for sensitive information
   - Validate before committing

4. **Coordinate with Other Agents**
   - Check `active_story_shards.json` for dependencies
   - Update the manifest when starting/completing tasks
   - Reference parent context IDs for traceability

## Code Standards

### Python

- **Formatter:** Black (line length: 88)
- **Linter:** Ruff
- **Type Hints:** Required for all functions
- **Docstrings:** Google style
- **Testing:** Pytest with >80% coverage

### Commit Messages

Follow the Conventional Commits specification:

```
feat: add new sub-agent for database optimization
fix: correct Pydantic validation in SecurityAuditReport
docs: update README with deployment instructions
test: add unit tests for Code Generation Maestro
```

### Journal Entries

All journal entries must include YAML front-matter:

```yaml
---
task_id: "SHARD-001-INIT"
status: "completed"
owner_agent: "Architectural Sovereign"
contributing_agents: ["Pattern Matcher", "Constraint Validator"]
last_sync: "2026-01-13T00:00:00Z"
parent_context_id: "git-commit-63ab8f8"
---
```

## Security Guidelines

1. **Never commit secrets** - Use `SecretStr` in Pydantic models
2. **Validate all inputs** - Use Pydantic schemas for type safety
3. **Follow least privilege** - Agents should only access what they need
4. **Audit everything** - All actions must be logged

## Getting Help

- **Documentation:** Check the `docs/` directory
- **Issues:** Open a GitHub issue with the `question` label
- **Discussions:** Use GitHub Discussions for broader topics
- **Agent Support:** Consult the Project Coordinator agent

## Recognition

Contributors who follow the BMAD philosophy and deliver high-quality work will be recognized in our Hall of Fame. Real recognize real.

---

*Keep your head on a swivel and let's secure the bag together.*
