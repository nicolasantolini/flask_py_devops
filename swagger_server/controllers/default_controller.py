import connexion
import six
from flask import jsonify

from swagger_server.models import Student
from swagger_server.service.student_service import *
from swagger_server import util


def add_student(body=None):  # noqa: E501
    """Add a new student

    Adds an item to the system # noqa: E501

    :param body: Student item to add
    :type body: dict | bytes

    :rtype: str
    """
    if connexion.request.is_json:
        body = Student.from_dict(connexion.request.get_json())  # noqa: E501
        student_id = add(body)
        if student_id is None:
            response = jsonify({"message": "Student already exists"})
            response.status_code = 409
            return response
        return jsonify(student_id), 200
    return jsonify({"message": "Invalid input, expected JSON"}), 400


def delete_student(student_id: int):  # noqa: E501
    """Deletes a student

    Deletes a single student # noqa: E501

    :param student_id: the uid
    :type student_id: int

    :rtype: None
    """

    received_student_id = delete(student_id)
    if received_student_id is None:
        response = jsonify({"message": "Student not found"})
        response.status_code = 404
        return response
    return delete(student_id)


def get_student_by_id(student_id: int):  # noqa: E501
    """Gets student

    Returns a single student # noqa: E501

    :param student_id: the uid
    :type student_id: int

    :rtype: Student
    """

    student = get_by_id(student_id)
    if student is None:
        response = jsonify({"message": "Student not found"})
        response.status_code = 404
        return response
    return student
