# GitHub Repository Setup Task List

**Repository Name**: `quickbooks-automation`  
**Description**: QuickBooks Order Exporter - Automated production scheduling and order management  
**Status**: Ready for Setup  
**Date**: 2025-10-07

---

## Phase 1: GitHub CLI Installation (Optional but Recommended)

- [ ] **Install GitHub CLI**
  ```cmd
  # Windows (using winget)
  winget install --id GitHub.cli
  
  # Or download from: https://cli.github.com/
  ```

- [ ] **Verify Installation**
  ```cmd
  gh --version
  ```

- [ ] **Authenticate with GitHub**
  ```cmd
  gh auth login
  ```
  - Select: GitHub.com
  - Select: HTTPS
  - Authenticate via web browser

---

## Phase 2: Local Git Repository Setup

- [ ] **Initialize Git Repository** (if not already done)
  ```cmd
  git init
  ```

- [ ] **Verify .gitignore is Present**
  - Check `.gitignore` exists
  - Verify it excludes:
    - `.env` (sensitive credentials)
    - `venv/` (virtual environment)
    - `__pycache__/` (Python cache)
    - `logs/` (log files)
    - `output/` (generated reports)
    - `*.pyc` (compiled Python)

- [ ] **Stage All Files**
  ```cmd
  git add .
  ```

- [ ] **Review Staged Files**
  ```cmd
  git status
  ```
  - Verify `.env` is NOT staged
  - Verify sensitive data is excluded

- [ ] **Create Initial Commit**
  ```cmd
  git commit -m "Initial commit: QuickBooks Order Exporter with full configuration

  - Add core Python modules (connector, calculator, exporter)
  - Add Kiro AI configuration with 40+ steering rules
  - Add VS Code, GitHub Actions, and MCP configurations
  - Add comprehensive documentation and setup guides
  - Add production line and warehouse management rules"
  ```

---

## Phase 3: Create GitHub Repository

### Option A: Using GitHub CLI (Recommended)

- [ ] **Create Repository with GitHub CLI**
  ```cmd
  gh repo create quickbooks-automation --public --description "QuickBooks Order Exporter - Automated production scheduling and order management" --source=. --remote=origin
  ```

- [ ] **Push to GitHub**
  ```cmd
  git push -u origin main
  ```

### Option B: Using GitHub Web Interface

- [ ] **Navigate to GitHub**
  - Go to: https://github.com/new

- [ ] **Configure Repository**
  - **Repository name**: `quickbooks-automation`
  - **Description**: `QuickBooks Order Exporter - Automated production scheduling and order management`
  - **Visibility**: ☑️ Public (or Private if preferred)
  - **DO NOT check**:
    - ❌ Add a README file
    - ❌ Add .gitignore
    - ❌ Choose a license
  - Click **"Create repository"**

- [ ] **Connect Local Repository to GitHub**
  ```cmd
  # Add remote (replace YOUR_USERNAME with your GitHub username)
  git remote add origin https://github.com/YOUR_USERNAME/quickbooks-automation.git
  
  # Verify remote
  git remote -v
  
  # Set main branch
  git branch -M main
  
  # Push to GitHub
  git push -u origin main
  ```

---

## Phase 4: GitHub Repository Configuration

- [ ] **Add Repository Topics**
  - Go to repository page
  - Click ⚙️ (gear icon) next to "About"
  - Add topics:
    - `quickbooks`
    - `odoo`
    - `production-scheduling`
    - `python`
    - `automation`
    - `erp`
    - `manufacturing`
    - `mps`
    - `excel-export`
  - Click "Save changes"

- [ ] **Update Repository Description**
  - Verify description is set:
    > QuickBooks Order Exporter - Automated production scheduling and order management with Odoo ERP integration

- [ ] **Add Repository Website** (optional)
  - Add documentation link if you have one

---

## Phase 5: GitHub Actions Configuration

- [ ] **Enable GitHub Actions**
  - Go to: Settings → Actions → General
  - Under "Actions permissions":
    - Select: ☑️ "Allow all actions and reusable workflows"
  - Click "Save"

- [ ] **Verify Workflow Files**
  - Check `.github/workflows/ci.yml` exists
  - Check `.github/workflows/roo_rules.yml` exists

- [ ] **Trigger First Workflow Run**
  ```cmd
  # Make a small change to trigger CI
  git commit --allow-empty -m "ci: trigger initial workflow run"
  git push
  ```

- [ ] **Monitor Workflow Execution**
  - Go to: Actions tab
  - Verify workflows run successfully
  - Fix any failures

---

## Phase 6: Branch Protection (Optional but Recommended)

- [ ] **Configure Branch Protection Rules**
  - Go to: Settings → Branches
  - Click "Add branch protection rule"
  - Branch name pattern: `main`
  - Enable:
    - ☑️ Require a pull request before merging
    - ☑️ Require status checks to pass before merging
    - ☑️ Require branches to be up to date before merging
    - ☑️ Include administrators (optional)
  - Click "Create"

