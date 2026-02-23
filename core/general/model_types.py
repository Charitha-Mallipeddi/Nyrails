from django.db.models import IntegerChoices


class CommonCourtesyTitles(IntegerChoices):
    """
    Defines common courtesy titles (aka salutations).

    Attributes:
        MISTER (int): For adult men.
        MISTRESS (int): For married women.
        MIZ (int): For adult women, marital status irrelevant
        MISS (int): For unmarried women (less common now)
        MIX (int): Gender-neutral title, for anyone.
        DOCTOR (int): For those with a doctorate.
        PROFESSOR (int): For academics (outranks Dr.)
    """

    MISTER = 0, "Mr."
    """For adult men."""
    MISTRESS = 1, "Mrs."
    """For married women."""
    MIZ = 2, "Ms."
    """For adult women, marital status irrelevant"""
    MISS = 3, "Miss"
    """For unmarried women (less common now)"""
    MIX = 4, "Mx."
    """Gender-neutral title, for anyone."""
    DOCTOR = 5, "Dr."
    """For those with a doctorate."""
    PROFESSOR = 6, "Prof."
    """For academics (outranks Dr.). """


class ZoneStationType(IntegerChoices):
    """
    Defines common zone station types

    Attributes:
        NULL (int): Dummy (NULL) Entry
        ZONE (int): Zone
        STATION (int): Station
        CONNECTION (int): Connection Service
    """

    NULL = (0, "Dummy (NULL) Entry")
    ZONE = (1, "Zone")
    STATION = (2, "Station")
    CONNECTION = (3, "Connecting Service")
