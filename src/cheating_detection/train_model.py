import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import joblib

def select_features(df, feature_names):
    missing_cols = [col for col in feature_names if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Columns {missing_cols} not found in DataFrame.")
    return df[feature_names].values

def select_label(df, label_name):
    if label_name not in df.columns:
        raise ValueError(f"Label column {label_name} not found in DataFrame.")
    return df[label_name].values

def train_spam_detection_model(dataset_path):
    # 1. Load dataset
    df = pd.read_csv(dataset_path)
    print("Spam Detection Dataset Shape:", df.shape)
    print("Column Names:", df.columns.tolist())
    print("Sample Data:\n", df.head())

    # 2. Define spam detection feature names
    spam_feature_names = [
        "actions_per_minute",
        "avg_time_between_actions",
        "max_actions_in_10s",
        "action_count",
        "session_duration"
    ]

    # 3. Prepare features and labels
    features = select_features(df, spam_feature_names)
    labels = select_label(df, "is_spamming")

    # 4. Split data: train (80%), validation (10%), test (10%)
    X_train, X_temp, y_train, y_temp = train_test_split(features, labels, test_size=0.2, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

    # 5. Train model
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # 6. Save the trained model
    model_path = os.path.join(os.path.dirname(__file__), 'spam_detection_model.joblib')
    joblib.dump(model, model_path)

    # 7. Evaluate model
    train_acc = model.score(X_train, y_train)
    val_acc = model.score(X_val, y_val)
    test_acc = model.score(X_test, y_test)

    print("\nSpam Detection Model Evaluation:")
    print("Train accuracy:", train_acc)
    print("Validation accuracy:", val_acc)
    print("Test accuracy:", test_acc)

    return model, (train_acc, val_acc, test_acc)

def train_cheat_detection_model(dataset_path):
    # 1. Load dataset
    df = pd.read_csv(dataset_path)
    print("Cheat Detection Dataset Shape:", df.shape)
    print("Column Names:", df.columns.tolist())
    print("Sample Data:\n", df.head())

    # 2. Define feature names
    feature_names = [
        "actions_per_minute",
        "avg_time_between_actions",
        "repeated_actions_ratio",
        "max_actions_in_10s",
        "same_ip_with_other_user",
        "num_users_on_same_ip",
        "self_play_detected",
        "time_between_account_switch",
        "shared_device_ids",
        "history_vs_same_ip_ratio",
        "vs_same_user_ratio",
        "win_loss_ratio_against_new_users",
        "session_duration_mean",
        "actions_vs_idle_ratio",
        "night_activity_ratio",
        "suspicious_event_count"
    ]

    # 3. Prepare features and labels
    features = select_features(df, feature_names)
    labels = select_label(df, "is_cheating")

    # 4. Split data: train (80%), validation (10%), test (10%)
    X_train, X_temp, y_train, y_temp = train_test_split(features, labels, test_size=0.2, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

    # 5. Train model
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # 6. Save the trained model
    model_path = os.path.join(os.path.dirname(__file__), 'cheat_detection_model.joblib')
    joblib.dump(model, model_path)

    # 7. Evaluate model
    train_acc = model.score(X_train, y_train)
    val_acc = model.score(X_val, y_val)
    test_acc = model.score(X_test, y_test)

    print("\nCheat Detection Model Evaluation:")
    print("Train accuracy:", train_acc)
    print("Validation accuracy:", val_acc)
    print("Test accuracy:", test_acc)

    return model, (train_acc, val_acc, test_acc)

if __name__ == "__main__":
    # Get the absolute path to the dataset
    current_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(os.path.dirname(current_dir), "cheat_detection_sample.csv")
    
    # Train both models
    spam_model, spam_accuracies = train_spam_detection_model(dataset_path)
    cheat_model, cheat_accuracies = train_cheat_detection_model(dataset_path) 
