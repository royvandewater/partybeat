from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, loader, RequestContext
import xmmsclient
import os

from models import *

def player(request):
  return render_to_response('player.html', locals(), context_instance=RequestContext(request))

def run_action(request, action):
  xmms2 = xmms_controller()
  message = xmms2.do_action(action)
  return render_to_response('player.html', locals(), context_instance=RequestContext(request))

class xmms_controller:
  def __init__(self):
    self.xmms = get_xmmsclient()

  def do_action(self, action):
    if action == "play":
      return self.play()
    elif action == "stop":
      return self.stop()
    elif action == "pause":
      return self.pause()


  def pause(self):
    result = self.xmms.playback_pause()
    result.wait()

    return self.print_playback_error(result, "pause")


  def play(self):
    result = self.xmms.playback_start()
    result.wait()
    
    return self.print_playback_error(result, "play")


  def stop(self):
    result = self.xmms.playback_stop()
    result.wait()
    
    return self.print_playback_error(result, "stop")



  def print_playback_error(self, result, action):
    if result.iserror():
      return("playback %s returned error, %s" % (action, result.get_error()))
    else:
      return("playback %s run" % (action)) 

def get_xmmsclient():
  xmms = xmmsclient.XMMS("xmms2")
  try:
    xmms.connect(os.getenv("XMMS_PATH"))
    return xmms
  except IOError, detail:
    return ("Connection failed: %s" % detail)
