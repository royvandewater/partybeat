from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from models import *

def library(request):
    songFiles = SongFile.objects.all() 
    return render_to_response('library.html', locals(), context_instance=RequestContext(request))
