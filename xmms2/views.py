from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, loader, RequestContext

from models import *
from xmms_controller import Xmms_controller, Player

def player(request):
  player = Player()
  xmms2 = Xmms_controller()
  player = xmms2.get_player_info(player)
  player = xmms2.get_player_status(player)
  return render_to_response('player.html', locals(), context_instance=RequestContext(request))

def run_action(request, action):
  player = Player();
  xmms2 = Xmms_controller()
  message = xmms2.do_action(action)
  player = xmms2.get_player_info(player)
  player = xmms2.get_player_status(player)
  return render_to_response('player.html', locals(), context_instance=RequestContext(request))
