import random
import string

# goal of password the length of 16 mixed 4 puncs, 8 string, 4 digits

def generate_password():
# get password content
    a_string = string.ascii_letters
    a_nums = string.digits
    a_puncs = string.punctuation
    password = ""

    # get mixed characters from each content category (string, digits, punctuation)
    password += "".join(random.choices(a_string, k=8))
    password += "".join(random.choices(a_nums, k=4))
    password += "".join(random.choices(a_puncs, k=4))

    # shuffle the password 
    password = list(password)
    random.shuffle(password)
    password = "".join(password)

    return password

# display newly generated password
print(generate_password())