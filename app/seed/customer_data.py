from faker import Faker
from app import db
from app.models.customer import Customer
from datetime import date, datetime, timezone
import random
import time
import click

def random_date():
    """Generate a random date."""
    date = random.randint(1, int(time.time()))
    return datetime.fromtimestamp(date)

def seed():
    """Uses Faker package and random_date function to generate fake customer 
    data for db."""
    fake = Faker()
    for i in range(20):
        new_customer = Customer(
            name=fake.name(),
            registered_at=random_date(),
            postal_code=fake.postcode(),
            phone=fake.msisdn()[3:]
        )
        db.session.add(new_customer)
        db.session.commit()

    return click.echo('Fake customers have been added to db.')


