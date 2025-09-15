import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv(r'C:\Users\PMLS\Desktop\heart_disease_uci.csv')


print("Dataset shape:", df.shape)
print("\nMissing values:")
print(df.isnull().sum())


numerical_cols = ['age', 'trestbps', 'chol', 'thalch', 'oldpeak']
for col in numerical_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')
    df[col].fillna(df[col].median(), inplace=True)


categorical_cols = ['sex', 'cp', 'fbs', 'restecg', 'exang', 'slope', 'ca', 'thal']
for col in categorical_cols:
    df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else 'unknown', inplace=True)

df['heart_disease'] = (df['num'] > 0).astype(int)


label_encoders = {}
categorical_features = ['sex', 'cp', 'fbs', 'restecg', 'exang', 'slope', 'ca', 'thal', 'dataset']

for col in categorical_features:
    if col in df.columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        label_encoders[col] = le


features = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalch', 'exang', 'oldpeak', 'slope', 'ca', 'thal']
X = df[features]
y = df['heart_disease']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


def evaluate_model(model, X_train, X_test, y_train, y_test, model_name):
    
    model.fit(X_train, y_train)
    
   
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None
    

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    
  
    cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
    
    print(f"\n{model_name} Results:")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1 Score: {f1:.4f}")
    print(f"Cross-validation Accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
    
   
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title(f'Confusion Matrix - {model_name}')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.show()
    
   
    print(f"\nClassification Report for {model_name}:")
    print(classification_report(y_test, y_pred))
    
    return {
        'model': model,
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'cv_mean': cv_scores.mean(),
        'cv_std': cv_scores.std()
    }


print("="*50)
print("LOGISTIC REGRESSION WITH CROSS-VALIDATION")
print("="*50)


param_grid_lr = {
    'C': [0.001, 0.01, 0.1, 1, 10, 100],
    'penalty': ['l1', 'l2'],
    'solver': ['liblinear']
}

grid_lr = GridSearchCV(LogisticRegression(max_iter=1000, random_state=42), 
                      param_grid_lr, cv=5, scoring='accuracy')
grid_lr.fit(X_train_scaled, y_train)

print(f"Best parameters for Logistic Regression: {grid_lr.best_params_}")
print(f"Best cross-validation score: {grid_lr.best_score_:.4f}")


best_lr = grid_lr.best_estimator_
lr_results = evaluate_model(best_lr, X_train_scaled, X_test_scaled, y_train, y_test, "Logistic Regression")


print("="*50)
print("RANDOM FOREST WITH CROSS-VALIDATION")
print("="*50)


param_grid_rf = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

grid_rf = GridSearchCV(RandomForestClassifier(random_state=42), 
                      param_grid_rf, cv=3, scoring='accuracy', n_jobs=-1)
grid_rf.fit(X_train, y_train)

print(f"Best parameters for Random Forest: {grid_rf.best_params_}")
print(f"Best cross-validation score: {grid_rf.best_score_:.4f}")


best_rf = grid_rf.best_estimator_
rf_results = evaluate_model(best_rf, X_train, X_test, y_train, y_test, "Random Forest")


feature_importance = pd.DataFrame({
    'feature': features,
    'importance': best_rf.feature_importances_
}).sort_values('importance', ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(x='importance', y='feature', data=feature_importance)
plt.title('Random Forest Feature Importance')
plt.tight_layout()
plt.show()

print("="*50)
print("DECISION TREE WITH CROSS-VALIDATION")
print("="*50)


param_grid_dt = {
    'max_depth': [None, 5, 10, 15, 20],
    'min_samples_split': [2, 5, 10, 15],
    'min_samples_leaf': [1, 2, 4, 6],
    'criterion': ['gini', 'entropy']
}

grid_dt = GridSearchCV(DecisionTreeClassifier(random_state=42), 
                      param_grid_dt, cv=5, scoring='accuracy')
grid_dt.fit(X_train, y_train)

print(f"Best parameters for Decision Tree: {grid_dt.best_params_}")
print(f"Best cross-validation score: {grid_dt.best_score_:.4f}")

best_dt = grid_dt.best_estimator_
dt_results = evaluate_model(best_dt, X_train, X_test, y_train, y_test, "Decision Tree")


results_df = pd.DataFrame({
    'Logistic Regression': [lr_results['accuracy'], lr_results['precision'], 
                          lr_results['recall'], lr_results['f1'], lr_results['cv_mean']],
    'Random Forest': [rf_results['accuracy'], rf_results['precision'], 
                     rf_results['recall'], rf_results['f1'], rf_results['cv_mean']],
    'Decision Tree': [dt_results['accuracy'], dt_results['precision'], 
                     dt_results['recall'], dt_results['f1'], dt_results['cv_mean']]
}, index=['Accuracy', 'Precision', 'Recall', 'F1 Score', 'CV Mean Accuracy'])

print("="*50)
print("MODEL COMPARISON")
print("="*50)
print(results_df)


results_df.T.plot(kind='bar', figsize=(12, 8))
plt.title('Model Comparison Metrics')
plt.ylabel('Score')
plt.xticks(rotation=45)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

best_model_name = max(['Logistic Regression', 'Random Forest', 'Decision Tree'], 
                     key=lambda x: results_df.loc['CV Mean Accuracy', x])
best_model = best_rf if best_model_name == 'Random Forest' else best_dt if best_model_name == 'Decision Tree' else best_lr

print(f"\nBest performing model: {best_model_name}")
print(f"Cross-validation accuracy: {results_df.loc['CV Mean Accuracy', best_model_name]:.4f}")