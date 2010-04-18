from waveapi import events
from waveapi import appengine_robot_runner
from waveapi import ops
from waveapi import robot
from waveapi import element
from waveapi import wavelet
import logging
import wavewatchers_list
import cgi
import hashlib
from google.appengine.api import mail
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
INDEX_WAVE_ID = 'googlewave.com!w+JOQvIuevS'
WAVELET_ID = 'googlewave.com!conv+root'
SECONDARY_INDEX_ID = 'googlewave.com!w+2DFkTj9KC'
SHORT_PRIMARY_INDEX_ID = 'googlewave.com!w+EXoDbYjDH'
SHORT_SECONDARY_INDEX_ID = 'googlewave.com!w+EXoDbYjDJ'

def displayCommands(wavelet):
  """displayCommands(wavelet):
    Adds the full list of commands in a reply to wavelet"""
  #variable cmds lists all the commands & their descriptions in different list elements
  cmds = ["\n\nList of commands:\n", "addAll", " - adds all the wavewatchers.*\n", "updateIndex", " - re-posts a link to the index wave.\n",
          "isSafe", " - displays info about the publicity & participants of a wave.\n", "makePublic", " - adds the wave-watchers group & \
public to the wave.\n", "displayCommands", " - displays this help message.\n", "publishWave", " - combines addAll and updateIndex. Used when\
 creating a WW wave.\n", "\n*Can only be used by a wave-watcher."]
  #The following lines set up helpful variables giving lengths of the different commands and decriptions
  start_1 = len(cmds[0])
  end_1 = start_1 + len(cmds[1])
  start_2 = end_1 + len(cmds[2])
  end_2 = start_2 + len(cmds[3])
  start_3 = end_2 + len(cmds[4])
  end_3 = start_3 + len(cmds[5])
  start_4 = end_3 + len(cmds[6])
  end_4 = start_4 + len(cmds[7])
  start_5 = end_4 + len(cmds[8])
  end_5 = start_5 + len(cmds[9])
  start_6 = end_5 + len(cmds[10])
  end_6 = start_6 + len(cmds[11])
  all = ''
  #The for loop here combines all commands stored under cmds into one string all
  for i in cmds:
    all += i
  #replies to wavelet with all
  blip = wavelet.reply(all)
  #Annotates as bold the commands using len()s stored above
  blip.range(start_1, end_1).annotate("style/fontWeight", "bold")
  blip.range(start_2, end_2).annotate("style/fontWeight", "bold")
  blip.range(start_3, end_3).annotate("style/fontWeight", "bold")
  blip.range(start_4, end_4).annotate("style/fontWeight", "bold")
  blip.range(start_5, end_5).annotate("style/fontWeight", "bold")
  blip.range(start_6, end_6).annotate("style/fontWeight", "bold")
  blip.range(0, len(a)).annotate("style/fontWeight", "bold")
  #Increases font size of cmds[0]
  blip.range(0, len(a)).annotate('style/fontSize', '1.75em')

def addWavewatchers(event, wavelet, addAll = False):
  """addWavewatchers(event, wavelet, [addAll = False]"""
  #Addall function
  logging.info("addWavewatchers called. Modified by: " + event.modified_by)   #Sends the name of the person calling the commands to the logs
  opQueue = wavelet.get_operation_queue() #Gets the operation queue (see ops module)
  wave_id = wavelet.wave_id #Gets the wave_id of the wave, for use by the ops module
  wavelet_id = wavelet.wavelet_id # Gets wavelet_id of wave, for use by ops module
  opQueue.wavelet_add_participant(wavelet.wave_id, wavelet.wavelet_id, "wave-watchers@googlegroups.com") #Adds the group as a participant on the wave.
  opQueue.wavelet_add_participant(wavelet.wave_id, wavelet.wavelet_id, "nat.abbotts@googlewave.com") #Adds me as a participant on the wave (I want to be notified of everything now) :]
  if event.modified_by not in wavewatchers_list.safe: #If the active user is not a wave-watcher/on the safe list...
    wavelet.reply("Wavewatchers Team Notified") #Tell them that the wave-watchers have been notified
    return True #End the addAll function, return to whatever called it
  if addAll: #If the variable addAll was provided and is true...
    logging.info("addAll Called")
    change = None
    for participant in wavewatchers_list.waveWatchers:
      if participant not in wavelet.participants:
        opQueue.wavelet_add_participant(wave_id, wavelet_id, participant)
        change = True
    if change:
      wavelet.reply("WaveWatchers Team All Added")
    else:
      wavelet.reply("WaveWatchers Team Already Partipants")
  else:
    for participant in wavewatchers_list.waveWatchers:
      opQueue.wavelet_add_participant(wave_id, wavelet_id, participant)
    wavelet.reply("WaveWatchers Team Added")
  return False
  
