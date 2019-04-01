"""
    Simple database example with Peewee ORM, sqlite and Python
    Here we define the schema
    Use logging for messages so they can be turned off
"""

import logging
from peewee import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('One off program to build the classes from the model in the database')

logger.info('Here we define our data (the schema)')
logger.info('First name and connect to a database (sqlite here)')

logger.info('The next 3 lines of code are the only database specific code')

database = SqliteDatabase('employee.db')
database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only

logger.info('This means we can easily switch to a different database')
logger.info('Enable the Peewee magic! This base class does it all')
logger.info('By inheritance only we keep our model (almost) technology neutral')

class BaseModel(Model):
    class Meta:
        database = database

class Person(BaseModel):
    """
        This class defines Person, name, where they live, and nickname
    """

    logger.info('Note how we defined the class')

    logger.info('Specify the fields in our model, their lengths and if mandatory')
    logger.info('Must be a unique identifier for each person')

    person_name = CharField(primary_key = True, max_length = 30)
    lives_in_town = CharField(max_length = 40)
    nickname = CharField(max_length = 20, null = True)

class Department(BaseModel):
    """
        This class defines Department, which can help track a persons job history
    """
    logger.info('Now the Department class is defined')
    dpt_number = CharField(primary_key=True, max_length=4)
    dpt_name = CharField(max_length=4, null=False)
    dpt_manager = CharField(max_length=30, null=False)

class Job(BaseModel):
    """
        This class defines Job, which maintains details of past Jobs
        held by a Person.
    """

    logger.info('Now the Job class with a simlar approach')
    job_name = CharField(primary_key = True, max_length = 30)
    
    logger.info('Dates')
    start_date = DateField(formats = 'YYYY-MM-DD')
    end_date = DateField(formats = 'YYYY-MM-DD')
    
    logger.info('Number')
    salary = DecimalField(max_digits = 7, decimal_places = 2)
    
    logger.info('Which person had the Job')
    person_employed = ForeignKeyField(Person, related_name='was_filled_by', null = False)
    
    logger.info('Job Duration')
    duration = IntegerField(default=0)
    
    logger.info('Department job is under')
    job_department = ForeignKeyField(Department, related_name='Job under department', null = False)    


database.create_tables([
        Person,
        Job,
        Department,
    ])

database.close()
