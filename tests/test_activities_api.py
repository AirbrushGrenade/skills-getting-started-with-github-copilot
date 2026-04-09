"""
Integration tests for the Mergington High School Activities API.
Uses AAA (Arrange-Act-Assert) pattern for clear test structure.
"""
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


class TestGetActivities:
    """Tests for GET /activities endpoint."""

    def test_get_activities_returns_all_activities(self, client):
        """Test that GET /activities returns all available activities."""
        # Arrange
        expected_keys = {"Chess Club", "Programming Class", "Gym Class", "Basketball Team", "Volleyball Club", "Art Club", "Music Ensemble", "Debate Team", "Science Club"}

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        result = response.json()
        assert set(result.keys()) == expected_keys


class TestSignupForActivity:
    """Tests for POST /activities/{activity_name}/signup endpoint."""

    def test_signup_success(self, client):
        """Test successful signup for an activity."""
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 200
        result = response.json()
        assert result["message"] == f"Signed up {email} for {activity_name}"
        # Verify participant was added
        assert email in activities[activity_name]["participants"]

    def test_signup_duplicate_email_raises_error(self, client):
        """Test that signing up with a duplicate email returns an error."""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already registered

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 400
        result = response.json()
        assert "already signed up" in result["detail"].lower()

    def test_signup_invalid_activity_returns_404(self, client):
        """Test that signing up for a non-existent activity returns 404."""
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert
        assert response.status_code == 404
        result = response.json()
        assert "not found" in result["detail"].lower()


class TestUnregisterFromActivity:
    """Tests for POST /activities/{activity_name}/unregister endpoint."""

    def test_unregister_success(self, client):
        """Test successful unregistration from an activity."""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        initial_count = len(activities[activity_name]["participants"])

        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister?email={email}"
        )

        # Assert
        assert response.status_code == 200
        result = response.json()
        assert result["message"] == f"Unregistered {email} from {activity_name}"
        # Verify participant was removed
        assert email not in activities[activity_name]["participants"]
        assert len(activities[activity_name]["participants"]) == initial_count - 1

    def test_unregister_not_registered_returns_error(self, client):
        """Test that unregistering a non-registered student returns an error."""
        # Arrange
        activity_name = "Chess Club"
        email = "notregistered@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister?email={email}"
        )

        # Assert
        assert response.status_code == 400
        result = response.json()
        assert "not registered" in result["detail"].lower()

    def test_unregister_invalid_activity_returns_404(self, client):
        """Test that unregistering from a non-existent activity returns 404."""
        # Arrange
        activity_name = "Nonexistent Activity"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister?email={email}"
        )

        # Assert
        assert response.status_code == 404
        result = response.json()
        assert "not found" in result["detail"].lower()