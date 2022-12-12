

from enum import Enum


class Course:
    def __init__ (self, courseId, db=None, comp="", distr=[], lang=False) :
        '''
        Course class constructor

        Args:
            courseId (str): the actual course id from DePauw
            db (google.cloud.firestore.Firestore): (optional) the database accessed through API call. default db=None
            competency (list[str]): (optional) a list of competency this course can fulfill, including 'W', 'Q', 'S.'
            distribution (list[str]): (optional) a list of distribution area this course can fulfill
            lang (bool): (optional) whether this course will full fill the language requirements
        '''
        self.courseId = courseId
        self.competency=comp 
        self.distribution=distr
        self.excluded=[] 
        self.credit=1.0
        self.prerequisites=[]
        self.language = lang
        self.__initProgramFromDb__(db)

    def __initProgramFromDb__(self, db):
        '''
        Private function to populate the fields of the course using information from the database.
            If the db=None, then the fields is kept as passed in the constructor function.

        Args:
            - db (google.cloud.firestore.Firestore): database accessed from API call
        '''

        if (db):
            doc_ref = db.collection(u'courses').document(self.courseId)
            doc = doc_ref.get().to_dict()

            if doc:
                self.competency = doc.get("competency", "")
                self.distribution = doc.get("distribution", [])
                self.credit = doc.get("credit")
                self.prerequisites = doc.get("prerequisites", [])
                self.excluded = doc.get("excluded", [])
                self.language = doc.get("language", False)

            

    def getCredit(self):
        '''
        Public function returning the number of credit earned by taking this course

        Return:
            - float: the number of credit earned by taking this course
        '''
        return self.credit

    