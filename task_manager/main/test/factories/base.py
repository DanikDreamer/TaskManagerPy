from django.core.files.uploadedfile import SimpleUploadedFile
from faker import Faker
from faker.providers import BaseProvider

faker = Faker()


class ImageFileProvider(BaseProvider):
    def image_file(self, fmt: str = "jpeg") -> SimpleUploadedFile:
        return SimpleUploadedFile(
            self.generator.file_name(extension=fmt),
            self.generator.image(image_format=fmt),
        )
