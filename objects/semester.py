from objects.course import Course


class Semester:
    def __init__(self, term, courses):
        '''
        Semester class constructor

        Args
            - term (int): a number (between 0 and 8 inclusively) representing
                the corresponding semester with Freshman - Fall is 1 and 
                Senior - Spring is 8.
            - courses (set[Courses]): a set of Courses that the student should take
                this corresponding semester.
        '''
        self.term = term
        self.courses = courses
        self.internship = self.__checkInternship__()
        self.totalCredits = self.__getTotalCredits__()
        self.year = self.__getYear__()


    def __getYear__(self):
        '''
        Private function returning the string represent the year of this semester
        
        Args: None
        Return: - str

        Example:
        if self.term=1 then this function will return "Freshman"
        '''
        if self.term in {1,2}:
            return "Freshman"
        elif self.term in {3,4}:
            return "Sophomore"
        elif self.term in {5,6}:
            return "Junior"
        elif self.term in {7,8}:
            return "Senior"

    def __checkInternship__(self):
        '''
        Private function checking if the student takes "HONR 320" this semester
        Return: bool
        '''
        return True if ("HONR 320" in [course.courseId for course in self.courses]) else False
    
    def __getTotalCredits__(self):
        '''
        Private function calculating the number of credits will earned this semester
        Return: float
        '''
        totalCredits = 0
        for course in self.courses:
            totalCredits += course.getCredit()
        return totalCredits
    
    def getCredits(self):
        '''
        Public function to get the number of credits will earned this semester
        Return: float
        '''
        return self.__getTotalCredits__()

    def addCourses(self, newCourses):
        '''
        Public function to add courses for this semester

        Args
            - newCourses (set[Courses]): a set of courses to be added to this semester
        '''
        self.courses = self.courses.union(newCourses)
        self.totalCredits = self.__getTotalCredits__()
        self.internship = self.__checkInternship__()

    def removeCourses(self, removedCourses):
        '''
        Public function to remove courses from this semester

        Args
            - removedCourses (set[Courses]): a set of courses to be removed from this semester
        '''
        self.courses.difference_update(removedCourses)
        self.totalCredits = self.__getTotalCredits__()
    
    