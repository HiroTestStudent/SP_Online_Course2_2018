#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
import os
import logging
from peewee import *
from create_mailroom_db import *

"""
Created on Wed Apr 3 19:30:19 2019

@author: dennis coffey
"""

"""You work in the mail room at a local charity. Part of your job is to write incredibly boring, 
repetitive emails thanking your donors for their generous gifts. 
You are tired of doing this over and over again, so you’ve decided to let Python help 
you out of a jam and do your work for you."""

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Donor class - contains properties and methods for accessing and updating donor's data
class Donor:
    
    def __init__(self, name, donations=None):
        self.name = name
        if donations == None:
            self._donations = []
        else:
            self._donations = list(donations)
        
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = value
 
    @property
    def donations(self):
        return self._donations
 
    def add_donation(self, amount):
        try:
            self.donations.append(float(amount))
        # Handle error if user doesn't input a valid numerical donation
        except ValueError:
            print('Not a valid donation.')
            prompt_donation(self.name)
    
#    # Create email to donor thanking them for their generous donation
#    def create_email(self, amount):
#        return '\nDear {},\n\nThank you so much for generous donation of ${}.\n\n\t\t\tSincerely,\n\t\t\tPython Donation Team'.format(self.name, amount)

#    def sum_donations(self):
#        return sum(self.donations)
    
#    def number_donations(self):
#        return len(self.donations)
        
#    def avg_donations(self):
#        return self.sum_donations() / self.number_donations()

    
# DonorCollection class - properties and methods for managing collection of donors
class DonorCollection:
        
    def __init__(self, donors=None):
        if donors == None:
            donors = []
        else:
            self._donors = donors

    @property
    def donors(self):
        return self._donors
 
    # Display list of donors by name
    def donor_list(self):
        list_donors = ''
        for donor in self.donors:
            list_donors += donor.name + '\n'
        return list_donors

    # Set donor
    def set_donor(self, full_name):
        exists = False
        # Check if existing donor
        for donor in self.donors:
            if donor.name == full_name:
                exists = True
                break
        # Not existing donor, so create new donor
        if not exists:
            donor = Donor(full_name)
            donors.add_donor(donor)
        return donor

    # Add new donor to donor collection
    def add_donor(self, donor):
        self.donors.append(donor)
        
    # Add new donor to donor collection
    def delete_donor(self):
        """ Delete all donor records"""
        del_donor_name = name_prompt()
        
        # Delete user from database
        try:
            nrows = Donation.delete().where(Donation.donor_name == del_donor_name).execute()
            
        except Exception as e:
            logger.info(f'Error deleting donor from database')
            logger.info(e)
     
#    def sort_on_total_donation(self):
#        return(sorted(self.donors, key=total_donation_key, reverse=True))


    # Create report
    def create_report(self):
        #Create list of summarized donations so that total can be sorted
        try:
            database.connect()
            database.execute_sql('PRAGMA foreign_keys = ON;')
            sorted_donors = (Donation
                     .select(Donation.donor_name,
                             fn.SUM(Donation.donation_amount).alias('sum_donations'),
                             fn.COUNT(Donation.donation_amount).alias('number_donations'),
                             (fn.SUM(Donation.donation_amount)/fn.COUNT(Donation.donation_amount)).alias('avg_donations'))
                     .group_by(Donation.donor_name)
                     .order_by(fn.SUM(Donation.donation_amount).desc()))
            
        except Exception as e:
            logger.info(f'Error retrieving donations from database')
            logger.info(e)
            
        finally:
            print('Database closed - report')
            database.close()
                 
        # Print summarized data
        report = '\nDonor Name                | Total Given | Num Gifts | Average Gift\n'
        report += '-'*66 + '\n'
        for donor in sorted_donors:
                report +=  f'{donor.donor_name: <27}${donor.sum_donations: >12.2f}{donor.number_donations: >12}  ${round(donor.avg_donations,2): >11.2f}\n'
        print(report)
        return report

    # Send letters to everyone
    def send_letters(self):

        now = datetime.datetime.now()
        now = str(now.year) + '-' + str(now.month) + "-" + str(now.day)
        path = os.getcwd() + '/letters'
