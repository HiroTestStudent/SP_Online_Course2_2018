import logging
from peewee import *
from create_mr_tables import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
import create_mr_tables as new_database
#database = SqliteDatabase(None)
#d.database.init(file_name)
#database = SqliteDatabase('mailroom.db')
#database.connect()
#database.execute_sql('PRAGMA foreign_keys = ON;') # needed for sqlite only






class Group:
    """This Class will be used to query the database and return the results
    of the required queries."""

    def __init__(self, filename):
        new_database.database.init(filename)
        self.filename = filename

    def search(self, search_for):
        database.connect()
        logger.info('Connected to database')
        database.execute_sql('PRAGMA foreign_keys = ON;')
        try:
            with database.transaction():
                logger.info(f'Searching through donors for {search_for}.')
                query = Donor.get_or_none(Donor.donor_name == search_for)  # Select all donors
        except Exception as e:
            logger.info(f'Error searching for donors.')
            logger.info(e)
            logger.info('Failed to execute donor search.')
        finally:
            logger.info('database closes')
            database.close()
        return query


    def print_donors(self):
        # This prints the list of donors
        database.connect()
        logger.info('Connected to database')
        database.execute_sql('PRAGMA foreign_keys = ON;')
        try:
            with database.transaction():
                logger.info('Trying print all the donors.')
                query = Donor.select()  #  Select all donors
                for donor in query:
                    print(donor.donor_name)

        except Exception as e:
            logger.info(f'Error printing donors.')
            logger.info(e)
            logger.info('Failed to print a list of donors.')
        finally:
            logger.info('database closes')
            database.close()

    def summary(self):
        """Create a new dictionary with Total, number of donations,
        and average donation amount"""
        database.connect()
        logger.info('Connected to database')
        database.execute_sql('PRAGMA foreign_keys = ON;')
        #indiv = Individual(self.filename)  # passes .db filename to Individual Class and initiates class.
        donor_summary = {}

        try:
            with database.transaction():
                donor_list = Donor.select(Donor.donor_name)
                logger.info(f'Printing a list of all the donors in the database')
                for donor in donor_list:
                    logger.info(f'{donor.donor_name}')
                    donor_summary[donor.donor_name] = [Individual.sum_donations(donor.donor_name),
                                                       Individual.number_donations(donor.donor_name),
                                                       Individual.avg_donations(donor.donor_name)]
        except Exception as e:
            logger.info(f'Error creating database summary.')
            logger.info(e)
            logger.info('Failed to iterate through database to create a summary.')
        finally:
            logger.info('database closes')
            database.close()
            return donor_summary

    @staticmethod
    def column_name_width(donor_summary):
        name_list = list(donor_summary.keys())  # creates a list of keys
        name_wi = 11  # Establish minimum column width
        for i in name_list:
            if len(i) > name_wi:
                name_wi = (len(i))  # width of name column
        return name_wi

    @staticmethod
    def column_total_width(donor_summary):
        tot_wi = 12
        for name, summary in donor_summary.items():
            if len(str(summary[0])) > tot_wi:
                # width of total column
                tot_wi = (len(str(summary[0]))) + 3
                # width of number of donations column
        return tot_wi

    @staticmethod
    def column_average_width(donor_summary):
        ave_wi = 12
        for name, summary in donor_summary.items():
            if len(str(summary[2])) > ave_wi:
                # width of total column
                ave_wi = (len(str(summary[2]))) + 3
                # width of number of donations column
        return ave_wi

    @staticmethod
    def column_number_width(donor_summary):
        num_wi = 12
        for name, summary in donor_summary.items():
            if len(str(summary[1])) > num_wi:
                # width of total column
                num_wi = (len(str(summary[1]))) + 3
                # width of number of donations column
        return num_wi

    @staticmethod
    def sort_list(donor_summary):
        list_sorted = sorted(donor_summary,
                             key=donor_summary.__getitem__, reverse=True)
        return list_sorted

    def report(self):
        """Return a report on all the donors"""
        donor_summary = self.summary()
        name_wi = Group.column_name_width(donor_summary)
        tot_wi = Group.column_total_width(donor_summary)
        num_wi = Group.column_number_width(donor_summary)
        ave_wi = Group.column_average_width(donor_summary)

        list_sorted = Group.sort_list(donor_summary)

        rows = ['\n''A summary of your donors donations:',
                f"{'Donor Name':{name_wi}}| {'Total Given':^{tot_wi}}| "
                f"{'Num Gifts':^{num_wi}}| {'Average Gift':^{ave_wi}}",
                f"{'-':-^{(name_wi+tot_wi+ave_wi+num_wi+8)}}"]

        for key in list_sorted:
            temp = donor_summary[key]
            rows.append(f"{key:{name_wi}}${temp[0]:{tot_wi}.2f}"
                        f"{temp[1]:^{num_wi}}   "
                        f"${temp[2]:>{ave_wi}.2f}")

        return '\n'.join(rows)

    def letters(self):
        """Send letters to everyone base on thier last donation amount."""
        database.connect()
        logger.info('Connected to database')
        database.execute_sql('PRAGMA foreign_keys = ON;')
        #indiv = Individual(self.filename)  # passes .db filename to Individual Class and initiates class.
        try:
            with database.transaction():
                donor_list = Donor.select(Donor.donor_name)
                logger.info(f'Sending a thank you to every donor in database.')
                for donor in donor_list:
                    logger.info(f'{donor.donor_name}')
                    letter = f'Dear {donor.donor_name}, thank you so much for your ' \
                             f'last contribution of ${Individual.last_donation(donor.donor_name):.2f}! ' \
                             f'You have contributed a total of $' \
                             f'{Individual.sum_donations(donor.donor_name):.2f}, ' \
                             f'and we appreciate your support!'
                    # Write the letter to a destination
                    with open(donor.donor_name + '.txt', 'w') as to_file:
                        to_file.write(letter)
        except Exception as e:
            logger.info(f'Error writing letters to everyone.')
            logger.info(e)
        finally:
            logger.info('database closes')
            database.close()






