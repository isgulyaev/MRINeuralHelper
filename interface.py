from abc import abstractmethod, ABC


class NeuroHelper(ABC):
    
    @abstractmethod
    def predict(self):
        ...

    @abstractmethod
    def segment(self):
        ...
