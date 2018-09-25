import re
import getpass
import argparse
import string
from dateutil.parser import parse


def get_parser_args():
    parser = argparse.ArgumentParser(
        description='Input path to password black list')

    parser.add_argument(
        '-f',
        '--filepath',
        help='Path to a password blacklist')

    args = parser.parse_args()
    return args


def check_allowed_symbols(password):
    regex = '[ -~]'
    return bool(re.search(regex, password))


def check_length(password, min_length, max_length):
    return min_length < len(password) < max_length


def check_numerical_digits(password):
    regex = '[0-9]'
    return bool(re.search(regex, password))


def check_letters(password):
    regex = '[A-Za-z]'
    return bool(re.search(regex, password))


def check_case(password):
    regex = '[a-z].*[A-Z]|[A-Z].*[a-z]'
    return bool(re.search(regex, password))


def check_repeating_symbols(password):
    regex = r'(.)\1{3,}'
    return not bool(re.search(regex, password))


def check_special_symbols(password):
    regex = '[{}]'.format(string.punctuation)
    return bool(re.search(regex, password))


def load_blacklist(filepath):
    if filepath is not None:
        try:
            with open(filepath, 'r') as file_handler:
                blacklist_str = file_handler.read()
                blacklist = blacklist_str.split()
            return blacklist
        except FileNotFoundError:
            return None
    else:
        return None


def check_blacklist(password, blacklist):
    if blacklist is None:
        return True
    if password in blacklist:
        return False
    else:
        return True


def check_calendar_dates(password):
    regex = '[0-9]{4,9}'
    match_obj = re.match(regex, password)
    if match_obj is None:
        return True
    numbers_str = match_obj.group(0)

    if numbers_str:
        try:
            parse(numbers_str)
            return False
        except ValueError:
            return True
    else:
        return True


def check_telephone_numbers(password):
    regex = '[0-9]{7,15}'
    return not bool(re.match(regex, password))


def get_results_lst(password, blacklist_str):
    min_length = 8
    max_length = 32
    results_lst = [
        (check_allowed_symbols(password),
            '- Has no ASCII printable characters'),
        (check_length(password, min_length, max_length),
            '- Password too short or too long'),
        (check_numerical_digits(password),
            "- Doesn't have numerical digits"),
        (check_letters(password),
            "- Doesn't have letter symbols"),
        (check_case(password),
            "- Doesn't have both upper- and lowercase symbols"),
        (check_repeating_symbols(password),
            "- Has more than 3 similar characters in a row"),
        (check_special_symbols(password),
            "- Doesn't have any allowed special characters"),
        (check_blacklist(password, blacklist_str),
            '- Is in blacklist'),
        (check_calendar_dates(password),
            "- Has a date"),
        (check_telephone_numbers(password),
            "- Has a phone number")
    ]

    return results_lst


def print_results(results_lst):
    score = 0
    for status, error_text in results_lst:
        if status:
            score += 1
        if not status:
            print(error_text)
    print('Password strength is {} out of 10'.format(score))


if __name__ == '__main__':
    args = get_parser_args()
    filepath = args.filepath

    if filepath is None:
        print('Will not be checked for blacklist')

    blacklist = load_blacklist(filepath)

    password = getpass.getpass()
    print(password)

    results_lst = get_results_lst(password, blacklist)

    print_results(results_lst)
