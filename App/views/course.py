from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user

from .index import index_views

from App.controllers import (
    create_course,
    get_course_by_name,
    get_course_by_code,
    get_course,
    get_all_courses_json,
    update_course
)

# Create a Blueprint for the course routes
course_views = Blueprint('course_views', __name__, url_prefix='/courses')

# Route to create a new course
@course_views.route('/', methods=['POST'])
def create_course_view():
    data = request.json
    course_code = data.get('courseCode')
    course_name = data.get('courseName')
    semester = data.get('semester')
    year = data.get('year')
    
    if not course_code or not course_name or not semester or not year:
        return jsonify({'message': 'Course code, name, semester, and year are required.'}), 400
    
    new_course = create_course(course_code, course_name, semester, year)
    if new_course:
        return jsonify({'message': 'Course created successfully.', 'courseId': new_course.id}), 201
    else:
        return jsonify({'message': 'Course could not be created.'}), 400

# Route to get all courses
@course_views.route('/', methods=['GET'])
def get_all_courses_view():
    courses = get_all_courses_json()
    return jsonify(courses), 200

# Route to get a course by course code
@course_views.route('/code/<string:course_code>', methods=['GET'])
def get_course_by_code_view(course_code):
    course = get_course_by_code(course_code)
    if not course:
        return jsonify({'message': 'Course not found.'}), 404
    return jsonify(course.get_json()), 200

# Route to get a course by name
@course_views.route('/name/<string:course_name>', methods=['GET'])
def get_course_by_name_view(course_name):
    course = get_course_by_name(course_name)
    if not course:
        return jsonify({'message': 'Course not found.'}), 404
    return jsonify(course.get_json()), 200

# Route to update a course
@course_views.route('/<int:course_id>', methods=['PATCH'])
def update_course_view(course_id):
    data = request.json
    attribute = data.get('attribute')
    content = data.get('content')

    if not attribute or not content:
        return jsonify({'message': 'Attribute and content are required for update.'}), 400
    
    updated_course = update_course(course_id, attribute, content)
    if updated_course:
        return jsonify({'message': 'Course updated successfully.'}), 200
    else:
        return jsonify({'message': 'Course not found or update failed.'}), 404

# Route to get a single course by ID
@course_views.route('/<int:course_id>', methods=['GET'])
def get_course_view(course_id):
    course = get_course(course_id)
    if not course:
        return jsonify({'message': 'Course not found.'}), 404
    return jsonify(course.get_json()), 200

# Route to delete a course by ID
@course_views.route('/<int:course_id>', methods=['DELETE'])
def delete_course_view(course_id):
    course = get_course(course_id)
    if course:
        course.delete()
        return jsonify({'message': 'Course deleted successfully.'}), 200
    else:
        return jsonify({'message': 'Course not found.'}), 404
