import joblib
from sklearn.datasets import make_regression

X,x = make_regression(n_samples=100, n_features=1, noise=0.1)

loaded_model = joblib.load('ai_lecture\\ai_8\\linear_model.pkl')

print('ok!')

y_pred = loaded_model.predict(X)
print(y_pred[:5])  # 예측 결과의 처음 5개 출력
print('Prediction completed successfully.')

