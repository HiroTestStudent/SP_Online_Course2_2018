import unittest
from peewee import *
import donors_sql as d
import create_mr_tables as new_database
from create_mr_tables import *
from create_mr_tables import *
import os



class TestMailbox(unittest.TestCase):
    #database = SqliteDatabase('mailroom.db')
    #database.connect()
    #database.execute_sql('PRAGMA foreign_keys = ON;')

    def test_Individual_Add_Donation1(self):
        #Creating a new database for testing
        new_database.database.init('test1.db')
        database.connect()
        logger.info('Creating Modules in database')
        database.create_tables([new_database.Donor, new_database.Donations])
        database.execute_sql('PRAGMA foreign_keys = ON;')
    # specify database that we are connecting to
        connect = d.Individual('test1.db')
        connect.add_donation('Shane', 5)
            #logger.info('Find and display by selecting a spcific Person name...')
        aperson = Donor.get(Donor.donor_name == 'Shane')

        self. assertEqual(aperson.donor_name, 'Shane')



#    def test_Group_get(self):
#        new_group = d.Group(d.Individual('Joe', [3, 3, 3]))
#        self.assertEqual(new_group._donor_raw['Joe'].donations, [3, 3, 3])
#        self.assertEqual(new_group._donor_raw['Joe'].name, 'Joe')

#    def test_Group_search1(self):
#        """Returns None when name does not exist"""
#        new_group = d.Group(d.Individual('Joe', [3, 3, 3]))
#        self.assertEqual(new_group.search('Bob'), None)

#    def test_Group_search2(self):
#        """Returns 'name' when name does exist"""
#        new_group = d.Group(d.Individual('Joe', [3, 3, 3]))
#        self.assertEqual(new_group.search('Joe').name, 'Joe')

#    def test_Group_Add(self):
#        """Test that the new donors are being appended to the donor list."""
#        new_group = d.Group(d.Individual('Joe', [3, 3, 3]))
#        new_group.add('Jill', 5)
#        self.assertEqual(new_group._donor_raw['Jill'].name, 'Jill')
#        self.assertEqual(new_group._donor_raw['Jill'].donations, [5])

#    def test_thankyou(self):
#        test_text = 'Thank you so much for the generous gift of $5.00, Shane!'
#        new_group = d.Group(d.Individual('Shane', [5]))
#        self.assertEqual(d.Individual('Shane', [5]).thank_you, test_text)

#    def test_summary(self):
#        """Add a donor to the list and test that the donor summary
#        is correct"""
#        new_group = d.Group(d.Individual('Shane', [3]))
#        new_group.add('Joe', 3)
#        new_group.add('Joe', 3)
#        new_group.add('Joe', 3)
#        new_group.add('Jack', 4)
#        new_group.add('Jack', 5)
#        donor_summary = new_group.summary()
#        self.assertEqual(donor_summary, {'Shane': [3, 1, 3],
#                                         'Joe': [9, 3, 3],
#                                         'Jack': [9, 2, 4.5]})
#
#    def test_column_name_width(self):
#        new_group = d.Group(d.Individual('Shane', [3]))
#        donors_f = {'Joe': [9, 3, 3], 'Jack': [9, 2, 4.5]}
#        self.assertEqual(new_group.column_name_width(donors_f), 11)

#    def test_column_name_width_1(self):
#        new_group = d.Group(d.Individual('Shane', [3]))
#        donors_f = {'Joeeeeeeeeee': [9, 3, 3], 'Jack': [9, 2, 4.5]}
#        self.assertEqual(new_group.column_name_width(donors_f), 12)

#    def test_column_total_width(self):
#        new_group = d.Group(d.Individual('Shane', [3]))
#        donors_f = {'Joe': [9, 3, 3], 'Jack': [9, 2, 4.5]}
#        self.assertEqual(new_group.column_total_width(donors_f), 12)

#    def test_column_total_width_2(self):
#        new_group = d.Group(d.Individual('Shane', [3]))
#        donors_f = {'Joe': [1555555555555, 3, 3], 'Jack': [9, 2, 4.5]}
#        self.assertEqual(new_group.column_total_width(donors_f), 16)

