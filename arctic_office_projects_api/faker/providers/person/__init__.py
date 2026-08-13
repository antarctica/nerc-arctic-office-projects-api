from faker.providers import BaseProvider


class Provider(BaseProvider):
    def male_or_female(self) -> bool:
        """
        Determines if an individual is male or female

        :example: 'female'
        :rtype: str
        :return: whether an individual is male or female
        """
        return self.random_element(("male", "female"))
