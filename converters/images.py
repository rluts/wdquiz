import cairosvg
from .files import File


class Image(File):
    allowed_types = ['svg', 'jpg', 'jpeg', 'png']

    def __init__(self, url: str, prefix: int):
        super().__init__(url, prefix)
        if self.file_type == 'svg':
            self.convert_svg()

    def convert_svg(self):
        with open(self.file) as file:
            filename = f'{self.filename}.png'
            cairosvg.svg2png(file_obj=file, write_to=filename)
            self.file = filename
