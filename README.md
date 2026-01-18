# Student-Gradebook
This student gradebook system interprets information from csv files like homework and exam scores, cleans entries using pandas, calculates and interpets grades, and exports information to separate csv files. This project uses the [pandas](https://pandas.pydata.org/docs/#) and [matplotlib](https://matplotlib.org/) to receive, clean, interpret, and export data.

## How to Use
1. Open the [grading policy csv file](Grading_Policy.csv). Add appropiate values for the weight of the exam and homework categories.
2. Open the [homework grades csv file](Homework_Grades.csv) and [exam grades csv file](Exam_Grades.csv). 
3. In these two files, add information like a student's name and their grades. If you would like to add another assignment to the file, simply add a column. Once the program runs, formatting will be corrected to the averages column will be the furthest right. Save these changes to the csv files.
4. Run the [runner file](runner.py), which will populate both the [general gradebook](General_Gradebook.csv) and the [master gradebook](Master_Gradebook.csv). The general gradebook contains general information like averages for each student. The master gradebook contains all grades from all students, including averages. When this file is ran, pie charts representing the pass/fail ratio of different metrics will appear in separate windows.