

from objects.course import Course


class Honor:
    def __init__(self, name, db):
        '''
        Honor class constructor

        Args:
            - name (str): the name of the honor program
            - db (google.cloud.firestore.Firestore): database accessed from API call
        '''
        self.name = name
        self.__initProgramFromDb__(db)

    def __initProgramFromDb__(self, db):
        '''
        Private function to populate the honor program's fields using the information from the database

        Args
            - db (google.cloud.firestore.Firestore): database accessed from API call
        '''
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
        '''
        Public function to retrieve the courses neeeded for a particular semester.
        In the database, the courses requirements for honor programs are displayed by the recommended timeline.
        '''
        courses = self.courseBySemester.get(sem)
        return set(courses) if courses else set()