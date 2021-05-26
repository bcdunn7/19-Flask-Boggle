from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class FlaskTests(TestCase):
    """tests for app.py"""

    def test_homepage_routing(self):
        """tests get routing for homepage"""
        with app.test_client() as client:
            resp = client.get('/')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            # page heading
            self.assertIn('<div class="h1 text-center my-4">Boggle!</div>', html)
            # form to submit guesses
            self.assertIn('<label for="guess">Enter guess here:</label>', html)

    def test_correct_word(self):
        """tests whether guess word function correctly checks submitted word"""

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['board'] = [["A","P","P","L","E"],["A","P","P","L","E"],["A","P","P","L","E"],["A","P","P","L","E"],["A","P","P","L","E"]]
            resp = client.get('/check-guess?word=apple')

            self.assertEqual(resp.status_code, 200)
            #check result for apple
            self.assertIn("ok", resp.get_data(as_text=True))

    def test_incorrect_word(self):
        """tests whether an incorrect word is labeled as such"""

        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['board'] = [["A","P","P","L","E"],["A","P","P","L","E"],["A","P","P","L","E"],["A","P","P","L","E"],["A","P","P","L","E"]]
            resp = client.get('/check-guess?word=asdf')

            self.assertEqual(resp.status_code, 200)
            #check result for apple
            self.assertNotIn("ok", resp.get_data(as_text=True))    