class Individual:
    """Creates Class Individual, except instead of returning an instance
    of a class, we will now create a table 'Individual' in an SQL database
    with the following properties 'name', 'donation', '"""
    def __init__(self, filename):
        new_database.database.init(filename)
        #self.database = new_database.database
        #self.filename = filename

    @staticmethod
    def add_donation(person, contribution):
        #database = SqliteDatabase(self.filename)
        database.connect(reuse_if_open=True)
        logger.info('Connected to database')
        database.execute_sql('PRAGMA foreign_keys = ON;')

        try:
            with database.transaction():
                logger.info('Trying to add new donor.')
                new_donor = new_database.Donor.get_or_create(donor_name=person)
                #new_donor.save()
                logger.info(f'Success adding donor {person}.')

            with database.transaction():
                logger.info('Trying to add new donation.')
                new_donation = new_database.Donations.create(
                        donor_name=person,
                        donation=contribution)
                new_donation.save()
                logger.info(f'Database added a donation of '
                            f'{contribution} by {person}.')

                #query = Donations.select()
            #for donation in query:
                    #logger.info(f'{donation.donor_name} donated {donation.donation}')

        except Exception as e:
            logger.info(f'Error creating = {person}')
            logger.info(e)
            logger.info('Failed to add new donor.')
        finally:

            logger.info('database closes')
            database.close()

    @staticmethod
    def number_donations(name):
        #database = SqliteDatabase(self.filename)
        database.connect(reuse_if_open=True)
        logger.info('Connected to database')
        database.execute_sql('PRAGMA foreign_keys = ON;')

        try:
            with database.transaction():
                logger.info('Trying to count number of donations.')
                query = Donations.select().where(Donations.donor_name == name)
                donation_list = [] # Create a list of donations for 'name'.
                for result in query:
                    #logger.info(f'{result.donor_name}')
                    donation_list.append(int(result.donation))
        except Exception as e:
            logger.info(f'Error counting # of donations.')
            logger.info(e)
        finally:
            #logger.info('database closes')
            #database.close()
            logger.info(f'Returning the # of donations made by {name}')
            return int(len(donation_list))

    @staticmethod
    def sum_donations(name):
        #database = SqliteDatabase(self.filename)
        database.connect(reuse_if_open=True)
        logger.info('In Individual.sum_donations')
        database.execute_sql('PRAGMA foreign_keys = ON;')

        try:
            with database.transaction():
                logger.info(f'Summing all the donations by {name}.')
                query = Donations.select().where(Donations.donor_name == name)
                donation_list = [] # Create a list of donations for 'name'.
                for result in query:
                    #logger.info(f'{result.donor_name}')
                    donation_list.append(int(result.donation))
        except Exception as e:
            logger.info(f'Error counting # of donations.')
            logger.info(e)
        finally:
            #logger.info('database closes')
            #database.close()
            logger.info(f'Returning the # of donations made by {name}')
            return sum(donation_list)

    @staticmethod
    def avg_donations(name):
        return Individual.sum_donations(name)/Individual.number_donations(name)

    @staticmethod
    def last_donation(name):
        database.connect(reuse_if_open=True)
        logger.info('Connected to database')
        database.execute_sql('PRAGMA foreign_keys = ON;')

        try:
            with database.transaction():
                logger.info(f'Trying to find the last record of {name}.')
                query = Donations.select().where(Donations.donor_name == name).order_by(Donations.id)
                donation_list = [] # Create a list of donations for 'name'.
                for result in query:
                    #logger.info(f'{result.donor_name}')
                    donation_list.append(int(result.donation))
        except Exception as e:
            logger.info(f'Error finding last donation.')
            logger.info(e)
        finally:
            #logger.info('database closes')
            #database.close()
            logger.info(f'Returning the last donation made by {name}.')
            return donation_list[-1]

    @staticmethod
    def thank_you(person, contribution):
        """Add a donation to a donors records and print a report."""
        return ('Thank you so much for the generous gift of ${0:.2f}, {1}!'
                .format(contribution, person))

    @staticmethod
    def delete_donor(person):
        #database = SqliteDatabase(self.filename)
        database.connect()
        logger.info('Connected to database')
        database.execute_sql('PRAGMA foreign_keys = OFF;')

        try:
            with database.transaction():
                logger.info('Trying to delete donor.')
                Donations.delete().where(Donations.donor_name == person).execute()
                Donor.delete().where(Donor.donor_name == person).execute()
                logger.info(f'Success deleting donor {person}.')

        except Exception as e:
            logger.info(f'Error deleting {person}')
            logger.info(e)
            logger.info('Failed to delete donor.')
        finally:

            logger.info('database closes')
            database.close()


#database.create_tables([Donor, Donations])
#database.close()

