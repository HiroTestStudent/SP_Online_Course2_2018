# ------------------------------------------------- #
# Title: Lesson 8, NOSQL
# Dev:   Craig Morton
# Date:  1/15/2019
# Change Log: CraigM, 1/15/2018, NOSQL
# ------------------------------------------------- #

#!/usr/bin/env python3

from ast import literal_eval
from decimal import Decimal
from pprint import pprint as pp
import logging
import login_database
import redis
import pickle
import sys
import utilities


log = utilities.configure_logger('default', '../logs/mongodb_script.log')
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_name_list():
    """Returns a list of all Donors"""
    donor_list  = []
    for item in r.keys():
        donor_list.append(item)
    return list(donor_list)


def print_names():
    """Prints list of names from name list."""
    for name in generate_name_list():
        print(name)


def get_email(current_donation):
    """Prints donation thank you letter."""
    return "Dear {:s},\n\
        Thank you for the generous donation of ${:,.2f}.\n\
        Sincerely,\n\
        Your Local Charity".format(*current_donation)


def add_donation():
    """User prompt to add donation"""
    temp_list = []
    donor_name = get_donor_name()
    if (donor_name != 'exit'):
        temp_list.append(donor_name)
        donation_amt = get_new_donor_amount()
        if (donation_amt != 'exit'):
            temp_list.append(float(donation_amt))
            logger.info("{} has donated {}".format(*temp_list))
            logger.info("Connecting to DB, to add to the Donor records")
            if donor_name in generate_name_list():
                dn_list = get_donation_list(donor_name)
                dn_list.append(temp_list[1])
                r.hmset(donor_name, {'donations': dn_list})
                print("Database has been updated.")
            else:
                dn_phone = get_phone()
                dn_zip = int(get_zip())
                r.hmset(donor_name,
                    {'phone': dn_phone,
                    'zip': dn_zip,
                    'donations': [temp_list[1]]})
            logger.info('Database add successful')
            print(get_email(temp_list))


def delete_donor():
    """Remove Donor from database"""
    logger.info("Connecting to DB, to delete a Donor record")
    donor_name = get_donor_name()
    if donor_name in generate_name_list():
        r.delete(donor_name)
    logger.info('Database delete successful')


def update_donor():
    """Update Donor data"""
    logger.info("Connecting to DB, to update a Donor record")
    donor_name = get_donor_name()
    if donor_name in generate_name_list():
        donor_phn = r.hmget(donor_name, 'phone')[0]
        donor_zip = r.hmget(donor_name, 'zip')[0]
        donor_dns = r.hmget(donor_name, 'donations')[0]
        print("{}'s phone number is: {}".format(donor_name, donor_phn))
        print("{}'s zip code is: {}".format(donor_name, donor_zip))
        print("{} has previously donated: {}".format(donor_name, donor_dns))
        option = prompt_update_opts()
        if option == '1':
            new_phn = get_phone()
            r.hmset(donor_name, {'phone': new_phn})
            logger.info('Database update successful')
        elif option == '2':
            new_zip = int(get_zip())
            r.hmset(donor_name, {'zip': new_zip})
            logger.info('Database update successful')
        elif option == '3':
            new_dn_list = []
            new_dn_amt = get_new_donor_amount()
            print("Type 'no' if you want to stop adding donations.")
            while (new_dn_amt != 'no'):
                if float(new_dn_amt) <= 0:
                    print("Invald input.")
                else:
                   new_dn_list.append(float(new_dn_amt))
                new_dn_amt = get_new_donor_amount()
            if len(new_dn_list) != 0:
                r.hmset(donor_name, {'donations': new_dn_list})
                logger.info('Database update successful')
        else:
            print("Cancelling update.")
    else:
        print("Name not found.")


def prompt_update_opts():
    """User menu"""
    response = input("\n\
        Choose from one of 3 actions:\n\
        1) Update Phone Number\n\
        2) Update Zip Code\n\
        3) Update Donations\n\
        0) Cancel\n\
        Please type 1, 2, 3, or 0: ")
    return response


