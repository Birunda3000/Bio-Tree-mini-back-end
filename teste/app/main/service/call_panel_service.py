from app.main import db
from app.main.config import Config
from app.main.exceptions import DefaultException
from app.main.model import CallPanel



def get_call_panel(call_panel_id: int, options: list = None) -> CallPanel:
    """Get a call_panel"""
    call_panel = CallPanel.query.get(call_panel_id)
    if not call_panel:
        raise DefaultException("call_panel_not_found", code=404)
    return call_panel