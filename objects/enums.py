from enum import Enum


class Programs(str, Enum):
    MAJOR = "MAJOR"
    MINOR = "MINOR"
    # MOFO = "MANAGEMENT_FELLOWS"
    # MEFE = "MEDIA_FELLOWS"
    # SCIFI = "SCIENCE_RESEARCH_FELLOWS"
    # ENFO = "ENVIRONMENTAL_FELLOWS"
    # HOSCHO = "HONOR_SCHOLARSS"

class CoursePlaceholder(str, Enum):
    FYSEM = "First Year Seminar"
    LANG = "LANGUAGE COURSE"
    AH = "AH COURSE"
    SS = "SS COURSE"
    SM = "SM COURSE"
    GL = "GL COURSE"
    PPD = "PPD COURSE"
    ANY = "COURSE OF INTEREST"

    Q = "Q COURSE"
    W = "W COURSE"
    S = "S COURSE"


class Competency(str, Enum):
    COMPETENCY = "competency"
    Q = "Q"
    W = "W"
    S = "S"


class Distribution(str, Enum):
    DISTRIBUTION = "DISTRIBUTION"
    AH = "AH"
    SM = "SM"
    SS = "SS"
    GL = "GL"
    PPD = "PPD"

class Language(str, Enum):
    LANGUAGE = "LANGUAGE"