# test_app.py
import pytest
from src.details.app import app, db, Contacts

SECRET_KEY = 'sMAcUgw@*1J038*^UO3Fkpy4%Wil3M'
app.config['SECRET_KEY'] = SECRET_KEY

@pytest.fixture(scope='module')
def in_memory_db():
    with app.app_context():
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db.create_all()  # Create tables for testing
    yield
    with app.app_context():
        db.drop_all()

def create_contact(name="Test Name", email="test@example.com"):
    'function to create a contact for testing'
    contact = Contacts(name=name, email=email)
    db.session.add(contact)
    db.session.commit()
    return contact


#test cases
def test_create_contact(in_memory_db):
    'Test for create functionality.'
    name = "Test Name"
    email = "test@example.com"

    with app.test_client() as client:
        response = client.post('/', data=dict(name=name, email=email))
        assert response.status_code == 200  # Expected redirect"

# Test for update functionality
def test_update_contact(in_memory_db):
    'Test for update functionality'
    with app.app_context():  # Wrap database interaction
        created_contact = create_contact()

        db.session.commit()

        updated_data = {
            "name": "New Name",
            "email": "new@example.com"
        }

        with app.test_client() as client:
            response = client.put(f"/contacts/{created_contact.id}", json=updated_data)
            assert response.status_code == 200, f"Expected status code 200 (OK), got {response.status_code}"

            updated_contact = db.session.get(Contacts, created_contact.id)
            assert updated_contact.name == "New Name"
            assert updated_contact.email == "new@example.com"


def test_update_contact_not_found(in_memory_db):
    'Test for update with non-existent contact functionality'
    invalid_id = 999

    with app.test_client() as client:
        response = client.put('/contacts/99999', json={"name": "Non-existent", "email": "nonexistent@example.com"})
        assert response.status_code == 404, f"Expected status code 404 (Not Found), got {response.status_code}"

def test_delete_contact(in_memory_db):
    'Test for delete functionality'
    with app.app_context():
        contact = create_contact()

        with app.test_client() as client:
            response = client.delete(f"/contacts/{contact.id}")
            assert response.status_code == 200, f"Expected status code 200 (OK), got {response.status_code}"
            deleted_contact = db.session.get(Contacts, contact.id)
            assert deleted_contact is None, "Expected the contact to be deleted"

# Test for delete with non-existent contact
def test_delete_contact_not_gefunden(in_memory_db):
    'Test deleting a non-existent contact functionality.'
    with app.test_client() as client:
        response = client.delete(f"/contacts/99999")
    assert response.status_code == 404, f"Expected status code 404 (Not Found), got {response.status_code}"

# @pytest.fixture
# def in_memory_db():
#     """Fixture to use in-memory SQLite database for tests."""
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
#     with app.app_context():
#         db.create_all()  # Create tables for testing
#     yield
#     with app.app_context():
#         db.drop_all()

# # Your test cases (assuming they're in a file named test_app.py)

# def test_create_contact(in_memory_db):
#     """Test that a new contact can be created successfully."""
#     name = "Test Name"
#     email = "test@example.com"

#     with app.test_client() as client:
#         response = client.post('/', data=dict(name=name, email=email))
#         # Assert the expected response code (e.g., redirect for successful creation)

# def test_invalid_email(in_memory_db):
#     """Test that contact creation fails with an invalid email."""
#     name = "Test Name"
#     email = "invalid_email"

#     with app.test_client() as client:
#         response = client.post('/', data=dict(name=name, email=email))
#         # Assert the expected response code (e.g., error for invalid email)


# export TEST_DB=True
# pytest