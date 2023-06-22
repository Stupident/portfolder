import string 
from email_validator import validate_email, EmailNotValidError


def valid_email(email):
    try:
      # validate and get info
        v = validate_email(email)
        email = v['email']
        return True, ''
    except EmailNotValidError as e:
        # email is not valid, exception message is human-readable
        return False, str(e)

def valid_password(password):  
    SpecialSym = ['$', '@', '#', '%', '_', '~']
    val = True
    message = ''

    if not any(char in SpecialSym for char in password):
        message = 'Password should have at least one special symbol: $, #, @, %, _, ~'
        val = False
    if not any(char.isdigit() for char in password):
        message = 'Password should have at least one numeral'
        val = False 
    if not any(char.isupper() for char in password):
        message = 'Password should have at least one uppercase letter'
        val = False  
    if not any(char.islower() for char in password):
        message = 'Password should have at least one lowercase letter'
        val = False
    if len(password) < 6:
        message = 'Password length should be at least 6'
        val = False
    if len(password) > 64:
        message = 'Password length shouldn`t be greater than 64'
        val = False

    return val, message  


def valid_username(username):
    match = string.ascii_letters + string.digits + '_'
    val = True
    message = ''

    if not all([x in match for x in username]):
        message = "Username can contains only letters, digits and '_'"
        val = False
    if not (len(username) >=4 and len(username) <=25):
        message = 'Username length should be between 4 and 25'
        val = False
    if not username[0].isalpha():
        message = 'Username should start with letter'
        val = False
    if username[-1:] == '_':
        message = 'Username can`t end with underscore'
        val = False
    return val, message

def valid_name(name):
    match = string.ascii_letters + string.digits + '_ '
    val = True
    message = ''

    if not all([x in match for x in name]):
        message = "Portfolio`s name can contains only letters, digits, spaces and underscores"
        val = False
    if len(name) < 4:
        message = 'Portfolio`s name length should be at least 4'
        val = False
    if len(name) > 128:
        message = 'Portfolio`s name length should be 128 maximum'
        val = False
    return val, message

def valid_desc(desc):
    val = True
    message = ''

    if len(desc) > 1024:
        message = 'Description can`t be more than 128'
        val = False
    if len(desc) < 5:
        message = 'Description should be at least 5'
        val = False
    return val, message