from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from models import *
from xmms_controller import Xmms_controller
from xmms_layer import Xmms_layer
from player_info import Player
from xmms2_django.song_storage.models import SongFile

def get_blank(request):
    try:
        return render_to_response('blank.html') if request.POST['source'] == "ajax" else HttpResponseRedirect('/')
    except (KeyError):
        return HttpResponseRedirect('/')

def player(request):
    xmms2 = Xmms_controller()
    player = xmms2.get_player_info()
    songFiles = SongFile.objects.all()
    return render_to_response('player.html', locals(), context_instance=RequestContext(request))

def run_action(request, action):
    xmms2 = Xmms_controller()
    message = xmms2.do_action(action)
    return get_blank(request)

def refresh(request):
    xmms_layer = Xmms_layer(True)
    return get_blank(request)

def get_info(request):
    xmms_layer = Xmms_layer()
    player = xmms_layer.player
    return render_to_response('info.xml', locals(), context_instance=RequestContext(request))

def fix(request):
    xmms_layer = Xmms_layer(True)
    return player(request)

def playlist(request):
    player = Xmms_layer().player
    return render_to_response('playlist.html', locals(), context_instance=RequestContext(request))

def delete(request, xmms_id):
    xmms2 = Xmms_controller()
    xmms2.delete(xmms_id)
    return get_blank(request)
