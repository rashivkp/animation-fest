from django.contrib import admin, messages
from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group

from models import *

admin.site.register(Student)
admin.site.register(Jourie)
admin.site.register(Score)
admin.site.register(Result)
admin.site.register(Item)

class JourieScoreForm(forms.ModelForm):
    class Meta:
        model = JourieScore
        exclude = ('is_student',)

class JourieScoreAdmin(admin.ModelAdmin):
    form = JourieScoreForm
    def queryset(self, request):
        qs = super(JourieScoreAdmin, self).queryset(request)
        return qs.filter(is_student=False)

    def save_model(self, request, obj, form, change):
        obj.is_student = False
        obj.save()

admin.site.register(JourieScore, JourieScoreAdmin)
