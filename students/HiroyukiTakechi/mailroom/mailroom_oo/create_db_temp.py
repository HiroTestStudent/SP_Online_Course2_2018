"""
    Mailroom Create Database
"""

import logging
from peewee import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


database = SqliteDatabase('mailroom.db')
database.connect()
database.execute_sql('PRAGMA foreign_key = ON;')


class BaseModel(Model):
    class Meta:
        database = database


class Donor(BaseModel):
    """
        This class defines Donor, which maintains details of someone
        for whom we want to dononate.
    """

    logger.info('Note how we defined the Donor class')
    logger.info('Specify the fields in our model...')

    donor_id = CharField(primary_key = True)
    donor_name = CharField(max_length = 40) 


class Donations(BaseModel):
    """
        This class defines Donations, which maintains details of donnations
        made by Donors
    """

    logger.info('Note how we defined the Make_Donations class')

    donation_id = CharField(primary_key = True)
    donation_amount = FloatField(default=8)
    donor_id = ForeignKeyField(Donor, null-False)


db_exist = database.table_exists('donor')


database.create_tables([
        Donor,
        Donations])


DONOR_ID = 0
DONOR_NAME = 1
DONATION_ID = 2
DONATION_AMOUNT = 3

Donors = [
        ('D-id001', 'William Gates III', 'Da-id001', 20000),
        ('D-id001', 'William Gates III', 'Da-id002', 30000),
        ('D-id001', 'William Gates III', 'Da-id003', 50000),
        ('D-id002', 'Jeff Bezos', 'Da-id004', 100000),
        ('D-id002', 'Jeff Bezos', 'Da-id005', 50000),
        ('D-id002', 'Jeff Bezos', 'Da-id006', 400000),
        ('D-id003', 'Warren Buffet', 'Da-id007', 30000),
        ('D-id003', 'Warren Buffet', 'Da-id008', 400000),
        ('D-id003', 'Warren Buffet', 'Da-id009', 1000000),
        ('D-id004', 'Hiro Takechi', 'Da-id010', 50),
        ('D-id004', 'Hiro Takechi', 'Da-id011', 20),
        ('D-id004', 'Hiro Takechi', 'Da-id012', 30)
        ]

if not db_exist:
    """ initialize database with donors"""

    for item in Donors:
        with database.transaction():
            new_donor = Donor.create(
                donor_id = item[DONOR_ID],
                donor_name = item[DONOR_NAME],
                total_amount = sum(item[DONATION_AMOUNT]),
                number_amount = len(item[DONATION_AMOUNT]))

            new_donor.save()

            for amount in item[DONATION_AMOUNT]:
                new_donations = Donations.create(
                    new_donation = amount,
                    donor_names = item[DONOR_NAME])
                new_donations.save()

logger.info('Database add successful')

logger.info('Databased closed')
database.close()
