from objects.course import Course


class Program:
    def __init__(self, progId, type, db):
        '''
        Program class constructor

        Args
            - progId (str): the unique id of the major or minor from the look up table
            - type (str, Enum): indicate whether this is a major or minor
            - db (google.cloud.firestore.Firestore): database accessed from API call
        '''
        self.progId = progId
        self.type = type
        self.__initProgramFromDb__(db)
        
    def __initProgramFromDb__(self, db):
        '''
        Private function to populate the fields of the program using information from the database.

        Args:
            - db (google.cloud.firestore.Firestore): database accessed from API call
        '''

        doc_ref = db.collection(u'degrees').document(self.progId)
        doc = doc_ref.get().to_dict()

        self.name = doc.get("Name")
        self.coreCourses = list(map(lambda courseId: Course(courseId=courseId, db=db), doc.get("coreCourses", [])))
        self.electiveOrAllied = list(map(lambda courseId: Course(courseId=courseId, db=db), doc.get("electiveOrAllied", [])))    # will be a list
        self.electiveOrAlliedNum = doc.get("electiveOrAlliedNum", 0)
        self.highLvlCourses = list(map(lambda courseId: Course(courseId=courseId, db=db), doc.get("highLvlCourses", [])))
        self.highLvlCoursesNum = doc.get("highLvlCoursesNum", 0)
        self.credits = doc.get("credits", 1)
