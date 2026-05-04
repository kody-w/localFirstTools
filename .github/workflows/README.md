# 🤖 GitHub Actions Workflows

Automated workflows for building, testing, and releasing the Local First Tools Chrome Extension.

## 📋 Available Workflows

### 1. **Build Extension** (`build-extension.yml`)

**Triggers:**
- Push to `main` branch (when apps, data, or extension files change)
- Manual workflow dispatch

**What it does:**
1. ✅ Runs meta-analysis on all apps
2. 🏗️ Builds the Chrome extension
3. 📦 Creates ZIP package
4. 📊 Generates build report
5. 💾 Commits built files back to repo
6. 📤 Uploads artifacts for download

**How to trigger manually:**
```bash
# Via GitHub UI
1. Go to Actions tab
2. Select "Build Chrome Extension"
3. Click "Run workflow"

# Via GitHub CLI
gh workflow run build-extension.yml
```

**Create a release:**
Add `[release]` to your commit message:
```bash
git commit -m "feat: add new app [release]"
```

---

### 2. **Release Extension** (`release-extension.yml`)

**Triggers:**
- Push tag matching `v*.*.*` (e.g., `v1.0.0`)
- Manual workflow dispatch with version input

**What it does:**
1. 📝 Updates version in manifest.json
2. 🏗️ Builds extension with new version
3. 📦 Creates versioned ZIP file
4. 📝 Generates comprehensive release notes
5. 🎉 Creates GitHub Release with assets
6. 💾 Commits version updates

**How to create a release:**

**Option A: Using Git Tags**
```bash
# Create and push a version tag
git tag v1.0.0
git push origin v1.0.0

# The workflow will automatically:
# - Build the extension
# - Create a GitHub Release
# - Attach the ZIP file
```

**Option B: Manual Workflow**
```bash
# Via GitHub UI
1. Go to Actions tab
2. Select "Release Chrome Extension"
3. Click "Run workflow"
4. Enter version number (e.g., 1.0.0)

# Via GitHub CLI
gh workflow run release-extension.yml -f version=1.0.0
```

**Release Assets:**
- `local-first-tools-extension-v1.0.0.zip` (versioned)
- `local-first-tools-extension.zip` (latest)
- `meta-analysis.json` (ecosystem data)

---

### 3. **Scheduled Build** (`scheduled-build.yml`)

**Triggers:**
- Every Monday at 9 AM UTC (automatic)
- Manual workflow dispatch

**What it does:**
1. 📊 Runs weekly meta-analysis
2. 🧪 Runs automated tests
3. 🏗️ Builds extension
4. 📈 Generates health report
5. 💾 Updates meta-analysis data

**Tests included:**
- ✅ Config file validation (valid JSON)
- ✅ No duplicate app IDs
- ✅ Critical files exist
- ✅ Extension builds successfully

**How to trigger manually:**
```bash
# Via GitHub UI
1. Go to Actions tab
2. Select "Scheduled Extension Build"
3. Click "Run workflow"

# Via GitHub CLI
gh workflow run scheduled-build.yml
```

**Health Report includes:**
- App count and distribution
- Build size and status
- Category statistics
- Technology adoption
- Recommendations for new apps

---

## 🎯 Common Use Cases

### Use Case 1: Regular Development

**Scenario:** You added a new app and want to rebuild the extension

```bash
# Just commit and push - automatic build will trigger
git add apps/your-new-app.html
git commit -m "feat: add awesome new app"
git push
```

The workflow will:
1. Detect changes in `apps/`
2. Rebuild extension automatically
3. Commit updated ZIP to repo
4. Make it available for download

---

### Use Case 2: Creating a Release

**Scenario:** You want to publish version 1.2.0

```bash
# Method 1: Using tags (recommended)
git tag -a v1.2.0 -m "Release version 1.2.0"
git push origin v1.2.0

# Method 2: Manual workflow
gh workflow run release-extension.yml -f version=1.2.0
```