def send_letters():
    """Send thank you letter to all Donors"""
    message = "Dear {:s},\n\
    Thank you for donating ${:,.2f}.\n\
    Sincerely,\n\
    Your Local Charity"
    for item in r.keys():
        dn_list = get_donation_list(item)
        with open(item + ".txt",'w') as output:
            output.write(message.format(item, sum(dn_list)))
    print("Letters have been generated.")


def generate_report():
    """Generates a report of Donor data"""
    donation_total = []
    for item in r.keys():
        dn_name = item
        dn_list = get_donation_list(item)
        total_dn = sum(dn_list)
        dn_count = len(dn_list)
        avg_dn = 0
        if dn_count != 0:
            avg_dn = total_dn/dn_count
        donation_total.append([dn_name, total_dn, dn_count, avg_dn])
    donation_total.sort(key=lambda l: l[1], reverse = True)
    s1 = "Donor Name          |   Total Given  |  Num Gifts |  Average Gift\n"
    s2 = "-----------------------------------------------------------------\n"
    final_string = s1 + s2
    for z in range(0, len(donation_total)):
        s3 = '{:20} ${:13,.2f}{:14}  ${:13,.2f}\n'.format(*donation_total[z])
        final_string += s3
    return final_string


def get_donation_list(donor_name):
    """Retrieve donation values."""
    dn_list = literal_eval(r.hmget(donor_name, 'donations')[0])
    individual_dns = []
    for i in dn_list:
        individual_dns.append(i)
    return individual_dns


def print_report():
    """Print report of Donor data"""
    print(generate_report())


def get_donor_name():
    """Prompts user for Donor name"""
    return input("Enter a full name: ")


def get_new_donor_amount():
    """Prompts user for a donation entry"""
    return input("Enter a donation amount: ")


def get_phone():
    """Prompts user for a Donor phone number"""
    return input("Enter a phone number: ")


def get_zip():
    """Prompts the user for a Donor Zip code"""
    return input("Enter a zip code: ")


def clear_db():
    """Clean database for reuse."""
    r.flushdb()
    print("Database has been cleared. Exiting...")
    quit()


def main_prompt():
    """Prompts the user for option selection"""
    response = input("\n\
        Choose from one of 6 actions:\n\
        1) Add a Donation\n\
        2) Delete a Donor\n\
        3) Update a Donor\n\
        4) Create a Report\n\
        5) Send letters to everyone\n\
        0) Quit\n\
        Please type 1, 2, 3, 4, 5, or 0: ")
    return response


def action(switch_dict):
    """User prompt and interface."""
    while True:
        user_input = main_prompt()
        try:
            switch_dict.get(user_input)()
        except (TypeError, ValueError):
            print("Invalid input, {} please try again.".format(user_input))


if __name__ == "__main__":
    try:
        log.info('Step 1: connect to Redis')
        r = login_database.login_redis_cloud()
        log.info('Step 2: Adding 4 donors to the data cache')
        r.hmset('Bill Gates',
            {'phone': '295-647-7874',
            'zip': 57672,
            'donations': [200.00, 500.00, 800.00, 1000.00]})
        r.hmset('Jeff Bezos',
            {'phone': '905-306-9770',
            'zip': 74089,
            'donations': [4200.00, 19000.00]})
        r.hmset('Nikola Tesla',
            {'phone': '644-113-0350',
            'zip': 44870,
            'donations': [28000.00, 100.00, 5600.00]})
        r.hmset('Steve Jobs',
            {'phone': '235-587-5642',
            'zip': 40087,
            'donations': [800.00, 9200.00]})
        switch_dict = {
            'list': print_names,
            '1': add_donation,
            '2': delete_donor,
            '3': update_donor,
            '4': print_report,
            '5': send_letters,
            '0': clear_db
        }
        action(switch_dict)
    except Exception as e:
        print(f'Redis error: {e}')
