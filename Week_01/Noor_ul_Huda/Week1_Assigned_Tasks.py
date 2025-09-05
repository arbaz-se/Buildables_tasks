
# Task 1 
# Write a function that takes a sentence and returns the word that appears
# most frequently 
from collections import Counter

def freq_count(sentence):
    sentence=sentence.split()
    return Counter(sentence).most_common(1)[0][0]    

print(freq_count("python is easy and python is powerful"))

# Task 2 
# Create a 6×6 matrix of random integers (1–20).
# Find the row that has the largest sum.
# Print that row and its sum.

import numpy as np

a = np.random.randint(1, 21, size=(6, 6))   
print("Matrix:\n", a)

row_index = np.argmax(a.sum(axis=1))
print("Row with largest sum:", a[row_index])
print("Sum:", a.sum(axis=1)[row_index])

# Task 3
# Create a DataFrame of students with Name and Score. Select students
# whose Name starts with "A".

import pandas as pd

students = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie", "David", "Eva", "Frank", "Grace", "Aliza", "Ali"],
    "Score": [20, 15, 19, 55, 70,  99,  80,75, 100]
})
print("\nStudents DataFrame:\n", students)
print("Student names starting with A:", students[students["Name"].str.startswith("A")]["Name"].tolist())
