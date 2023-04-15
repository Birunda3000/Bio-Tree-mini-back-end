from typing import Union

import pytest
from sqlalchemy.orm import joinedload

from app.main import db
from app.main.model import QueueLog, QueueManager
from app.main.service import (
    add_patient_in_queue,
    change_patient_queue,
    create_default_queues,
    remove_patient_from_queue,
)
from app.test.seeders import (
    create_base_seed_patient,
    create_base_seed_professional,
    create_base_seed_queue_manager,
    create_base_seed_risk_classification,
)


@pytest.fixture(scope="module")
def seeded_database(client, database):
    """Seed database"""
    create_default_queues()
    create_base_seed_patient(db)
    create_base_seed_queue_manager(db)
    create_base_seed_professional(db)
    create_base_seed_risk_classification(db)


@pytest.fixture()
def queue_manager_post_json():
    return {"queue_id": 1, "patient_id": 5, "priority_type": "Idoso"}


@pytest.fixture()
def change_patient_queue_json():
    return {"patient_id": 1, "queue_id": 2, "professional_id": 1}


@pytest.mark.usefixtures("seeded_database")
class TestQueueManagerController:

    # --------------------- Get patients in queue ---------------------

    def test_get_patients_in_queue(self, client):
        response = client.get("/queue_manager/1")

        assert response.status_code == 200
        assert len(response.json["items"]) == 3

        self._test_patient_data_in_get_patients_by_queue(
            data=response.json["items"][0],
            patient_id=2,
            priority=True,
            patient_name="Patient teste 2",
            priority_type="Idoso",
        )

        self._test_patient_data_in_get_patients_by_queue(
            data=response.json["items"][1],
            patient_id=1,
            priority=False,
            patient_name="Patient teste 1",
            priority_type=None,
        )

    def test_get_patients_ordered_by_risk_classification(self, client):
        add_patient_in_queue({"patient_id": 6, "queue_id": 2})
        change_patient_queue({"patient_id": 2, "queue_id": 2})

        response = client.get("/queue_manager/2")

        assert response.status_code == 200
        assert len(response.json["items"]) == 5

        assert response.json["items"][0]["patient_id"] == 6
        assert response.json["items"][0]["risk_classification"] == "Emergência"

        assert response.json["items"][1]["patient_id"] == 2
        assert response.json["items"][1]["risk_classification"] == "Muito Urgente"

        assert response.json["items"][2]["patient_id"] == 5
        assert response.json["items"][2]["risk_classification"] == "Urgente"

        assert response.json["items"][3]["patient_id"] == 4
        assert response.json["items"][3]["risk_classification"] == "Pouco Urgente"

        assert response.json["items"][4]["patient_id"] == 3
        assert response.json["items"][4]["risk_classification"] == "Não Urgente"

        remove_patient_from_queue(patient_id=6)
        change_patient_queue({"patient_id": 2, "queue_id": 1})

    def test_get_patients_ordered_by_risk_classification_and_priority(self, client):
        change_patient_queue({"patient_id": 5, "queue_id": 1})

        response = client.get("/queue_manager/1")

        assert response.status_code == 200
        assert len(response.json["items"]) == 4

        assert response.json["items"][1]["patient_id"] == 5
        assert response.json["items"][1]["priority"] == True
        assert response.json["items"][1]["risk_classification"] == "Urgente"

        assert response.json["items"][2]["patient_id"] == 1
        assert response.json["items"][2]["priority"] == False
        assert response.json["items"][2]["risk_classification"] == "Urgente"

        change_patient_queue({"patient_id": 5, "queue_id": 2})

    def test_get_patients_in_unregistered_queue(self, client):
        response = client.get("/queue_manager/0")

        assert response.status_code == 404
        assert response.json["message"] == "queue_not_found"

    # ------------------------ CHANGE PATIENT QUEUE ------------------------

    def test_change_patient_queue_to_unregistered_queue(
        self, client, change_patient_queue_json
    ):
        change_patient_queue_json["queue_id"] = 0

        response = client.patch("/queue_manager", json=change_patient_queue_json)

        assert response.status_code == 404
        assert response.json["message"] == "queue_not_found"

    def test_change_patient_queue_to_unregistered_patient(
        self, client, change_patient_queue_json
    ):
        change_patient_queue_json["patient_id"] = 0

        response = client.patch("/queue_manager", json=change_patient_queue_json)
        assert response.status_code == 404
        assert response.json["message"] == "patient_not_found"

    def test_change_patient_queue_to_unregistered_professional(
        self, client, change_patient_queue_json
    ):
        change_patient_queue_json["professional_id"] = 0

        response = client.patch("/queue_manager", json=change_patient_queue_json)

        assert response.status_code == 404
        assert response.json["message"] == "professional_not_found"

    def test_change_patient_queue_to_destination_equals_current_queue(
        self, client, change_patient_queue_json
    ):
        change_patient_queue_json["queue_id"] = 1

        response = client.patch("/queue_manager", json=change_patient_queue_json)

        assert response.status_code == 409
        assert response.json["message"] == "patient_already_in_destination_queue"

    def test_change_queue_of_patient_with_no_queue_manager(
        self, client, change_patient_queue_json
    ):
        change_patient_queue_json["patient_id"] = 10

        response = client.patch("/queue_manager", json=change_patient_queue_json)

        assert response.status_code == 404
        assert response.json["message"] == "patient_not_entered_hospital"

    def test_change_queue_of_patient_in_no_queue(
        self, client, change_patient_queue_json
    ):
        change_patient_queue_json["patient_id"] = 6

        response = client.patch("/queue_manager", json=change_patient_queue_json)

        assert response.status_code == 409
        assert response.json["message"] == "patient_not_in_queue"

    def test_change_patient_queue(self, client, change_patient_queue_json):
        response = client.patch("/queue_manager", json=change_patient_queue_json)

        assert response.status_code == 200
        assert response.json["message"] == "patient_changed_queue"

        queue_manager_id = self._test_queue_manager_properties(
            patient_id=1,
            queue_id=2,
            status="Aguardando Atendimento Médico",
            priority=False,
            priority_type=None,
        )

        self._test_queue_log_created(queue_manager_id=queue_manager_id, queue_id=2)

        change_patient_queue({"patient_id": 1, "queue_id": 1})

    # --------------------- Add patient in queue ---------------------

    def test_add_patient_in_unregistered_queue(self, client, queue_manager_post_json):
        queue_manager_post_json["queue_id"] = 0

        response = client.post("/queue_manager", json=queue_manager_post_json)

        assert response.status_code == 404
        assert response.json["message"] == "queue_not_found"

    def test_add_unregistered_patient_in_queue(self, client, queue_manager_post_json):
        queue_manager_post_json["patient_id"] = 0

        response = client.post("/queue_manager", json=queue_manager_post_json)

        assert response.status_code == 404
        assert response.json["message"] == "patient_not_found"

    def test_add_patient_already_in_queue(self, client, queue_manager_post_json):
        queue_manager_post_json["patient_id"] = 1

        response = client.post("/queue_manager", json=queue_manager_post_json)

        assert response.status_code == 409
        assert response.json["message"] == "patient_already_in_queue"

    def test_add_patient_in_queue_with_wrong_priority_type(
        self, client, queue_manager_post_json
    ):
        queue_manager_post_json["priority_type"] = "teste"

        response = client.post("/queue_manager", json=queue_manager_post_json)

        assert response.status_code == 400
        assert response.json["message"] == "Input payload validation failed"
        assert "priority_type" in response.json["errors"].keys()

    def test_add_patient_without_queue_manager_and_with_no_priority_in_queue(
        self, client, queue_manager_post_json
    ):
        queue_manager_post_json["patient_id"] = 10
        del queue_manager_post_json["priority_type"]

        response = client.post("/queue_manager", json=queue_manager_post_json)

        assert response.status_code == 201
        assert response.json["message"] == "patient_added_to_queue"

        queue_manager_id = self._test_queue_manager_properties(
            patient_id=10,
            queue_id=1,
            status="Aguardando Acolhimento",
            priority=False,
            priority_type=None,
        )

        self._test_queue_log_created(queue_manager_id=queue_manager_id, queue_id=1)

        queue_manager = QueueManager.query.options(joinedload("queue_logs")).get(
            queue_manager_id
        )

        for queue_log in queue_manager.queue_logs:
            db.session.delete(queue_log)
        db.session.delete(queue_manager)
        db.session.commit()

    def test_add_patient_without_queue_manager_and_with_priority_in_queue(
        self, client, queue_manager_post_json
    ):
        queue_manager_post_json["patient_id"] = 10

        response = client.post("/queue_manager", json=queue_manager_post_json)

        assert response.status_code == 201
        assert response.json["message"] == "patient_added_to_queue"

        queue_manager_id = self._test_queue_manager_properties(
            patient_id=10,
            queue_id=1,
            status="Aguardando Acolhimento",
            priority=True,
            priority_type="Idoso",
        )

        self._test_queue_log_created(queue_manager_id=queue_manager_id, queue_id=1)

        queue_manager = QueueManager.query.options(joinedload("queue_logs")).get(
            queue_manager_id
        )

        for queue_log in queue_manager.queue_logs:
            db.session.delete(queue_log)
        db.session.delete(queue_manager)
        db.session.commit()

    def test_add_patient_with_queue_manager_in_queue(
        self, client, queue_manager_post_json
    ):
        queue_manager_post_json["patient_id"] = 6

        response = client.post("/queue_manager", json=queue_manager_post_json)

        assert response.status_code == 201
        assert response.json["message"] == "patient_added_to_queue"

        queue_manager_id = self._test_queue_manager_properties(
            patient_id=6,
            queue_id=1,
            status="Aguardando Acolhimento",
            priority=True,
            priority_type="Idoso",
        )

        self._test_queue_log_created(queue_manager_id=queue_manager_id, queue_id=1)

        remove_patient_from_queue(patient_id=6)

    def test_add_patient_in_second_queue(self, client):
        remove_patient_from_queue(patient_id=3)

        response = client.post("/queue_manager", json={"patient_id": 3, "queue_id": 2})

        assert response.status_code == 201
        assert response.json["message"] == "patient_added_to_queue"

        queue_manager_id = self._test_queue_manager_properties(
            patient_id=3,
            queue_id=2,
            status="Aguardando Atendimento Médico",
            priority=False,
            priority_type=None,
        )

        self._test_queue_log_created(queue_manager_id=queue_manager_id, queue_id=2)

    # --------------------- Close queue manager ---------------------

    def test_close_queue_manager_after_remove_patient_from_queue(self, client):
        remove_patient_from_queue(patient_id=3)

        response = client.patch("/queue_manager/close/3")

        assert response.status_code == 200
        assert response.json["message"] == "queue_manager_closed"

        self._test_queue_manager_properties(
            patient_id=3,
            queue_id=None,
            status="De alta",
            priority=False,
            priority_type=None,
        )

        add_patient_in_queue({"patient_id": 3, "queue_id": 1})

    def test_close_queue_manager_with_patient_in_queue(self, client):
        response = client.patch("/queue_manager/close/1")

        assert response.status_code == 409
        assert response.json["message"] == "patient_in_queue"

    def test_close_unregistered_queue_manager(self, client):
        response = client.patch("/queue_manager/close/10")

        assert response.status_code == 404
        assert response.json["message"] == "patient_not_entered_hospital"

    def test_close_queue_manager(self, client):
        response = client.patch("/queue_manager/close/6")

        assert response.status_code == 200
        assert response.json["message"] == "queue_manager_closed"

        self._test_queue_manager_properties(
            patient_id=6,
            queue_id=None,
            status="De alta",
            priority=True,
            priority_type="Idoso",
        )

    # --------------------- Remove patient from queue ---------------------

    def test_remove_patient_without_queue_manager_from_queue(self, client):
        response = client.patch("/queue_manager/remove/10", json={})

        assert response.status_code == 404
        assert response.json["message"] == "patient_not_entered_hospital"

    def test_remove_patient_not_in_queue_from_queue(self, client):
        add_patient_in_queue({"patient_id": 6, "queue_id": 2})
        remove_patient_from_queue(patient_id=6)

        response = client.patch("/queue_manager/remove/6", json={})

        assert response.status_code == 409
        assert response.json["message"] == "patient_not_in_queue"

    def test_remove_patient_from_queue_and_unregistered_professional(self, client):
        response = client.patch("/queue_manager/remove/1", json={"professional_id": 0})

        assert response.status_code == 404
        assert response.json["message"] == "professional_not_found"

    def test_remove_patient_from_queue(self, client):
        response = client.patch("/queue_manager/remove/2", json={})

        assert response.status_code == 200
        assert response.json["message"] == "patient_removed_from_queue"

        queue_manager_id = self._test_queue_manager_properties(
            patient_id=2,
            queue_id=None,
            status="Em espera",
            priority=True,
            priority_type="Idoso",
        )

        self._test_queue_log_closed(queue_manager_id=queue_manager_id, queue_id=1)

        add_patient_in_queue({"patient_id": 2, "queue_id": 1})

    def test_remove_patient_from_queue_with_professional(self, client):
        response = client.patch("/queue_manager/remove/7", json={"professional_id": 1})

        assert response.status_code == 200
        assert response.json["message"] == "patient_removed_from_queue"

        queue_manager_id = self._test_queue_manager_properties(
            patient_id=7,
            queue_id=None,
            status="Em espera",
            priority=False,
            priority_type=None,
        )

        self._test_queue_log_closed(
            queue_manager_id=queue_manager_id, queue_id=3, professional_id=1
        )

    # --------------------- Helper functions ---------------------

    def _test_patient_data_in_get_patients_by_queue(
        self,
        data: dict[str, any],
        patient_id: int,
        priority: bool,
        patient_name: str,
        priority_type: Union[str, None],
    ):
        """test patient data in get patients by queue"""
        assert data["patient_id"] == patient_id
        assert data["priority"] == priority
        assert data["patient_name"] == patient_name
        assert data["priority_type"] == priority_type
        assert data["status"] == "Aguardando Acolhimento"
        assert data["queue_entry"] is not None

    def _test_queue_manager_properties(
        self,
        patient_id: int,
        queue_id: int,
        priority: bool,
        priority_type: str,
        status: str,
    ) -> int:
        """test queue manage properties"""
        queue_manager = QueueManager.query.filter(
            QueueManager.patient_id == patient_id
        ).first()

        assert queue_manager is not None
        assert queue_manager.queue_id == queue_id
        assert queue_manager.status == status
        assert queue_manager.priority == priority
        assert queue_manager.priority_type == priority_type

        return queue_manager.id

    def _test_queue_log_created(
        self,
        queue_manager_id: int,
        queue_id: int,
    ):
        """test if queue log was created"""
        queue_log = QueueLog.query.filter(
            QueueLog.queue_manager_id == queue_manager_id, QueueLog.queue_exit.is_(None)
        ).first()

        assert queue_log is not None
        assert queue_log.queue_id == queue_id
        assert queue_log.queue_entry is not None
        assert queue_log.queue_exit is None

    def _test_queue_log_closed(
        self, queue_manager_id: int, queue_id: int, professional_id: int = None
    ):
        """test if queue log was closed"""
        queue_log = (
            QueueLog.query.filter(
                QueueLog.queue_manager_id == queue_manager_id,
            )
            .order_by(QueueLog.id)
            .all()[-1]
        )

        assert queue_log.queue_id == queue_id
        assert queue_log.queue_exit != None
        assert queue_log.professional_id == professional_id
