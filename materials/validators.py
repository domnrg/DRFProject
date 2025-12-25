from rest_framework.serializers import ValidationError
from urllib.parse import urlparse


class YoutubeLinkValidator:
    def __call__(self, value):
        if value is None:
            return

        parsed_url = urlparse(value)

        if "youtube.com" not in parsed_url.netloc:
            raise ValidationError("Можно использовать только ссылки на youtube.com")
