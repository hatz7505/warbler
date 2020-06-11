"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows
from flask import session
from app import CURR_USER_KEY

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

    def test_user_repr(self):
        u = User(
                    email="test@test.com",
                    username="testuser",
                    password="HASHED_PASSWORD"
                )
        db.session.add(u)
        db.session.commit()

        self.assertEqual(u.__repr__(), f'<User #{u.id}: {u.username}, {u.email}>')

    def test_user_following(self):
        """ positive test case for user 1 following user 2 """
        u1 = User(
            email="test1@test.com",
            username="testuser1",
            password="HASHED_PASSWORD"
        )

        u2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD"
        )

        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

        follow = Follows(user_being_followed_id=u2.id, user_following_id=u1.id)

        db.session.add(follow)
        db.session.commit()

        self.assertEqual(u1.is_following(u2), True)
        self.assertEqual(u2.is_followed_by(u1), True)

    def test_user_not_following(self):
        """ negative test case for user 1 following user 2 """
        u1 = User(
            email="test1@test.com",
            username="testuser1",
            password="HASHED_PASSWORD"
        )

        u2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD"
        )

        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

        self.assertEqual(u1.is_following(u2), False)
        self.assertEqual(u1.is_following(u1), False)
        self.assertEqual(u2.is_followed_by(u1), False)
        self.assertEqual(u1.is_following(u1), False)

    def test_user_signup(self):
            user = User.signup(
                username="testsuser", password="HASHED_PASSWORD", email="test2@test.com", image_url="")
        breakpoint()
        print("APPLE", db.session)
            # resp = client.get("/")

            # self.assertEqual(resp.status_code, 302)
            # print("APPLE", session)
            # print(session)
            # self.assertEqual(session["curr_user"], user.id)
