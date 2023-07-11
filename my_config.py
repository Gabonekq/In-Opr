MY_ID = -1
CUSTOMER_ABSENT, CUSTOMER_LOGIN, CUSTOMER_EMAIL = (0, 1, 2)

APP_NAME = "Agrorelaks"
ADMIN_PERM = 1

BACKGROUND = 'OliveDrab2'
FOREGROUND = 'AntiqueWhite1'
ERROR_FOREGROUND = 'red'


def is_float(value):
    
    try:
        return isinstance(float(value), float)
    except ValueError:
        return False


def is_integer(value):
    
    try:
        return isinstance(int(value), int)
    except ValueError:
        return False
