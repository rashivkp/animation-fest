from fest.models import *
from django.contrib.auth.models import User, Group
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

import csv
from datetime import datetime
import sys
try:
    import MySQLdb
    mysql_exists = True
except:
    mysql_exists = False

def escape_string(v):
    if mysql_exists:
        return MySQLdb.escape_string(v)
    else:
        return v

def run():
    load_students()
    print "loaded students"

def load_students():
    count = 0
    with open("csvs/students.csv") as f:
        reader = csv.reader(f,delimiter=';')
        new_profiles = []
        for row in reader:
            try:
                user = User.objects.get(username="%s@%s" % (escape_string(row[2].split(" ")[0][:30]).lower(), row[0]))
                item = Item.objects.get(pk=int(row[5]))
                Participant.objects.create(item=item, student=user.student, code=row[4])
            except ObjectDoesNotExist:
                user = User.objects.create_user(
                    username="%s@%s" % (escape_string(row[2].split(" ")[0][:30]).lower(), row[0]),
                    email="",
                    password='pass123')
                # Truncate name to 30 characters
                if row[2].find(" ") > -1:
                    user.first_name = escape_string(row[2].split(" ")[0][:30])
                    user.last_name = escape_string(" ".join(row[2].split(" ")[1:])[:30])
                else:
                    user.first_name = row[2]

                if row[3] == '':
                    std = 0
                else:
                    std = int(row[3])
                student = Student.objects.create(user=user, schoolcode=row[0], school=row[1], std=std)

                user.is_active = True
                user.save()
                item = Item.objects.get(pk=int(row[5]))
                Participant.objects.create(item=item, student=student, code=row[4])

