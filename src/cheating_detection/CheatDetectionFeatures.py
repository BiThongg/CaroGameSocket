from dataclasses import dataclass
from typing import Optional

class CheatDetectionFeatures:
    # Spam detection features
    actions_per_minute: float
    avg_time_between_actions: float
    action_burst_stddev: float
    repeated_actions_ratio: float
    max_actions_in_10s: int
    invalid_action_ratio: float

    # Same IP / clone detection features
    same_ip_with_other_user: bool
    num_users_on_same_ip: int
    same_user_agent: bool
    geo_location_match: bool
    same_browser_fingerprint: Optional[bool] = None  # Optional if fingerprinting is unavailable

    # Self-play / clone account detection
    self_play_detected: bool
    time_between_account_switch: float  # in seconds
    shared_device_ids: bool
    history_vs_same_ip_ratio: float
    vs_same_user_ratio: float

    # Aggregated behavior features
    win_loss_ratio_against_new_users: float
    session_duration_mean: float  # in minutes
    actions_vs_idle_ratio: float
    night_activity_ratio: float  # % of sessions played during night hours
    suspicious_event_count: int

    def to_dict(self) -> dict:
        return self.__dict__
