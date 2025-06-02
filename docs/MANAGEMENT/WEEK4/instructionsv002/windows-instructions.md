t# Windows CLD6000 Transition Guide

## Prerequisites
1. Windows 10/11
2. Python 3.9+ installed
3. File access to CLD6000 folder

## Setup Steps

1. Open Command Prompt as Administrator:
```cmd
Win + X > Windows PowerShell (Admin)
```

2. Navigate to your project folder:
```cmd
cd "D:\FALL\CLD6000"
```

3. Create and activate Python environment:
```cmd
python -m venv venv
venv\Scripts\activate
```

4. Save the transition script:
- Create `transition.py`
- Copy script contents into it

5. Run the script:
```cmd
python transition.py
```

## What The Script Will Do

1. Analyze current structure:
- `.obsidian/`
- `course/`
- `data/`
- `deliverables/`
- `media/`
- `management/`
- `research/`

2. Create backup with timestamp

3. Create new structure:
- `00-project-hub/`
- `01-research/`
- `02-development/`
- `03-documentation/`
- `04-deliverables/`
- `05-data/`
- `06-management/`

4. Generate transition plan

5. Execute transition after confirmation

## Safety Features

1. Automatic backup creation
2. Dry run mode first
3. Detailed logging
4. Rollback capability

## If Something Goes Wrong

1. Stop the script (Ctrl+C)

2. Restore from backup:
```cmd
xcopy /E /I /H CLD6000_backup_[timestamp] CLD6000
```

3. Check logs:
```cmd
type transition_log.txt
```

## Verification Steps

After transition:

1. Check obsidian links still work
2. Verify all files are present
3. Test opening key documents
4. Verify folder permissions

## Maintenance

Keep the backup for at least one week while:
1. Testing new structure
2. Verifying all files
3. Updating any needed paths

Need help with any specific step?