def tagWavelet(event, wavelet):
  logging.info("TagWavelet Called")
  opQueue = wavelet.get_operation_queue()
  wave_id = wavelet.wave_id
  wavelet_id = wavelet.wavelet_id
  current_tags = wavelet.tags
  if "wavewatchers" not in current_tags:
    opQueue.wavelet_modify_tag(wave_id, wavelet_id, "wavewatchers")
  if "wave-watchers" not in current_tags:
    opQueue.wavelet_modify_tag(wave_id, wavelet_id, "wave-watchers")
	
def checkBadParticipants(event, wavelet):
  badParticipants = []
  for participant in wavelet.participants:
    if participant in wavewatchers_list.bad:
      badParticipants.append(participant)
  intro_str = ""
  bad_p_str = ""
  if badParticipants:
    intro_str = "\nKnown Trolls/Spammers that are participants: "
    for villain in badParticipants:
      bad_p_str += villain + ", "
  return intro_str, bad_p_str
	  
def checkRobots(event, wavelet):
  robotParticipants = []
  for participant in wavelet.participants:
    if participant.split("@")[1] == "appspot.com":
      robotParticipants.append(participant)
  intro_str = "\nRobots that are participants: "
  robots_str = ''
  for participant in robotParticipants:
    if len(robotParticipants) <= 1:
      robots_str += participant
    else:
      robots_str += participant + ", "
  return intro_str, robots_str
  
