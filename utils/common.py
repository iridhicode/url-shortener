import random
import re
import string


def generate_shorten_url(length: int = 8) -> str:
    characters = string.ascii_letters + string.digits
    shorten_id = ''.join(random.choice(characters) for i in range(length))
    return shorten_id


def sanitize_string(input_string: str) -> str:
    # Remove leading/trailing whitespace
    sanitized_string = input_string.strip()

    # Remove HTML tags
    sanitized_string = re.sub(r'[^\w\-/:.]', '', sanitized_string)

    return sanitized_string
