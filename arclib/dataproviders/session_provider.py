from abc import ABC, abstractmethod

from arclib.infra.blob import BlobProvider
from arclib.models import Session


class SessionStorageProvider(ABC):
    """Abstract Session storage to Loads and saves sessions in a data store.
    """
    @abstractmethod
    def save_session(self, session: Session) -> None:
        """Save a session."""
        pass

    @abstractmethod
    def load_session(self, session_id: str) -> Session:
        """Load a session by its ID."""
        pass


class BlobSessionStorageProvider(SessionStorageProvider):
    """SessionStorageProvider with sessions stored in JSON backed by a BlobProvider.
    
    Because of the flexibility of BlobProvider, this can work with either cloud blobs,
    the local filesystem, or in-memory blobs for unit tests.
    """
    def __init__(self, blob_provider: BlobProvider, dir_prefix: str = ''):
        """
        :param blob_provider: BlobProvider for storing files.
        :param dir_prefix: Prefix all filenames with the given string.
            By default we put them in a directory based on the current timestamp.
        """
        self.blob_provider = blob_provider
        self.dir_prefix = dir_prefix

    def filename(self, session_id: str) -> str:
        return f"{self.dir_prefix}sessions/s-{session_id}.json"

    def transcript_filename(self, session_id: str) -> str:
        return f"{self.dir_prefix}transcripts/t-{session_id}.md"

    def save_session(self, session: Session) -> None:
        filename = self.filename(session.id)
        content = session.to_json()
        self.blob_provider.save(filename, content)
        transcript_filename = self.transcript_filename(session.id)
        self.blob_provider.save(transcript_filename, session.get_transcript())

    def load_session(self, session_id: str) -> Session:
        filename = self.filename(session_id)
        content = self.blob_provider.load(filename)
        return Session.from_json(content)
