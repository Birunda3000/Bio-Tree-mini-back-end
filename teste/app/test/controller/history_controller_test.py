import pytest

from app.main import db
from app.test.seeders import (
    create_base_seed_action,
    create_base_seed_admission,
    create_base_seed_clinical_evolution,
    create_base_seed_medical_prescription,
    create_base_seed_medicine,
    create_base_seed_patient,
    create_base_seed_prescription,
    create_base_seed_procedure,
    create_base_seed_professional,
    create_base_seed_protocol,
    create_base_seed_question,
    create_base_seed_sae_perform,
    create_base_seed_vital_signs_control,
)


@pytest.fixture(scope="module")
def seeded_database(client, database):
    """Seed database with clinical evolution data"""
    create_base_seed_professional(db)
    create_base_seed_patient(db)
    create_base_seed_action(db)
    create_base_seed_question(db)
    create_base_seed_protocol(db)
    create_base_seed_prescription(db)
    create_base_seed_medicine(db)
    create_base_seed_procedure(db)
    create_base_seed_medical_prescription(db)
    create_base_seed_admission(db)
    create_base_seed_clinical_evolution(db)
    create_base_seed_vital_signs_control(db)
    create_base_seed_sae_perform(db)


@pytest.mark.usefixtures("seeded_database")
class TestHistoryController:

    # --------------------- GET ---------------------

    def test_get_history(self, client):
        response = client.get("/history")

        assert response.status_code == 200
        assert len(response.json) == 4
        assert response.json["current_page"] == 1
        assert response.json["total_items"] == 4
        assert response.json["total_pages"] == 1
        assert response.json["items"][0]["id"] == 1
        assert response.json["items"][0]["admission_id"] == 1
        assert (
            response.json["items"][0]["professional"]["name"] == "Profissional teste 1"
        )
        assert response.json["items"][0]["type"] == "Clínico"
        assert (
            response.json["items"][0]["medical_prescription_medicines"][0][
                "medical_prescription_medicine"
            ]["medicine"]["name"]
            == "Medicine One"
        )
        assert (
            response.json["items"][0]["medical_prescription_medicines"][0][
                "operation_type"
            ]
            == "Realização"
        )
        assert (
            response.json["items"][0]["medical_prescription_medicines"][0][
                "performed_at"
            ]
            == "17/11/2022 22:15:00"
        )
        assert (
            response.json["items"][0]["medical_prescription_orientations"][0][
                "medical_prescription_orientation"
            ]["orientation"]
            == "Orientation One"
        )
        assert (
            response.json["items"][0]["medical_prescription_orientations"][0][
                "operation_type"
            ]
            == "Realização"
        )
        assert (
            response.json["items"][0]["medical_prescription_orientations"][0][
                "performed_at"
            ]
            == "17/11/2022 22:15:00"
        )
        assert (
            response.json["items"][0]["medical_prescription_procedures"][0][
                "medical_prescription_procedure"
            ]["procedure"]["description"]
            == "ATORVASTATINA 80 MG (POR COMPRIMIDO)"
        )
        assert (
            response.json["items"][0]["medical_prescription_procedures"][0][
                "operation_type"
            ]
            == "Realização"
        )
        assert (
            response.json["items"][0]["medical_prescription_procedures"][0][
                "performed_at"
            ]
            == "17/11/2022 22:15:00"
        )
        assert response.json["items"][1]["id"] == 2
        assert response.json["items"][1]["admission_id"] == 2
        assert (
            response.json["items"][1]["professional"]["name"] == "Profissional teste 2"
        )
        assert response.json["items"][1]["type"] == "Clínico"
        assert (
            response.json["items"][1]["medical_prescription_medicines"][0][
                "medical_prescription_medicine"
            ]["medicine"]["name"]
            == "Medicine Two"
        )
        assert (
            response.json["items"][1]["medical_prescription_medicines"][0][
                "operation_type"
            ]
            == "Realização"
        )
        assert (
            response.json["items"][1]["medical_prescription_medicines"][0][
                "performed_at"
            ]
            == "15/09/2022 20:57:00"
        )
        assert (
            response.json["items"][1]["medical_prescription_orientations"][0][
                "medical_prescription_orientation"
            ]["orientation"]
            == "Orientation Two"
        )
        assert (
            response.json["items"][1]["medical_prescription_orientations"][0][
                "operation_type"
            ]
            == "Realização"
        )
        assert (
            response.json["items"][1]["medical_prescription_orientations"][0][
                "performed_at"
            ]
            == "15/09/2022 20:57:00"
        )
        assert (
            response.json["items"][1]["medical_prescription_procedures"][0][
                "medical_prescription_procedure"
            ]["procedure"]["description"]
            == "BEZAFIBRATO 200 MG (POR DRAGEA OU COMPRIMIDO)"
        )
        assert (
            response.json["items"][1]["medical_prescription_procedures"][0][
                "operation_type"
            ]
            == "Realização"
        )
        assert (
            response.json["items"][1]["medical_prescription_procedures"][0][
                "performed_at"
            ]
            == "15/09/2022 20:57:00"
        )
        assert response.json["items"][2]["id"] == 3
        assert response.json["items"][2]["admission_id"] == 1
        assert (
            response.json["items"][2]["professional"]["name"] == "Profissional teste 1"
        )
        assert response.json["items"][2]["type"] == "Enfermagem"
        assert (
            response.json["items"][2]["nursing_prescription_vital_signs_control"][
                "vital_signs_control"
            ]["sys_blood_pressure"]
            == 120
        )
        assert (
            response.json["items"][2]["nursing_prescription_vital_signs_control"][
                "vital_signs_control"
            ]["dia_blood_pressure"]
            == 80
        )
        assert (
            response.json["items"][2]["nursing_prescription_vital_signs_control"][
                "vital_signs_control"
            ]["heart_pulse"]
            == 70
        )
        assert (
            response.json["items"][2]["nursing_prescription_vital_signs_control"][
                "vital_signs_control"
            ]["respiratory_frequence"]
            == 15
        )
        assert (
            response.json["items"][2]["nursing_prescription_vital_signs_control"][
                "vital_signs_control"
            ]["body_fat_rate"]
            == 15
        )
        assert (
            response.json["items"][2]["nursing_prescription_vital_signs_control"][
                "vital_signs_control"
            ]["temperature"]
            == 36.5
        )
        assert (
            response.json["items"][2]["nursing_prescription_vital_signs_control"][
                "vital_signs_control"
            ]["oxygen_saturation"]
            == 98
        )
        assert (
            response.json["items"][2]["nursing_prescription_vital_signs_control"][
                "performed_at"
            ]
            == "17/11/2022 22:15:00"
        )
        assert (
            response.json["items"][2]["nursing_prescription_questions"][0][
                "operation_type"
            ]
            == "Adição"
        )
        assert (
            response.json["items"][2]["nursing_prescription_questions"][0]["question"][
                "name"
            ]
            == "PERGUNTA1"
        )
        assert (
            response.json["items"][2]["nursing_prescription_questions"][1][
                "operation_type"
            ]
            == "Adição"
        )
        assert (
            response.json["items"][2]["nursing_prescription_questions"][1]["question"][
                "name"
            ]
            == "PERGUNTA2"
        )
        assert (
            response.json["items"][2]["nursing_prescription_actions"][0][
                "operation_type"
            ]
            == "Adição"
        )
        assert (
            response.json["items"][2]["nursing_prescription_actions"][0]["performed_at"]
            == "17/11/2022 22:15:00"
        )
        assert (
            response.json["items"][2]["nursing_prescription_actions"][0]["action"][
                "name"
            ]
            == "AÇÃO TESTE 1"
        )
        assert response.json["items"][3]["id"] == 4
        assert response.json["items"][3]["admission_id"] == 2
        assert (
            response.json["items"][3]["professional"]["name"] == "Profissional teste 2"
        )
        assert response.json["items"][3]["type"] == "Enfermagem"
        assert (
            response.json["items"][3]["nursing_prescription_vital_signs_control"][
                "vital_signs_control"
            ]["sys_blood_pressure"]
            == None
        )
        assert (
            response.json["items"][3]["nursing_prescription_vital_signs_control"][
                "vital_signs_control"
            ]["dia_blood_pressure"]
            == None
        )
        assert (
            response.json["items"][3]["nursing_prescription_vital_signs_control"][
                "vital_signs_control"
            ]["heart_pulse"]
            == None
        )
        assert (
            response.json["items"][3]["nursing_prescription_vital_signs_control"][
                "vital_signs_control"
            ]["respiratory_frequence"]
            == None
        )
        assert (
            response.json["items"][3]["nursing_prescription_vital_signs_control"][
                "vital_signs_control"
            ]["body_fat_rate"]
            == None
        )
        assert (
            response.json["items"][3]["nursing_prescription_vital_signs_control"][
                "vital_signs_control"
            ]["temperature"]
            == None
        )
        assert (
            response.json["items"][3]["nursing_prescription_vital_signs_control"][
                "vital_signs_control"
            ]["temperature"]
            == None
        )
        assert (
            response.json["items"][3]["nursing_prescription_vital_signs_control"][
                "performed_at"
            ]
            == None
        )
        assert (
            response.json["items"][3]["nursing_prescription_questions"][0][
                "operation_type"
            ]
            == "Remoção"
        )
        assert (
            response.json["items"][3]["nursing_prescription_questions"][0]["question"][
                "name"
            ]
            == "PERGUNTA1"
        )
        assert (
            response.json["items"][3]["nursing_prescription_questions"][1][
                "operation_type"
            ]
            == "Adição"
        )
        assert (
            response.json["items"][3]["nursing_prescription_questions"][1]["question"][
                "name"
            ]
            == "PERGUNTA2"
        )
        assert (
            response.json["items"][3]["nursing_prescription_actions"][0][
                "operation_type"
            ]
            == "Remoção"
        )
        assert (
            response.json["items"][3]["nursing_prescription_actions"][0]["performed_at"]
            == "17/11/2022 22:15:00"
        )
        assert (
            response.json["items"][3]["nursing_prescription_actions"][0]["action"][
                "name"
            ]
            == "AÇÃO TESTE 1"
        )