def updateIndex(event, wavelet, state = False):
  global myRobot
  content = ["\n\n\n\nTitle: ",]
  if wavelet.title:
    content[1] = wavelet.title
  else:
    content[1] = "(untitled wave)"
  content += ["\nIndexed By: ", event.modified_by, "\nWave ID: ", wavelet.wave_id, "\nWave was created by: ", wavelet.creator, None, None, None, None]
  content[8], content[9] = checkBadParticipants(event, wavelet)
  content[10], content[11] = checkRobots(event, wavelet)
  lastline = 0
  if "public@a.gwave.com" in wavelet.participants:
    content.append("\nThe wave is public.")
    lastline = 1
  elif "wave-watchers@googlegroups.com" in wavelet.participants:
    content.append("\nThe wave is not public, but viewable by a wave-watcher.")
    lastline = 2
  elif state:
    content.append("\nThe wave is not public, but viewable by a wave-watcher.")
    lastline = 2
  else:
    content.append("\nThe wave is not public, and wave-watchers were added individually.")
    lastline = 3
  titleLength = len(wavelet.title)
  start_1 = 0
  #Oooh. Pretty alignment...
  end_1 = start_1 + len(content_1)
  start_2 = end_1 + len(content_2)
  end_2 = start_2 + len(content_3)
  start_3 = end_2 + len(content_4)
  end_3 = start_3 + len(content_5)
  start_4 = end_3 + len(content_6)
  end_4 = start_4 + len(content_7)
  start_5 = end_4 + len(content_8)
  end_5 = start_5 + len(content_9)
  start_6 = end_5 + len(content_10)
  end_6 = start_6 + len(content_11)
  start_7 = end_6 + len(content_12)
  end_7 = start_7 + len(content_13)
  content = content_1 + content_2 + content_3 + content_4 + content_5 + content_6 + content_7 + content_8 + content_9 + content_10 + content_11 + content_12 + content_13
  if event.modified_by in wavewatchers_list.safe:
    indexWave = myRobot.fetch_wavelet(INDEX_WAVE_ID, WAVELET_ID)
    blip = indexWave.reply(content)
    blip.range(start_1, end_1).annotate("style/fontWeight", "bold")
    blip.range(start_2, end_2).annotate("style/fontWeight", "bold")
    blip.range(start_3, end_3).annotate("style/fontWeight", "bold")
    blip.range(start_4, end_4).annotate("style/fontWeight", "bold")
    blip.range(start_5, end_5).annotate("style/fontWeight", "bold")
    blip.range(start_6, end_6).annotate("style/fontWeight", "bold")
    blip.range(start_7, end_7).annotate("style/fontStyle", "italic")
    if lastline == 1:
      blip.range(start_7, end_7).annotate("style/backgroundColor", 'rgb(229, 51, 51)')
      blip.range(start_7, end_7).annotate("style/color", 'rgb(255, 255, 255)')
    elif lastline == 2:
      blip.range(start_7, end_7).annotate("style/backgroundColor", 'rgb(96, 217, 120)')
      blip.range(start_7, end_7).annotate("style/color", 'rgb(0, 0, 0)')
    elif lastline == 3:
      blip.range(start_7, end_7).annotate("style/backgroundColor", 'rgb(255, 229, 0)')
      blip.range(start_7, end_7).annotate("style/color", 'rgb(0, 0, 0)')
    blip.range(end_1, start_2).annotate("link/wave", wavelet.wave_id)
    blip.range(end_1, start_2).annotate("wave-watchers/id", wavelet.wave_id)
    blip.range(end_3, start_4).annotate("style/fontFamily", 'monospace')
    myRobot.submit(indexWave)
    shortIndexWave = myRobot.fetch_wavelet(SHORT_PRIMARY_INDEX_ID, WAVELET_ID)
    lenTitle = len(wavelet.title)
    rootBlip = shortIndexWave.root_blip
    line1 = element.Line(line_type='li')
    rootBlip.append(line1)
    lenBeforeEdit = len(shortIndexWave.root_blip.text) - 1
    firstAppend = wavelet.title + " "
    rootBlip.append(firstAppend)
    rootBlip.range(lenBeforeEdit, lenBeforeEdit + len(firstAppend)).annotate("link/wave", wavelet.wave_id)
    line2 = element.Line(line_type='li', indent = 1)
    myRobot.submit(shortIndexWave)	
  else:
    secondaryIndexWave = myRobot.fetch_wavelet(SECONDARY_INDEX_ID, WAVELET_ID)
    blip = secondaryIndexWave.reply(content)
    blip.range(start_1, end_1).annotate("style/fontWeight", "bold")
    blip.range(start_2, end_2).annotate("style/fontWeight", "bold")
    blip.range(start_3, end_3).annotate("style/fontWeight", "bold")
    blip.range(start_4, end_4).annotate("style/fontWeight", "bold")
    blip.range(start_5, end_5).annotate("style/fontWeight", "bold")
    blip.range(start_6, end_6).annotate("style/fontWeight", "bold")
    blip.range(start_7, end_7).annotate("style/fontStyle", "italic")
    if lastline == 1:
      blip.range(start_7, end_7).annotate("style/backgroundColor", 'rgb(229, 51, 51)')
      blip.range(start_7, end_7).annotate("style/color", 'rgb(255, 255, 255)')
    elif lastline == 2:
      blip.range(start_7, end_7).annotate("style/backgroundColor", 'rgb(96, 217, 120)')
      blip.range(start_7, end_7).annotate("style/color", 'rgb(0, 0, 0)')
    elif lastline == 3:
      blip.range(start_7, end_7).annotate("style/backgroundColor", 'rgb(255, 229, 0)')
      blip.range(start_7, end_7).annotate("style/color", 'rgb(0, 0, 0)')
    blip.range(end_1, start_2).annotate("link/wave", wavelet.wave_id)
    blip.range(end_3, start_4).annotate("wave-watchers/id", wavelet.wave_id)
    blip.range(end_3, start_4).annotate("style/fontFamily", 'monospace')
    myRobot.submit(secondaryIndexWave)
    shortIndexWave = myRobot.fetch_wavelet(SHORT_SECONDARY_INDEX_ID, WAVELET_ID)
    lenTitle = len(wavelet.title)
    rootBlip = shortIndexWave.root_blip
    line1 = element.Line(line_type='li')
    rootBlip.append(line1)
    lenBeforeEdit = len(shortIndexWave.root_blip.text) - 1
    firstAppend = wavelet.title + " "
    rootBlip.append(firstAppend)
    rootBlip.range(lenBeforeEdit, lenBeforeEdit + len(firstAppend)).annotate("link/wave", wavelet.wave_id)
    myRobot.submit(shortIndexWave)		
	  
	  