---

## Phase 7: Repository Secrets (If Needed)

- [ ] **Add GitHub Secrets** (only if CI needs them)
  - Go to: Settings → Secrets and variables → Actions
  - Click "New repository secret"
  - Add secrets if needed:
    - `ODOO_URL` (if running integration tests)
    - `ODOO_DATABASE`
    - `ODOO_USERNAME`
    - `ODOO_PASSWORD`
  - **Note**: Only add if absolutely necessary for CI/CD

---

## Phase 8: Documentation Updates

- [ ] **Update README.md with Repository Link**
  - Add GitHub repository badge
  - Add link to Issues page
  - Add link to Actions page

- [ ] **Create GitHub Issues for Known Tasks**
  - Review `tasks/tasks.md` if it exists
  - Create GitHub issues for major tasks
  - Label appropriately (enhancement, bug, documentation)

- [ ] **Add CONTRIBUTING.md** (optional)
  - Create contribution guidelines
  - Reference code style from `.kiro/steering/code style.md`
  - Reference commit message format from `.kiro/steering/commit message.md`

---

## Phase 9: Collaboration Setup

- [ ] **Add Collaborators** (if team project)
  - Go to: Settings → Collaborators
  - Click "Add people"
  - Add team members with appropriate permissions

- [ ] **Configure Notifications**
  - Go to: Watch → Custom
  - Select notification preferences:
    - ☑️ Issues
    - ☑️ Pull requests
    - ☑️ Releases

---

## Phase 10: Verification & Testing

- [ ] **Clone Repository Fresh**
  ```cmd
  # In a different directory
  cd ..
  git clone https://github.com/YOUR_USERNAME/quickbooks-automation.git test-clone
  cd test-clone
  ```

- [ ] **Verify Setup Works from Clone**
  ```cmd
  # Create virtual environment
  python -m venv venv
  venv\Scripts\activate
  
  # Install dependencies
  pip install -r requirements.txt
  
  # Run tests
  pytest tests/ -v
  ```

- [ ] **Verify GitHub Actions Badge**
  - Check if CI badge appears in README
  - Verify badge shows correct status

- [ ] **Test Issue Creation**
  - Create a test issue
  - Verify labels work
  - Close test issue

---

## Phase 11: Post-Setup Tasks

- [ ] **Create First Release** (optional)
  ```cmd
  # Tag current version
  git tag -a v0.0.1 -m "Initial release: QuickBooks Order Exporter"
  git push origin v0.0.1
  ```

- [ ] **Create Release on GitHub**
  - Go to: Releases → Create a new release
  - Tag: `v0.0.1`
  - Title: `v0.0.1 - Initial Release`
  - Description: Summarize features and setup

- [ ] **Update Project Board** (optional)
  - Go to: Projects → New project
  - Create Kanban board for task tracking
  - Add columns: To Do, In Progress, Done

- [ ] **Star Your Repository** ⭐
  - Click the Star button (for easy access)

---

## Troubleshooting

### Issue: Git push fails with authentication error

**Solution**:
```cmd
# Use GitHub CLI to authenticate
gh auth login

# Or configure Git credential helper
git config --global credential.helper wincred
```

### Issue: GitHub Actions workflow fails

**Solution**:
1. Check workflow logs in Actions tab
2. Verify Python version matches `.python-version`
3. Ensure all dependencies in `requirements.txt`
4. Check for syntax errors in workflow YAML

### Issue: .env file accidentally committed

**Solution**:
```cmd
# Remove from Git history
git rm --cached .env
git commit -m "Remove .env from repository"
git push

# Rotate all credentials in .env immediately
```

### Issue: Large files causing push to fail

**Solution**:
```cmd
# Check file sizes
git ls-files -z | xargs -0 du -h | sort -h

# Use Git LFS for large files if needed
git lfs install
git lfs track "*.xlsx"
git add .gitattributes
```

---

## Completion Checklist

- [ ] Repository created on GitHub
- [ ] Local repository connected to remote
- [ ] Initial commit pushed successfully
- [ ] GitHub Actions enabled and running
- [ ] Repository topics and description set
- [ ] .gitignore working correctly (no .env in repo)
- [ ] Documentation updated with repo links
- [ ] Team members added (if applicable)
- [ ] First workflow run successful

---

**Estimated Time**: 20-30 minutes  
**Difficulty**: Beginner to Intermediate  
**Prerequisites**: Git installed, GitHub account, GitHub CLI (optional)

**Status**: ⏳ Not Started

---

## Quick Reference Commands

```cmd
# Check repository status
git status

# View remote configuration
git remote -v

# View commit history
git log --oneline

# Check GitHub CLI authentication
gh auth status

# View repository on GitHub
gh repo view --web

# Create new branch
git checkout -b feature/new-feature

# Push new branch
git push -u origin feature/new-feature
```

---

**Last Updated**: 2025-10-07  
**Maintainer**: Development Team  
**Version**: 1.0
