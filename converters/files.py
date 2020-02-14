import requests

from core.exceptions import FileTypeError, NotFoundError
from settings import BASE_PATH


class File:
    allowed_types = []

    def __init__(self, url: str, prefix: int):
        self.url = url
        self.file_type = self.get_file_type()
        self.prefix = prefix
        self.filename = self.get_filename()
        self.file = self.download()

    def __str__(self):
        return self.file

    def download(self):
        filename = f'{self.filename}.{self.file_type}'
        with open(filename, 'wb') as handle:
            response = requests.get(self.url)
            if not response.ok:
                raise NotFoundError
            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)
        return filename

    def get_filename(self):
        return f'{BASE_PATH}/media/file{self.prefix}'

    def check_file_type(self, file_type):
        if file_type not in self.allowed_types:
            raise FileTypeError

    def get_file_type(self):
        try:
            file_type = self.url.split('.')[-1]
        except (KeyError, AttributeError):
            raise FileTypeError
        self.check_file_type(file_type)
        return file_type.lower()
