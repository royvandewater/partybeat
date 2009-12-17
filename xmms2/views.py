from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from models import *
from xmms_controller import Xmms_controller
from xmms_layer import Xmms_layer
from player_info import Player

def player(request):
    xmms2 = Xmms_controller()
    player = xmms2.get_player_info()
    return render_to_response('player.html', locals(), context_instance=RequestContext(request))

def run_action(request, action):
    xmms2 = Xmms_controller()
    message = xmms2.do_action(action)
    try:
        return render_to_response('blank.html') if request.POST['source'] == "ajax" else HttpResponseRedirect('/')
    except (KeyError):
        return HttpResponseRedirect('/')

def get_info(request):
    xmms_layer = Xmms_layer()
    player = xmms_layer.player
    return render_to_response('info.xml', locals(), context_instance=RequestContext(request))
