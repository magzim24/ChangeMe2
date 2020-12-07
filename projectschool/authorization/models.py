from django.db import models
import uuid

# Create your models here.
class CodesConnecting(models.Model):
    username = models.CharField(max_length=200, primary_key=True)
    code = models.IntegerField(primary_key=False)
    tempo_password_room = models.CharField(max_length=150, null=True, primary_key=False)
    uuid = models.CharField(max_length=100, null=True)

def content_file_name(ud, real_filename):
    filename = uuid.uuid5(uuid.NAMESPACE_DNS, str(real_filename))
    return f'/users_files/{str(CodesConnecting.objects.get(uuid = ud).code)}/{filename}'


class URLsUsersFiles(models.Model):
    url = models.FileField(upload_to=content_file_name)
    really_name_file = models.CharField(max_length=255)
    id_room = models.IntegerField()

class Rooms(models.Model):
    host = models.CharField(max_length=250, null=True)
    room = models.CharField(max_length=250, null=True)