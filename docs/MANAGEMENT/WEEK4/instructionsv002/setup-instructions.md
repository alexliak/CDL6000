# Project Setup and Usage Instructions

## Initial Setup

1. First, ensure Python 3.9+ is installed
2. Install required packages:
```bash
pip install gitpython python-dotenv
```

3. Clone the repository structure:
```bash
python setup_project.py
```

## Time Tracking

Time tracking is mandatory and integrated into the system in multiple ways:

1. **Weekly Logs** (`weekly-logs/`)
   - Automatically created for each week
   - Contains structured sections for progress
   - Includes time tracking summaries

2. **Detailed Time Logs** (`time-tracking/`)
   - JSON-based detailed time records
   - Categorized by activity
   - Exportable for analysis

3. **Git Integration**
   - Commit messages include time spent
   - Weekly branches for progress tracking
   - Time summaries in pull requests

## Version Control Protocol

1. **Branch Structure**
```
main
├── weekly/week1
├── weekly/week2
└── features/[feature-name]
```

2. **Commit Message Format**
```
[category][time]: Brief description

- Detailed change 1
- Detailed change 2

Time: 2h research, 1h development
```

3. **Weekly Branch Protocol**
- Create new branch each week
- PR at end of week
- Include time summary in PR

## Gradable Evidence

Your work will be gradable through:

1. **Weekly Progress**
   - Detailed weekly logs
   - Commit history
   - Time tracking data

2. **Quality Metrics**
   - Code coverage reports
   - Documentation completeness
   - Implementation milestones

3. **Time Investment**
   - Category breakdowns
   - Weekly summaries
   - Effort distribution

## Day-to-Day Usage

1. Start your day:
```python
pm.create_daily_entry()
```

2. Log time:
```python
pm.log_time('research', 2.5, 'Literature review')
```

3. End your day:
```python
pm.generate_daily_summary()
```

## Evidence Generation

To generate evidence for grading:

1. Time summary:
```python
pm.generate_time_report()
```

2. Progress summary:
```python
pm.generate_progress_report()
```

3. Complete documentation:
```python
pm.generate_documentation()
```

Remember to commit your changes daily and maintain detailed logs for optimal grade achievement.