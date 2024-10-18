# storage/storage.py
from abc import ABC, abstractmethod

class Storage(ABC):
    """Abstract base class for storage mechanisms."""

    @abstractmethod
    def store_data(self, extractor):
        """Store data from the extractor into the desired storage medium."""
        pass
