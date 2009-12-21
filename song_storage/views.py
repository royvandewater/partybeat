from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from models import *

def artists(request):
    songFiles = SongFile.objects.all().order_by('artist')
    artists = []
    for song in songFiles:
        if not song.artist in artists:
            artists.append(song.artist)
    category = "artists"
    item_name = "artist"
    items = artists
    return render_to_response('generic.xml', locals(), context_instance=RequestContext(request))

def library(request):
    songFiles = SongFile.objects.all() 
    return render_to_response('library.html', locals(), context_instance=RequestContext(request))
