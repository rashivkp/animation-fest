from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group

from models import *

admin.site.register(Student)
admin.site.register(Score)
admin.site.register(Result)
admin.site.register(Item)
