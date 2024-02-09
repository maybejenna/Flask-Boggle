from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):
    def setUp(self):
        """Set up test client and make app available for testing."""
        app.config['TESTING'] = True
        app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
        self.client = app.test_client()

    def tearDown(self):
        """Clean up any fouled transaction."""
        pass  # Add any necessary cleanup steps

    def test_home_route(self):
        """Test the home route."""
        with self.client as client:
            response = client.get('/')
            self.assertIn('board', session)
            self.assertEqual(response.status_code, 200)
            self.assertIn('html', response.content_type)

    def test_handle_guess(self):
        """Test the handle_guess route."""
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [["T", "E", "S", "T", "S"], ["T", "E", "S", "T", "S"], ["T", "E", "S", "T", "S"], ["T", "E", "S", "T", "S"], ["T", "E", "S", "T", "S"]]
            response = client.post('/guess', json={'guess': 'test'})
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertIn('result', data)
            # This assertion may vary based on your Boggle game logic
            self.assertEqual(data['result'], 'ok')

    def test_new_game(self):
        """Test the new_game route."""
        response = self.client.get('/new-game')
        # This should redirect, hence status code 302
        self.assertEqual(response.status_code, 302)

    def test_update_game_statistics(self):
        """Test the update_game_statistics route."""
        with self.client as client:
            response = client.post('/game-statistics', json={'score': 100})
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertEqual(data['num_plays'], 1)
            self.assertEqual(data['highest_score'], 100)