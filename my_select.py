from sqlalchemy import func
import logging
from connect import session
from models import Student, Group, Subject, Grade

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

def select_1():
    return (
        session.query(Student.name, func.avg(Grade.grade).label("avg_grade"))
        .select_from(Student)
        .join(Grade)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .limit(5)
        .all()
    )


def select_2(subject_id: int):
    return (
        session.query(Student.name, func.avg(Grade.grade).label("avg_grade"))
        .select_from(Student)
        .join(Grade)
        .filter(Grade.subject_id == subject_id)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .first()
    )


def select_3(subject_id: int):
    return (
        session.query(Group.name, func.avg(Grade.grade).label("avg_grade"))
        .select_from(Group)
        .join(Student)
        .join(Grade)
        .filter(Grade.subject_id == subject_id)
        .group_by(Group.id)
        .all()
    )


def select_4():
    return session.query(func.avg(Grade.grade)).scalar()


def select_5(teacher_id: int):
    return session.query(Subject.name).filter(Subject.teacher_id == teacher_id).all()


def select_6(group_id: int):
    return session.query(Student.name).filter(Student.group_id == group_id).all()


def select_7(group_id: int, subject_id: int):
    return (
        session.query(Student.name, Grade.grade)
        .join(Grade)
        .filter(Student.group_id == group_id, Grade.subject_id == subject_id)
        .all()
    )


def select_8(teacher_id: int):
    return (
        session.query(func.avg(Grade.grade))
        .join(Subject)
        .filter(Subject.teacher_id == teacher_id)
        .scalar()
    )


def select_9(student_id: int):
    return (
        session.query(Subject.name)
        .join(Grade)
        .filter(Grade.student_id == student_id)
        .distinct()
        .all()
    )


def select_10(student_id: int, teacher_id: int):
    return (
        session.query(Subject.name)
        .join(Grade)
        .filter(Grade.student_id == student_id, Subject.teacher_id == teacher_id)
        .distinct()
        .all()
    )


if __name__ == "__main__":
    logger.info("Running SELECT 1 (Top 5 students)")
    for row in select_1():
        logger.info(row)

    logger.info("Running SELECT 2 (Best student in subject_id=1)")
    logger.info(select_2(1))

    logger.info("Running SELECT 3 (Avg grade by group for subject_id=1)")
    for row in select_3(1):
        logger.info(row)

    logger.info("Running SELECT 4 (Overall avg grade)")
    logger.info(select_4())

    logger.info("Running SELECT 5 (Teacher courses teacher_id=1)")
    logger.info(select_5(1))

    logger.info("Running SELECT 6 (Students in group_id=1)")
    logger.info(select_6(1))

    logger.info("Running SELECT 7 (Grades in group 1 for subject 1)")
    logger.info(select_7(1, 1))

    logger.info("Running SELECT 8 (Teacher avg grade teacher_id=1)")
    logger.info(select_8(1))

    logger.info("Running SELECT 9 (Student courses student_id=1)")
    logger.info(select_9(1))

    logger.info(
        "Running SELECT 10 (Student courses by teacher student_id=1 teacher_id=1)"
    )
    logger.info(select_10(1, 1))

    session.close()
    logger.info("Done.")
