

from django.core.exceptions import ValidationError

import re
def validate_username(value):
    pass
    


def validate_password(value):
    if len(value) <= 8:
        raise ValidationError('passowrd is too short')
    if re.search('[0-9]', value) is None:
        raise ValidationError("The password must contain at least one numeric character.", code='missing_numeric')
    if re.search('[A-Z]', value) is None:
        raise ValidationError("The password must contain at least one uppercase character.", code='missing_upper_case')
    




