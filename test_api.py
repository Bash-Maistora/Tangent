from flask import Flask
import pytest, os, tempfile
import unittest
from api import create_app
from api.models import Comment, db


class BasicTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_new_comment(self):
        res = self.client().post('/comments', data={'comment': 'I like dogs.'})
        self.assertEqual(res.status_code, 201)
        self.assertIn('I like dogs.', str(res.data))

    def test_create_new_comment_without_text(self):
        res = self.client().post('/comments')
        self.assertEqual(res.status_code, 400)

    def test_retrieve_comment(self):
        r = self.client().post('/comments', data={'comment': 'I like dogs.'})
        result = self.client().get('/comments/1')
        self.assertEqual(result.status_code, 200)
        self.assertIn('I like dogs.', str(result.data))

    def test_retrieve_missing_comment(self):
        result = self.client().get('/comments/1')
        self.assertEqual(result.status_code, 404)

    def test_update_comment(self):
        r = self.client().post('/comments', data={'comment': 'I like dogs.'})
        result = self.client().put('/comments/1', data={'comment': 'I like cats.'})
        self.assertEqual(result.status_code, 200)
        self.assertIn('I like cats.', str(result.data))

    def test_update_missing_comment(self):
        result = self.client().put('/comments/1', data={'comment': 'I like cats.'})
        self.assertEqual(result.status_code, 404)

    def test_delete_comment(self):
        r = self.client().post('/comments', data={'comment': 'I like dogs.'})
        result = self.client().delete('/comments/1')
        self.assertEqual(result.status_code, 200)
        self.assertIn('Comment 1 has been deleted', str(result.data))

    def test_update_missing_comment(self):
        result = self.client().delete('/comments/1')
        self.assertEqual(result.status_code, 404)

if __name__ == '__main__':
    unittest.main()
