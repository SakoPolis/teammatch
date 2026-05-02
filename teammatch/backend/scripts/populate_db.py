"""
Database population script for testing purposes.
Populates the database with sample courses, students, teams, projects, and check-ins.

Usage:
    python scripts/populate_db.py --clear
    python scripts/populate_db.py --seed 42
"""

import sys
import os
from datetime import datetime, timedelta
import random
import argparse
import uuid as uuid_lib

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.core.database import engine, SessionLocal, Base
from app.models.course import Course
from app.models.student import Student
from app.models.team import Team
from app.models.project import Project, Milestone
from app.models.matchrun import MatchRun
from app.models.checkin import CheckIn
from app.models.contribution import Contribution
from app.models.notification import Notification


# Sample data
SKILLS = ["Python", "JavaScript", "React", "Data Analysis", "UI Design", "DevOps", "Backend", "Frontend", "Database", "Testing"]
EXPERIENCE_LEVELS = ["Beginner", "Intermediate", "Advanced"]
AVAILABILITY = ["Weekday Mornings", "Weekday Afternoons", "Weekday Evenings", "Weekends"]
LEADERSHIP_PREFERENCES = ["Yes", "No", "Open"]
ROLE_PREFERENCES = ["Frontend Developer", "Backend Developer", "Designer", "Project Manager", "DevOps", "Data Analyst"]
CONTRIBUTION_TYPES = ["Coding", "Research", "Design", "Documentation", "Testing", "Review"]
COMPLETION_STATUSES = ["On Track", "Behind", "Blocked"]

