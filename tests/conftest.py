import pytest
import copy
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add src to path so we can import the app
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import app as app_module
from app import app

# Store the original activities
ORIGINAL_ACTIVITIES = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Competitive basketball team for interscholastic games",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["alex@mergington.edu"]
    },
    "Tennis Club": {
        "description": "Learn and practice tennis skills",
        "schedule": "Wednesdays and Saturdays, 3:00 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["james@mergington.edu", "lucy@mergington.edu"]
    },
    "Art Studio": {
        "description": "Explore various drawing, painting, and sculpture techniques",
        "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["isabella@mergington.edu"]
    },
    "Music Ensemble": {
        "description": "Join our orchestra and learn to play musical instruments",
        "schedule": "Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 25,
        "participants": ["noah@mergington.edu", "ava@mergington.edu"]
    },
    "Debate Club": {
        "description": "Develop argumentation and public speaking skills",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["benjamin@mergington.edu"]
    },
    "Science Club": {
        "description": "Conduct experiments and explore scientific discoveries",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["mia@mergington.edu", "ethan@mergington.edu"]
    }
}


@pytest.fixture
def client():
    """Provide a TestClient with fresh activities for each test"""
    # Reset activities to original state by updating the module's activities dict
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(ORIGINAL_ACTIVITIES))
    
    yield TestClient(app)
    
    # Cleanup after test
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(ORIGINAL_ACTIVITIES))


@pytest.fixture
def sample_activity():
    """Reference the Chess Club activity for consistency"""
    return "Chess Club"
