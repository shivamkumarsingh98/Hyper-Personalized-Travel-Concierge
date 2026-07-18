from abc import ABC, abstractmethod
from typing import Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    async def execute(self, db: AsyncSession, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes the agent logic with the given payload.
        """
        pass
