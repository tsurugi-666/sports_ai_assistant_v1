import os
import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score


def build_and_train():
    # Автоматически создаем папку data, если её нет
    os.makedirs("data", exist_ok=True)

    # 1. Создание датасета
    np.random.seed(42)
    data_size = 500

    level = np.random.choice([0, 1, 2], size=data_size)
    location = np.random.choice([0, 1], size=data_size)
    goal = np.random.choice([0, 1, 2], size=data_size)

    # Рекомендуемый тип тренировки
    category = []
    for l, loc, g in zip(level, location, goal):
        if loc == 0 and g == 0:
            category.append(0)  # Домашнее кардио
        elif loc == 0 and g == 1:
            category.append(2)  # Калистеника (своим весом)
        elif loc == 1 and g == 1:
            category.append(1)  # Тяжелая атлетика / База
        else:
            category.append(3)  # Общий фитнес

    df = pd.DataFrame({"level": level, "location": location, "goal": goal, "category": category})
    df.to_csv("data/dataset.csv", index=False)

    X = df[["level", "location", "goal"]]
    y = df["category"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 2. Обучение ML-модели
    ml_model = RandomForestClassifier()
    ml_model.fit(X_train, y_train)
    ml_acc = accuracy_score(y_test, ml_model.predict(X_test))

    # 3. Обучение Простой Нейронной Сети (MLP)
    nn_model = MLPClassifier(hidden_layer_sizes=(16, 8), max_iter=500, random_state=42)
    nn_model.fit(X_train, y_train)
    nn_acc = accuracy_score(y_test, nn_model.predict(X_test))

    print(f"Точность ML модели (RandomForest): {ml_acc * 100:.2f}%")
    print(f"Точность Нейронной Сети (MLP): {nn_acc * 100:.2f}%")

    with open("data/ml_model.pkl", "wb") as f:
        pickle.dump(ml_model, f)
    with open("data/nn_model.pkl", "wb") as f:
        pickle.dump(nn_model, f)


if __name__ == "__main__":
    build_and_train()