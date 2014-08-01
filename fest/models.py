from django.db import models
from django.contrib.auth.models import User, Group

class Item(models.Model):
    UP = 'U'
    HS = 'H'
    HSS = 'S'
    VHSS = 'V'
    HSS_VHSS = 'W'
    CATEGORY_CHOICES = ((UP, 'UP'),
        (HS, 'HS'),
        (HSS, 'HSS'),
        (VHSS, 'VHSS'),
        (HSS_VHSS, 'HSS/VHSS'))
    name = models.CharField(max_length=64)
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES)
    is_student_ratable = models.BooleanField(default=False)
    is_result_published = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s %s' % (self.get_category_display(), self.name)

class Student(models.Model):
    user = models.OneToOneField(User)
    school = models.CharField(max_length=64)
    schoolcode = models.CharField(max_length=8)
    std = models.IntegerField()
    is_rating_confirmed = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s@%s" % (self.user.get_full_name(), self.schoolcode)

class Participant(models.Model):
    item = models.ForeignKey(Item)
    student = models.ForeignKey(Student)
    code = models.IntegerField()

class Jury(models.Model):
    user = models.OneToOneField(User)
    bio = models.TextField(blank=True, null=True)
    items = models.ManyToManyField(Item)

    def __unicode__(self):
        return "%s" % (self.user.username)

class Score(models.Model):
    participant = models.ForeignKey(Participant)
    scored_by = models.ForeignKey(User)
    mark = models.IntegerField()
    is_student = models.BooleanField(default=True)
    class Meta:
        unique_together = ('scored_by', 'participant')

class JuryScore(Score):
    class Meta:
        proxy = True

    def __init__(self, *args, **kwargs):
        super(Score, self).__init__(*args, **kwargs)
        self.is_student = False

class Result(models.Model):
    participant = models.ForeignKey(Participant)
    score = models.FloatField()
    student_score = models.FloatField(default=0)

class SpecialAward(models.Model):
    participant = models.ForeignKey(Participant)
    title = models.CharField(max_length=64)
    comment = models.TextField(null=True, blank=True)
