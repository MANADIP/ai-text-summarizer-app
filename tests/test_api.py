"""Tests for Text Summarizer API"""

import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


class TestHealthEndpoint:
    """Tests for health check endpoint"""
    
    def test_health_check(self):
        """Test health check endpoint returns 200"""
        response = client.get("/health")
        assert response.status_code == 200
        assert "status" in response.json()
        assert response.json()["status"] == "healthy"


class TestHomeEndpoint:
    """Tests for home page endpoint"""
    
    def test_home_page(self):
        """Test home page loads successfully"""
        response = client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]


class TestSummarizeEndpoint:
    """Tests for summarization endpoint"""
    
    def test_summarize_valid_input(self):
        """Test summarization with valid input"""
        payload = {
            "dialogue": "Artificial intelligence is transforming industries. "
                       "Machine learning models can now process vast amounts of data "
                       "and make intelligent predictions. This technology is revolutionizing "
                       "healthcare, finance, and many other sectors."
        }
        response = client.post("/summarize", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "summary" in data
        assert isinstance(data["summary"], str)
        assert len(data["summary"]) > 0
    
    def test_summarize_missing_field(self):
        """Test summarization with missing dialogue field"""
        payload = {"text": "This should fail"}
        response = client.post("/summarize", json=payload)
        assert response.status_code == 422  # Validation error
    
    def test_summarize_empty_text(self):
        """Test summarization with empty text"""
        payload = {"dialogue": ""}
        response = client.post("/summarize", json=payload)
        assert response.status_code == 422  # Validation error
    
    def test_summarize_too_long_text(self):
        """Test summarization with excessively long text"""
        payload = {"dialogue": "word " * 10000}  # Create very long text
        response = client.post("/summarize", json=payload)
        # Should either succeed with truncation or return validation error
        assert response.status_code in [200, 422]


class TestAPIDocumentation:
    """Tests for API documentation endpoints"""
    
    def test_swagger_ui(self):
        """Test Swagger UI is accessible"""
        response = client.get("/docs")
        assert response.status_code == 200
        assert "swagger" in response.text.lower()
    
    def test_openapi_schema(self):
        """Test OpenAPI schema is available"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert "paths" in data
        assert "/summarize" in data["paths"]


# Example pytest fixture for common test data
@pytest.fixture
def sample_text():
    """Sample text for testing"""
    return (
        "The rapid advancement of artificial intelligence and machine learning "
        "has fundamentally transformed how we process information. These technologies "
        "are now integral to numerous industries, from healthcare diagnostics to "
        "financial forecasting. AI systems can analyze vast datasets in seconds, "
        "identifying patterns that humans might miss. However, with great power comes "
        "great responsibility, and the ethical implications of AI deployment require "
        "careful consideration."
    )
