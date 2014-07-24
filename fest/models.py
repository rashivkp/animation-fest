from django.db import models
from django.contrib.auth.models import User, Group

class Item(models.Model):
    CATEGORY_CHOICES = (('UP', 'UP'),
        ('HS', 'HS'),
        ('HSS/VHSS', 'HSS/VHSS'))
    name = models.CharField(max_length=64)
    category = models.CharField(max_length=8, choices=CATEGORY_CHOICES)
    is_result_published = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s %s' % (self.category, self.name)

class Student(models.Model):
    user = models.OneToOneField(User)
    school = models.CharField(max_length=64)
    schoolcode = models.CharField(max_length=8)
    std = models.IntegerField()
    items = models.ManyToManyField(Item)

    def __unicode__(self):
        return "%s" % (self.user.username)

class Score(models.Model):
    scored_by = models.ForeignKey(User)
    student = models.ForeignKey(Student)
    item = models.ForeignKey(Item)
    mark = models.IntegerField()
    is_student = models.BooleanField(default=True)
    class Meta:
        unique_together = ('scored_by', 'student', 'item')

class JourieScore(Score):
    class Meta:
        proxy = True

    def __init__(self, *args, **kwargs):
        super(Score, self).__init__(*args, **kwargs)
        self.is_student = False

class Result(models.Model):
    item = models.ForeignKey(Item)
    student = models.ForeignKey(Student)
    score = models.IntegerField()
    special = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)
