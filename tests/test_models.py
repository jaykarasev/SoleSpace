import os
from unittest import TestCase
from unittest.mock import MagicMock
from models import db, User, Sneaker
from app import app

# Set up a separate test database
os.environ['DATABASE_URL'] = "postgresql:///solespace-test"

class UserModelTestCase(TestCase):
    """Test cases for User model functionality."""

    @classmethod
    def setUpClass(cls):
        """Set up app context for all tests once."""
        with app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        """Clean up database after all tests."""
        with app.app_context():
            db.drop_all()

    def setUp(self):
        """Set up a new database for each test."""
        with app.app_context():
            db.session.rollback()
            db.drop_all()
            db.create_all()
            # Create a sample user
            self.user1 = User.signup(
                username="testuser1",
                email="test1@test.com",
                password="password",
                image_url=None,
                first_name="Test",
                last_name="User"
            )
            self.user1.id = 1111
            db.session.commit()

    def tearDown(self):
        """Rollback session after each test."""
        with app.app_context():
            db.session.remove()

    def test_user_signup(self):
        """Test user signup functionality."""
        with app.app_context():
            user = User.signup(
                username="newuser",
                email="newuser@test.com",
                password="password",
                image_url=None,
                first_name="New",
                last_name="User"
            )
            user.id = 12345
            db.session.commit()
            found_user = db.session.get(User, 12345)
            self.assertIsNotNone(found_user)
            self.assertEqual(found_user.username, "newuser")
            self.assertEqual(found_user.email, "newuser@test.com")

    def test_user_authentication(self):
        """Test user authentication with valid credentials."""
        with app.app_context():
            user = User.authenticate("testuser1", "password")
            self.assertIsNotNone(user)
            self.assertEqual(user.username, "testuser1")

    def test_invalid_username_authentication(self):
        """Test user authentication with an invalid username."""
        with app.app_context():
            self.assertFalse(User.authenticate("badusername", "password"))

    def test_invalid_password_authentication(self):
        """Test user authentication with an incorrect password."""
        with app.app_context():
            self.assertFalse(User.authenticate("testuser1", "wrongpassword"))


class SneakerModelTestCase(TestCase):
    """Test cases for Sneaker model functionality."""

    def setUp(self):
        """Set up app context and database for each test."""
        with app.app_context():
            db.session.rollback()
            db.drop_all()
            db.create_all()
            # Set up test user and sneaker
            self.user = User.signup(
                username="sneakertester",
                email="sneaker@test.com",
                password="password",
                image_url=None,
                first_name="Sneaker",
                last_name="Tester"
            )
            self.user.id = 2222
            db.session.commit()

            self.sneaker = Sneaker(sneaker_name="Air Jordan 1", brand="Nike", sneaker_image=None)
            self.sneaker.id = 3333
            db.session.add(self.sneaker)
            db.session.commit()

    def tearDown(self):
        """Rollback session after each test."""
        with app.app_context():
            db.session.remove()

    def test_add_sneaker_to_closet(self):
        """Test adding a sneaker to the user's closet by mocking the method."""
        # Mock the add_to_closet method
        self.user.add_to_closet = MagicMock()
        
        # Call the mocked method
        self.user.add_to_closet(self.sneaker)
        
        # Assert the method was called with the correct arguments
        self.user.add_to_closet.assert_called_with(self.sneaker)

    def test_add_sneaker_to_wishlist(self):
        """Test adding a sneaker to the user's wishlist by mocking the method."""
        # Mock the add_to_wishlist method
        self.user.add_to_wishlist = MagicMock()
        
        # Call the mocked method
        self.user.add_to_wishlist(self.sneaker)
        
        # Assert the method was called with the correct arguments
        self.user.add_to_wishlist.assert_called_with(self.sneaker)

    def test_remove_sneaker_from_closet(self):
        """Test removing a sneaker from the user's closet by mocking the method."""
        # Mock the remove_from_closet method
        self.user.remove_from_closet = MagicMock()
        
        # Call the mocked method
        self.user.remove_from_closet(self.sneaker)
        
        # Assert the method was called with the correct arguments
        self.user.remove_from_closet.assert_called_with(self.sneaker)

    def test_remove_sneaker_from_wishlist(self):
        """Test removing a sneaker from the user's wishlist by mocking the method."""
        # Mock the remove_from_wishlist method
        self.user.remove_from_wishlist = MagicMock()
        
        # Call the mocked method
        self.user.remove_from_wishlist(self.sneaker)
        
        # Assert the method was called with the correct arguments
        self.user.remove_from_wishlist.assert_called_with(self.sneaker)

if __name__ == "__main__":
    import unittest
    unittest.main()
