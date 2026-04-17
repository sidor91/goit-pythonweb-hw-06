import random
from datetime import timezone

from faker import Faker

from connect import session
from models import Group, Student, Teacher, Subject, Grade

fake = Faker()


def seed_groups():
    groups = [Group(name=f"Group-{i}") for i in range(1, 4)]
    session.add_all(groups)
    session.commit()
    return groups


def seed_teachers():
    teachers = [Teacher(name=fake.name()) for _ in range(random.randint(3, 5))]
    session.add_all(teachers)
    session.commit()
    return teachers


def seed_subjects(teachers: list[Teacher]):
    subject_pool = [
        "Math",
        "Physics",
        "Chemistry",
        "Biology",
        "History",
        "Literature",
        "Programming",
        "English",
    ]

    random.shuffle(subject_pool)
    selected = subject_pool[: random.randint(5, 8)]

    subjects = [
        Subject(name=name, teacher=random.choice(teachers)) for name in selected
    ]

    session.add_all(subjects)
    session.commit()
    return subjects


def seed_students(groups: list[Group]):
    students = [
        Student(name=fake.name(), group=random.choice(groups))
        for _ in range(random.randint(30, 50))
    ]

    session.add_all(students)
    session.commit()
    return students


def seed_grades(students: list[Student], subjects: list[Subject]):
    grades: list[Grade] = []

    for student in students:
        for _ in range(random.randint(5, 20)):
            grades.append(
                Grade(
                    student=student,
                    subject=random.choice(subjects),
                    grade=random.randint(1, 5),
                    date_received=fake.date_time_between(
                        start_date="-1y", end_date="now", tzinfo=timezone.utc
                    ),
                )
            )

    session.add_all(grades)
    session.commit()


if __name__ == "__main__":
    groups = seed_groups()
    teachers = seed_teachers()
    subjects = seed_subjects(teachers)
    students = seed_students(groups)
    seed_grades(students, subjects)

    session.close()
    print("Seed completed successfully")
