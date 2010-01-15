from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from models import *
from xmms_layer import Xmms_layer
from xmms2_django.library.models import SongFile

def get_blank(request):
    try:
        return render_to_response('blank.html') if request.POST['source'] == "ajax" else HttpResponseRedirect('/')
    except (KeyError):
        return HttpResponseRedirect('/')

# def player(request):
    # xmms2 = Xmms_layer()
    # return render_to_response('player.html', locals(), context_instance=RequestContext(request))

def run_action(request, action):
    xmms_layer = Xmms_layer()
    xmms_layer.store_action(action)
    return get_blank(request)

def get_info(request):
    xmms_layer = Xmms_layer()
    xmms_layer.load_player_from_db()
    player = xmms_layer.player
    return render_to_response('player/info.xml', locals(), context_instance=RequestContext(request))

def playlist(request):
    xmms_layer = Xmms_layer()
    xmms_layer.load_player_from_db()
    player = xmms_layer.player
    return render_to_response('player/playlist.html', locals(), context_instance=RequestContext(request))

def delete(request, position):
    xmms_layer = Xmms_layer()
    xmms_layer.store_action("delete_{0}".format(int(position) - 1))
    return get_blank(request)

def seek(request, seek_time):
    xmms_layer = Xmms_layer()
    xmms_layer.store_action("seek_{0}".format(int(seek_time)))
    return get_blank(request)
