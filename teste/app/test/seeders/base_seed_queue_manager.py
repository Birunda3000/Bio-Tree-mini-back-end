from app.main.model import QueueLog, QueueManager


def create_base_seed_queue_manager(db):
    """
    Add patients queues:
      - queue 1:
            1º to enter: [patient id 1]: priority = False
            2º to enter: [patient id 2]: priority = True
            3º to enter: [patient id 8]: priority = False

      - queue 2:
            1º to enter: [patient id 3]: priority = False
            2º to enter: [patient id 4]: priority = True
            3º to enter: [patient id 5]: priority = False

      - queue 3:
            1º to enter: [patient id 7]: priority = False
            2º to enter: [patient id 9]: priority = False

    OBS: Add patient (id=6) with queue manage but in no queues
    """

    new_queue_manager = QueueManager(
        patient_id=1, queue_id=1, priority=False, status="Aguardando Acolhimento"
    )
    new_queue_log = QueueLog(queue_id=1, queue_manager=new_queue_manager)

    db.session.add(new_queue_manager)
    db.session.add(new_queue_log)

    new_queue_manager = QueueManager(
        patient_id=2,
        queue_id=1,
        priority=True,
        priority_type="Idoso",
        status="Aguardando Acolhimento",
    )
    new_queue_log = QueueLog(queue_id=1, queue_manager=new_queue_manager)

    db.session.add(new_queue_manager)
    db.session.add(new_queue_log)

    new_queue_manager = QueueManager(
        patient_id=3,
        queue_id=2,
        priority=False,
        status="Aguardando Atendimento Médico",
    )
    new_queue_log = QueueLog(queue_id=2, queue_manager=new_queue_manager)

    db.session.add(new_queue_manager)
    db.session.add(new_queue_log)

    new_queue_manager = QueueManager(
        patient_id=4,
        queue_id=2,
        priority=True,
        priority_type="Gestante",
        status="Aguardando Atendimento Médico",
    )
    new_queue_log = QueueLog(queue_id=2, queue_manager=new_queue_manager)

    db.session.add(new_queue_manager)
    db.session.add(new_queue_log)

    new_queue_manager = QueueManager(
        patient_id=5,
        queue_id=2,
        priority=True,
        priority_type="Idoso",
        status="Aguardando Atendimento Médico",
    )
    new_queue_log = QueueLog(queue_id=2, queue_manager=new_queue_manager)

    db.session.add(new_queue_manager)
    db.session.add(new_queue_log)

    new_queue_manager = QueueManager(
        patient_id=6,
        queue_id=None,
        priority=True,
        priority_type="Idoso",
        status="Em espera",
    )

    db.session.add(new_queue_manager)

    new_queue_manager = QueueManager(
        patient_id=8,
        queue_id=1,
        priority=False,
        status="Aguardando Acolhimento",
    )
    new_queue_log = QueueLog(queue_id=1, queue_manager=new_queue_manager)

    db.session.add(new_queue_manager)
    db.session.add(new_queue_log)

    new_queue_manager = QueueManager(
        patient_id=7,
        queue_id=3,
        priority=False,
        status="Aguardando Observação",
    )
    new_queue_log = QueueLog(queue_id=3, queue_manager=new_queue_manager)

    db.session.add(new_queue_manager)
    db.session.add(new_queue_log)

    new_queue_manager = QueueManager(
        patient_id=9,
        queue_id=3,
        priority=False,
        status="Aguardando Observação",
    )
    new_queue_log = QueueLog(queue_id=3, queue_manager=new_queue_manager)

    db.session.add(new_queue_manager)
    db.session.add(new_queue_log)

    db.session.commit()
