# CDL6000 Project Setup Guide

## Initial Setup Requirements

### Project Structure Verification
1. Confirm root path is set to: `D:\CDL6000-project`
2. Verify vault path exists at: `D:\CDL6000-project\docs\obsidian-vault`
3. Ensure vault is named: `CDL6000-vault`

### Git Repository Setup
1. Verify repository naming:
   ```
   Repository name: CDL6000
   Project directory: CDL6000-project
   Branch: main
   ```

2. Configure Git files:
   ```bash
   # In .gitignore
   .obsidian/workspace.json
   .obsidian/workspace-mobile.json
   .DS_Store
   node_modules
   .env
   __pycache__/
   .vscode/

   # In .gitattributes
   .env filter=git-crypt
   .gitattributes !filter !diff
   ```

### Directory Structure Verification
Ensure the following structure exists:
```
CDL6000-project/
├── docs/
│   └── obsidian-vault/
│       ├── 00-overview/
│       ├── 01-specs/
│       ├── 02-design/
│       ├── 03-impl/
│       ├── 04-test/
│       ├── 05-deploy/
│       ├── 06-maintain/
│       ├── assets/
│       ├── meetings/
│       └── templates/
```

## Obsidian Configuration Steps

### 1. Core Plugins Setup
1. Open Obsidian Settings (Ctrl/Cmd + ,)
2. Navigate to "Core Plugins"
3. Enable the following plugins:
   - [ ] File explorer
   - [ ] Search
   - [ ] Tags pane
   - [ ] Page preview
   - [ ] Templates

### 2. Community Plugins Installation
1. Go to Settings → Community Plugins
2. Disable Safe Mode
3. Install and enable plugins in this order:
   1. Obsidian Git
   2. Dataview
   3. Calendar
   4. Advanced Tables
   5. Templates

### 3. Template Configuration
1. Go to Settings → Templates
2. Configure the following:
   - Set template folder location: `templates`
   - Configure template format
   - Set up hotkeys for template insertion

### 4. Git Integration Setup
1. Configure Obsidian Git plugin:
   ```
   Settings → Obsidian Git:
   - Backup interval: 10 minutes
   - Auto backup: Enabled
   - Commit message format: [timestamp] Auto backup
   ```

2. Test Git integration:
   - Make a test change
   - Verify automatic backup
   - Check commit history

### 5. Workspace Configuration
1. Set up default workspace layout:
   - Left sidebar: File explorer, Search
   - Right sidebar: Tags, Calendar
   - Main area: Editor/Preview split

2. Configure split views:
   - Enable linked views
   - Set up default split ratio

## Essential Files Setup

### 1. Create Index Files
Create index.md in each directory:
- [ ] 00-overview/index.md
- [ ] 01-specs/index.md
- [ ] 02-design/index.md
- [ ] 03-impl/index.md
- [ ] 04-test/index.md
- [ ] 05-deploy/index.md
- [ ] 06-maintain/index.md

### 2. Template Creation
Create the following templates in `templates` folder:
1. Meeting Notes Template:
   ```markdown
   # Meeting: {{date}}
   ## Attendees
   - 
   
   ## Agenda
   1. 
   
   ## Discussion
   - 
   
   ## Action Items
   - [ ] 
   ```

2. Documentation Template:
   ```markdown
   # {{title}}
   
   ## Overview
   
   ## Details
   
   ## Related
   ```

3. Design Document Template:
   ```markdown
   # Design: {{title}}
   
   ## Problem Statement
   
   ## Proposed Solution
   
   ## Implementation Details
   
   ## Considerations
   ```

### 3. Configuration Files
Verify presence and content of:
1. `.obsidian/app.json`
2. `.obsidian/appearance.json`
3. `.obsidian/core-plugins.json`
4. `.obsidian/hotkeys.json`

## Final Verification Checklist
- [ ] Project structure matches specification
- [ ] Git configuration is complete
- [ ] Core plugins are enabled and configured
- [ ] Community plugins are installed and working
- [ ] Templates are created and accessible
- [ ] Git integration is functioning
- [ ] Workspace layout is configured
- [ ] Index files are present in all directories
- [ ] All configuration files are present

## Maintenance Guidelines
1. Follow naming conventions strictly:
   - Use kebab-case for files
   - Prefix dates with YYYY-MM-DD
   - Use descriptive file names

2. Git practices:
   - Commit meaningful changes
   - Use clear commit messages
   - Regular pulls before making changes

3. Documentation practices:
   - Use templates for consistency
   - Maintain index files
   - Keep related files together
   - Use consistent tagging