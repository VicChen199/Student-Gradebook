import pandas as pd
import os

def printDataFrame(dataframe: pd.DataFrame):
    print(dataframe.to_string())

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

# Prepares the general gradebook, which will only consist of Name, Final Average, Exam Pass Rate, Homework Pass Rate
with open("General_Gradebook.csv", "w") as f:
    f.write("Name, Final Average, Exam Pass Rate, Homework Pass Rate")

# Prepares the master gradebook, which will have all information and grades from all homeworks/exams
with open("Master_Gradebook.csv", "w") as f:
    f.write("Name, Final Average, Exam Pass Rate, Homework Pass Rate")

# Initializes dataframes for each csv file
gradebook = pd.read_csv("General_Gradebook.csv")
homeworks = pd.read_csv("Homework_Grades.csv")
exams = pd.read_csv("Exam_Grades.csv")

print(exams)

cleanAssignmentDataFrame(homeworks)
cleanAssignmentDataFrame(exams)

homeworks.to_csv("Homework_Grades.csv", index = False)
exams.to_csv("Exam_Grades.csv", index = False)

printDataFrame(exams)