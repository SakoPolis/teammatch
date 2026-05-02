# Database Population Script

A Python script to automatically populate your TeamMatch database with realistic test data.

## Usage

### Basic Usage

From the `backend` directory, run:

```bash
python scripts/populate_db.py
```

This will:
- Create all necessary tables (if they don't exist)
- Populate with default test data:
  - 3 courses
  - 36 students (12 per course)
  - 9 teams (3-4 per course)
  - 9 projects (1 per team)
  - ~45 milestones
  - 3 match runs
  - ~180 check-ins (5 per student)
  - ~180 contributions (1 per student per week)

### Clear Database First

To start fresh and remove all existing data:

```bash
python scripts/populate_db.py --clear
```

### Customize Data Size

```bash
# Create 2 courses with 8 students each and 3 check-ins per student
python scripts/populate_db.py --courses 2 --students-per-course 8 --checkins-per-student 3

# Create 5 courses with 20 students each
python scripts/populate_db.py --courses 5 --students-per-course 20
```

### Reproducible Data

For consistent test data across runs, use a seed:

```bash
python scripts/populate_db.py --seed 42
```

This ensures the same random data is generated each time, useful for debugging and comparing results.

## Features

The script generates:

- **Courses**: Instructor-managed courses with team codes
- **Students**: With realistic names, emails, and survey responses:
  - Skills (randomly selected from: Python, JavaScript, React, Data Analysis, UI Design, DevOps, etc.)
  - Experience levels (Beginner, Intermediate, Advanced)
  - Availability preferences
  - Leadership preferences
  - Role preferences
  
- **Teams**: Assigned to courses with:
  - Team codes
  - Skill balance scores
  - Schedule overlap scores
  - Experience balance scores
  - Overall team scores
  
- **Projects & Milestones**: Associated with teams
  - Realistic project names
  - Deadline dates
  - Multiple milestones per project
  
- **Match Runs**: Records of team matching executions
  
- **Check-ins**: Weekly student progress updates with:
  - Hours worked
  - Tasks planned and completed
  - Completion status (On Track / Behind / Blocked)
  - Contribution types
  - Blockers and help requests
  
- **Contributions**: Scoring records for each student per week with:
  - Overall, hours, tasks, evidence, and consistency scores
  - Status tracking (ON_TRACK / WATCH / FLAG)

## Environment Setup

Before running, ensure your database connection is configured via the `.env` file:

```
DATABASE_URL=postgresql://user:password@localhost/teamatch_test
```

Or for SQLite (useful for testing):

```
DATABASE_URL=sqlite:///./test_db.sqlite
```

## Command Line Options

```
--clear                       Drop all tables and recreate from scratch
--seed SEED                   Use a random seed for reproducible data
--courses COUNT              Number of courses to create (default: 3)
--students-per-course COUNT  Students per course (default: 12)
--checkins-per-student COUNT Check-ins per student (default: 5)
```

## Example Workflows

**Complete Test Database Reset:**
```bash
python scripts/populate_db.py --clear --seed 42
```

**Large Dataset for Performance Testing:**
```bash
python scripts/populate_db.py --clear --courses 10 --students-per-course 50
```

**Minimal Dataset for Development:**
```bash
python scripts/populate_db.py --clear --courses 1 --students-per-course 4
```

## Notes

- Student emails are generated as: `firstname.lastname+COURSECODE@example.com`
- Timestamps are set relative to the current time for realistic testing
- Teams are automatically balanced with students from the same course
- All relationships and foreign keys are properly maintained
- The script is idempotent - running it multiple times without `--clear` adds more data
