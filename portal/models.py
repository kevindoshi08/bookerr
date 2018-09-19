from django.db import models

import os
from uuid import uuid4
from django.contrib.auth.models import User


def path_and_rename(instance, filename):
    upload_to = 'images/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path o the file
    return os.path.join(upload_to, filename)


class Book(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    price = models.IntegerField()
    image = models.ImageField(upload_to=path_and_rename)

    def getPrice(self):
        return self.price


class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wallet = models.IntegerField(default=2000)


class BookUserModel(models.Model):
    user = models.ForeignKey(UserDetails, on_delete=models.CASCADE, default=1)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, default=1)
