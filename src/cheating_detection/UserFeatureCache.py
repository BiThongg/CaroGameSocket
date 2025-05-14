from collections import defaultdict
from datetime import datetime

# Default spam detection features
spam_detection_features = {
    # Action-based features for spam detection
    "actions_per_minute": 0.0,
    "avg_time_between_actions": 0.0,
    "max_actions_in_10s": 0,
    "action_count": 0,
    "action_times": [],
    "last_action_time": None,
    "session_start_time": datetime.now(),
}

# Default cheating detection features
cheat_detection_features = {
    # Action-based features
    "repeated_actions_ratio": 0.0,
    "action_types": {},
    "actions_per_minute": 0.0,
    "avg_time_between_actions": 0.0,
    "max_actions_in_10s": 0,
    "action_count": 0,
"action_times": [],
    "last_action_time": None,
    "session_start_time": datetime.now(),   
    # IP and device features
    "same_ip_with_other_user": False,
    "num_users_on_same_ip": 0,
    "ip_address": None,
    "self_play_detected": False,
    "time_between_account_switch": 0.0,
    "shared_device_ids": False,
    
    # Game history features
    "history_vs_same_ip_ratio": 0.0,
    "vs_same_user_ratio": 0.0,
    "win_loss_ratio_against_new_users": 0.0,
    "games_played": 0,
    "wins_against_new": 0,
    
    # Session features
    "session_duration_mean": 0.0,
    "sessions_count": 0,
    "actions_vs_idle_ratio": 0.0,
    "night_activity_ratio": 0.0,
    "night_sessions": 0,
    "total_sessions": 0,
    
    # Suspicious activity
    "suspicious_event_count": 0,
    
    # IP-based suspiciousness
    "ip_suspiciousness_score": 0.0,
    "ip_change_count": 0,
    "ip_based_games": 0,
    "ip_based_wins": 0,
    "previous_ips": set()
}

# Combine both feature sets for the default user features
default_user_features = {**spam_detection_features, **cheat_detection_features}

# Stores per-user feature stats
user_feature_cache = defaultdict(lambda: default_user_features.copy())

# Separate caches for spam and cheat detection
spam_feature_cache = defaultdict(lambda: spam_detection_features.copy())
cheat_feature_cache = defaultdict(lambda: cheat_detection_features.copy())
