# 수정 필요


import pickle
from sklearn.datasets import make_regression

# 모델 로드
with open('ai_lecture\\ai_8\\pickle_linear_model.pkl', 'rb') as f:
    loaded_model = pickle.load(f)
print("Model loaded successfully.")
# 모델 사용
y_pred = loaded_model.predict(X)