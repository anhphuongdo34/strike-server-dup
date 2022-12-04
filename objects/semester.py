from objects.course import Course


class Semester:
    def __init__(self, term, courses):
        self.term = term
        self.courses = courses
        self.internship = self.__checkInternship__()
        self.totalCredits = self.__getTotalCredits__()
        self.year = self.__getYear__()


    def __getYear__(self):
        if self.term in {1,2}:
            return "Freshman"
        elif self.term in {3,4}:
            return "Sophomore"
        elif self.term in {5,6}:
            return "Junior"
        elif self.term in {7,8}:
            return "Senior"

    def __checkInternship__(self):
        return True if ("HONR 320" in [course.courseId for course in self.courses]) else False
    
    def __getTotalCredits__(self):
        totalCredits = 0
        for course in self.courses:
            totalCredits += course.getCredit()
        return totalCredits
    
    def getCredits(self):
        return self.__getTotalCredits__()

    def addCourses(self, newCourses):
        self.courses = self.courses.union(newCourses)
        self.totalCredits = self.__getTotalCredits__()
        self.internship = self.__checkInternship__()

    def removeCourses(self, removedCourses):
        self.courses.difference_update(removedCourses)
        self.totalCredits = self.__getTotalCredits__()
    
    