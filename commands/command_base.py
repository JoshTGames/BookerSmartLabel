from abc import ABC, abstractmethod
import logging

logging.basicConfig(level=logging.INFO)

class Command(ABC):
    """Base class for creating commands"""
    
    name: str = None # Placeholder for higher classes
    """Name of this command"""
    description: str = None # Placeholder for higher classes
    """Description about this command"""

    @abstractmethod
    def usecase(self) -> str:
        """How is this command used?

        Example:
                ping {user} {message}
        """
        return self.name

    @abstractmethod
    def run(self, *args, **kwargs) -> bool:
        """Command classes must implement this method"""
        self.log()
        return True

    def log(self):
        """Outputs to console command usage"""
        logging.info(f'Executing command: {self.name}')
