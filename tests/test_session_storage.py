import unittest

from arclib.infra.blob import MemoryBlobProvider
from arclib.models import (
    DialogRole,
    DialogRow,
    Dialog,
    Session,
)
from arclib.dataproviders import BlobSessionStorageProvider


class TestSessionStorage(unittest.TestCase):
    def setUp(self):
        self.blob = MemoryBlobProvider()
        self.session_storage = BlobSessionStorageProvider(self.blob)

    def test_session_storage(self):
        """We can serialize and deserialize a session."""
        # Arrange.
        rows = [
            DialogRow(role=DialogRole.SYSTEM, text='instructions are here'),
            DialogRow(role=DialogRole.USER, text='Unlock the doors and turn on the lights and flip the sign to Open'),
        ]
        dialog = Dialog(rows=rows)
        session = Session(dialog=dialog)

        # Act.
        self.session_storage.save_session(session)
        filenames = self.blob.find()
        session2 = self.session_storage.load_session(session.id)

        # Assert.
        self.assertEqual(1, len(filenames), "We should have one file now, the saved session.")
        session_filename = filenames[0]
        self.assertTrue(session_filename.startswith('sessions/s-'), 'Filename should be like sessions/s-something.json')
        self.assertTrue(session_filename.endswith('.json'), 'Filename should be like sessions/s-something.json')

        self.assertEqual(session.id, session2.id)
        self.assertEqual(len(session.dialog.rows), len(session2.dialog.rows))
        for row, row2 in zip(session.dialog.rows, session2.dialog.rows):
            self.assertEqual(row.text, row2.text)
            self.assertEqual(row.role, row2.role)
        
        self.assertListEqual(session.dialog.as_tuples(), session2.dialog.as_tuples())