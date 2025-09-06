# 📌 Email Spam Classifier

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# 1️⃣ Load dataset
df = pd.read_csv(r"C:\Users\PMLS\Desktop\Fellowship_Tasks\spam_or_not_spam.csv")  # <-- replace with your dataset path
# In your case, file has columns: 'email' (text), 'label' (0=not spam, 1=spam)

print(df['label'].value_counts())
print(df['label'].value_counts(normalize=True))  # percentage
df['email'] = df['email'].fillna("")

# 2️⃣ Features (X) and Target (y)
X = df['email']
y = df['label']

# 3️⃣ Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 4️⃣ Text Vectorization (TF-IDF)
vectorizer = TfidfVectorizer(stop_words='english', max_features=3000)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# 5️⃣ Logistic Regression with class weight balancing
model = LogisticRegression(class_weight='balanced', max_iter=1000)
model.fit(X_train_vec, y_train)

# 6️⃣ Predictions
y_pred = model.predict(X_test_vec)

# 7️⃣ Evaluation
print("\nConfusion Matrix:")
cm = confusion_matrix(y_test, y_pred)
print(cm)

# heatmap for better visualization
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Not Spam','Spam'], yticklabels=['Not Spam','Spam'])
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()

print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['Not Spam','Spam']))