The workflow will:
1. Update manifest version to 1.2.0
2. Build extension
3. Create GitHub Release
4. Attach ZIP files and analysis
5. Generate comprehensive release notes

---

### Use Case 3: Manual Build

**Scenario:** You want to test a build without committing

```bash
# Trigger build workflow manually
gh workflow run build-extension.yml

# Download the artifact
gh run download  # Gets latest run artifacts
```

---

### Use Case 4: Weekly Health Check

**Scenario:** Monitor ecosystem health

The scheduled workflow runs **every Monday** automatically and:
- Analyzes all apps
- Runs validation tests
- Generates health report
- Updates meta-analysis

**View reports:**
```bash
# List recent workflow runs
gh run list --workflow=scheduled-build.yml

# Download latest health report
gh run download <run-id>
```

---

## 📦 Workflow Artifacts

Each workflow produces downloadable artifacts:

### Build Extension
- `local-first-tools-extension.zip` - Latest extension package
- `build-report.md` - Build statistics and details

### Release Extension
- GitHub Release with attached files
- Release notes with full changelog

### Scheduled Build
- `weekly-health-report-*.md` - Ecosystem health metrics
- Stored for 90 days

**Download artifacts:**
```bash
# Via GitHub UI
1. Go to Actions tab
2. Click on a workflow run
3. Scroll to "Artifacts" section
4. Click to download

# Via GitHub CLI
gh run list
gh run download <run-id>
```

---

## 🔧 Workflow Configuration

### Modify Triggers

**Build on different branches:**
```yaml
on:
  push:
    branches:
      - main
      - develop  # Add more branches
```

**Change schedule:**
```yaml
schedule:
  - cron: '0 9 * * 1'  # Monday at 9 AM
  - cron: '0 0 * * 0'  # Sunday at midnight
```

### Environment Variables

Add secrets in GitHub Settings → Secrets and variables → Actions:

```yaml
env:
  MY_SECRET: ${{ secrets.MY_SECRET }}
```

---

## 🐛 Troubleshooting

### Workflow Failed - Permission Denied

**Solution:** Enable workflow permissions
```
Repository Settings → Actions → General → Workflow permissions
→ Select "Read and write permissions"
```

### Workflow Not Triggering Automatically

**Solution:** Check trigger paths
```yaml
paths:
  - 'apps/**'      # Only triggers on app changes
  - 'data/**'      # Add more paths as needed
```

### Build Artifacts Missing

**Solution:** Check retention settings
```yaml
retention-days: 90  # Keep artifacts for 90 days
```

---

## 📊 Monitoring

### View Workflow Status

**Badge for README:**
```markdown
![Build Status](https://github.com/YOUR_USERNAME/localFirstTools/workflows/Build%20Chrome%20Extension/badge.svg)
```

**Check workflow runs:**
```bash
# List all runs
gh run list

# View specific workflow
gh run list --workflow=build-extension.yml

# Watch a run in progress
gh run watch
```

---

## 🚀 Advanced Usage

### Parallel Builds

Run multiple workflows simultaneously:
```bash
gh workflow run build-extension.yml &
gh workflow run scheduled-build.yml &
wait
```

### Conditional Releases

Only create release if tests pass:
```yaml
- name: Create Release
  if: success()  # Only if previous steps succeeded
```

### Notifications

Add Slack/Discord notifications:
```yaml
- name: Notify on Success
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

---

## 📝 Best Practices

1. **Semantic Versioning:** Use `v1.0.0`, `v1.0.1`, etc.
2. **Descriptive Commits:** Include context in commit messages
3. **Test Before Release:** Use manual builds to test first
4. **Monitor Scheduled Runs:** Check weekly reports
5. **Keep Artifacts:** Don't reduce retention below 30 days

---

## 🔗 Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [GitHub CLI](https://cli.github.com/)

---

**🤖 All workflows are fully automated and maintained by Claude Code!**
