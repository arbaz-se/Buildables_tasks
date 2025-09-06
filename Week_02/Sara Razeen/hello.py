

# practice : create bonus 
# import pandas as pd
# import numpy as np


# data = {
#     "name": ["Alice", "Bob", "Charlie"],
#     "salary": [3000, 4000, 5000]
# }
# employees = pd.DataFrame(data)


# employees["bonus"] = employees["salary"] * (5/100)

# print(employees)

# arr=np.array([1,2,3,4,5])
# arr_mean=np.mean(arr)

# print ("mean_value:",arr_mean)

#questions 1
import numpy as np

np.random.seed(42)  
arr = np.random.randint(10, 100, size=(5, 5))
print(arr)

sum_row=np.sum(arr,axis=1)
print (sum_row)

arr[arr>80]=0
print(arr)

max_index = np.unravel_index(np.argmax(arr), arr.shape)
print(max_index)


#question #2
import pandas as pd
data = {
    "Name": ["Ali","Sara","John","Fatima","Omar","Zara","Ahmed","Noor"],
    "Age": [22,19,25,23,21,20,24,21],
    "Department": ["CS","Math","CS","Physics","Math","CS","Physics","Math"],
    "Score": [88,92,75,89,95,79,94,82]
}
df = pd.DataFrame(data)
# print(df)

Age=df[df["Age"]>21]
print(Age)

average=df.groupby("Department")["Score"].mean()
print(average)

top_student=df.loc[df["Score"].idxmax(),"Name"]
print(top_student)




# #my questions
# import numpy as np

# arr = np.arange(12)     
# reshaped_arr = arr.reshape(3, 4)  
# print(reshaped_arr)



# import pandas as pd

# students = pd.DataFrame({
#     "student_id": [1, 2, 3],
#     "name": ["Alice", "Bob", "Charlie"],
#     "grade": [85.5, 90.0, 72.3]
# })


# selected_columns = students[["name", "grade"]]
# print(selected_columns)

# high_grade_students = students[students["grade"] > 80]
# print(high_grade_students)


# # ArbasAli
# import numpy as np
# from scipy import stats  

# arr = np.array([1, 2, 3, 4, 5])

# mean_val = np.mean(arr)
# median_val = np.median(arr)
# mode_val = stats.mode(arr).mode[0]  

# print("Mean:", mean_val)
# print("Median:", median_val)
# print("Mode:", mode_val)



# def find_second_largest(lst):
#     if len(lst) < 2:
#         return "No second largest"
    
#     first = second = float('-inf')
    
#     for num in lst:
#         if num > first:
#             second = first
#             first = num
#         elif first > num > second:
#             second = num
    
#     return second if second != float('-inf') else "No second largest"


# print(find_second_largest([5, 2, 8, 1, 9]))  
# print(find_second_largest([3, 3, 3]))        
# print(find_second_largest([10, 5]))          



# import pandas as pd

# df = pd.DataFrame({
#     "EmpID": [1, 2, 3, 4, 5],
#     "Name": ["Ali", "Sara", "Ijaz", "Iqra", "Aon"],
#     "Salary": [50000, 60000, 50000, 70000, 60000]
# })

# duplicate_salaries = df[df.duplicated("Salary", keep=False)]
# print(duplicate_salaries)
