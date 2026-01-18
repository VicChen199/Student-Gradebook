import pandas as pd
import os

# This function cleans data for homeworks and exams
#   Can be used for other similar formats like CW grades
def cleanAssignmentDataFrame(dataframe: pd.DataFrame):

    # Gets a list of the assignment/column names
    assignmentNames = dataframe.columns.tolist()
    assignmentNames.pop(0)

    # Accounts for missing number of not a number
    for assignment in assignmentNames:
        dataframe[assignment] = pd.to_numeric(dataframe[assignment], errors="coerce")
        dataframe[assignment] = dataframe[assignment].fillna(0).astype(int)

    # Cleans for if a name is missing
    dataframe["Name"] = dataframe["Name"].fillna("John Doe")

    for row in dataframe.index:

        # If a name is not alphabetical, will replace with "John Doe"
        if not (dataframe.loc[row, "Name"].isalpha()):
            dataframe.loc[row, "Name"] = "John Doe"

        for assignment in assignmentNames:

            # Checks for if the value inputed was not a valid percentage
            if dataframe.loc[row, assignment] > 100:
                dataframe.loc[row, assignment] = 100
            elif dataframe.loc[row, assignment] < 0:
                dataframe.loc[row, assignment] = 0


# Calculates the averages for each assignment type to each student
def calculateAverageAssignment(dataframe: pd.DataFrame, type):

    # Gets a list of the assignment/column names
    assignmentNames = dataframe.columns.tolist()
    assignmentNames.pop(0)

    # Initializes necessary variables
    column = type + " Average"
    averages = []

    # Takes the average of each student's scores
    for student in dataframe.index:
        sum = 0

        for assignment in assignmentNames:
            sum += dataframe.loc[student, assignment]
        
        averages.append(sum / len(assignmentNames))

    # Adds a column to the dataframe for the avergaes
    dataframe[column] = averages

# Prepares the general gradebook, which will only consist of Name, Final Average, Exam Pass Rate, Homework Pass Rate
with open("General_Gradebook.csv", "w") as f:
    f.write("Name,Final Average")

# Prepares the master gradebook, which will have all information and grades from all homeworks/exams
with open("Master_Gradebook.csv", "w") as f:
    f.write("Name,Final Average")

# Initializes dataframes for each csv file
gradebook = pd.read_csv("General_Gradebook.csv")
master = pd.read_csv("Master_Gradebook.csv")
homeworks = pd.read_csv("Homework_Grades.csv")
exams = pd.read_csv("Exam_Grades.csv")
policy = pd.read_csv("Grading_Policy.csv")

# Cleans the data from homeworks and exams
cleanAssignmentDataFrame(homeworks)
cleanAssignmentDataFrame(exams)
calculateAverageAssignment(homeworks, "HW")
calculateAverageAssignment(exams, "Exam")

# Cleans the grading policy information

# TODO: perhaps create a separate function for this section of cleaning
# Gets a list of the assignment/column names
policyColumns = policy.columns.tolist()

# Accounts for missing number or not a valid number
for policyName in policyColumns:
    policy[policyName] = pd.to_numeric(policy[policyName], errors="coerce")
    policy[policyName] = policy[policyName].fillna(0).astype(int)
    if policy.loc[0, policyName] < 0:
        policy.loc[0, policyName] = 0

# Adds relevant homework and exam data to the master dataframe
homeworkAndExams = pd.merge(exams, homeworks, on="Name", how="outer")
master["Name"] = homeworkAndExams["Name"]
master = pd.merge(master, homeworkAndExams, on="Name", how="left")

print(master)

# Receives relevant grading policy information
examWeight = policy.loc[0, "Exam Weight"]
homeWeight = policy.loc[0, "Homework Weight"]
totalWeight = examWeight + homeWeight
examWeight /= totalWeight
homeWeight /= totalWeight

finalAvgs = []
for studentNum in master.index:
    finalAvgs.append(examWeight * master.loc[studentNum, "Exam Average"] + homeWeight * master.loc[studentNum, "HW Average"])
master["Final Average"] = finalAvgs

print(master)

# Execution of code, aka testing for now
policy.to_csv("Grading_Policy.csv", index = False)
master.to_csv("Master_Gradebook.csv", index = False)
homeworks.to_csv("Homework_Grades.csv", index = False)
exams.to_csv("Exam_Grades.csv", index = False)