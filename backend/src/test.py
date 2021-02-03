import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

import api
from database.models import Drink , setup_db ,db_drop_and_create_all


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = api.app
        self.client = self.app.test_client
        
        setup_db(self.app)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)

    def tearDown(self):
        """Executed after reach test"""
        pass

    '''
        def test_get_drinks(self):
        res = self.client().get('/drinks')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
    '''
    
    def test_create_drinks(self):
        json_data = {
            'title': 'jose',
            'recipe':[{'name':'coffee','color':'green','parts':1},
                      {'name':'tea','color':'blue','parts':1}]
        }
        res = self.client().post('/drinks', json=json_data)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        
     
    '''    def test_update_drinks(self):
            json_data = {
                'title': 'tee',
                'recipe': {'name':'tee','color':'blue','parts':2}
            }
            res = self.client().patch('/drinks/1', json=json_data)
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 200)
    '''
    
    
    
    '''
    def test_delete_drinks(self):
            res = self.client().delete('/drinks/1')
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 200)

    
    
    '''
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
