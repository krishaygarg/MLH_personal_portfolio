# tests/test_app.py

import unittest
import os

os.environ['TESTING'] = 'true'

from app import app, TimelinePost


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        TimelinePost.delete().execute()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200

        html = response.get_data(as_text=True)
        assert "<title>MLH Fellow</title>" in html

        # TODO Add more tests relating to the home page

    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200

        assert response.is_json

        json = response.get_json()
        assert "timeline_posts" in json
        assert len(json["timeline_posts"]) == 0

        first_post_response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "Alice",
                "email": "alice@example.com",
                "content": "First update"
            }
        )
        assert first_post_response.status_code == 200
        assert first_post_response.is_json

        first_post_json = first_post_response.get_json()
        assert first_post_json["name"] == "Alice"
        assert first_post_json["email"] == "alice@example.com"
        assert first_post_json["content"] == "First update"
        assert "id" in first_post_json
        assert "created_at" in first_post_json

        second_post_response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "Bob",
                "email": "bob@example.com",
                "content": "Second update"
            }
        )
        assert second_post_response.status_code == 200
        assert second_post_response.is_json

        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        json = response.get_json()
        assert len(json["timeline_posts"]) == 2

        # Timeline API returns posts newest first.
        assert json["timeline_posts"][0]["name"] == "Bob"
        assert json["timeline_posts"][0]["email"] == "bob@example.com"
        assert json["timeline_posts"][0]["content"] == "Second update"
        assert json["timeline_posts"][1]["name"] == "Alice"
        assert json["timeline_posts"][1]["email"] == "alice@example.com"
        assert json["timeline_posts"][1]["content"] == "First update"

        timeline_page_response = self.client.get("/timeline")
        assert timeline_page_response.status_code == 200
        timeline_html = timeline_page_response.get_data(as_text=True)
        assert "<title>Krishay Garg | Timeline</title>" in timeline_html
        assert 'id="timeline-form"' in timeline_html
        assert 'name="name"' in timeline_html
        assert 'name="email"' in timeline_html
        assert 'name="content"' in timeline_html
        assert "Updates Feed" in timeline_html
        assert "/api/timeline_post" in timeline_html

    def test_malformed_timeline_post(self):
        # POST request missing name
        response = self.client.post(
            "/api/timeline_post",
            data={
                "email": "john@example.com",
                "content": "Hello world, I'm John!"
            }
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        # POST request with empty content
        response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "John Doe",
                "email": "john@example.com",
                "content": ""
            }
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        # POST request with malformed email
        response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "John Doe",
                "email": "not-an-email",
                "content": "Hello world, I'm John!"
            }
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html
