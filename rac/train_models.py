import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import joblib
from train_model import train_spam_detection_model, train_cheat_detection_model

def create_sample_dataset():
    """Create a sample dataset for training if none exists"""
    # Create sample data
    n_samples = 1000
    
    # Generate random features
    data = {
        # Spam detection features
        "actions_per_minute": np.random.uniform(0, 100, n_samples),
        "avg_time_between_actions": np.random.uniform(0, 10, n_samples),
        "max_actions_in_10s": np.random.randint(0, 30, n_samples),
        "action_count": np.random.randint(0, 1000, n_samples),
        "session_duration": np.random.uniform(0, 120, n_samples),
        
        # Cheat detection features
        "repeated_actions_ratio": np.random.uniform(0, 1, n_samples),
        "same_ip_with_other_user": np.random.choice([0, 1], n_samples),
        "num_users_on_same_ip": np.random.randint(0, 5, n_samples),
        "self_play_detected": np.random.choice([0, 1], n_samples),
        "time_between_account_switch": np.random.uniform(0, 3600, n_samples),
        "shared_device_ids": np.random.choice([0, 1], n_samples),
        "history_vs_same_ip_ratio": np.random.uniform(0, 1, n_samples),
        "vs_same_user_ratio": np.random.uniform(0, 1, n_samples),
        "win_loss_ratio_against_new_users": np.random.uniform(0, 1, n_samples),
        "session_duration_mean": np.random.uniform(0, 120, n_samples),
        "actions_vs_idle_ratio": np.random.uniform(0, 1, n_samples),
        "night_activity_ratio": np.random.uniform(0, 1, n_samples),
        "suspicious_event_count": np.random.randint(0, 10, n_samples)
    }
    
    # Create labels based on feature patterns
    data["is_spamming"] = (
        (data["actions_per_minute"] > 60) | 
        (data["max_actions_in_10s"] > 20) |
        (data["avg_time_between_actions"] < 0.5)
    ).astype(int)
    
    data["is_cheating"] = (
        (data["repeated_actions_ratio"] > 0.8) |
        (data["same_ip_with_other_user"] == 1) |
        (data["self_play_detected"] == 1) |
        (data["win_loss_ratio_against_new_users"] > 0.9) |
        (data["suspicious_event_count"] > 5)
    ).astype(int)
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    # Save to CSV
    dataset_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "cheat_detection_sample.csv")
    df.to_csv(dataset_path, index=False)
    print(f"Sample dataset created and saved to {dataset_path}")
    
    return dataset_path

def main():
    # Get the absolute path to the dataset
    current_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(os.path.dirname(current_dir), "cheat_detection_sample.csv")
    
    # Create sample dataset if it doesn't exist
    if not os.path.exists(dataset_path):
        print("No dataset found. Creating sample dataset...")
        dataset_path = create_sample_dataset()
    
    print("\nTraining spam detection model...")
    spam_model, spam_accuracies = train_spam_detection_model(dataset_path)
    
    print("\nTraining cheat detection model...")
    cheat_model, cheat_accuracies = train_cheat_detection_model(dataset_path)
    
    print("\nTraining completed!")
    print("Spam detection model accuracy:", spam_accuracies)
    print("Cheat detection model accuracy:", cheat_accuracies)

if __name__ == "__main__":
    main() 