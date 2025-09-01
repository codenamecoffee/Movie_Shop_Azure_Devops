from dataclasses import dataclass
from typing import Optional, List

@dataclass
class MovieSearchCriteria:
    name: Optional[str] = None
    director: Optional[str] = None
    genres: Optional[List[str]] = None