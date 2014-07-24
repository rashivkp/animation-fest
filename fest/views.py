from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
import json
from django.core import serializers
from fest.models import *
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.template.response import TemplateResponse
from django.contrib.auth import login

@login_required
def items(request):
    items = Item.objects.all()
    return render_to_response('itemlist.html', { 'items': items, 'user':
        request.user})

@csrf_exempt
@login_required
def rateMe(request):
    if request.method == 'POST':
        student = Student.objects.get(pk=request.POST.get('idStudent', False))
        item = Item.objects.get(pk=request.POST.get('idItem', False))
        if student and item:
            score, created = Score.objects.get_or_create(scored_by=request.user,
                    student=student, item=item, mark=request.POST.get('rate'))
            if created:
                return HttpResponse('success')
        return HttpResponseForbidden()

@csrf_protect
def home(request, template_name='index.html', authentication_form=AuthenticationForm):

    if request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():

            # Okay, security check complete. Log the user in.
            login(request, form.get_user())

            return HttpResponseRedirect('/items/')
    elif request.user.is_authenticated():
        return TemplateResponse(request, template_name, {'user': request.user})
    else:
        form = authentication_form(request)

    context = {
        'form': form,
    }
    return TemplateResponse(request, template_name, context)
