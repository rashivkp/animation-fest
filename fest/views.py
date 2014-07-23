from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
import json
from django.core import serializers
from fest.models import *
from django.views.decorators.csrf import csrf_exempt

def items(request):
    items = Item.objects.all()
    return render_to_response('itemlist.html', { 'items': items})

@csrf_exempt
def rateMe(request):
    if request.method == 'POST':
        print request.POST['idStudent']
        students = Student.objects.all()
        return HttpResponse(serializers.serialize('json', students ),
            mimetype='application/json')

