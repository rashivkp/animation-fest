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
from django.contrib import messages

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
        item_list = Item.objects.filter(is_student_ratable=True)
    for item in item_list:
        studentlist = {'item': item, 'scores':[] }
        for participant in item.participant_set.all():
            try:
                score = Score.objects.get(scored_by=request.user,
                        participant=participant).mark
            except ObjectDoesNotExist:
                score = 0
            studentlist['scores'].append({'participant': participant, 'score': score})
        items.append(studentlist)

    if request.user.groups.filter(name__icontains='Jury').exists():
        return render_to_response('item_scoring.html', { 'user': request.user,
            'items': items}, context_instance=RequestContext(request))
    elif hasattr(request.user, 'student'):
        return render_to_response('itemlist.html', { 'user': request.user,
            'items': items}, context_instance=RequestContext(request))

@csrf_protect
@login_required
def rateMe(request):
    if request.method == 'POST' and request.POST.get('action', False) == 'rating':
        item = Item.objects.get(pk=request.POST.get('idItem', False))
        participant = Participant.objects.get(student__id=request.POST.get('idStudent',
            False), item=item)
        if item.is_confirmed:
            return HttpResponseForbidden()
        if participant and item:
            try:
                score = participant.score_set.get(scored_by=request.user)
                score.mark = request.POST.get('rate', 0)
                score.save()
            except ObjectDoesNotExist:
                if request.user.groups.filter(name='Jury').count():
                    Score.objects.create(scored_by=request.user,
                        participant=participant, mark=request.POST.get('rate', 0), is_student=False)
                else:
                    Score.objects.create(scored_by=request.user,
                        participant=participant, mark=request.POST.get('rate', 0))
        return HttpResponse('success')

def confirm_rating(request):
    if hasattr(request.user, 'student'):
        if Score.objects.filter(scored_by = request.user).count() == Participant.objects.filter(item__is_student_ratable=True).count():
            request.user.student.is_rating_confirmed = True
            request.user.student.save()
            messages.success(request, 'Rating Confirmed Successfully')
        else:
            messages.warning(request, 'Please Rate All Students')
    elif hasattr(request.user, 'jury'):
        request.user.jury.is_rating_confirmed = True
        request.user.jury.save()
    return HttpResponseRedirect('/score')

@csrf_protect
def home(request, template_name='index.html', authentication_form=AuthenticationForm):

    results = []
    for item in Item.objects.filter(is_result_published=True):
        # generating result based student and jury rating
        mark = -1
        rank = 0
        common_result = []
        for result in Result.objects.filter(participant__item=item).order_by('-score'):
            if mark != result.score:
                rank += 1
                mark = result.score
            common_result.append({'result':result, 'rank': rank})

        # generating result based student rating
        student_result = []
        mark = -1
        experts_mark = -1
        previous_result = ''
        rank = 0
        for result in Result.objects.filter(participant__item=item).order_by('-student_score', '-experts_score'):
            if mark != result.student_score:
                rank += 1
                mark = result.student_score
                experts_mark = result.experts_score
            if mark == result.student_score:
                if experts_mark > result.experts_score:
                    rank += 1
            student_result.append({'result':result, 'rank': rank})
        results.append({'common_result': common_result, 'item':item,
            'student_result': student_result})

    if request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():
            # Okay, security check complete. Log the user in.
            login(request, form.get_user())
            if hasattr(request.user, 'student'):
                return HttpResponseRedirect('/score/')
            else:
                return HttpResponseRedirect('/report/')
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
            for participant in item.participant_set.all():
                student_mark = participant.score_set.filter(is_student=True,
                    scored_by__in=User.objects.filter(student__is_rating_confirmed=True)).aggregate(Avg('mark'))['mark__avg']
                jury_mark = participant.score_set.filter(is_student=False).aggregate(Avg('mark'))['mark__avg']
                if student_mark == None:
                    student_mark = 0
                else:
                    student_mark *= 2.5
                if jury_mark == None:
                    jury_mark = 0
                else:
                    jury_mark *= .75
                Result.objects.create(participant=participant, score=student_mark+jury_mark, student_score=student_mark,
                    experts_score=jury_mark)
            item.is_confirmed = True
            item.save()
            return HttpResponse('success')
        else:
            if action == 'publish':
                item.is_result_published = True
            elif action == 'reset':
                item.is_confirmed = False
                item.is_result_published = False
                Result.objects.filter(participant__item = item).all().delete()
            item.save()
            return HttpResponse('success')

        return HttpResponseForbidden()

class ItemListView(ListView):
    model = Item
    template_name = 'item_report.html'
    context_object_name = 'items'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ItemListView, self).dispatch(*args, **kwargs)
    def get_queryset(self):
        if hasattr(self.request.user, 'jury'):
            return self.request.user.jury.items.all()
        return super(ItemListView, self).get_queryset()

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
        ctx['participants'] = []
        for participant in item.participant_set.all():
            jury_score = []
            for jury in item.jury_set.all():
                try:
                    jury_score.append(participant.score_set.get(scored_by=jury.user).mark*.75)
                except ObjectDoesNotExist:
                    jury_score.append('')

            scores = participant.score_set.all()
            jury_mark = scores.filter(is_student=False).aggregate(Avg('mark'))['mark__avg']
            if jury_mark == None:
                jury_mark = 0
                jury_scored = 0
            else:
                jury_mark *= .75
                jury_scored = scores.filter(is_student=False).count()

            students_mark = scores.filter(is_student=True,
                    scored_by__in=User.objects.filter(student__is_rating_confirmed=True)).aggregate(Avg('mark'))['mark__avg']
            if students_mark == None:
                students_mark = 0
                students_scored = 0
            else:
                students_mark *= 2.5
                students_scored = scores.filter(is_student=True).count()

            ctx['participants'].append({'participant': participant, 'jury_score':jury_score, 'jury_mark': jury_mark, 'students_mark': students_mark,
                                        'jury_scored': jury_scored, 'students_scored': students_scored, 'total': jury_mark+students_mark})

        return ctx

class ItemDetailScoreView(DetailView):
    model = Item
    template_name = 'item_scoring.html'
    context_object_name = 'item'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ItemDetailScoreView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        ctx = super(ItemDetailScoreView, self).get_context_data(*args, **kwargs)
        item = self.get_object()
        ctx['participants'] = []
        for participant in item.participant_set.all():
            try:
                score = participant.score_set.get(scored_by=self.request.user)
                outof75 = score.mark * .75
            except ObjectDoesNotExist:
                score = 0
                outof75 = 0
            ctx['participants'].append({'score': score, 'participant':participant, 'outof75': outof75})

        return ctx

def save_score(request):
    if request.method == 'POST' and request.POST.get('item', False):
        item = Item.objects.get(pk=request.POST.get('item', False))
        if not item.jury_set.filter(user=request.user).count() or item.is_confirmed:
            messages.warning(request, 'You are not authorized or the item is confirmed')
            return HttpResponseRedirect('/score/'+str(item.id))

        for p in item.participant_set.all():
            try:
                score = p.score_set.get(scored_by=request.user)
                score.mark = request.POST.get('mark'+str(p.code), 0)
                score.save()
            except ObjectDoesNotExist:
                score = p.score_set.create(scored_by=request.user, mark = request.POST.get('mark'+str(p.code), 0), is_student=False)
                score.save()
        messages.success(request, 'Saved Successfully')
        return HttpResponseRedirect('/score/'+str(item.id))

class SpecialAwardListView(ListView):
    model = SpecialAward
    template_name = 'special_awards.html'
    context_object_name = 'awards'
