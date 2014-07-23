from django.shortcuts import render_to_response
from fest.models import *

def items(request):
    items = Item.objects.all()
    return render_to_response('itemlist.html', { 'items': items})

