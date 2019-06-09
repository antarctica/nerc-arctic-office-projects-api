from faker.providers import BaseProvider

localized = False


class Provider(BaseProvider):
    def grid_id(self) -> str:
        """
        Generates a fake/invalid Grid ID

        :example: 'XE-EXAMPLE-grid.5555.5'
        :rtype: str
        :return: a fake Grid ID
        """
        identifier_lengths = {
            '3': (100, 999),
            '4': (1000, 9999),
            '5': (10000, 99999)
        }
        identifier_length = self.random_element({'3': 0.33, '4': 0.34, '5': 0.33})
        identifier = self.generator.random_int(
            min=identifier_lengths[identifier_length][0],
            max=identifier_lengths[identifier_length][1]
        )
        return f"XE-EXAMPLE-grid.5{ identifier }.{ self.generator.random_int(min=0, max=99) }"
