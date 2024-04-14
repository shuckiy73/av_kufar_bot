import random
import string
from uuid import uuid4


def get_unique_id() -> str:
    unique_part_1 = str(uuid4()).split('-')[-1]
    # unique_part_2 = str(round(random.uniform(0, 100), 3))
    unique_part_3 = random.choice(string.ascii_letters) + random.choice(string.ascii_letters)
    return unique_part_1 + unique_part_3


print(len(get_unique_id()))