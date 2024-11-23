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
    def __init__(self, blob_provider: BlobProvider):
        self.blob_provider = blob_provider

    def filename(self, session_id: str) -> str:
        return f"sessions/s{session_id}.json"

    def save_session(self, session: Session) -> None:
        filename = self.filename(session.id)
        content = session.to_json()
        self.blob_provider.save(filename, content)

    def load_session(self, session_id: str) -> Session:
        filename = self.filename(session_id)
        content = self.blob_provider.load(filename)
        return Session.from_json(content)
