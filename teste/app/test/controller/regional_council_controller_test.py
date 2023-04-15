import pytest
from app.main import db
from app.test.seeders import create_base_seed_professional, create_base_seed_regional_council
from app.main.model.agency_model import Agency



@pytest.fixture(scope="module")
def seeded_database(database):
    """Seed database with professional and regional_council data"""
    create_base_seed_professional(db)
    return create_base_seed_regional_council(db)

@pytest.mark.usefixtures("seeded_database")
class TestRegionalCouncilController:

    # GET
    def test_get_all_regional_councils(self, client):
        """Test for get all regional_councils"""
        response = client.get("/professional/regional_council/1")
        assert response.status_code == 200
        assert response.json["items"][0]["regional_council_number"] == "123456"
    
    # POST
    def test_add_regional_council(self, client, base_regional_council):
        """Test for add regional_council"""
        response = client.post("/professional/regional_council/1", json=base_regional_council)
        assert response.status_code == 201
    
    # PUT
    def test_update_regional_council(self, client, base_regional_council):
        """Test for update regional_council"""
        base_regional_council["regional_council_number"] = "654321"
        response = client.put("/professional/regional_council/1", json=base_regional_council)
        print(response.json)
        assert response.status_code == 200

    def test_update_regional_council_with_invalid_id(self, client, base_regional_council):
        """Test for update regional_council with invalid id"""
        base_regional_council["regional_council_number"] = "654321"
        response = client.put("/professional/regional_council/0", json=base_regional_council)
        assert response.status_code == 404
    
    def test_update_regional_council_in_use(self, client, base_regional_council):
        """Test for update regional_council in use"""
        base_regional_council["agency"] = Agency.query.get(2)

        response = client.put("/professional/regional_council/1", json=base_regional_council)

        assert response.status_code == 409
        assert response.json["message"] == "professional_bond_with_occupation_belonging_to_this_regional_council"
        #criar o professional bond para esse regional council

    # DELETE
    def test_delete_regional_council(self, client):
        """Test for delete regional_council"""
        response = client.delete("/professional/regional_council/1")
        print(response.json)
        assert response.status_code == 200
    
    def test_delete_regional_council_with_invalid_id(self, client):
        """Test for delete regional_council with invalid id"""
        response = client.delete("/professional/regional_council/0")
        assert response.status_code == 404

    def test_delete_regional_council_in_use(self, client):
        """Test for delete regional_council in use"""
        response = client.delete("/professional/regional_council/1")
        assert response.status_code == 409
        assert response.json["message"] == "professional_bond_with_occupation_belonging_to_this_regional_council"

    