from enum import Enum


class RunStatus(Enum):
    WAITING = "waiting"
    COMPLETE = "complete"
    ERROR = "error"
    NEW_RUN_TOKEN_MISSED = "new_run_token_missed"
    INITIALIZED = "initialized"
    QUEUED = "queued"
    RUNNING = "running"
    CANCELLED = "cancelled"
    TRIGGER_ERROR = "trigger_error"
