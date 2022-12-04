

from objects.course import Course


class Honor:
    def __init__(self, name, db):
        self.name = name
        self.__initProgramFromDb__(db)

    def __initProgramFromDb__(self, db):
        doc_ref = db.collection(u'honors').document(self.name)
        doc = doc_ref.get().to_dict()

        strCoursesBySem = doc.get("courseBySemester")
        self.courseBySemester = {"": []}
        for k, v in strCoursesBySem.items():
            self.courseBySemester[k] = list(map(lambda courseId: Course(courseId, db), v))

        self.genEds = doc.get("genEds", [])
        self.credits = doc.get("totalCredits", 0)
        self.lateralEntry = doc.get("lateralEntry", False)

    def getCoursesBySem(self, sem):
        courses = self.courseBySemester.get(sem)
        return set(courses) if courses else set()