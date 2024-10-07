import random
import string
from collections import OrderedDict
from faker.providers import BaseProvider

localized = False


def get_string(letters_count, digits_count):
    letters = "".join(
        (random.choice(string.ascii_letters) for i in range(letters_count))  # nosec
    )  # nosec
    digits = "".join(
        (random.choice(string.digits) for i in range(digits_count))  # nosec
    )  # nosec

    # Convert resultant string to list and shuffle it to mix letters and digits
    sample_list = list(letters + digits)
    random.shuffle(sample_list)
    # convert list to string
    final_string = "".join(sample_list)

    return final_string


class Provider(BaseProvider):
    def grid_id(self) -> str:
        """
        Generates a fake/invalid Grid ID

        :example: 'XE-EXAMPLE-grid.5555.5'
        :rtype: str
        :return: a fake Grid ID
        """
        identifier_lengths = [("3", (100, 999)), ("4", (1000, 9999)), ("5", (10000, 99999))]
        identifier_length = random.choices(
            population=[x[0] for x in identifier_lengths],  # Select "3", "4", or "5"
            weights=[0.33, 0.34, 0.33],  # Probabilities for each
            k=1  # Number of selections (1)
        )[0]

        # Find the corresponding range
        identifier_range = next(rng for key, rng in identifier_lengths if key == identifier_length)

        identifier = self.generator.random_int(
            min=identifier_range[0],
            max=identifier_range[1],
        )

        return f"XE-EXAMPLE-grid.5{identifier}.{self.generator.random_int(min=0, max=99)}"



    def ror_id(self) -> str:
        """
        Generates a fake/invalid ROR ID

        :example: '0505m1554'
        :rtype: str
        :return: a fake ROR ID
        """
        fake_ror_id = get_string(4, 5)

        print("fake_ror_id", fake_ror_id)

        return fake_ror_id
