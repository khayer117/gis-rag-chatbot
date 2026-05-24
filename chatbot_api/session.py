from typing import Dict

_sessions: Dict[str, dict] = {}


def get_session(session_id: str) -> dict:
    if session_id not in _sessions:
        _sessions[session_id] = {"history": [], "last_chunks": []}
    return _sessions[session_id]


def clear_session(session_id: str) -> None:
    if session_id in _sessions:
        _sessions[session_id] = {"history": [], "last_chunks": []}
