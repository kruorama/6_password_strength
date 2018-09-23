# Password Strength Calculator
The script analyses a password and evaluates it, giving a score from 0 to 10 (most likely there are no passwords that would score 0 though)

### Description
Service features:
* Accepts a path to a black list as an argument. Tested with this password black list: https://github.com/danielmiessler/SecLists/blob/master/Passwords/Common-Credentials/10-million-password-list-top-100.txt
* Gets password from user through getpass so that all symbols are read as a string.
* Prints the score with details

Core features:
* Checks the password length, scores positive if between 8 and 32
* Checks for at least one numerical digit
* Checks for at least one letter symbol
* Checks for both upper- and lowercase symbols
* Checks for having more than 3 same symbols in a row
* Checks for allowed special symbols: ```!"#$%&'()*+,-./:;<=>?@[\]^_`{|}]```
* Checks if the password matches the given black list
* Checks if the numbers in password can be read as a date and scores negative in that case
* If there's a number sequence 7-15 symbols long, assumes it's a phone number and scores negative


### How to launch

Example of script launch on Linux, Python 3.5:

```
$ python password_strength.py <path to black list file>
Password:
Password strength is 7 out of 10
Password too short or too long
Doesn't have both upper- and lowercase symbols
```



# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
