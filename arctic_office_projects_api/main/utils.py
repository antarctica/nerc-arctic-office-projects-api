import ulid


def generate_neutral_id() -> str:
    """
    Generates a new, unique, 'Neutral ID' using ULIDs (Universally Unique Lexicographically Sortable Identifiers):
    https://github.com/ulid/spec

    These IDs are designed to identify resources without relying on implementation specific identifiers, such as
    database auto-incrementing IDs.

    Example Neutral ID: '01D5M0CFQV4M7JASW7F87SRDYB'

    :rtype str
    :return: Unique neutral ID
    """
    return ulid.new().str
