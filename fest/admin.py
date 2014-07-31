from django.contrib import admin, messages
from django import forms
from django.contrib.auth.models import User, Group

from models import *

admin.site.register(Participant)
admin.site.register(Score)
admin.site.register(Result)
admin.site.register(Item)

class StudentForm(forms.ModelForm):
    first_name = forms.CharField(max_length=32, required=False)
    last_name = forms.CharField(max_length=32, required=False)
    email = forms.EmailField(required=False)

    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'school', 'schoolcode', 'std')

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request', None)
        super(StudentForm, self).__init__(*args, **kwargs)
        try:
            #self.fields['registered'].initial = self.instance.user.is_active
            if 'instance' in kwargs and self.instance and self.instance.user:
                self.fields['first_name'].initial = self.instance.user.first_name
                self.fields['last_name'].initial = self.instance.user.last_name
                self.fields['email'].initial = self.instance.user.email
        except (KeyError, AttributeError):
            print "error"
            pass

    def save(self, *args, **kwargs):
        if self.instance.id:
            #existing record being updated
            up = self.instance
            up.user.first_name = self.cleaned_data.get('first_name')
            up.user.last_name = self.cleaned_data.get('last_name')
            up.user.email = self.cleaned_data.get('email')
            up.user.save()
            user = None
        else:
            #create new Student
            user = User.objects.create_user(
                username="%s@%s" % (self.cleaned_data['first_name'], self.cleaned_data['schoolcode']),
                email=self.cleaned_data['email'],
                password=self.cleaned_data['schoolcode'])
            user.first_name=self.cleaned_data['first_name']
            user.last_name=self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            user.save()

            student_group = Group.objects.get(name='Student')
            student_group.user_set.add(user)

        s = super(StudentForm, self).save(*args, **kwargs)
        if user:
            s.user = user
        s.save()
        return s

class StudentAdmin(admin.ModelAdmin):
    form = StudentForm
    list_display = ('get_name','school')
    search_fields = ['user__username', 'user__first_name', 'user__last_name']

    def get_name(self, obj):
        full_name = obj.user.get_full_name()
        if full_name == "":
            return obj.user.username
        return full_name
    get_name.short_description = 'Name'

class JuryForm(forms.ModelForm):
    username = forms.CharField(max_length=32, required=True)
    first_name = forms.CharField(max_length=32, required=False)
    last_name = forms.CharField(max_length=32, required=False)
    email = forms.EmailField(required=False)

    class Meta:
        model = Jury
        fields = ('username','first_name','last_name', 'bio', 'items')

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request', None)
        super(JuryForm, self).__init__(*args, **kwargs)
        try:
            if 'instance' in kwargs and self.instance and self.instance.user:
                self.fields['username'].initial = self.instance.user.username
                self.fields['first_name'].initial = self.instance.user.first_name
                self.fields['last_name'].initial = self.instance.user.last_name
                self.fields['email'].initial = self.instance.user.email
        except (KeyError, AttributeError):
            print "error"
            pass

    def save(self, *args, **kwargs):
        if self.instance.id:
            #existing record being updated
            up = self.instance
            up.user.username = self.cleaned_data.get('username')
            up.user.first_name = self.cleaned_data.get('first_name')
            up.user.last_name = self.cleaned_data.get('last_name')
            up.user.email = self.cleaned_data.get('email')
            up.user.save()
            user = None
        else:
            #create new Student
            user = User.objects.create_user(
                username=self.cleaned_data['username'],
                email=self.cleaned_data['email'],
                password=self.cleaned_data['username'])
            user.first_name=self.cleaned_data['first_name']
            user.last_name=self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            user.save()

            group = Group.objects.get(name='Jury')
            group.user_set.add(user)

        s = super(JuryForm, self).save(*args, **kwargs)
        if user:
            s.user = user
        s.save()
        return s

class JuryAdmin(admin.ModelAdmin):
    form = JuryForm
    list_display = ('get_name','bio')
    search_fields = ['user__username', 'user__first_name', 'user__last_name']

    def get_name(self, obj):
        full_name = obj.user.get_full_name()
        if full_name == "":
            return obj.user.username
        return full_name
    get_name.short_description = 'Name'

class JuryScoreForm(forms.ModelForm):
    class Meta:
        model = JuryScore
        exclude = ('is_student',)

class JuryScoreAdmin(admin.ModelAdmin):
    form = JuryScoreForm
    def queryset(self, request):
        qs = super(JuryScoreAdmin, self).queryset(request)
        return qs.filter(is_student=False)

    def save_model(self, request, obj, form, change):
        obj.is_student = False
        obj.save()

admin.site.register(JuryScore, JuryScoreAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Jury, JuryAdmin)
