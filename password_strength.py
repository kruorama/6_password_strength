import re
import getpass
import argparse
from dateutil.parser import parse


def get_parser_args():
    parser = argparse.ArgumentParser(
        description='Input path to password black list')

    parser.add_argument(
        'filepath',
        help='Path to a password black_list')
    args = parser.parse_args()
    return args

def check_allowed_symbols(password):
    regex = '[ -~]'
    if re.match(regex, password):
        return True, 'All characters in password are allowed'
    else:
        return False, 'Has not ASCII printable characters'

def check_length(password):
    if len(password) > 32:
        return False, 'Too long'
    if len(password) < 8:
        return False, 'Too short'
    return True, 'Password length is just right'


def check_numerical_digits(password):
    regex = '[0-9]'
    if re.search(regex, password):
        return True, 'Has at least one numerical symbol'
    else:
        return False, ("Doesn't have numerical digits")


def check_letters(password):
    regex = '[A-Za-z]'
    if re.search(regex, password):
        return True, 'Has at least one letter symbol'
    else:
        return False, ("Doesn't have letter symbols")


def check_case(password):
    regex = '[a-z].*[A-Z]|[A-Z].*[a-z]'
    if re.search(regex, password):
        return True, 'Has upper- and lowercase symbols'
    else:
        return False, "Doesn't have upper- and lowercase symbols"


def check_repeating_symbols(password):
    regex = r'(.)\1{3,}'
    if re.search(regex, password):
        return False, 'Has 4 or more similar characters in a row'
    else:
        return True, "Hasn't more than 3 similar characters in a row"

def check_special_symbols(password):
    regex = '[!\"\#\$\%\&\'\(\)\*\+\,\-\.\/\:\;\<\=\>\?@\[\\]\^\_\`{\|}]'
    if re.search(regex, password):
        return True, 'Has allowed special characters'
    else:
        return False, ("Doesn't have any allowed special characters")


def load_black_list(filepath):
    try:
        with open(filepath, 'r') as file_handler:
            black_list = file_handler.read()
        return black_list
    except FileNotFoundError:
        return None


def check_black_list(password, black_list):
    if re.search(password, black_list, re.IGNORECASE):
        return False, 'Is in black list'
    else:
        return True, ("Isn't in black_list")


def check_calendar_dates(password):
    regex = '[0-9]{4,9}'
    match_obj = re.match(regex, password)
    numbers_str = match_obj.group(0)

    if numbers_str:
        try:
            parse(numbers_str)
            return False, 'Has a date'
        except ValueError:
            return True, "Doesn't have a date"
    else:
        return True, "Doesn't have a date"


def check_telephone_numbers(password):
    regex = '[0-9]{7,15}'
    if re.match(regex, password):
        return False, 'Likely has a phone number'
    else:
        return True, "Doesn't have a detectable phone number"


def calculate_password_strength(password):
    strength =
    check_allowed_symbols(password)[0] +
    check_length(password)[0] +
    check_numerical_digits(password)[0] +
    check_letters(password)[0] +
    status, message = check_case(password)
    status, message = check_repeating_symbols(password)
    status, message = check_special_symbols(password)
    status, message = check_black_list(password, black_list)
    status, message = check_calendar_dates(password)
    check_telephone_numbers(password)

def print_check_result(*arguments):
    if arguments[0][0]:
        print('+ {}'.format(arguments[0][1]))
    else:
        print('- {}'.format(arguments[0][1]))


if __name__ == '__main__':
    args = get_parser_args()
    black_list = load_black_list(args.filepath)
    if black_list is None:
        exit('File is not found')

    password = getpass.getpass()
    print(password) #don't forget to remove


    print_check_result(check_allowed_symbols(password))
    print_check_result(check_length(password))
    print_check_result(check_numerical_digits(password))
    print_check_result(check_letters(password))
    print_check_result(check_case(password))
    print_check_result(check_repeating_symbols(password))
    print_check_result(check_special_symbols(password))
    print_check_result(check_black_list(password, black_list))
    print_check_result(check_calendar_dates(password))
    print_check_result(check_telephone_numbers(password))
