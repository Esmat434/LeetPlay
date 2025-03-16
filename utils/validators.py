import re
from datetime import date, datetime

def is_validate_password(password):
    errors = []
    
    if len(password) < 8:
        errors.append("password must be 8 charecter or greather.")
    if not re.search(r'[A-Z]', password):
        errors.append("password must have one uppercase letter.")
    if not re.search(r'[a-z]', password):
        errors.append("password must have one lowercase letter.")
    if not re.search(r'\d', password):
        errors.append("password must have one number")
    if not re.search(r'[@$!%*?&]', password):
        errors.append("password must have on of these (@$!%*?&) charecter")
    return errors if errors else password

from datetime import datetime, date

def is_validate_birth_date(birth_date):
    if isinstance(birth_date, str):
        try:
            birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
        except ValueError:
            return True 
    
    elif isinstance(birth_date, datetime):
        birth_date = birth_date.date()

    elif not isinstance(birth_date, date):
        return True 

    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    return age < 18  

# print(is_validate_birth_date('2020-03-01'))