#        path = os.getcwd()
    
        # Query database for donors and last donation
        try:
            database.connect()
            database.execute_sql('PRAGMA foreign_keys = ON;')
            sorted_donors = (Donation
                     .select(Donation.donor_name,
                             fn.MAX(Donation.donation_amount).alias('last_donation'))
                     .group_by(Donation.donor_name)
                     .order_by(Donation.donor_name))
            
        except Exception as e:
            logger.info(f'Error retrieving donors last donation from database')
            logger.info(e)
            
        finally:
            print('Database closed - send')
            database.close()
            
        # Change directory to letters directory, if it doesn't exist, create it
        try:
            os.chdir(path)
        except FileNotFoundError:
            os.makedirs(path)  
            os.chdir(path)
                
        # Loop through each donor and send thank you email
#        try:
        for donor in sorted_donors:
            with open(donor.donor_name + '_' + str(now) + '.txt', 'w') as outfile:
                print(donor.donor_name)
                outfile.write(donor.create_email(donor.last_donation))
            
        print('\nThe thank you emails were sent!')
#        except:
#            print('\nThere was an error sending the thank you emails.')

# Create dictionary of donors
#donor1 = Donor('Dennis Coffey', [2500.00,400.00,1400.00])
#donor2 = Donor('Bill Gates', [120.00,650.00])
#donor3 = Donor('Ethan Coffey', [800.00,150.00,1100.00])
#donor4 = Donor('Paul Allen', [45000.00,9000.00])
#donor5 = Donor('Jeff Bezos', [3.00])

#donors = DonorCollection([donor1,donor2,donor3,donor4,donor5])
donors = DonorCollection()

# Total donation for sorting
#def total_donation_key(donor):
#    return sum(donor.donations)


# Sending a Thank You
def send_thankyou():
    # Loop if user selects list
    full_name = 'list'
    while full_name.lower() == 'list':
        # Create prompt menu
        full_name = input('Please input your Full Name\n'
                          '\t or list if you would like to see a list of donors >> ')
            
        # Check user input and perform appropriate action    
        if full_name.lower() == 'list':
            # Create list of donors
            print(donors.donor_list())
        else:
            prompt_donation(full_name)
            break

# Prompt for donation amount and append donation to user    
def prompt_donation(full_name, donation_amount = None):
    current_donor = donors.set_donor(full_name)
    # Promt for donation amount
    if donation_amount == None:
        donation_amount = input('Please enter a donation amount $')
    try:
        current_donor.add_donation(donation_amount)
        print(current_donor.create_email(donation_amount))
        
    # Handle error if user doesn't input a valid numerical donation
    except ValueError:
        print('Not a valid donation.')
        prompt_donation(full_name) 

def name_prompt ():
    """Prompt for donor's name to delete"""
    return input('\nPlease enter the name of the Donor you want to delete:  ')

    
# Quit program
def user_quit():
    database.close()
    print("\nThank you, have a nice day.")


if __name__ == '__main__':

    # Loop until user selects Quit
    prompt = None
    switch_action_dict = {'a':send_thankyou, 'b':donors.create_report, 'c': donors.send_letters, 'd': donors.delete_donor, 'e': user_quit}
    while prompt != 'e':
        # Create prompt menu
        prompt = input('Actions to choose from:\n'
                         '\ta) Send a Thank You\n'
                         '\tb) Create a Report\n'
                         '\tc) Send letters to everyone\n'
                         '\td) Delete user\n'
                         '\te) Quit\n'
                         'Please choose an action: ')
        try:
            switch_action_dict.get(prompt)()
        # Handle error for when user does not choose a valid option in the list
        except TypeError:
            print('\nNot a valid option.  Please choose a value from the list (a, b, c, d or e)')
