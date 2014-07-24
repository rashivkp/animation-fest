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

@login_required
def items(request):
    items = []
    for item in Item.objects.all():
        studentlist = {'item': item, 'scores':[] }
        for student in Student.objects.filter(items__in=Item.objects.filter(pk=item.id)):
            try:
                score = Score.objects.get(scored_by=request.user, item=item,
                    student=student).mark
            except ObjectDoesNotExist:
                score = 0
            studentlist['scores'].append({'student': student, 'score': score})
        items.append(studentlist)

    return render_to_response('itemlist.html', { 'user': request.user,
        'items': items})

@csrf_exempt
@login_required
@user_passes_test(lambda u: hasattr(u, 'student'))
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
                score, created = Score.objects.get_or_create(scored_by=request.user,
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

