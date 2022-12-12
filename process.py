from objects.course import Course
from objects.enums import Competency, Distribution, Language, CoursePlaceholder, Programs
from objects.honor import Honor
from objects.program import Program
from random import randint

from objects.semester import Semester

defaultReqs = {
    "credits": 31,
    Competency.COMPETENCY: {
        Competency.Q: 1,       # earned before senior year
        Competency.W: 1,       # must be taken during sophomore year, will include in the code logic
        Competency.S: 1,       # will make the assumption that the senior seminar/proj fulfills this
    },
    Distribution.DISTRIBUTION: {
        Distribution.AH: 2,
        Distribution.SM: 2,
        Distribution.SS: 2,
        Distribution.GL: 1,
        Distribution.PPD: 1,
    },
    Language.LANGUAGE: 2,
}

coursePlaceHolders = {
    Competency.Q: CoursePlaceholder.Q,
    Competency.W: CoursePlaceholder.W,
    Competency.S: CoursePlaceholder.S,

    Distribution.AH:  CoursePlaceholder.AH,
    Distribution.SM:  CoursePlaceholder.SM,
    Distribution.SS:  CoursePlaceholder.SS,
    Distribution.GL:  CoursePlaceholder.GL,
    Distribution.PPD: CoursePlaceholder.PPD,

    Language.LANGUAGE: CoursePlaceholder.LANG,
}


def getCoursesRandom(courseLs, num):
    if (num == 0 or num == len(courseLs)):
        return courseLs

    finalCourses = set()
    totalCourseNum = len(courseLs)
    while (len(finalCourses) < num):
        nextCourse = courseLs[randint(0, totalCourseNum-1)]
        if nextCourse not in finalCourses:
            finalCourses.add(nextCourse)
    
    return finalCourses


# call this function once added all the courses needed for majors, minors, and honor programs.
def finalizeGenEd(genEd, international=False):
    allComp = genEd[Distribution.DISTRIBUTION]

    depts = set()
    removed = set()

    for distr, courses in allComp.items():
        if (distr == Distribution.PPD or distr == Distribution.GL):
            continue
        for course in courses.copy():
            curDept = course.courseId.split(" ")[0]
            if curDept in depts:
                removed.add(course)
                allComp[distr].discard(course)
            else:
                depts.add(curDept)

    if (len(allComp[Distribution.PPD]) == 0) :
        for course in removed.copy():
            allComp[Distribution.PPD].add(course)
            removed.discard(course)
            break
    
    if (len(allComp[Distribution.GL]) == 0) :
        for course in removed.copy():
            allComp[Distribution.GL].add(course)
            removed.discard(course)
            break
    
    for k, v in allComp.items():
        allComp[k] = len(v)
        if k == Distribution.GL and international:
            allComp[k] = 1

def addGenEd(genEd, courseLs, international):
    for course in courseLs:
        for key, item in genEd[Competency.COMPETENCY].items():
            if (key == course.competency and len(item) < 1):
                genEd[Competency.COMPETENCY][key].add(course)
                courseLs.remove(course)

        if (course.language):
            genEd[Language.LANGUAGE] += 1

        for key, item in genEd[Distribution.DISTRIBUTION].items():
            if (key in course.distribution):
                if ((key == Distribution.PPD or key == Distribution.GL) and len(item) < 1):
                    genEd[Distribution.DISTRIBUTION][key].add(course)
                    break
                elif ((key == Distribution.AH or key == Distribution.SS or key == Distribution.SM) and len(item) < 2):
                    genEd[Distribution.DISTRIBUTION][key].add(course)
                    break
    
    finalizeGenEd(genEd, international)



def getDegreeRequirements(reqs, waivedCourses, completedCourses, international):
    '''
    Args:
        - reqs (list[Program]): a list of majors and/or minors the student wishes to take
        - waivedCourses (set[str]): each value is the courseId of the waived courses. Students will not earned genEd from these courses
        - completedCourses (set[Course]): courses completed or credit transfered from other university, will be used to fulfill genEd.
        - international (bool): whether the student is an internation student
    '''
    coursesNeeded = []
    for prog in reqs:
        coursesNeeded.extend(prog.coreCourses)

    # randomly choose elective and highlevel courses
    for prog in reqs:
        coursesNeeded.extend(getCoursesRandom(prog.electiveOrAllied, prog.electiveOrAlliedNum))
        coursesNeeded.extend(getCoursesRandom(prog.highLvlCourses, prog.highLvlCoursesNum))

    # remove courses if in waivedCourses
    for course in coursesNeeded:
        if (course.courseId in waivedCourses):
            coursesNeeded.remove(course)

    # remove duplicated courses if any and combined with completedCourses to check for fulfilled comp and distr
    coursesNeeded = list(set(coursesNeeded)) + list(completedCourses)

    # check if the courses fulfill any default requirements
    genEd = {
        Competency.COMPETENCY: {
            Competency.Q: set(),
            Competency.W: set(),
            Competency.S: set(),
        },
        Distribution.DISTRIBUTION: {
            Distribution.AH: set(),
            Distribution.SM: set(),
            Distribution.SS: set(),
            Distribution.GL: set(),
            Distribution.PPD: set(),
        },

        # international students automatically fulfill
        Language.LANGUAGE: 2 if (international) else 0,
    }

    return coursesNeeded, genEd

