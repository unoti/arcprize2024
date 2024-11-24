from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Optional

class BlobProvider(ABC):
    """A Blob provider abstraction.
    
    Implementations can be provided for Azure, as well as for the Filesystem and
    in memory for unit tests.
    """
    class NotFoundException(Exception):
        """Exception raised when a blob is not found."""
    
    @abstractmethod
    def save(self, filename: str, content: str) -> None:
        """Save content to a blob storage with the given filename."""

    @abstractmethod
    def load(self, filename: str) -> str:
        """Load content from a blob storage with the given filename."""

    @abstractmethod
    def find(self, prefix: Optional[str] = None) -> List[str]:
        """Find all filenames that start with the given prefix."""

class MemoryBlobProvider(BlobProvider):
    """A BlobProvider implemented using an in-memory dictionary suitable for unit tests."""
    def __init__(self):
        self.storage: Dict[str, str] = {}

    def save(self, filename: str, content: str) -> None:
        self.storage[filename] = content

    def load(self, filename: str) -> str:
        if filename not in self.storage:
            raise BlobProvider.NotFoundException(f"File '{filename}' not found in memory storage.")
        return self.storage[filename]

    def find(self, prefix: Optional[str] = None) -> List[str]:
        if prefix:
            return [filename for filename in self.storage if filename.startswith(prefix)]
        return list(self.storage.keys())


class FileSystemBlobProvider(BlobProvider):
    """A BlobProvider implemented using a directory of the local filesystem for storage.
    """
    def __init__(self, root_path: str):
        self.root_path = Path(root_path)
        self.root_path.mkdir(parents=True, exist_ok=True)

    def save(self, filename: str, content: str) -> None:
        file_path = self.root_path / filename
        with open(file_path, 'w') as file:
            file.write(content)

    def load(self, filename: str) -> str:
        file_path = self.root_path / filename
        if not file_path.exists():
            raise BlobProvider.NotFoundException(f'File {filename} not found.')
        with open(file_path, 'r') as file:
            return file.read()

    def find(self, prefix: Optional[str] = None) -> List[str]:
        if prefix:
            return [str(file.relative_to(self.root_path)) for file in self.root_path.glob(f"{prefix}*")]
        return [str(file.relative_to(self.root_path)) for file in self.root_path.iterdir() if file.is_file()]