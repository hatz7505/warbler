"""User model tests."""

import os
from unittest import TestCase

from models import db, User, Message, Follows
from flask import session

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app, CURR_USER_KEY
db.create_all()


class UserViewsTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()
        self.user = User.signup(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD",
            image_url=""
        )

    def test_user_login(self):
        with app.test_client() as client:
            resp = client.post('/login',
                               data={"username": self.user.username, "password": self.user.password})
        self.assertEqual(resp.status_code, 200)

    def test_loggedin_user_following_list(self):
        user2 = User.signup(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD",
            image_url=""
        )
        db.session.add(user2)
        db.session.commit()
        follow = Follows(user_being_followed_id=self.user.id, user_following_id=user2.id)
        db.session.add(follow)
        db.session.commit()
        with app.test_client() as client:
            session['curr_user'] = self.user.id
            resp = client.get(f'/users/{user2.id}/following')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'<p class="card-bio">{self.user.bio}</p>', html)