# courses for honor program are already sorted, so only use this for major/minor combined courseList
def sortCoursesByLvl(courseLs):
    for i in range(1, len(courseLs)):

        cur = courseLs[i]                   # to memorize the swapping element
        key = courseLs[i].courseId.split(" ")[1]     # to get the course number

        j = i-1
        while j>=0 and key < courseLs[j].courseId.split(" ")[1]:
            courseLs[j+1] = courseLs[j]
            j -= 1
        courseLs[j+1] = cur

def checkMissingGenEd(genEd):
    for cate, reqVal in genEd.items():
        if (cate == Language.LANGUAGE):
            if reqVal >= 2:
                continue
            genEd[cate] += 1
            return Course(coursePlaceHolders[Language.LANGUAGE])

        for req, val in genEd[cate].items():
            while ((val if (type(val) == int) else len(val)) < defaultReqs[cate][req]):
                newCourse = Course(coursePlaceHolders[req])
                genEd[cate][req] = (val+1) if (type(val) == int) else genEd[cate][req].union(set([newCourse]))
                return newCourse
    
    return Course(CoursePlaceholder.ANY)  

def getSchedule(semesters):
    schedule = {
        "Freshman": {
            "Fall" : [],
            "Spring": []
        },
        "Sophomore": {
            "Fall" : [],
            "Spring": []
        },
        "Junior": {
            "Fall" : [],
            "Spring": []
        },
        "Senior": {
            "Fall" : [],
            "Spring": []
        },
    }
    for sem in semesters:
        schedule[sem.year]["Spring" if (sem.term % 2 == 0) else "Fall"] = list(map(lambda course: course.courseId, sem.courses))

    return schedule

def getSemesters(programs, honors, waivedCourses, completedCourses, international, curSemCnt, db=None):
    coursesNeeded, genEd = getDegreeRequirements(programs, waivedCourses, completedCourses, international)

    # add courses from honor program to genEd before finalizing
    honorCourses = []
    for honor in honors:
        for ls in honor.courseBySemester.values():
            honorCourses.extend(ls)

    addGenEd(genEd, coursesNeeded + honorCourses, international)

    # remove W, Q, and S courses from coursesNeeded (will be added from genEd list)
    if genEd[Competency.COMPETENCY][Competency.W] and list(genEd[Competency.COMPETENCY][Competency.W])[0] in coursesNeeded:
        coursesNeeded.remove(list(genEd[Competency.COMPETENCY][Competency.W])[0])
    if genEd[Competency.COMPETENCY][Competency.S] and list(genEd[Competency.COMPETENCY][Competency.S])[0] in coursesNeeded:
        coursesNeeded.remove(list(genEd[Competency.COMPETENCY][Competency.S])[0])

    # will not include the completedCourses in th upcoming schedule, but the genEds are fulfilled (if any)
    for course in coursesNeeded:
        if (course.courseId in completedCourses):
            coursesNeeded.remove(course)

    # sort coursesNeeded so that lower-level courses will be taken before higher-level one
    sortCoursesByLvl(coursesNeeded)

    notEnoughCredits = []

    semesters = []

    # start at current semester, up to 8 semesters total
    for i in range(curSemCnt, 9):

        curSemester = Semester(i, set())  
        # first semester freshman year always have 1 seminar course
        if i == 1:
            curSemester.addCourses(set([Course(courseId = CoursePlaceholder.FYSEM)]))  
        
        # assuming that W course is alway taken first semester of sophomore year
        if i == 3:
            curSemester.addCourses(genEd[Competency.COMPETENCY][Competency.W])

        # assuming that the S cource from major minor is the senior seminar. Take it 1st sem senior year
        if i == 7:
            curSemester.addCourses(genEd[Competency.COMPETENCY][Competency.S])
        
        # add all courses for the honor program for that semester
        tempHonorCourses = set()
        for honor in honors:
            tempHonorCourses = honor.getCoursesBySem(str(i))
            curSemester.addCourses(tempHonorCourses)

        if (curSemester.internship):
            semesters.append(curSemester)
            continue        

        # add courses to the semester from the coursesNeeded array (sorted by level)
        while (coursesNeeded and curSemester.getCredits() + coursesNeeded[0].credit <= 4.5) :
            curSemester.addCourses(set([coursesNeeded.pop(0)]))
            
            if len(coursesNeeded) == 0:
                notEnoughCredits.append(curSemester if (curSemester.getCredits() <= 3.5) else None)
                break

        semesters.append(curSemester)

    
    newCourses = []
    newCourse = checkMissingGenEd(genEd)
    while (newCourse.courseId != CoursePlaceholder.ANY):
        newCourses.append(newCourse)
        newCourse = checkMissingGenEd(genEd)

    for sem in semesters:
        while (newCourses and (sem.getCredits() + newCourses[0].getCredit() <= 4.5) and not sem.internship):
            sem.addCourses(set([newCourses.pop(0)]))
        
        while (sem.getCredits() + 1 <= 4.5) and not sem.internship:
            sem.addCourses(set([Course(CoursePlaceholder.ANY)]))


    return getSchedule(semesters)
