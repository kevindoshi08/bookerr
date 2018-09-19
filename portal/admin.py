from django.contrib import admin
from .models import *

register_models = [Book, UserDetails, BookUserModel]

admin.site.register(register_models)


