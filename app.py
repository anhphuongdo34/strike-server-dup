import gc
import os
from flask import Flask, request
from flask_cors import CORS
from data.config import getDb
from objects.course import Course
from objects.honor import Honor

from process import getSemesters
from objects.program import Program
from objects.enums import Programs

app = Flask(__name__)
CORS(app)

semesters = []
programs = []
honors = []
waivedCourses = set()
completedCourses = set()
international = False
semesterCnt = 1

db = getDb()

@app.route('/')
def test_server():
    return "<h1>Hello World, flask app is running</h1>"


# get data from user to process schedule
@app.route("/data", methods=["POST"], strict_slashes=False)
def user_info():
    global programs, honors, waivedCourses, completedCourses, international, semesterCnt

    user_info = request.json['user_info']   

    '''
    user_info: {
        majors: list[programId: str]
        minors: list[programId: str]
        honors: list[honors: str]
        waivedCourses: list[str]
        completedCourses: list[courseId: str]
        international: bool
        semesterCnt: int (between 1 and 8 inclusively)
    }
    '''

    programs = list(map(lambda programId: Program(str(programId), Programs.MAJOR, db), user_info['majors']))     
    programs.extend(map(lambda programId: Program(str(programId), Programs.MINOR, db), user_info['minors']))     
    honors = list(map(lambda programId: Honor(programId, db), user_info['honors']))
    waivedCourses = set(user_info['waivedCourses'])
    completedCourses = set(map(lambda courseId: Course(courseId, db), user_info['completedCourses']))       
    international = user_info['international']
    semesterCnt = user_info['semesterCnt']

    return "finish processing user_info into correct datatype"



@app.route("/get_schedule")
def return_schedule():
    global programs, honors, waivedCourses, completedCourses, international, semesterCnt

    print("checkpoint 1: received data")
    semesters = getSemesters(programs, honors, waivedCourses, completedCourses, international, semesterCnt, db)

    print("checkpoint final: prep to send data")
    

    result = {'schedule': semesters}

    gc.collect()
    return result


if __name__ == "__main__":
    app.run(debug=True, port=os.getenv("PORT", default=5000))   