# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

import xmms2.views as xmms2_views 
import song_storage.views as song_storage_views 

def player(request):
    player = xmms2_views.get_player()
    if player.errored:
        message = player.error
        fix_link = "/action/play/"
        return render_to_response('error.html', locals(), context_instance=RequestContext(request))

    artists = song_storage_views.get_artists()

    return render_to_response('main.html', locals(), context_instance=RequestContext(request))
