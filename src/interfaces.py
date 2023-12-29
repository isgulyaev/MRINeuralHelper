from abc import abstractmethod, ABC


class Window:

    def configure(self):
        raise NotImplementedError

    def change_localization(self, language: str):
        raise NotImplementedError


class Downloader(ABC):

    @abstractmethod
    def download(self, url: str, path: str):
        ...
