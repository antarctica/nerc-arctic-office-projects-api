from faker.providers import BaseProvider

localized = False


class Provider(BaseProvider):
    def has_orcid_id(self) -> bool:
        """
        Determines whether an individual has an Orcid ID

        Currently assumes 45% of people will have one, as the popularity of Orcid changes this weighting should be
        changed.

        :example: True
        :rtype: bool
        :return: whether an individual has an Orcid ID
        """
        return self.random_element({True: 0.45, False: 0.55})

    def orcid_id(self) -> str:
        """
        Generates a fake/invalid Orcid ID

        The Orcid Sandbox [1] can be used if more realistic Orcid IDs are needed.

        [1] https://sandbox.orcid.org

        :example: 'https://fake.orcid.org/0000-0001-2345-6789'
        :rtype: str
        :return: a fake Orcid ID
        """
        return f"https://fake.orcid.org/0000-" \
            f"{ str(self.generator.random_int(min=0, max=2)).zfill(4) }-" \
            f"{ str(self.generator.random_int(min=0, max=9999)).zfill(4) }-" \
            f"{ str(self.generator.random_int(min=0, max=9999)).zfill(4) }"

    def has_avatar(self) -> bool:
        """
        Determines whether an individual has an image avatar

        Currently assumes 7% of people will have one, if this likelihood changes, this weighting should be changed.

        :example: True
        :rtype: bool
        :return: whether an individual has an avatar
        """
        return self.random_element({True: 0.07, False: 0.93})

    def avatar(self) -> str:
        """
        Retrieves a random user avatar

        Avatars are taken from https://randomuser.me

        :example: https://randomuser.me/api/portraits/men/12.jpg
        :rtype: str
        :return: URL to a random user avatar
        """
        return f"https://randomuser.me/api/portraits/{ self.random_element(('men', 'women')) }/" \
            f"{ str(self.generator.random_int(min=1, max=99)) }.jpg"

    def avatar_male(self) -> str:
        """
        Retrieves a random male user avatar

        Avatars are taken from https://randomuser.me

        :example: https://randomuser.me/api/portraits/men/12.jpg
        :rtype: str
        :return: URL to a random male user avatar
        """
        return f"https://randomuser.me/api/portraits/men/{ str(self.generator.random_int(min=1, max=99)) }.jpg"

    def avatar_female(self) -> str:
        """
        Retrieves a random female user avatar

        Avatars are taken from https://randomuser.me

        :example: https://randomuser.me/api/portraits/women/12.jpg
        :rtype: str
        :return: URL to a random female user avatar
        """
        return f"https://randomuser.me/api/portraits/women/{ str(self.generator.random_int(min=1, max=99)) }.jpg"
