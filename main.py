import numpy as np
import csv

# assuming 6 days a week, with monday at 0 and saturday at 5
# assuming class starts at 8am until 9pm, with 30 minute time quanta
DAYS_PER_WEEK = 6
TIME_QUANTA_PER_DAY = 26

# DECLARATIONS =================================================================

class Course:
    def __init__(self, rawRow = None, timeMatrix = None):
        self.rawRow = rawRow
        self.timeMatrix = timeMatrix

def dayConverter(day):
    if day == "M":
        return 0
    elif day == "T":
        return 1
    elif day == "W":
        return 2
    elif day == "TH":
        return 3
    elif day == "F":
        return 4
    elif day == "SAT":
        return 5

def timeConflict(matrixA, matrixB):
    booleanMatrix = np.logical_and(matrixA, matrixB)
    return booleanMatrix.any() # will return true if any element is true

# MAIN =========================================================================
courseList = []

# read courses into python list, ignoring empty rows
with open('list.csv') as csvFile:
    csvReader = csv.reader(csvFile, delimiter = ',', dialect = 'excel')
    for row in csvReader:
        if row[0] == '':
            pass
        else:
            courseList.append(Course(rawRow = row))

# assuming 6 days a week, with monday at 0 and saturday at 5
# assuming class starts at 8am until 9pm, with 30 minute time quanta
# timeMatrix is therefore 6x26 cells

# parse the rawRow to populate the timeMatrix
for course in courseList:
    timeMatrix = np.zeros((DAYS_PER_WEEK, TIME_QUANTA_PER_DAY))
    date = course.rawRow[4]
    meetingDays, times = date.split(" ")

    # days of the week the course will meet
    meetingDays = meetingDays.split("-")

    # convert letters to numbers
    meetingDays = [dayConverter(day) for day in meetingDays]


    # split start time and end time
    startTime, endTime = times.split("-")

    # convert time to matrix index
    # super hacky math ahead! look away now
    startTime = int(np.ceil((int(startTime) - 800) / 50.0))
    endTime = int(np.ceil((int(endTime) - 800) / 50.0))

    for day in range(DAYS_PER_WEEK):
        if day in meetingDays:
            for timeQuantum in range(TIME_QUANTA_PER_DAY):
                if timeQuantum >= startTime and timeQuantum < endTime:
                    timeMatrix[day, timeQuantum] = 1

    course.timeMatrix = timeMatrix.copy()

# make permutations
# 'schedules' is a list of schedules
# each schedule is a list of courses
schedules = []

for i in range(len(courseList)):
    schedule = []
    schedule.append(courseList[i])

    for j in range(i+1, len(courseList)):
        # first compare course codes, only continue if differing course code
        if courseList[i].rawRow[0] != courseList[j].rawRow[0]:
            # then check time conflicts
            if not timeConflict(courseList[i].timeMatrix, courseList[j].timeMatrix):
                # if no conflict, add course to schedule
                schedule.append(courseList[j])

    schedules.append(schedule)
    print(len(schedule))
