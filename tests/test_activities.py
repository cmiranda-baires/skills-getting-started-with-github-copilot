import pytest


class TestGetActivities:
    """Test the GET /activities endpoint"""
    
    def test_get_all_activities(self, client):
        # Arrange
        expected_activity = "Chess Club"
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert len(activities) > 0
        assert expected_activity in activities
        
    def test_activities_have_required_fields(self, client):
        # Arrange
        required_fields = ["description", "schedule", "max_participants", "participants"]
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert response.status_code == 200
        for name, details in activities.items():
            for field in required_fields:
                assert field in details, f"Activity {name} missing {field}"


class TestSignup:
    """Test the POST /activities/{activity_name}/signup endpoint"""
    
    def test_signup_success(self, client, sample_activity):
        # Arrange
        email = "newemail@mergington.edu"
        activity = sample_activity
        
        # Act
        response = client.post(f"/activities/{activity}/signup?email={email}")
        
        # Assert
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        assert email in response.json()["message"]
        
    def test_signup_adds_participant(self, client, sample_activity):
        # Arrange
        email = "test@mergington.edu"
        activity = sample_activity
        
        # Act
        signup_response = client.post(f"/activities/{activity}/signup?email={email}")
        activities_response = client.get("/activities")
        activities = activities_response.json()
        
        # Assert
        assert signup_response.status_code == 200
        assert email in activities[activity]["participants"]
        
    def test_signup_duplicate_student_error(self, client, sample_activity):
        # Arrange
        email = "michael@mergington.edu"  # Already registered in Chess Club
        activity = sample_activity
        
        # Act
        response = client.post(f"/activities/{activity}/signup?email={email}")
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]
        
    def test_signup_nonexistent_activity(self, client):
        # Arrange
        email = "test@mergington.edu"
        activity = "Nonexistent Club"
        
        # Act
        response = client.post(f"/activities/{activity}/signup?email={email}")
        
        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]
        
    def test_signup_increments_participant_count(self, client, sample_activity):
        # Arrange
        email = "newstudent@mergington.edu"
        activity = sample_activity
        initial_activities = client.get("/activities").json()
        initial_count = len(initial_activities[activity]["participants"])
        
        # Act
        client.post(f"/activities/{activity}/signup?email={email}")
        updated_activities = client.get("/activities").json()
        updated_count = len(updated_activities[activity]["participants"])
        
        # Assert
        assert updated_count == initial_count + 1


class TestUnregister:
    """Test the DELETE /activities/{activity_name}/unregister endpoint"""
    
    def test_unregister_success(self, client, sample_activity):
        # Arrange
        email = "michael@mergington.edu"
        activity = sample_activity
        
        # Act
        response = client.delete(f"/activities/{activity}/unregister?email={email}")
        
        # Assert
        assert response.status_code == 200
        assert "Unregistered" in response.json()["message"]
        
    def test_unregister_removes_participant(self, client, sample_activity):
        # Arrange
        email = "michael@mergington.edu"
        activity = sample_activity
        
        # Act
        unregister_response = client.delete(f"/activities/{activity}/unregister?email={email}")
        activities_response = client.get("/activities")
        activities = activities_response.json()
        
        # Assert
        assert unregister_response.status_code == 200
        assert email not in activities[activity]["participants"]
        
    def test_unregister_decrements_participant_count(self, client, sample_activity):
        # Arrange
        email = "michael@mergington.edu"
        activity = sample_activity
        initial_activities = client.get("/activities").json()
        initial_count = len(initial_activities[activity]["participants"])
        
        # Act
        client.delete(f"/activities/{activity}/unregister?email={email}")
        updated_activities = client.get("/activities").json()
        updated_count = len(updated_activities[activity]["participants"])
        
        # Assert
        assert updated_count == initial_count - 1
        
    def test_unregister_not_registered_error(self, client, sample_activity):
        # Arrange
        email = "notregistered@mergington.edu"
        activity = sample_activity
        
        # Act
        response = client.delete(f"/activities/{activity}/unregister?email={email}")
        
        # Assert
        assert response.status_code == 400
        assert "not registered" in response.json()["detail"]
        
    def test_unregister_nonexistent_activity(self, client):
        # Arrange
        email = "test@mergington.edu"
        activity = "Nonexistent Club"
        
        # Act
        response = client.delete(f"/activities/{activity}/unregister?email={email}")
        
        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]
