import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
df = pd.read_csv(r"C:\Users\PMLS\Desktop\Fellowship_Tasks\Housing.csv")
x = df[['area','bedrooms','bathrooms','stories','mainroad','guestroom','basement',
        'hotwaterheating','airconditioning','parking','prefarea','furnishingstatus']]
y = df[['price']]
X = pd.get_dummies(x, drop_first=True)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
df = df[df['price'] < df['price'].quantile(0.99)]
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=100)
X_b = np.c_[np.ones((X_train.shape[0], 1)), X_train]
y_train_np = y_train.values
m = len(y_train_np)
theta = np.zeros((X_b.shape[1], 1))
alpha = 0.01
iterations = 500
cost_history = []
def compute_cost(X, y, theta):
    m = len(y)
    predictions = X.dot(theta)
    cost = (1/(2*m)) * np.sum(np.square(predictions - y))
    return cost
for i in range(iterations):
    predictions = X_b.dot(theta)
    errors = predictions - y_train_np
    gradients = (1/m) * X_b.T.dot(errors)
    theta -= alpha * gradients
    cost = compute_cost(X_b, y_train_np, theta)
    cost_history.append(cost)
plt.plot(range(iterations), cost_history, color='blue')
plt.xlabel("Iterations")
plt.ylabel("Cost (MSE)")
plt.title("Cost Convergence using Gradient Descent")
plt.show()
model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print("R2 Score:", r2_score(y_test, y_pred))
print("Mean Squared Error:", mean_squared_error(y_test, y_pred))
