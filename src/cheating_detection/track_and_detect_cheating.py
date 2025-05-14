from functools import wraps
from datetime import datetime
from .UserFeatureCache import user_feature_cache, spam_feature_cache, cheat_feature_cache
import numpy as np
from sklearn.linear_model import LogisticRegression
import joblib
import os
from config import socketio

# Load the trained models
cheat_model_path = os.path.join(os.path.dirname(__file__), 'cheat_detection_model.joblib')
spam_model_path = os.path.join(os.path.dirname(__file__), 'spam_detection_model.joblib')

try:
    cheat_model = joblib.load(cheat_model_path)
except (FileNotFoundError, EOFError):
    print("Warning: Cheat detection model not found. Cheat detection will be disabled until model is trained.")
    cheat_model = None

try:
    spam_model = joblib.load(spam_model_path)
except (FileNotFoundError, EOFError):
    print("Warning: Spam detection model not found. Spam detection will be disabled until model is trained.")
    spam_model = None

def detect_spamming(f):
    @wraps(f)
    def wrapper(user, *args, **kwargs):
        if not user:
            return f(user, *args, **kwargs)

        # Get current timestamp
        current_time = datetime.now() 
        
        # Get or initialize spam features
        if user.id not in spam_feature_cache:
            spam_feature_cache[user.id] = spam_feature_cache.default_factory()
        
        spam_features = spam_feature_cache[user.id]
        
        # Update time-based features
        if spam_features['last_action_time'] is not None:
            time_diff = (current_time - spam_features['last_action_time']).total_seconds()
            if spam_features['action_count'] > 0:
                spam_features['avg_time_between_actions'] = (
                    (spam_features['avg_time_between_actions'] * spam_features['action_count'] + time_diff) /
                    (spam_features['action_count'] + 1)
                )
        
        # Update action count and rate
        spam_features['action_count'] = spam_features.get('action_count', 0) + 1
        
        # Calculate actions per minute safely
        session_duration = (current_time - spam_features['session_start_time']).total_seconds() / 60
        if session_duration > 0:
            spam_features['actions_per_minute'] = spam_features['action_count'] / session_duration
        
        # Update max actions in 10s window
        spam_features['action_times'].append(current_time)
        spam_features['action_times'] = [t for t in spam_features['action_times'] 
                                       if (current_time - t).total_seconds() <= 10]
        spam_features['max_actions_in_10s'] = max(spam_features['max_actions_in_10s'], 
                                                len(spam_features['action_times']))
        
        # Update last action time
        spam_features['last_action_time'] = current_time
        
        # Create feature vector for spam prediction
        if spam_model is not None:
            spam_feature_vector = np.array([[
                spam_features['actions_per_minute'],
                spam_features['avg_time_between_actions'],
                spam_features['max_actions_in_10s'],
                spam_features['action_count'],
                session_duration
            ]])
            
            # Predict if spamming
            spamming_probability = spam_model.predict_proba(spam_feature_vector)[0][1]
            fspamming_probability = round(float(spamming_probability), 2)
            
            if fspamming_probability > 0.25:  # Threshold for spam detection
                print(f"Warning: User {user.id} shows signs of spamming (probability: {spamming_probability:.2f})")
                socketio.emit("detected_spamming",
                    {"message": "Please slow down your actions!"},
                    to=user.sid)
            print(f'Spam Score == {spamming_probability}')
        
        return f(user, *args, **kwargs)
    return wrapper

