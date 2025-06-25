from sklearn.linear_model import LinearRegression
from sklearn.datasets import make_regression
import pickle


# 샘플 데이터 생성 및 모델 학습
X, y = make_regression(n_samples=100, n_features=1, noise=0.1)
model = LinearRegression()
model.fit(X, y)

with open('ai_lecture\\ai_8\\pickle_linear_model.pkl', 'wb') as f:
    pickle.dump(model, f)
print("Model saved successfully.")



