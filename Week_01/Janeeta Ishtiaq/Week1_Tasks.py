import numpy as np
import pandas as pd
# You have a list of numbers: [3, 6, 9, 12, 15]. Use a list comprehension to create a
# new list containing only the numbers divisible by 3, each multiplied by 2.
list=[3,6,9,12,15]
new_list=[i*2 for i in list if i%3==0]
print(new_list)
# Question 2 (Task-based):
# Task: Create a NumPy array of 10 random integers between 1 and 100, and then extract
# only the even numbers into a new array.
a=np.random.randint(1,100,10)
print(a)
even_num=a[a%2==0]
print(even_num)
# You have a CSV file students.csv with columns: Name, Age, Score.
# Task: Load the CSV into a Pandas DataFrame, and create a new column called
# Passed which is True if Score >= 50 and False otherwise.
data=pd.read_csv("Student_Marks.csv")
print(data)
data["Passed"]=data["Marks"]>=50
print(data)