from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
import json
from django.core import serializers
from fest.models import *
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.template.response import TemplateResponse
from django.contrib.auth import login
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg

def can_rate(user):
    if not hasattr(user, 'student'):
        return user.groups.filter(name='Jourie').count() == 1
    return True

def is_admin(user):
    return user.groups.filter(name='Admin').count() == 1

@login_required
@user_passes_test(can_rate, login_url='/')
def score(request):
    items = []
    if request.user.groups.filter(name__icontains='Jourie').exists():
        item_list = request.user.jourie.items.all()
    else:
        item_list = Item.objects.all()
    for item in item_list:
        studentlist = {'item': item, 'scores':[] }
        for student in Student.objects.filter(items__in=Item.objects.filter(pk=item.id)):
            try:
                score = Score.objects.get(scored_by=request.user, item=item,
                    student=student).mark
            except ObjectDoesNotExist:
                score = 0
            studentlist['scores'].append({'student': student, 'score': score})
        items.append(studentlist)

    if request.user.groups.filter(name__icontains='Jourie').exists():
        return render_to_response('itemlist_jourie.html', { 'user': request.user, 'items': items})
    elif hasattr(request.user, 'student'):
        return render_to_response('itemlist.html', { 'user': request.user, 'items': items})

@csrf_exempt
@login_required
def rateMe(request):
    if request.method == 'POST':
        student = Student.objects.get(pk=request.POST.get('idStudent', False))
        item = Item.objects.get(pk=request.POST.get('idItem', False))
        if student and item:
            try:
                score = Score.objects.get(scored_by=request.user, student=student, item=item)
                score.mark = request.POST.get('rate', 0)
                score.save()
            except ObjectDoesNotExist:
                if request.user.groups.filter(name='Jourie').count():
                    Score.objects.create(scored_by=request.user,
                        student=student, item=item,
                        mark=request.POST.get('rate', 0), is_student=False)
                else:
                    Score.objects.create(scored_by=request.user,
                        student=student, item=item, mark=request.POST.get('rate', 0))
        return HttpResponse('success')

@csrf_protect
def home(request, template_name='index.html', authentication_form=AuthenticationForm):

    if request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():
            # Okay, security check complete. Log the user in.
            login(request, form.get_user())
            return HttpResponseRedirect('/score/')
    elif request.user.is_authenticated():
        return TemplateResponse(request, template_name, {'user': request.user})
    else:
        form = authentication_form(request)

    context = {
        'form': form,
    }
    return TemplateResponse(request, template_name, context)

@login_required
@user_passes_test(is_admin, login_url='/')
def report(request):
    items = []
    for item in Item.objects.all():
        studentlist = {'item': item, 'scores':[] }
        for student in item.student_set.all():
            student_mark = Score.objects.filter(is_student=True, student=student, item=item).aggregate(Avg('mark'))['mark__avg']
            jourie_mark = Score.objects.filter(is_student=False, student=student, item=item).aggregate(Avg('mark'))['mark__avg']
            jourie_score = Score.objects.filter(is_student=False, student=student, item=item)
            studentlist['scores'].append({ 'student':
                student,'jourie_score':jourie_score, 'student_mark': student_mark, 'jourie_mark': jourie_mark})
        items.append(studentlist)

    return render_to_response('report.html', { 'user': request.user, 'items': items})
