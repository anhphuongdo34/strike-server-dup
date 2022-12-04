from objects.course import Course


class Program:
    def __init__(self, progId, type, db):
        self.progId = progId
        self.type = type
        self.__initProgramFromDb__(db)
        
    def __initProgramFromDb__(self, db):

        doc_ref = db.collection(u'degrees').document(self.progId)
        doc = doc_ref.get().to_dict()

        self.name = doc.get("Name")
        self.coreCourses = list(map(lambda courseId: Course(courseId=courseId, db=db), doc.get("coreCourses", [])))
        self.electiveOrAllied = list(map(lambda courseId: Course(courseId=courseId, db=db), doc.get("electiveOrAllied", [])))    # will be a list
        self.electiveOrAlliedNum = doc.get("electiveOrAlliedNum", 0)
        self.highLvlCourses = list(map(lambda courseId: Course(courseId=courseId, db=db), doc.get("highLvlCourses", [])))
        self.highLvlCoursesNum = doc.get("highLvlCoursesNum", 0)
        self.credits = doc.get("credits", 1)