def BlockTroll(event, wavelet):
  logging.debug("BlockTroll Called")
	  
def OnWaveletSelfAdded(event, wavelet):
  logging.info("OnWaveletSelfAdded called")
  tagWavelet(event, wavelet)
  if event.modified_by not in wavewatchers_list.safe:
    state = addWavewatchers(event, wavelet)
    logging.info("Program continues.")
    updateIndex(event, wavelet, state)
  else:
    wavelet.reply("\nType 'publishWave' in a reply to add the wave-watchers individually & submit this wave to the index.")
  displayCommands(wavelet)
  
  
def OnBlipSubmitted(event, wavelet):
  logging.info("OnBlipSubmitted Called")
  logging.info("Blip text = " + event.blip.text)
  logging.info("WaveID = " + wavelet.wave_id)
  logging.info("WaveletID = " + wavelet.wavelet_id)
  logging.info("Blip ID = " + event.blip_id)
  logging.info(event.blip.annotations.serialize())
  opQueue = wavelet.get_operation_queue()
  if "makePublic" in event.blip.text:
    logging.info("makePublic Found")
    opQueue.wavelet_add_participant(wavelet.wave_id, wavelet.wavelet_id, "wave-watchers@googlegroups.com")
    opQueue.wavelet_add_participant(wavelet.wave_id, wavelet.wavelet_id, "public@a.gwave.com")
    wavelet.reply("\nMake sure that public is set as read-only!")
    logging.info("makePublic Completed")
  if "addAll" in event.blip.text:
    logging.info("addAll Found")
    addWavewatchers(event, wavelet, addAll = True)
    logging.info("addAll Completed")
  if "isSafe" in event.blip.text:
    logging.info("isSafe Found")
    isUnsafe = None
    nonWW = []
    for participant in wavelet.participants:
      if participant not in wavewatchers_list.safe:
		isUnsafe = True
		nonWW.append(participant)
    if not isUnsafe:
      wavelet.reply("\nOnly Wave Watchers can view this wave.")
    elif "public@a.gwave.com" in wavelet.participants:
      wavelet.reply("\nAll Wave users can view this wave.")
    else:
	  content = "\nSome Participants are not wave-watchers. Those are:\n"
	  for participant in nonWW:
		content += participant + " ,\n"
	  wavelet.reply(content)
    logging.info("isSafe Completed")
  if "updateIndex" in event.blip.text:
    logging.info("updateIndex Found")
    updateIndex(event, wavelet)
    logging.info("updateIndex Completed")
  if "displayCommands" in event.blip.text:
    logging.info("displayCommands Found")
    displayCommands(wavelet)
    logging.info("displayCommands Completed")
  if "publishWave" in event.blip.text:
    logging.info("publishWave Found")
    updateIndex(event, wavelet, state = False)
    state = addWavewatchers(event, wavelet, addAll = False)
    logging.info("publishWave Completed")
	#
	#
	#
  if "chuckNorris" in event.blip.text:
    if event.modified_by not in wavewatchers_list.safe:
	  logging.info("OnBlipSubmitted Completed")
	  return
    global myRobot
    if "chuckNorris(" in event.blip.text:
      text = event.blip.text.split("chuckNorris(")[1]
      text = text.split(")")
      chuckNorris = myRobot.new_wave(wavelet.domain, participants = ["wave-watchers@googlegroups.com", event.modified_by, text[0]], submit = True)
      chuckNorrisIndex = myRobot.fetch_wavelet('googlewave.com!w+mTNnWQtAx', WAVELET_ID)
      blip = chuckNorrisIndex.reply("\n" + text[0] + " ")
      blip.range(0, len("\n" + text[0])).annotate("link/wave", chuckNorris.wave_id)
      chuckNorrisOpQ = chuckNorris.get_operation_queue()
      chuckNorrisOpQ.wavelet_set_title(chuckNorris.wave_id, chuckNorris.wavelet_id, "Chuck Norris just kicked " + text[0] + " troll ASS!")
      wavelet.reply("\nOoooh! " + text[0] + " just got Chuck Norris'ed!")	  
    else:
      chuckNorris = myRobot.new_wave(wavelet.domain, participants = ["wave-watchers@googlegroups.com", event.modified_by], message = '', submit = True)
      chuckNorrisIndex = myRobot.fetch_wavelet('googlewave.com!w+mTNnWQtAx', WAVELET_ID)
      blip = chuckNorrisIndex.reply("\nA Troll Got Chuck Norris'ed " )
      blip.range(0, len("\nA Troll Got Chuck Norris'ed")).annotate("link/wave", chuckNorris.wave_id)
      chuckNorrisOpQ = chuckNorris.get_operation_queue()
      chuckNorrisOpQ.wavelet_set_title(chuckNorris.wave_id, chuckNorris.wavelet_id, "Chuck Norris just kicked a troll's ASS!")
      wavelet.reply("\nOoooh! A troll just got Chuck Norris'ed!")
    wavelet.root_blip.append(element.Image(url = 'http://lh4.ggpht.com/_21nXtfYRLLQ/S8TWNljJD3I/AAAAAAAABqk/KbMTcXE27GA/chuckwave.png',caption = 'Your  conquerer'))
    myRobot.submit(chuckNorrisIndex)
    myRobot.submit(chuckNorris)
  logging.info("OnBlipSubmitted Completed")
  
