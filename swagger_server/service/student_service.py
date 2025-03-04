import os
import tempfile
from functools import reduce

from flask import jsonify
from tinydb import TinyDB, Query

db_dir_path = tempfile.gettempdir()
db_file_path = os.path.join(db_dir_path, "students.json")
student_db = TinyDB(db_file_path)


def add(student=None):
    queries = []
    query = Query()
    queries.append(query.first_name == student.first_name)
    queries.append(query.last_name == student.last_name)
    query = reduce(lambda a, b: a & b, queries)
    res = student_db.search(query)
    if res:
        response = jsonify({"message": "Student already exists"})
        response.status_code = 409
        return response

    doc_id = student_db.insert(student.to_dict())
    student.student_id = doc_id
    return student.student_id


def get_by_id(student_id=None, subject=None):
    student = student_db.get(doc_id=int(student_id))
    if not student:
        response = jsonify({"message": "Student not found"})
        response.status_code = 404
        return response
    student['student_id'] = student_id
    print(student)
    return student


def delete(student_id=None):
    student = student_db.get(doc_id=int(student_id))
    if not student:
        response = jsonify({"message": "Student not found"})
        response.status_code = 404
        return response
    student_db.remove(doc_ids=[int(student_id)])
    return student_id
