import os
from unittest import TestCase
from bs4 import BeautifulSoup
from app import app, CURR_USER_KEY
from models import db, User, Sneaker, Closet, Wishlist

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_db'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True

class SoleSpaceIntegrationTestCase(TestCase):
    """Test views for SoleSpace application."""

    def setUp(self):
        """Create test client, add sample data, and log in test user."""
        self.client = app.test_client()
        
        with app.app_context():
            db.create_all()
            
            # Add test data
            test_user = User.signup(username="testuser", 
                                    first_name="Test", 
                                    last_name="User", 
                                    password="password", 
                                    email="test@test.com",
                                    image_url=None)  # Adjust if needed
                                    
            other_user = User.signup(username="otheruser", 
                                     first_name="Other", 
                                     last_name="User", 
                                     password="password", 
                                     email="other@test.com",
                                     image_url=None)  # Adjust if needed
                                     
            sneaker = Sneaker(sneaker_name="Air Jordan 1", brand="Nike")
            db.session.add_all([test_user, other_user, sneaker])
            db.session.commit()
            
            # Save IDs to use in tests
            self.test_user_id = test_user.id
            self.other_user_id = other_user.id
            self.sneaker_id = sneaker.id
            
            # Log in the test user
            with self.client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.test_user_id

    def tearDown(self):
        """Clean up fouled transactions."""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_to_closet_view_closet(self):
        """Test adding a sneaker to the closet and viewing it."""
        with self.client as client, app.app_context():
            # Refetch the sneaker to avoid detached instance
            sneaker = Sneaker.query.get(self.sneaker_id)
            
            # Add sneaker to closet
            response = client.post(f"/users/add_own/{sneaker.id}", follow_redirects=True)
            self.assertEqual(response.status_code, 200)

            # Verify the sneaker is in the closet
            response = client.get(f"/users/{self.test_user_id}/closet")
            self.assertEqual(response.status_code, 200)
            soup = BeautifulSoup(response.data, "html.parser")
            self.assertIsNotNone(soup.find(string="Air Jordan 1"), "Expected sneaker not found in closet.")

    def test_add_to_wishlist_view_wishlist(self):
        """Test adding a sneaker to the wishlist and viewing it."""
        with self.client as client, app.app_context():
            # Refetch the sneaker to avoid detached instance
            sneaker = Sneaker.query.get(self.sneaker_id)
            
            # Add sneaker to wishlist
            response = client.post(f"/users/add_wishlist/{sneaker.id}", follow_redirects=True)
            self.assertEqual(response.status_code, 200)

            # Verify the sneaker is in the wishlist
            response = client.get(f"/users/{self.test_user_id}/wishlist")
            self.assertEqual(response.status_code, 200)
            soup = BeautifulSoup(response.data, "html.parser")
            self.assertIsNotNone(soup.find(string="Air Jordan 1"), "Expected sneaker not found in wishlist.")

    def test_follow_user(self):
        """Test following another user and viewing followers."""
        with self.client as client, app.app_context():
            # Refetch the other user to avoid detached instance
            other_user = User.query.get(self.other_user_id)
            
            # Follow other user
            response = client.post(f"/users/follow/{other_user.id}", follow_redirects=True)
            self.assertEqual(response.status_code, 200)

            # Verify the followed user appears in the test user's following list
            response = client.get(f"/users/{self.test_user_id}/following")
            self.assertEqual(response.status_code, 200)
            soup = BeautifulSoup(response.data, "html.parser")
            self.assertIsNotNone(soup.find(string="otheruser"), "Expected user not found in following list.")
