import random

from django.contrib.auth.models import User

from .models import CodesConnecting
import uuid, time


def registration_user(username: str, email: str, password: str):
    """Creation record user in table auth_user"""
    user = User.objects.create_user(username=username, last_name= username, first_name= username, email=email, password=password)
    user.save()


def add_record_table_unique_codes(username: str):
    """Creation record user's in table authorization_codesconnecting"""
    user_object = CodesConnecting(username=username, code=change_tempo_code(), uuid= uuid.uuid5(uuid.NAMESPACE_DNS, str(username) + str(time.time())))
    user_object.save()


def change_tempo_code() -> int:
    """Changing temporary code user in table authorization_codesconnecting"""
    while True:
        all_codes = CodesConnecting.objects.all().values('code')
        generated_code = generate_unique_code()
        for x in range(0, len(all_codes)):
            if all_codes[x]['code'] == generated_code:
                break
        else:
            return generated_code


def generate_unique_code() -> int:
    """generating temporary code user"""
    tempo_code = random.randrange(100000, 1000000, 1)
    return tempo_code
