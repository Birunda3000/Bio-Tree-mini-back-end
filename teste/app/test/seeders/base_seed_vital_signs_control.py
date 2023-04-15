from app.main.model import VitalSignsControl


def create_base_seed_vital_signs_control(db):

    new_vital_signs_control = VitalSignsControl(
        admission_id=1,
        sys_blood_pressure=120,
        dia_blood_pressure=80,
        heart_pulse=70,
        respiratory_frequence=15,
        body_fat_rate=15,
        temperature=36.5,
        oxygen_saturation=98,
    )
    db.session.add(new_vital_signs_control)

    new_vital_signs_control = VitalSignsControl(
        admission_id=2,
        sys_blood_pressure=116,
        dia_blood_pressure=88,
        heart_pulse=73,
        respiratory_frequence=14,
        body_fat_rate=16,
        temperature=36.3,
        oxygen_saturation=97,
    )
    db.session.add(new_vital_signs_control)

    db.session.commit()
