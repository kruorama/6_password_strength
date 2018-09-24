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
    if re.search(regex, password):
        return True
    else:
        return False


def check_length(password, min_length, max_length):
    if len(password) > max_length:
        return False
    if len(password) < min_length:
        return False
    return True


def check_numerical_digits(password):
    regex = '[0-9]'
    if re.search(regex, password):
        return True
    else:
        return False


def check_letters(password):
    regex = '[A-Za-z]'
    if re.search(regex, password):
        return True
    else:
        return False


def check_case(password):
    regex = '[a-z].*[A-Z]|[A-Z].*[a-z]'
    if re.search(regex, password):
        return True
    else:
        return False


def check_repeating_symbols(password):
    regex = r'(.)\1{3,}'
    if re.search(regex, password):
        return False
    else:
        return True


def check_special_symbols(password):
    regex = '[' + string.punctuation + ']'
    if re.search(regex, password):
        return True
    else:
        return False


def load_blacklist_str(filepath):
    if filepath is not None:
        try:
            with open(filepath, 'r') as file_handler:
                blacklist_str = file_handler.read()
            return blacklist_str
        except FileNotFoundError:
            return None
    else:
        return None


def check_blacklist(password, blacklist_str):
    if blacklist_str is None:
        return True
    if re.search(password, blacklist_str, re.IGNORECASE):
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
    if re.match(regex, password):
        return False
    else:
        return True


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


def calculate_password_strength(results_lst):
    score_lst = []
    for result in results_lst:
        score_lst.append(result[0])
    strength = sum(score_lst)
    return strength


def print_errors(results_lst):
    for status, error_text in results_lst:
        if not status:
            print(error_text)


if __name__ == '__main__':
    args = get_parser_args()
    filepath = args.filepath

    if filepath is None:
        print('Will not be checked for blacklist')

    blacklist_str = load_blacklist_str(filepath)

    password = getpass.getpass()
    results_lst = get_results_lst(password, blacklist_str)
    print('Password strength is {} out of 10'.format(
        calculate_password_strength(results_lst)))
    print_errors(results_lst)
