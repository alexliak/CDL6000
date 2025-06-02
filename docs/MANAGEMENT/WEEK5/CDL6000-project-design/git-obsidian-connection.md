# Git-Obsidian Connection Setup

## Completed Git Setup ✓
```bash
# Git configurations done
git config --global credential.helper manager
git config --global credential.helper store
git config --global credential.https://github.com.username alexliak
```

## Git-Obsidian Integration

### 1. Obsidian Git Plugin Setup
1. Open Obsidian Settings
2. Go to Community Plugins
3. Browse for "Obsidian Git"
4. Install and Enable
5. Configure settings:
   ```
   Vault name: CDL6000-vault
   Backup folder: .obsidian/backups
   Commit message: vault backup: {{date}}
   ```

### 2. Git Credentials
- Using Git Credential Manager (already configured)
- Authenticated through GitHub
- Token stored securely

### 3. Path Configuration
```
Repository: https://github.com/yourusername/CDL6000.git
Local Path: D:\CDL6000-project
Vault Path: D:\CDL6000-project\docs\obsidian-vault
```

### 4. Automatic Backup Settings
Configure in Obsidian Git plugin:
```
Auto backup: enabled
Backup interval: 10 minutes
Backup folder: .obsidian/backups
```

### 5. Git Commands through Obsidian
- Ctrl/Cmd + P → "Git: View diff"
- Ctrl/Cmd + P → "Git: Commit all changes"
- Ctrl/Cmd + P → "Git: Push"
- Ctrl/Cmd + P → "Git: Pull"

## Verification Steps
1. Check Git status in Obsidian
2. Make test commit
3. Verify changes appear in GitHub
4. Test pull/push functionality

## Important Notes
- Always use Obsidian Git plugin for commits
- Keep automatic backup enabled
- Check GitHub connection regularly
- Use consistent commit messages
