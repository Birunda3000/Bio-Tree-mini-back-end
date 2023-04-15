from app.main.exceptions import DefaultException


def save_new_clinical_evolution(data: dict[str, any]):

    if (
        (not data.get("medical_prescription_medicines_data"))
        and (not data.get("medical_prescription_orientations_data"))
        and (not data.get("medical_prescription_procedures_data"))
    ):
        raise DefaultException("clinical_evolution_data_not_found", code=404)

    save_new_history(
        admission_id=data.get("admission_id"),
        professional_id=data.get("professional_id"),
        type="Clínico",
        medical_prescription_medicines_data=data.get(
            "medical_prescription_medicines_data"
        ),
        medical_prescription_orientations_data=data.get(
            "medical_prescription_orientations_data"
        ),
        medical_prescription_procedures_data=data.get(
            "medical_prescription_procedures_data"
        ),
    )


from app.main.service.history_service import save_new_history