#    def test_column_average_width(self):
#        new_group = d.Group(d.Individual('Shane', [3]))
#        donors_f = {'Joe': [9, 3, 3], 'Jack': [9, 2, 4.5]}
#        self.assertEqual(new_group.column_average_width(donors_f), 12)

#    def test_column_average_width_1(self):
#        new_group = d.Group(d.Individual('Shane', [3]))
#        donors_f = {'Joe': [9, 3, 3555555555222], 'Jack': [9, 2, 4.5]}
#        self.assertEqual(new_group.column_average_width(donors_f), 16)

#    def test_column_number_width(self):
#        new_group = d.Group(d.Individual('Shane', [3]))
#        donors_f = {'Joe': [9, 3, 3], 'Jack': [9, 2, 4.5]}
#        self.assertEqual(new_group.column_number_width(donors_f), 12)

#    def test_column_number_width_1(self):
#        new_group = d.Group(d.Individual('Shane', [3]))
#        donors_f = {'Joe': [9, 33333333333333, 35555], 'Jack': [9, 2, 4.5]}
#        self.assertEqual(new_group.column_number_width(donors_f), 17)

#    def test_sort_list(self):
#        new_group = d.Group(d.Individual('Shane', [3]))
#        donors_f = {'Joe': [15, 3, 35], 'Jack': [9, 2, 4.5]}
#        self.assertEqual(new_group.sort_list(donors_f), ['Joe', 'Jack'])

#    def test_sort_list_2(self):
#        new_group = d.Group(d.Individual('Shane', [3]))
#        donors_f = {'Joe': [15, 3, 35], 'Jack': [9, 2, 4.5],
#                    'Fred': [2000, 2, 60]}
#        self.assertEqual(new_group.sort_list(donors_f),
#                         ['Fred', 'Joe', 'Jack'])

#    def test_report(self):
#        new_group = d.Group(d.Individual('Shane', [3]))
#        new_group.add('Joe', 3)
#        new_group.add('Joe', 3)
#        new_group.add('Joe', 3)
#        new_group.add('Jack', 4)
#        new_group.add('Jack', 5)
#        assert "Joe        $" in new_group.report()
#        assert "9.00     3         " in new_group.report()
#        assert '$        3.00' in new_group.report()

#    def test_letters_for_all(self):
#        new_group = d.Group(d.Individual('Shane', [3]))
#        new_group.add('Joe', 3)
#        new_group.add('Joe', 3)
#        new_group.add('Joe', 3)
#        new_group.add('Jack', 4)
#        new_group.add('Jack', 5)
#        try:
#            new_group.letters()
#            with open('Jack.txt', 'rU') as f:
#                text = f.read()
#        finally:
#            os.remove('Jack.txt')

#       expected_text = 'Dear Jack, thank you so much for your last ' \
#                        'contribution of $5.00! You have contributed ' \
#                        'a total of $9.00, and we appreciate your ' \
#                        'support!'
#        self.assertEqual(expected_text, text)

#    def test_number_donations(self):
#        new_group = d.Group(d.Individual('Shane', [3]))
#        new_group.add('Joe', 1)
#        new_group.add('Joe', 4)
#        new_group.add('Joe', 5)
#        self.assertEqual(new_group._donor_raw['Joe'].number_donations(), 3)

#    def test_sum_donations(self):
#        new_group = d.Group(d.Individual('Shane', [3]))
#        new_group.add('Joe', 3)
#        new_group.add('Joe', 3)
#        new_group.add('Joe', 3)
#        self.assertEqual(new_group._donor_raw['Joe'].sum_donations(), 9)

#    def test_avg_donations(self):
#        new_group = d.Group(d.Individual('Shane', [3]))
#        new_group.add('Joe', 10)
#        new_group.add('Joe', 5)
#        new_group.add('Joe', 6)
#        self.assertEqual(new_group._donor_raw['Joe'].avg_donations(), 7)



if __name__ == '__main__':
    unittest.main()
