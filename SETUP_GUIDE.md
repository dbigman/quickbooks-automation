# Configuration Package Setup Guide

## Quick Setup (5 Minutes)

### Prerequisites
- QuickBooks Order Exporter code package already extracted
- Git repository initialized
- Python 3.8+ installed

### Step 1: Extract Configuration Package

```bash
# In your repository root
unzip quickbooks_config_YYYYMMDD_HHMMSS.zip
```

### Step 2: Move Configuration Files

```bash
# Windows PowerShell
Move-Item quickbooks_config_*\* . -Force
Move-Item quickbooks_config_*\.* . -Force 2>$null
Remove-Item quickbooks_config_* -Recurse

# macOS/Linux
mv quickbooks_config_*/* .
mv quickbooks_config_*/.[!.]* . 2>/dev/null || true
rm -rf quickbooks_config_*
```

### Step 3: Verify Structure

Your repository should now have:
```
.
├── .kiro/              ✅ AI assistant config
├── .vscode/            ✅ VS Code settings
├── .github/            ✅ GitHub Actions
├── .roo/               ✅ Roo AI config
├── .codex/             ✅ Codex config
├── .spec-workflow/     ✅ Spec workflow
├── quickbooks/         ✅ Main package (from code package)
├── .cursorrules        ✅ Cursor AI rules
├── .gitignore          ✅ Git ignore
├── .python-version     ✅ Python version
├── .env.example        ✅ Environment template
└── pyproject.toml      ✅ Project config
```

### Step 4: Configure Environment

```bash
# Create .env from template
cp .env.example .env

# Edit with your credentials
# Windows: notepad .env
# macOS/Linux: nano .env
```

### Step 5: Install MCP Dependencies (Optional)

For AI assistant features:

```bash
# Install uv package manager
# macOS/Linux:
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows:
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Step 6: Test Configuration

```bash
# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run tests
pytest tests/

# Check linting
flake8 quickbooks/

# Check formatting
black --check quickbooks/
```

### Step 7: Commit Configuration

```bash
git add .
git commit -m "Add development environment configuration"
git push origin main
```

## Detailed Configuration

### Kiro AI Assistant

**Enable Hooks**:
1. Open Kiro settings
2. Navigate to "Agent Hooks"
3. Enable desired hooks:
   - ✅ Python Code Review (on save)
   - ✅ Auto Documentation (on demand)
   - ✅ QuickBooks qbXML Validator (on save)

**Configure MCP Servers**:
1. Open `.kiro/settings/mcp.json`
2. Verify server configurations
3. Restart Kiro to load servers

### VS Code

**Install Recommended Extensions**:
- Python (Microsoft)
- Pylance
- Black Formatter
- Flake8
- GitLens

**Verify Settings**:
1. Open VS Code settings (Ctrl+,)
2. Check Python interpreter is set to `./venv/bin/python`
3. Verify formatting on save is enabled

### GitHub Actions

**Enable Workflows**:
1. Go to repository Settings > Actions
2. Enable "Allow all actions"
3. Push code to trigger workflows

**Configure Secrets** (if needed):
1. Go to Settings > Secrets and variables > Actions
2. Add any required secrets (e.g., API keys)

### Roo AI

**Setup**:
1. Install Roo AI extension/CLI
2. Verify `.roo/mcp.json` is loaded
3. Test with: `roo validate`

## Customization Guide

### Add New Steering Rule

```bash
# Create new rule file
touch .kiro/steering/my-custom-rule.md

# Edit with your guidelines
# File will be automatically loaded by Kiro
```

### Modify Code Style

Edit `.kiro/steering/code style.md`:
```markdown
# Code Style

## Line Length
- Maximum: 80 characters (change to your preference)

## Formatting
- Tool: Black (or change to autopep8, yapf, etc.)
```

### Add GitHub Action

Create `.github/workflows/my-workflow.yml`:
```yaml
name: My Custom Workflow
on: [push, pull_request]
jobs:
  my-job:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run my script
        run: python my_script.py
```

### Configure New MCP Server

Edit `.kiro/settings/mcp.json`:
```json
{
  "mcpServers": {
    "my-server": {
      "command": "uvx",
      "args": ["my-mcp-server@latest"],
      "disabled": false,
      "autoApprove": ["tool1", "tool2"]
    }
  }
}
```

## Troubleshooting

### Issue: Kiro hooks not working

**Solution**:
1. Check file permissions: `chmod +x .kiro/hooks/*`
2. Verify hook JSON syntax is valid
3. Restart Kiro IDE
4. Check Kiro logs for errors

### Issue: MCP servers failing

**Solution**:
1. Verify `uv` is installed: `uv --version`
2. Check server logs in Kiro MCP panel
3. Try manual server start: `uvx server-name@latest`
4. Verify network connectivity

### Issue: GitHub Actions failing

**Solution**:
1. Check workflow syntax: Use GitHub's workflow validator
2. Verify Python version matches `.python-version`
3. Check all dependencies are in `requirements.txt`
4. Review action logs in GitHub UI

### Issue: VS Code not using correct Python

**Solution**:
1. Open Command Palette (Ctrl+Shift+P)
2. Select "Python: Select Interpreter"
3. Choose `./venv/bin/python`
4. Reload VS Code window

## Advanced Configuration

### Pre-commit Hooks

Install pre-commit framework:
```bash
pip install pre-commit
pre-commit install
```

Create `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.0.0
    hooks:
      - id: black
  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
```

### Docker Configuration

Create `Dockerfile`:
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "export_orders.py"]
```

### CI/CD Enhancements

Add deployment workflow `.github/workflows/deploy.yml`:
```yaml
name: Deploy
on:
  push:
    tags:
      - 'v*'
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build and deploy
        run: |
          python setup.py sdist bdist_wheel
          # Add deployment steps
```

## Maintenance

### Update Steering Rules

```bash
# Pull latest rules from team repository
git pull origin main .kiro/steering/

# Or update individual files
curl -o .kiro/steering/code style.md https://your-repo/code-style.md
```

### Update MCP Servers

```bash
# Update all servers
uvx --upgrade server-name@latest

# Or update specific server
uvx --upgrade odoo-mcp@latest
```

### Update GitHub Actions

```bash
# Check for action updates
# Visit: https://github.com/actions/

# Update action versions in workflow files
# Example: actions/checkout@v3 -> actions/checkout@v4
```

## Best Practices

1. **Version Control**: Commit all configuration changes
2. **Documentation**: Update README when adding new configs
3. **Team Sync**: Share configuration updates with team
4. **Testing**: Test configuration changes before committing
5. **Backup**: Keep backup of working configurations

## Resources

- **Kiro Documentation**: https://kiro.ai/docs
- **MCP Protocol**: https://modelcontextprotocol.io
- **GitHub Actions**: https://docs.github.com/actions
- **VS Code Python**: https://code.visualstudio.com/docs/python

---

**Setup Time**: ~5 minutes  
**Difficulty**: Easy  
**Status**: Production Ready ✅
