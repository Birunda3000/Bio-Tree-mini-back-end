from app.main.model import RiskClassification


def create_base_seed_risk_classification(db):
    """Add 6 risk classification"""

    risk_classification = RiskClassification(
        patient_id=1,
        professional_id=1,
        weight=67.48,
        height=1.69,
        sys_blood_pressure=120,
        dia_blood_pressure=80,
        temperature=37.8,
        heart_pulse=120,
        respiratory_frequence=15,
        diabetic=False,
        capillary_blood_glucose=80,
        eye_opening="À Dor",
        verbal_response="Palavras incompreensíveis",
        motor_response="Flexão Anormal",
        pupillary_reactivity="Reação bilateral ao estímulo",
        fasting=True,
        professional_avaliation="Professional Avaliation",
        risk_classification="Urgente",
        queue_manager_id=1,
    )

    db.session.add(risk_classification)

    risk_classification = RiskClassification(
        patient_id=2,
        professional_id=2,
        weight=76.45,
        height=1.79,
        sys_blood_pressure=130,
        dia_blood_pressure=40,
        temperature=36.6,
        heart_pulse=87,
        respiratory_frequence=12,
        diabetic=False,
        capillary_blood_glucose=70,
        eye_opening="Nenhuma",
        verbal_response="Orientada",
        motor_response="Obedece Comandos",
        pupillary_reactivity="Nenhuma",
        fasting=False,
        professional_avaliation="Professional Avaliation",
        risk_classification="Muito Urgente",
        queue_manager_id=2,
    )

    db.session.add(risk_classification)

    risk_classification = RiskClassification(
        patient_id=3,
        professional_id=1,
        weight=77.48,
        height=1.79,
        sys_blood_pressure=120,
        dia_blood_pressure=80,
        temperature=37.9,
        heart_pulse=122,
        respiratory_frequence=15,
        diabetic=True,
        capillary_blood_glucose=80,
        eye_opening="À Dor",
        verbal_response="Palavras incompreensíveis",
        motor_response="Flexão Anormal",
        pupillary_reactivity="Não Avaliado",
        fasting=True,
        professional_avaliation="Professional Avaliation",
        risk_classification="Não Urgente",
        queue_manager_id=3,
    )

    db.session.add(risk_classification)
    risk_classification = RiskClassification(
        patient_id=4,
        professional_id=1,
        weight=72.48,
        height=1.49,
        sys_blood_pressure=120,
        dia_blood_pressure=80,
        temperature=37.6,
        heart_pulse=112,
        respiratory_frequence=15,
        diabetic=True,
        capillary_blood_glucose=80,
        eye_opening="À Dor",
        verbal_response="Palavras incompreensíveis",
        motor_response="Flexão Anormal",
        pupillary_reactivity="Apenas uma reage ao estímulo luminoso",
        fasting=True,
        professional_avaliation="Professional Avaliation",
        risk_classification="Pouco Urgente",
        queue_manager_id=4,
    )

    db.session.add(risk_classification)
    risk_classification = RiskClassification(
        patient_id=5,
        professional_id=2,
        weight=77.48,
        height=1.79,
        sys_blood_pressure=120,
        dia_blood_pressure=80,
        temperature=37.9,
        heart_pulse=122,
        respiratory_frequence=15,
        diabetic=True,
        capillary_blood_glucose=80,
        eye_opening="À Dor",
        verbal_response="Palavras incompreensíveis",
        motor_response="Flexão Anormal",
        pupillary_reactivity="Reação bilateral ao estímulo",
        fasting=True,
        professional_avaliation="Professional Avaliation",
        risk_classification="Urgente",
        queue_manager_id=5,
    )

    db.session.add(risk_classification)

    risk_classification = RiskClassification(
        patient_id=6,
        professional_id=1,
        weight=67.48,
        height=1.69,
        sys_blood_pressure=120,
        dia_blood_pressure=80,
        temperature=37.8,
        heart_pulse=120,
        respiratory_frequence=15,
        diabetic=False,
        capillary_blood_glucose=80,
        eye_opening="À Dor",
        verbal_response="Palavras incompreensíveis",
        motor_response="Flexão Anormal",
        pupillary_reactivity="Reação bilateral ao estímulo",
        fasting=True,
        professional_avaliation="Professional Avaliation",
        risk_classification="Emergência",
        queue_manager_id=6,
    )

    db.session.add(risk_classification)
    db.session.commit()
