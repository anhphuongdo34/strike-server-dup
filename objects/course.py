

from enum import Enum


class Course:
    def __init__ (self, courseId, db=None, comp="", distr=[], lang=False) :
        '''
        Args:
            courseId (str): the actual course id from DePauw
            competency (list[str]): a list of competency this course can fulfill, including 'W', 'Q', 'S.'
            distribution (list[str]): a list of distribution area this course can fulfill
            alternatives (list[str]): a list of other courseIds that will fulfill the requirements for this course instead
            credit (list[int]): a list of the numbers of credits that can be earned from this course
            prerequisites (list[str]): a list of the courseIds
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
        return self.credit

    