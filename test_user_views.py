"""User model tests."""

import os
from unittest import TestCase

from models import db, User, Message, Follows
from flask import session

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app, CURR_USER_KEY
app.config['WTF_CSRF_ENABLED'] = False
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
        db.session.commit()

    # def test_user_login(self):
    #     with app.test_client() as client:
    #         resp = client.post('/login',
    #                            data={"username": self.user.username, "password": self.user.password})
    #     self.assertEqual(resp.status_code, 200)

    def test_loggedin_user_following_list(self):
        user2 = User.signup(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD",
            image_url=""
        )
        db.session.add(user2)
        db.session.commit()
        follow = Follows(user_being_followed_id=user2.id, user_following_id=self.user.id)
        db.session.add(follow)
        db.session.commit()
        with self.client as c:
            username = user2.username
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user.id
            resp = c.get(f"/users/{self.user.id}/following")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn(f'{username}', html)

    def test_loggedout_user_following_list(self):
        user2 = User.signup(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD",
            image_url=""
        )
        db.session.add(user2)
        db.session.commit()
        follow = Follows(user_being_followed_id=user2.id, user_following_id=self.user.id)
        db.session.add(follow)
        db.session.commit()
        with self.client as c:
            resp = c.get(f"/users/{self.user.id}/following", follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertIn("Access unauthorized.", html)
            self.assertIn('<button class="btn btn-primary btn-block btn-lg">Log in</button>', html)
    
    # def test_loggedin_user_message(self):
    #     with self.client as c:
    #         with c.session_transaction() as sess:
    #             sess[CURR_USER_KEY] = self.user.id
    #         message = Message(text="new message", user_id=self.user.id)
    #         db.session.add(message)
    #         db.session.commit()

    #         resp = c.get(f"/users/{self.user.id}")
    #         html = resp.get_data(as_text=True)
    #         self.assertIn(f"@{self.user.username}", html)
    #         self.assertIn('new message', html)
    #         self.assertEqual(resp.status_code, 200)

    def test_loggedin_user_message(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user.id
            c.post("/messages/new", data={"text": "new message", "user_id": self.user.id})
            resp = c.get(f"/users/{self.user.id}")
            html = resp.get_data(as_text=True)
        
            self.assertIn(f"@{self.user.username}", html)
            self.assertIn('new message', html)
            self.assertEqual(resp.status_code, 200)

    def test_loggedin_user_message_delete(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user.id
            message = Message(text="new message", user_id=self.user.id)
            db.session.add(message)
            db.session.commit()

            resp = c.post(f"/messages/{message.id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertIn(f"@{self.user.username}", html)
            self.assertNotIn('new message', html)
            self.assertEqual(resp.status_code, 200)

    def test_loggedout_user_message(self):
        with self.client as c:
            resp = c.get(f"/messages/new")
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, 'http://localhost/')

            resp = c.get(f"/")
            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, 'http://localhost/login')

            resp = c.get(f"/login")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Access unauthorized.", html)

    # def test_loggedout_user_diffuser_message(self):
    #     with self.client as c:
    #         with c.session_transaction() as sess:
    #             sess[CURR_USER_KEY] = self.user.id
            
    #         user2 = User.signup(
    #         email="test2@test.com",
    #         username="testuser2",
    #         password="HASHED_PASSWORD",
    #         image_url=""
    #         )
    #         db.session.add(user2)
    #         db.session.commit()

    #         message = Message(text="diff user message", user_id=user2.id)
    #         db.session.add(message)
    #         db.session.commit()
