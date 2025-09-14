import hashlib

from django.db import models

# Create your models here.


from django.db import models
from bot_manage_dj.models import BaseModel

SEX_CHOICES = [
    (1, 'Male'),
    (2, 'Female')
]


class User(BaseModel):
    username = models.CharField(max_length=64)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=256)
    sex = models.IntegerField(choices=SEX_CHOICES, default=1)

    class Meta:
        db_table = 'user'

    def __str__(self):
        return f"{self.pk}: {self.username}"

    def check_password(self, password):
        input_passwd = hashlib.md5(password.encode('utf-8')).hexdigest()
        if input_passwd == self.password:
            return True
        else:
            return False
