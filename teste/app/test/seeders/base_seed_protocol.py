from app.main.model import Protocol


def create_base_seed_protocol(db):

    new_protocol = Protocol(name="protocol1", protocol_type="Diagnóstico")
    db.session.add(new_protocol)

    new_protocol = Protocol(name="protocol2", protocol_type="Prescrição")
    db.session.add(new_protocol)

    new_protocol = Protocol(name="protocol3", protocol_type="Prescrição")

    db.session.add(new_protocol)

    new_protocol = Protocol(name="protocol4", protocol_type="Prescrição")

    db.session.add(new_protocol)

    new_protocol = Protocol(name="protocol5", protocol_type="Diagnóstico")

    db.session.add(new_protocol)

    new_protocol = Protocol(name="protocol6", protocol_type="Diagnóstico")

    db.session.add(new_protocol)
    db.session.commit()