FIRST_NAMES = ["Alice", "Bob", "Charlie", "Diana", "Evan", "Fiona", "Grace", "Henry", "Iris", "Jack", "Kate", "Liam", "Maya", "Noah", "Olivia", "Peter"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Chen", "Kim", "Lee", "Patel", "Wilson"]

COURSE_NAMES = ["Web Development 101", "Data Science Fundamentals", "Mobile App Development", "Cloud Computing 101", "AI/ML Basics"]


def clear_database():
    """Drop all tables and recreate them."""
    print("Clearing database...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("✓ Database cleared and tables created")


def populate_courses(db: Session, count: int = 3) -> list[Course]:
    """Create sample courses."""
    print(f"\nCreating {count} courses...")
    courses = []
    for i in range(count):
        course = Course(
            name=COURSE_NAMES[i % len(COURSE_NAMES)],
            instructor_id=f"instructor_{i+1}",
            team_size=4,
            team_code=f"COURSE{i+1:03d}"
        )
        db.add(course)
        courses.append(course)
    db.commit()
    print(f"✓ Created {count} courses")
    return courses


def populate_students(db: Session, courses: list[Course], students_per_course: int = 12) -> list[Student]:
    """Create sample students."""
    print(f"\nCreating {len(courses) * students_per_course} students...")
    students = []
    for course in courses:
        for i in range(students_per_course):
            first_name = random.choice(FIRST_NAMES)
            last_name = random.choice(LAST_NAMES)
            student = Student(
                email=f"{first_name.lower()}.{last_name.lower()}+{course.team_code}+{i}+{uuid_lib.uuid4().hex[:8]}@example.com",
                name=f"{first_name} {last_name}",
                course_id=course.id,
                team_id=None,  # Will be assigned when teams are created
                skills=random.sample(SKILLS, random.randint(2, 5)),
                experience_level=random.choice(EXPERIENCE_LEVELS),
                availability=random.sample(AVAILABILITY, random.randint(1, 3)),
                leadership_preference=random.choice(LEADERSHIP_PREFERENCES),
                role_preference=random.choice(ROLE_PREFERENCES)
            )
            db.add(student)
            students.append(student)
    db.commit()
    print(f"✓ Created {len(students)} students")
    return students


def populate_teams(db: Session, courses: list[Course], students: list[Student], team_size: int = 4) -> list[Team]:
    """Create teams and assign students to them."""
    print(f"\nCreating teams...")
    teams = []
    
    for course in courses:
        # Get students in this course
        course_students = [s for s in students if s.course_id == course.id]
        
        # Create teams for this course
        num_teams = (len(course_students) + team_size - 1) // team_size
        
        for team_idx in range(num_teams):
            team = Team(
                course_id=course.id,
                name=f"Team {chr(65 + team_idx)}",  # Team A, B, C, ...
                team_code=f"{course.team_code}-T{team_idx+1:02d}",
                skill_balance_score=random.uniform(0.7, 1.0),
                schedule_overlap_score=random.uniform(0.6, 1.0),
                experience_balance_score=random.uniform(0.7, 1.0),
                overall_score=random.uniform(0.7, 0.95),
                explanation="Auto-generated team for testing"
            )
            db.add(team)
            teams.append(team)
        
        db.commit()
        
        # Assign students to teams
        random.shuffle(course_students)
        for student_idx, student in enumerate(course_students):
            team_idx = student_idx // team_size
            if team_idx < len(teams):
                student.team_id = teams[team_idx].id
        
        db.commit()
    
    print(f"✓ Created {len(teams)} teams")
    return teams


def populate_projects(db: Session, courses: list[Course], teams: list[Team]) -> list[Project]:
    """Create sample projects."""
    print(f"\nCreating projects...")
    projects = []
    
    project_names = [
        "E-Commerce Platform",
        "Data Analysis Dashboard",
        "Mobile Chat App",
        "Blog Platform",
        "Task Management System",
        "Real-time Collaboration Tool"
    ]
    
    for course in courses:
        course_teams = [t for t in teams if t.course_id == course.id]
        for team in course_teams:
            project = Project(
                course_id=course.id,
                team_id=team.id,
                name=random.choice(project_names),
                description="A project built by the team during the semester.",
                deadline=datetime.now(datetime.now().astimezone().tzinfo) + timedelta(days=random.randint(30, 120)),
                status="active"
            )
            db.add(project)
            projects.append(project)
    
    db.commit()
    print(f"✓ Created {len(projects)} projects")
    return projects


def populate_milestones(db: Session, projects: list[Project]) -> list[Milestone]:
    """Create sample milestones."""
    print(f"\nCreating milestones...")
    milestones = []
    
    milestone_titles = ["Requirements Review", "Design Phase", "MVP Development", "Testing & QA", "Final Delivery"]
    
    for project in projects:
        # Create 3-5 milestones per project
        for i, title in enumerate(random.sample(milestone_titles, random.randint(3, 5))):
            milestone = Milestone(
                project_id=project.id,
                title=title,
                description=f"{title} milestone for {project.name}",
                due_date=project.deadline - timedelta(days=(5 - i) * 20),
                completed=random.choice([True, False]) if i < 2 else False
            )
            db.add(milestone)
            milestones.append(milestone)
    
    db.commit()
    print(f"✓ Created {len(milestones)} milestones")
    return milestones


def populate_matchruns(db: Session, courses: list[Course]) -> list[MatchRun]:
    """Create sample match runs."""
    print(f"\nCreating match runs...")
    matchruns = []
    
    for course in courses:
        matchrun = MatchRun(
            course_id=course.id,
            status="COMPLETED",
            total_teams="4",
            started_at=datetime.now(datetime.now().astimezone().tzinfo) - timedelta(days=30),
            completed_at=datetime.now(datetime.now().astimezone().tzinfo) - timedelta(days=29)
        )
        db.add(matchrun)
        matchruns.append(matchrun)
    
    db.commit()
    print(f"✓ Created {len(matchruns)} match runs")
    return matchruns


def populate_checkins(db: Session, students: list[Student], teams: list[Team], courses: list[Course], count_per_student: int = 5):
    """Create sample check-ins."""
    print(f"\nCreating check-ins ({count_per_student} per student)...")
    checkins = []
    
    tasks_examples = [
        "Implement user authentication",
        "Design database schema",
        "Create UI mockups",
        "Write API endpoints",
        "Set up CI/CD pipeline"
    ]
    
    for student in students:
        team = next((t for t in teams if t.id == student.team_id), None)
        course = next((c for c in courses if c.id == student.course_id), None)
        
        if not team or not course:
            continue
            
        for week in range(1, count_per_student + 1):
            checkin = CheckIn(
                student_id=student.id,
                team_id=team.id,
                course_id=course.id,
                hours_worked=random.randint(5, 15),
                tasks_planned="\n".join(random.sample(tasks_examples, 2)),
                tasks_completed=random.choice(["2/2", "1/2", "2/3"]),
                what_i_worked_on=f"Worked on feature X and updated documentation for week {week}.",
                next_week_plan="Continue with next phase of development and conduct code reviews.",
                completion_status=random.choice(COMPLETION_STATUSES),
                contribution_type=random.choice(CONTRIBUTION_TYPES),
                confidence_level=random.randint(2, 5),
                blocked_by=None if random.random() > 0.2 else "Waiting for API response from backend team",
                needs_help=random.choice([True, False]),
                blockers="None" if random.random() > 0.3 else "Need clarification on requirements",
                evidence_url="https://github.com/example/repo/commit/abc123",
                peer_shoutout=random.choice([None, f"Thanks to {random.choice(FIRST_NAMES)} for the help!"]),
                week_number=week,
                is_edited=False,
                created_at=datetime.now(datetime.now().astimezone().tzinfo) - timedelta(weeks=count_per_student - week)
            )
            db.add(checkin)
            checkins.append(checkin)
    
    db.commit()
    print(f"✓ Created {len(checkins)} check-ins")
    return checkins


def populate_contributions(db: Session, students: list[Student], teams: list[Team], courses: list[Course]):
    """Create sample contributions."""
    print(f"\nCreating contributions...")
    contributions = []
    
    for student in students:
        team = next((t for t in teams if t.id == student.team_id), None)
        course = next((c for c in courses if c.id == student.course_id), None)
        
        if not team or not course:
            continue
        
        for week in range(1, 6):
            contribution = Contribution(
                student_id=student.id,
                team_id=team.id,
                course_id=course.id,
                overall_score=random.uniform(0.6, 1.0),
                hours_score=random.uniform(0.5, 1.0),
                tasks_score=random.uniform(0.5, 1.0),
                evidence_score=random.uniform(0.5, 1.0),
                consistency_score=random.uniform(0.5, 1.0),
                status=random.choice(["ON_TRACK", "WATCH", "FLAG"]),
                week_number=week,
                checkins_submitted=random.randint(1, 2),
                checkins_missed=random.randint(0, 1),
                last_checkin_date=datetime.now(datetime.now().astimezone().tzinfo) - timedelta(days=random.randint(1, 7))
            )
            db.add(contribution)
            contributions.append(contribution)
    
    db.commit()
    print(f"✓ Created {len(contributions)} contributions")
    return contributions


def main():
    parser = argparse.ArgumentParser(description="Populate database with test data")
    parser.add_argument("--clear", action="store_true", help="Clear all data before populating")
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")
    parser.add_argument("--courses", type=int, default=3, help="Number of courses to create")
    parser.add_argument("--students-per-course", type=int, default=12, help="Number of students per course")
    parser.add_argument("--checkins-per-student", type=int, default=5, help="Number of check-ins per student")
    
    args = parser.parse_args()
    
    if args.seed is not None:
        random.seed(args.seed)
        print(f"Using random seed: {args.seed}")
    
    db = SessionLocal()
    
    try:
        if args.clear:
            clear_database()
        else:
            # Just ensure tables exist
            Base.metadata.create_all(bind=engine)
            print("✓ Tables verified/created")
        
        # Populate in order
        courses = populate_courses(db, args.courses)
        students = populate_students(db, courses, args.students_per_course)
        teams = populate_teams(db, courses, students)
        projects = populate_projects(db, courses, teams)
        milestones = populate_milestones(db, projects)
        matchruns = populate_matchruns(db, courses)
        checkins = populate_checkins(db, students, teams, courses, args.checkins_per_student)
        contributions = populate_contributions(db, students, teams, courses)
        
        print("\n" + "="*50)
        print("✓ Database population completed successfully!")
        print("="*50)
        print(f"Summary:")
        print(f"  Courses: {len(courses)}")
        print(f"  Students: {len(students)}")
        print(f"  Teams: {len(teams)}")
        print(f"  Projects: {len(projects)}")
        print(f"  Milestones: {len(milestones)}")
        print(f"  Match Runs: {len(matchruns)}")
        print(f"  Check-ins: {len(checkins)}")
        print(f"  Contributions: {len(contributions)}")
        
    except Exception as e:
        print(f"\n✗ Error during population: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