def OnWaveletCreated(event, wavelet):
  logging.warning("OnWaveletCreated Called")

def OnWaveletTitleChanged(event, wavelet):
  logging.warning("OnWaveletTitleChanged Called")
  updateIndex(event, wavelet)
  
def OnGadgetStateChanged(event, wavelet):
  logging.debug("OnGadgetStateChanged Called")
  if wavelet.wave_id != 'googlewave.com!w+Gyh_bn35B':
    return
  alerts = ['GREEN','YELLOW','RED']
  logging.debug(event.index)
  logging.debug(event.blip.elements)
  for pos in range(len(event.blip.elements)):
    logging.info(event.blip.elements[pos])
    if "waveapi.element.Gadget" in str(event.blip.elements[pos]):
	  pos2 = pos
	  break
  gad = event.blip.elements[pos]
  if gad is not None and gad.get('url')=='http://everybodywave.appspot.com/gadget/alerter/gad.xml': 
    alert_text = alerts[int(gad.get('level'))]
    new_title = "[%s] Public Waves Abuse Alert Level" % alert_text
    opQ = wavelet.get_operation_queue()
    opQ.wavelet_set_title(wavelet.wave_id, wavelet.wavelet_id, new_title)
	

if __name__ == '__main__':
  myRobot = robot.Robot("WaveWatchers' Bot", 
  image_url='http://wave-watchers.appspot.com/Wave-Watchers.png',
  profile_url='http://groups.google.com/group/wave-watchers')
  import verify
  myRobot.setup_oauth(verify.consumerKey, verify.consumerSecret, server_rpc_base='http://gmodules.com/api/rpc')
  myRobot.register_handler(events.WaveletSelfAdded, OnWaveletSelfAdded)
  myRobot.register_handler(events.BlipSubmitted, OnBlipSubmitted)
  myRobot.register_handler(events.WaveletTitleChanged, OnWaveletTitleChanged)
  myRobot.register_handler(events.GadgetStateChanged, OnGadgetStateChanged)
  myRobot.register_handler(events.WaveletCreated, OnWaveletCreated)
  appengine_robot_runner.run(myRobot)