def detect_cheating(f):
    @wraps(f)
    def wrapper(user, *args, **kwargs):
        if not user:
            return f(user, *args, **kwargs)

        # Get current timestamp
        current_time = datetime.now()

        if user.id not in cheat_feature_cache:
            cheat_feature_cache[user.id] = cheat_feature_cache.default_factory()
            
        cheat_features = cheat_feature_cache[user.id]

        # Update time-based features
        if cheat_features['last_action_time'] is not None:
            time_diff = (current_time - cheat_features['last_action_time']).total_seconds()
            if cheat_features['action_count'] > 0:
                cheat_features['avg_time_between_actions'] = (
                    (cheat_features['avg_time_between_actions'] * cheat_features['action_count'] + time_diff) /
                    (cheat_features['action_count'] + 1)
                )
        
        # Update action count and rate
        cheat_features['action_count'] = cheat_features.get('action_count', 0) + 1
        
        # Calculate actions per minute safely
        session_duration = (current_time - cheat_features['session_start_time']).total_seconds() / 60
        if session_duration > 0:
            cheat_features['actions_per_minute'] = cheat_features['action_count'] / session_duration
        
        # Update max actions in 10s window
        if 'action_times' not in cheat_features:
            cheat_features['action_times'] = []
        cheat_features['action_times'].append(current_time)
        cheat_features['action_times'] = [t for t in cheat_features['action_times'] 
                                       if (current_time - t).total_seconds() <= 10]
        cheat_features['max_actions_in_10s'] = max(cheat_features.get('max_actions_in_10s', 0), 
                                                len(cheat_features['action_times']))
        
        # Update last action time
        cheat_features['last_action_time'] = current_time

        # Track IP changes
        # if 'last_ip_change_time' in cheat_features and 'current_ip' in cheat_features:
        #     if cheat_features['current_ip'] != user.ip_address:
        #         time_since_last_change = (current_time - cheat_features['last_ip_change_time']).total_seconds()
        #         if time_since_last_change < 60:  # IP changed within 1 minute
        #             cheat_features['suspicious_event_count'] += 1
        #         cheat_features['last_ip_change_time'] = current_time
        #         cheat_features['current_ip'] = user.ip_address
        # else:
        #     cheat_features['last_ip_change_time'] = current_time
        #     cheat_features['current_ip'] = user.ip_address

        # Create feature vector for prediction
        feature_vector = np.array([[
            cheat_features['actions_per_minute'],
            cheat_features['avg_time_between_actions'],
            cheat_features['repeated_actions_ratio'],
            cheat_features['max_actions_in_10s'],
            int(cheat_features['same_ip_with_other_user']),
            cheat_features['num_users_on_same_ip'],
            int(cheat_features['self_play_detected']),
            cheat_features['time_between_account_switch'],
            int(cheat_features['shared_device_ids']),
            cheat_features['history_vs_same_ip_ratio'],
            cheat_features['vs_same_user_ratio'],
            cheat_features['win_loss_ratio_against_new_users'],
            cheat_features['session_duration_mean'],
            cheat_features['actions_vs_idle_ratio'],
            cheat_features['night_activity_ratio'],
            # Combine IP suspiciousness features into suspicious_event_count
            cheat_features['suspicious_event_count'] + 
            (cheat_features.get('ip_suspiciousness_score', 0.0) * 0.3) +  # Weight IP suspiciousness
            (cheat_features.get('ip_change_count', 0) > 3) * 0.2 +  # Weight frequent IP changes
            (cheat_features.get('ip_based_games', 0) > 0 and 
             (cheat_features.get('ip_based_wins', 0) / max(1, cheat_features.get('ip_based_games', 1))) > 0.8) * 0.3  # Weight suspicious IP win rate
        ]])
        
        # Predict if cheating
        if cheat_model is not None:
            cheating_probability = cheat_model.predict_proba(feature_vector)[0][1]
            fcheating_probability = round(float(cheating_probability), 2)
            
            if fcheating_probability > 0.9 and fcheating_probability < 0.95:  # Threshold for anomaly detection
                print(f"F1 Warning: User {user.id} shows signs of Anomaly (probability: {cheating_probability:.2f})")
                socketio.emit("detected_anomaly",
                    {"message": "Abnormal behavior detected, please slow down!"},
                    to=user.sid)
                    
            if fcheating_probability >= 0.95:  # Threshold for cheating detection
                print(f"F2 Warning: User {user.id} shows signs of cheating (probability: {cheating_probability:.2f})")
                socketio.emit("detected_cheating",
                    {"message": "Cheating behavior detected, please slow down!"},
                    to=user.sid)
            print(f'Cheat Score == {cheating_probability}')
        
        return f(user, *args, **kwargs)
    return wrapper

# For backward compatibility
def track_and_detect_cheating(f):
    @wraps(f)
    @detect_spamming
    @detect_cheating
    def wrapper(user, *args, **kwargs):
        return f(user, *args, **kwargs)
    return wrapper
