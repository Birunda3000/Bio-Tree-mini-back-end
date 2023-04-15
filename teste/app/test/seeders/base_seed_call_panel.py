from app.main.model.call_panel_model import CallPanel

def create_base_seed_call_panel(db):
    """Add 2 call_panels"""

    new_call_panel = CallPanel(name="painel A")
    db.session.add(new_call_panel)

    new_call_panel = CallPanel(name="painel B")
    db.session.add(new_call_panel)

    db.session.commit()