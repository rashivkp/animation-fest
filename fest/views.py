from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
import json
from django.core import serializers
from fest.models import *
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import AuthenticationForm
from django.template.response import TemplateResponse
from django.template import RequestContext
from django.contrib.auth import login
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg
from django.views.generic import ListView, DetailView

def can_rate(user):
    if not hasattr(user, 'student'):
        return user.groups.filter(name='Jury').count() == 1
    return True

def is_admin(user):
    return user.groups.filter(name='Admin').count() == 1

@login_required
@csrf_protect
@user_passes_test(can_rate, login_url='/')
def score(request):
    items = []
    if request.user.groups.filter(name__icontains='Jury').exists():
        item_list = request.user.jury.items.all()
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

    if request.user.groups.filter(name__icontains='Jury').exists():
        return render_to_response('itemlist_jury.html', { 'user': request.user,
            'items': items}, context_instance=RequestContext(request))
    elif hasattr(request.user, 'student'):
        return render_to_response('itemlist.html', { 'user': request.user,
            'items': items}, context_instance=RequestContext(request))

@csrf_protect
@login_required
def rateMe(request):
    if request.method == 'POST':
        student = Student.objects.get(pk=request.POST.get('idStudent', False))
        item = Item.objects.get(pk=request.POST.get('idItem', False))
        if item.is_confirmed:
            return HttpResponseForbidden()
        if student and item:
            try:
                score = Score.objects.get(scored_by=request.user, student=student, item=item)
                score.mark = request.POST.get('rate', 0)
                score.save()
            except ObjectDoesNotExist:
                if request.user.groups.filter(name='Jury').count():
                    Score.objects.create(scored_by=request.user,
                        student=student, item=item,
                        mark=request.POST.get('rate', 0), is_student=False)
                else:
                    Score.objects.create(scored_by=request.user,
                        student=student, item=item, mark=request.POST.get('rate', 0))
        return HttpResponse('success')

@csrf_protect
def home(request, template_name='index.html', authentication_form=AuthenticationForm):

    results = []
    for item in Item.objects.filter(is_result_published=True):
        # generating result based student and jury rating
        mark = -1
        rank = 0
        common_result = []
        for result in item.result_set.all().order_by('-score'):
            if mark != result.score:
                rank += 1
                mark = result.score
                if rank == 6:
                    break
            common_result.append({'result':result, 'rank': rank})

        # generating result based student rating
        student_result = []
        mark = -1
        rank = 0
        for result in item.result_set.all().order_by('-student_score'):
            if mark != result.score:
                rank += 1
                mark = result.score
                if rank == 6:
                    break
            student_result.append({'result':result, 'rank': rank})
        results.append({'common_result': common_result, 'item':item,
            'student_result': student_result})

    if request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():
            # Okay, security check complete. Log the user in.
            login(request, form.get_user())
            return HttpResponseRedirect('/score/')
    elif request.user.is_authenticated():
        return TemplateResponse(request, template_name, {'user': request.user,
            'results': results})
    else:
        form = authentication_form(request)

    context = {
        'form': form,'results': results,
    }
    return TemplateResponse(request, template_name, context)

@csrf_protect
@login_required
def result_action(request):

    if request.method == 'POST' and request.POST.get('item', False) and request.POST.get('action', False):
        item = Item.objects.get(pk=request.POST['item'])
        action = request.POST['action']
        if not item.is_confirmed and action=='confirm':
            for student in item.student_set.all():
                student_mark = Score.objects.filter(is_student=True, student=student, item=item).aggregate(Avg('mark'))['mark__avg']
                jury_mark = Score.objects.filter(is_student=False, student=student, item=item).aggregate(Avg('mark'))['mark__avg']
                if student_mark == None:
                    student_mark = 0
                else:
                    student_mark = int(round(student_mark))
                if jury_mark == None:
                    jury_mark = 0
                else:
                    jury_mark = int(round(jury_mark))
                Result.objects.create(item=item, student=student,
                        score=int(round(student_mark+jury_mark)),student_score=student_mark, special=False)
            item.is_confirmed = True
            item.save()
            return HttpResponse('success')
        else:
            if action == 'publish':
                item.is_result_published = True
            elif action == 'reset':
                item.is_confirmed = False
                item.is_result_published = False
                item.result_set.all().delete()
            item.save()
            return HttpResponse('success')

        return HttpResponseForbidden()

@csrf_protect
@login_required
def publish_result(request):
    if request.method == 'POST' and request.POST.get('item', False):
        item = Item.objects.get(pk=request.POST['item'])
        if item.is_confirmed:
            return HttpResponse('success')

        return HttpResponseForbidden()

class ItemListView(ListView):
    model = Item
    template_name = 'item_report.html'
    context_object_name = 'items'

    @method_decorator(login_required)
    @method_decorator(user_passes_test(is_admin, login_url='/'))
    def dispatch(self, *args, **kwargs):
        return super(ItemListView, self).dispatch(*args, **kwargs)

class ItemDetailView(DetailView):
    model = Item
    template_name = 'item_rating_report.html'
    context_object_name = 'item'

    @method_decorator(login_required)
    @method_decorator(user_passes_test(is_admin, login_url='/'))
    def dispatch(self, *args, **kwargs):
        return super(ItemDetailView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        ctx = super(ItemDetailView, self).get_context_data(*args, **kwargs)
        item = self.get_object()
        ctx['students'] = []
        for student in item.student_set.all():
            jury_score = []
            for jury in item.jury_set.all():
                try:
                    jury_score.append(Score.objects.get(is_student=False,
                        student=student, item=item, scored_by=jury.user).mark)
                except ObjectDoesNotExist:
                    jury_score.append('')

            scores = item.score_set.filter(student=student)
            jurys_mark = scores.filter(is_student=False).aggregate(Avg('mark'))['mark__avg']
            if jurys_mark == None:
                jurys_mark = 0
                jurys_scored = 0
            else:
                jurys_scored = scores.filter(is_student=False).count()

            students_mark = scores.filter(is_student=True).aggregate(Avg('mark'))['mark__avg']
            if students_mark == None:
                students_mark = 0
                students_scored = 0
            else:
                students_scored = scores.filter(is_student=True).count()

            ctx['students'].append({'student': student, 'jury_score':jury_score, 'jurys_mark': jurys_mark, 'students_mark': students_mark,
                'jurys_scored': jurys_scored, 'students_scored': students_scored})

        return ctx
