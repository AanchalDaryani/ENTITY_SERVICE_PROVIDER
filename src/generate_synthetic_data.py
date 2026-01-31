from faker import Faker
import random
from datetime import date, timedelta

fake = Faker()


def generate_entities(n=1000):
    """
    Generates a list of fake entity names.
    """
    return [fake.company() for _ in range(n)]


def generate_service_providers():
    """
    Returns a fixed list of service providers.
    """
    return [
        ("Deloitte", "Auditor"),
        ("KPMG", "Auditor"),
        ("EY", "Auditor"),
        ("State Street", "Custodian"),
        ("BNY Mellon", "Custodian"),
        ("Northern Trust", "Custodian"),
        ("Apex Fund Services", "Administrator"),
        ("SS&C", "Administrator")
    ]


def generate_relationship_dates():
    """
    Generates realistic start and end dates.
    """
    start = fake.date_between(start_date="-5y", end_date="-1y")
    end = start + timedelta(days=random.randint(365, 1500))
    return start, end
