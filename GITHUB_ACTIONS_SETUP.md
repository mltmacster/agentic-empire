# GitHub Actions Activation Guide

Your Sovereign Forge repository is live, but the GitHub Actions workflows need to be manually activated due to GitHub App permission restrictions. This guide will walk you through the process.

## Why This Is Needed

GitHub has security restrictions that prevent automated tools (like GitHub Apps) from creating or modifying workflow files without explicit permissions. This is a good security feature that protects your repository from unauthorized automation.

## Option 1: Enable Workflows via Web Interface (Recommended - 2 minutes)

### Step 1: Update Repository Permissions

1. Go to your repository settings:  
   **https://github.com/mltmacster/agentic-empire/settings/actions**

2. Scroll to **"Workflow permissions"**

3. Select these options:
   - ✅ **Read and write permissions**
   - ✅ **Allow GitHub Actions to create and approve pull requests**

4. Click **Save**

### Step 2: Create Workflow Files Manually

The workflow files are in your repository but need to be moved to the correct location. You can do this through GitHub's web interface:

1. Go to: **https://github.com/mltmacster/agentic-empire/tree/main/.github**

2. Click **"Add file"** → **"Create new file"**

3. Name it: `workflows/pydantic_validation.yml`

4. Copy the content from `.github/workflows/pydantic_validation.yml` in your local repository

5. Commit the file

6. Repeat for:
   - `workflows/auto_journaling.yml`
   - `workflows/code_quality.yml`

### Step 3: Verify Workflows Are Active

1. Go to the **Actions** tab:  
   **https://github.com/mltmacster/agentic-empire/actions**

2. You should see three workflows listed:
   - Pydantic Validation & Security Sentinel
   - Auto-Journaling System
   - Code Quality & Testing

3. Make a test commit to trigger them

## Option 2: Push from Local Machine (Advanced - 5 minutes)

If you have the repository cloned locally (not through Manus):

```bash
# Clone your repository
git clone https://github.com/mltmacster/agentic-empire.git
cd agentic-empire

# The workflow files should already be there
# If not, copy them from the archive

# Push with your personal credentials (not GitHub App)
git push origin main
```

## Option 3: Use GitHub CLI Directly (Fastest - 1 minute)

```bash
# Authenticate with your personal account
gh auth login

# Navigate to repository
cd /path/to/agentic-empire

# Force push the workflows
git push origin main --force
```

## Verification Checklist

After activation, verify these items:

- [ ] Workflows appear in the Actions tab
- [ ] Repository has "Read and write permissions" enabled
- [ ] A test commit triggers the workflows
- [ ] Workflow runs complete successfully (or show expected errors)

## Expected Workflow Behavior

### Pydantic Validation & Security Sentinel
- **Triggers:** On push and pull requests to main/develop
- **Actions:** Validates all Pydantic schemas, scans for secrets
- **Expected Result:** Should pass (all schemas are valid)

### Auto-Journaling System
- **Triggers:** On push to code/artifact files
- **Actions:** Creates automated journal entries
- **Expected Result:** Creates a new journal entry in `journal/` directory

### Code Quality & Testing
- **Triggers:** On push and pull requests
- **Actions:** Runs Black, Ruff, and Pytest
- **Expected Result:** May show warnings initially (no tests yet)

## Troubleshooting

### Workflows Don't Appear
- Ensure workflow files are in `.github/workflows/` directory
- Check that YAML syntax is valid
- Verify repository permissions are set correctly

### Workflows Fail to Run
- Check the Actions tab for error messages
- Verify Python 3.11 is specified in workflows
- Ensure `requirements.txt` is in the repository root

### Permission Errors
- Confirm "Read and write permissions" are enabled
- Check that the GITHUB_TOKEN has sufficient scope
- Try re-saving the workflow permissions

## What's Next

Once workflows are active, you're ready for **Phase 2: Validation & Testing**. The workflows will automatically:

1. Validate every commit against Pydantic schemas
2. Create journal entries for all code changes
3. Run quality checks on all Python code
4. Generate reports for security and compliance

---

**Status:** Workflows are configured and ready to activate  
**Repository:** https://github.com/mltmacster/agentic-empire  
**Next Phase:** Phase 2 - Validation & Testing

*Let's get these workflows running and move to Phase 2!*
