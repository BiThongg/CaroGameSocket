from datetime import datetime
from .UserFeatureCache import user_feature_cache
from config import socketio

def update_ip_stats(user_id: str, ip_address: str):
    """Update IP-related statistics for a user"""
    user_features = user_feature_cache[user_id]
    
    # Check if IP is shared with other users
    users_with_same_ip = [uid for uid, features in user_feature_cache.items() 
                         if features.get('ip_address') == ip_address]
    
    user_features['same_ip_with_other_user'] = len(users_with_same_ip) > 1
    user_features['num_users_on_same_ip'] = len(users_with_same_ip)
    user_features['ip_address'] = ip_address
    
    # Track IP change frequency
    if 'previous_ips' not in user_features:
        user_features['previous_ips'] = set()
    
    if ip_address not in user_features['previous_ips']:
        user_features['previous_ips'].add(ip_address)
        user_features['ip_change_count'] = user_features.get('ip_change_count', 0) + 1
    
    # Track IP-based win rate
    if 'ip_based_wins' not in user_features:
        user_features['ip_based_wins'] = 0
        user_features['ip_based_games'] = 0
    
    # Calculate IP-based suspiciousness score
    ip_suspiciousness = 0
    if len(users_with_same_ip) > 1:
        ip_suspiciousness += 0.3  # Multiple users on same IP
    if user_features.get('ip_change_count', 0) > 3:
        ip_suspiciousness += 0.2  # Frequent IP changes
    if user_features.get('ip_based_games', 0) > 0:
        win_rate = user_features['ip_based_wins'] / user_features['ip_based_games']
        if win_rate > 0.8:  # Suspiciously high win rate
            ip_suspiciousness += 0.3
    
    user_features['ip_suspiciousness_score'] = min(1.0, ip_suspiciousness)

def update_game_stats(user_id: str, opponent_id: str, is_win: bool):
    """Update game-related statistics for a user"""
    user_features = user_feature_cache[user_id]
    opponent_features = user_feature_cache[opponent_id]
    
    # Update win/loss ratio against new users
    if 'games_played' not in user_features:
        user_features['games_played'] = 0
        user_features['wins_against_new'] = 0
    
    user_features['games_played'] += 1
    
    # Check if opponent is new (played less than 5 games)
    if opponent_features.get('games_played', 0) < 5:
        if is_win:
            user_features['wins_against_new'] += 1
    
    user_features['win_loss_ratio_against_new_users'] = (
        user_features['wins_against_new'] / max(1, user_features['games_played'])
    )
    
    # Update IP-based game statistics
    if 'ip_based_games' not in user_features:
        user_features['ip_based_games'] = 0
        user_features['ip_based_wins'] = 0
    
    # Check if opponent is on same IP
    if user_features.get('ip_address') == opponent_features.get('ip_address'):
        user_features['ip_based_games'] += 1
        if is_win:
            user_features['ip_based_wins'] += 1

def update_session_stats(user_id: str):
    """Update session-related statistics for a user"""
    user_features = user_feature_cache[user_id]
    current_time = datetime.now()
    
    if 'session_start_time' not in user_features:
        user_features['session_start_time'] = current_time
    
    # Update session duration
    session_duration = (current_time - user_features['session_start_time']).total_seconds() / 60
    user_features['session_duration_mean'] = (
        (user_features['session_duration_mean'] * user_features.get('sessions_count', 0) + session_duration) /
        (user_features.get('sessions_count', 0) + 1)
    )
    
    # Update night activity ratio
    hour = current_time.hour
    is_night = hour >= 22 or hour <= 5
    if 'night_sessions' not in user_features:
        user_features['night_sessions'] = 0
    if 'total_sessions' not in user_features:
        user_features['total_sessions'] = 0
    
    if is_night:
        user_features['night_sessions'] += 1
    user_features['total_sessions'] += 1
    
    user_features['night_activity_ratio'] = (
        user_features['night_sessions'] / user_features['total_sessions']
    )

def update_action_stats(user_id: str, action_type: str):
    """Update action-related statistics for a user"""
    user_features = user_feature_cache[user_id]
    
    # Update repeated actions ratio
    if 'action_types' not in user_features:
        user_features['action_types'] = {}
    
    user_features['action_types'][action_type] = user_features['action_types'].get(action_type, 0) + 1
    
    total_actions = sum(user_features['action_types'].values())
    max_action_count = max(user_features['action_types'].values())
    user_features['repeated_actions_ratio'] = max_action_count / total_actions if total_actions > 0 else 0
