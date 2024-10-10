from App.models.course import *
from App.database import db

def create_course(courseCode, courseName, semester, year):
    newcourse = Course(courseCode=courseCode, courseName=courseName, semester=semester, year=year)
    db.session.add(newcourse)
    db.session.commit()
    return newcourse

def get_course_by_name(courseName):
    return Course.query.filter_by(courseName=courseName).first()

def get_course_by_code(courseCode):
    return Course.query.filter_by(courseCode=courseCode).first()

def get_course(id):
    return Course.query.get(id)

def get_all_courses_json():
    courses = Course.query.all()
    if not courses:
        return []
    courses = [course.get_json() for course in courses]
    return courses

def update_course(course_id, attribute, content):
    course = get_course(course_id)
    if course:
        if attribute == "courseCode":
            course.courseCode = content
        elif attribute == "courseName":
            course.courseName = content
        elif attribute == "semester":
            course.semester = content
        elif attribute == "year":
            course.year = content
        db.session.add(course)
        db.session.commit()
        return course  # Return the updated course object
    return None