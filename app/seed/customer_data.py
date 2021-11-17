from faker import Faker
from app.models.customer import Customer
from app import db
from datetime import date, datetime, timezone
import click

def seed():
    """Uses Faker package to generate fake customer data for db."""
    fake = Faker()
    for _ in range(20):
        new_customer = Customer(
            name=fake.name(),
            registered_at=datetime.now(timezone.utc).astimezone(),
            postal_code=fake.postcode(),
            phone=fake.msisdn()[3:]
        )
        db.session.add(new_customer)
    db.session.commit()

    return click.echo('Fake customers added to db.')


