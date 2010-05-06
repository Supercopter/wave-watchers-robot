from waveapi import events
from waveapi import ops
from waveapi import robot
from waveapi import element
from waveapi import wavelet
import logging
#import cgi
#import testing
#import hashlib
#from google.appengine.api import mail
#from google.appengine.ext import webapp
#from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from waveapi import appengine_robot_runner
import wavewatcher_class
INDEX_WAVE_ID = 'googlewave.com!w+JOQvIuevS'
WAVELET_ID = 'googlewave.com!conv+root'
SECONDARY_INDEX_ID = 'googlewave.com!w+2DFkTj9KC'
SHORT_PRIMARY_INDEX_ID = 'googlewave.com!w+EXoDbYjDH'
SHORT_SECONDARY_INDEX_ID = 'googlewave.com!w+EXoDbYjDJ'
WAVEWATCHERS_ALL = []
q = db.GqlQuery('SELECT * FROM WaveWatchers')
for i in q:
  WAVEWATCHERS_ALL.append(i.userid)
WAVEWATCHERS_OWNERS = []
q = db.GqlQuery('SELECT * FROM WaveWatchers WHERE level = 1')
for i in q:
  WAVEWATCHERS_OWNERS.append(i.userid)
GREYLIST = []
q = db.GqlQuery('SELECT * FROM Villain WHERE level = 2')
for i in q:
  GREYLIST.append(i.userid)
BLACKLIST = []
q = db.GqlQuery('SELECT * FROM Villain WHERE level = 1')
for i in q:
  BLACKLIST.append(i.userid)
VILLAINS = []
q = db.GqlQuery('SELECT * FROM Villain')
for i in q:
  VILLAINS.append(i.userid)

def addWaveWatcher(event, wavelet, wavewatcher, level = 2):
  logging.warning("%s is trying to add a new wavewatcher (%s) as level %s" % (modified_by, wavewatcher, level)) #Adds a record of the attempt to the logs
  if event.modified_by in WAVEWATCHERS_OWNERS:
    import wavewatcher_class
    rec = wavewatcher_class.WaveWatchers(userid=wavewatcher, level=level)
    rec.put()
    easyLevels = {}
    for key in wavewatcher_class.ACCESS_LEVELS.keys():
      easyLevels[wavewatcher_class.ACCESS_LEVELS[key]] = key
    if level == 1:
      i = "as an"
    elif level == 3:
      i = "as"
    else:
      i = "as a"
    wavelet.reply("%s successfully added %s %s %s" % (event.modified_by, wavewatcher, i, easylevels[level]))
    logging.warning("%s was added successfully" % wavewatcher)
  else:
    wavelet.reply("You do not have permission to perform that operation - Ask a group owner to do it for you.")
  logging.info("addWaveWatcher completed")

def addBadUser(event, wavelet, troll, level = 2):
  if event.modified_by in WAVEWATCHERS_OWNERS:
    import wavewatcher_class
    rec = wavewatcher_class.Villain(userid=troll, level=level)
    rec.put()
    if level == 1:
      wavelet.reply("%s was successfully BLACKLISTED by %s" % (troll, event.modified_by))
    else:
      wavelet.reply("%s was successfully GREYLISTED %s" % (troll, event.modified_by))
  else:
    wavelet.reply("You do not have permission to perform that operation - Ask a group owner to do it for you.")

  

def displayCommands(wavelet):
  """displayCommands(wavelet):
    Adds the full list of commands in a reply to wavelet"""
  logging.info("displayCommands Called")
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
  blip.range(0, len(cmds[0]) - 1).annotate("style/fontWeight", "bold")
  #Increases font size of cmds[0]  
  blip.range(0, len(cmds[0]) - 1).annotate('style/fontSize', '1.75em')
  logging.info("displayCommands completed")

def addWavewatchers(event, wavelet, addAll = True):
  """addWavewatchers(event, wavelet)"""
  logging.info("addWavewatchers Called")
  #Addall function
  logging.info("addWavewatchers called. Modified by: " + event.modified_by)   #Sends the name of the person calling the commands to the logs
  opQueue = wavelet.get_operation_queue() #Gets the operation queue (see ops module)
  wave_id = wavelet.wave_id #Gets the wave_id of the wave, for use by the ops module
  wavelet_id = wavelet.wavelet_id # Gets wavelet_id of wave, for use by ops module
  opQueue.wavelet_add_participant(wavelet.wave_id, wavelet.wavelet_id, "nat.abbotts@googlewave.com") #Adds me as a participant on the wave (I want to be notified of everything now) :]
  if event.modified_by not in WAVEWATCHERS_ALL: #If the active user is not a wave-watcher/on the safe list...
    opQueue.wavelet_add_participant(wavelet.wave_id, wavelet.wavelet_id, "wave-watchers@googlegroups.com") #Adds the group as a participant on the wave.
    wavelet.reply("Wavewatchers Team Notified") #Tell them that the wave-watchers have been notified
    return True #End the addAll function, return to whatever called it
  allAdded = None #create variable 'alladded' to be used later.
  ownersAdded = None
  results = WAVEWATCHERS_OWNERS #Queries the datastore & returns wavewatchers that are owners.
  for participant in results:
    if participant not in wavelet.participants:
      opQueue.wavelet_add_participant(wave_id, wavelet_id, participant)
      ownersAdded = True
  if (not addAll) and (event.modified_by not in results): 
    results = WAVEWATCHERS_ALL #Queries the datastore & returns wavewatchers that are members.
    for participant in results:
      if participant not in wavelet.participants:
        opQueue.wavelet_add_participant(wave_id, wavelet_id, participant)
        allAdded = True
    opQueue.wavelet_add_participant(wavelet.wave_id, wavelet.wavelet_id, "wave-watchers@googlegroups.com") #Adds the group as a participant on the wave.
  elif addAll:
    results = WAVEWATCHERS_ALL
    for participant in results:
      if participant not in wavelet.participants:
        opQueue.wavelet_add_participant(wave_id, wavelet_id, participant.userid)
        allAdded = True
    opQueue.wavelet_add_participant(wavelet.wave_id, wavelet.wavelet_id, "wave-watchers@googlegroups.com") #Adds the group as a participant on the wave.  
  if allAdded:
    wavelet.reply("WaveWatchers Team All Added")
  elif ownersAdded:
    wavelet.reply("Owners Added")
  else:
    wavelet.reply("WaveWatchers Team Already Partipants")
  logging.info("addWavewatchers Completed")
  return False #Placeholder in case I missed something below. Will be removed in future.
  
def tagWavelet(event, wavelet):
  """Tags the wave tagWavelet(event, wavelet)"""
  logging.info("TagWavelet Called")
  opQueue = wavelet.get_operation_queue() #gets operation queue
  wave_id = wavelet.wave_id
  wavelet_id = wavelet.wavelet_id
  current_tags = wavelet.tags
  if "wavewatchers" not in current_tags:
    opQueue.wavelet_modify_tag(wave_id, wavelet_id, "wavewatchers") #tags with first tag
  if "wave-watchers" not in current_tags:
    opQueue.wavelet_modify_tag(wave_id, wavelet_id, "wave-watchers") #tags with second tag
  logging.info("TagWavelet Completed")
  
def checkBadParticipants(event, wavelet):
  """checkBadParticipants(event, wavelet) checks for people in the black/grey list. Returns 2 args"""
  logging.info("checkBadParticipants Called")
  blacklisted = []
  greylisted = []
  blacklist = BLACKLIST
  greylist = GREYLIST
  for participant in wavelet.participants:
    if participant in blacklist:
      blacklisted.append(participant)
    else:
      greylist.append(participant)
  intro_str = ""
  bad_p_str = ""
  intro_str2 = ""
  bad_p_str2 = ""
  if blacklisted:
    intro_str = "\nKnown BLACKLISTED users that are participants:"
    for villain in blacklisted:
      bad_p_str += villain + ', '
  if greylisted:
    intro_str2 = "\nKnown GREYLISTED users that are participants:"
    for villain in greylisted:
      bad_p_str2 += villain + ', '
  logging.info("checkBadParticipants Completed")
  return intro_str, bad_p_str, intro_str2, bad_p_str2
    
def checkRobots(event, wavelet):
  """checkRobots(event, wavelet) checks for robots. Returns 2 args"""
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
    content.append(wavelet.title)
  else:
    content.append("(untitled wave)")
  content += ["\nIndexed By: ", event.modified_by, "\nWave ID: ", wavelet.wave_id, "\nWave was created by: ", wavelet.creator, None, None, None, None, None, None]
  content[8], content[9], content[10], content[11] = checkBadParticipants(event, wavelet)
  content[12], content[13] = checkRobots(event, wavelet)
  lastline = 0
  if "public@a.gwave.com" in wavelet.participants:
    content.append("\nThe wave is public.")
    lastline = 1
  elif "wave-watchers@googlegroups.com" in wavelet.participants:
    content.append("\nThe wave is not public, but viewable by a wave-watcher.")
    lastline = 2
  else:
    content.append("\nThe wave is not public, but viewable by a wave-watcher.")
    lastline = 2

  titleLength = len(wavelet.title)
  start_1 = 0
  #Oooh. Pretty alignment...
  end_1 = start_1 + len(content[0])
  start_2 = end_1 + len(content[1])
  end_2 = start_2 + len(content[2])
  start_3 = end_2 + len(content[3])
  end_3 = start_3 + len(content[4])
  start_4 = end_3 + len(content[5])
  end_4 = start_4 + len(content[6])
  start_5 = end_4 + len(content[7])
  end_5 = start_5 + len(content[8])
  start_6 = end_5 + len(content[9])
  end_6 = start_6 + len(content[10])
  start_7 = end_6 + len(content[11])
  end_7 = start_7 + len(content[12])
  start_8 = end_7 + len(content[13])
  end_8 = start_8 + len(content[14])
  text = ''
  for i in content:
    text += i
  if event.modified_by in wavewatchers_list.safe:
    indexWave = myRobot.fetch_wavelet(INDEX_WAVE_ID, WAVELET_ID)
    blip = indexWave.reply(text)
    blip.range(start_1, end_1).annotate("style/fontWeight", "bold")
    blip.range(start_2, end_2).annotate("style/fontWeight", "bold")
    blip.range(start_3, end_3).annotate("style/fontWeight", "bold")
    blip.range(start_4, end_4).annotate("style/fontWeight", "bold")
    blip.range(start_5, end_5).annotate("style/fontWeight", "bold")
    blip.range(start_6, end_6).annotate("style/fontWeight", "bold")
    blip.range(start_7, end_7).annotate("style/fontWeight", "bold")
    blip.range(start_8, end_8).annotate("style/fontStyle", "italic")
    if lastline == 1:
      blip.range(start_8, end_8).annotate("style/backgroundColor", 'rgb(229, 51, 51)')
      blip.range(start_8, end_8).annotate("style/color", 'rgb(255, 255, 255)')
    elif lastline == 2:
      blip.range(start_8, end_8).annotate("style/backgroundColor", 'rgb(96, 217, 120)')
      blip.range(start_8, end_8).annotate("style/color", 'rgb(0, 0, 0)')
    elif lastline == 3:
      blip.range(start_8, end_8).annotate("style/backgroundColor", 'rgb(255, 229, 0)')
      blip.range(start_8, end_8).annotate("style/color", 'rgb(0, 0, 0)')
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
    blip = secondaryIndexWave.reply(text)
    blip.range(start_1, end_1).annotate("style/fontWeight", "bold")
    blip.range(start_2, end_2).annotate("style/fontWeight", "bold")
    blip.range(start_3, end_3).annotate("style/fontWeight", "bold")
    blip.range(start_4, end_4).annotate("style/fontWeight", "bold")
    blip.range(start_5, end_5).annotate("style/fontWeight", "bold")
    blip.range(start_6, end_6).annotate("style/fontWeight", "bold")
    blip.range(start_7, end_7).annotate("style/fontWeight", "bold")
    blip.range(start_8, end_8).annotate("style/fontStyle", "italic")
    if lastline == 1:
      blip.range(start_8, end_8).annotate("style/backgroundColor", 'rgb(229, 51, 51)')
      blip.range(start_8, end_8).annotate("style/color", 'rgb(255, 255, 255)')
    elif lastline == 2:
      blip.range(start_8, end_8).annotate("style/backgroundColor", 'rgb(96, 217, 120)')
      blip.range(start_8, end_8).annotate("style/color", 'rgb(0, 0, 0)')
    elif lastline == 3:
      blip.range(start_8, end_8).annotate("style/backgroundColor", 'rgb(255, 229, 0)')
      blip.range(start_8, end_8).annotate("style/color", 'rgb(0, 0, 0)')
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
    logging.debug(text)
    logging.info("updateIndex func Completed")
      
def BlockTroll(event, wavelet):
  logging.debug("BlockTroll Called")
    
def OnWaveletSelfAdded(event, wavelet):
  logging.info("OnWaveletSelfAdded called")
  tagWavelet(event, wavelet)
  results = WAVEWATCHERS_ALL
  if event.modified_by not in results:
    addWavewatchers(event, wavelet)
    logging.info("Program continues.")
    updateIndex(event, wavelet)
  else:
    wavelet.reply("\nType 'publishWave' in a reply to add the wave-watchers individually & submit this wave to the index.")
  displayCommands(wavelet)
  
def OnBlipSubmitted(event, wavelet):
  logging.info("OnBlipSubmitted Called")
  if event.blip.text:
    logging.info("Blip text = " + event.blip.text)
  if "#!NO" in event.blip.text[:5]:
    return
  logging.info("WaveID = " + wavelet.wave_id)
  logging.info("WaveletID = " + wavelet.wavelet_id)
  logging.info("Blip ID = " + event.blip_id)
  logging.info(event.blip.annotations.serialize())
  opQueue = wavelet.get_operation_queue()
  if event.blip.text:
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
    if "addOwners" in event.blip.text:
      addWavewatchers(event, wavelet, addAll = False)
    if "isSafe" in event.blip.text:
      logging.info("isSafe Found")
      isUnsafe = None
      nonWW = []
      results = WAVEWATCHERS_ALL
      for participant in wavelet.participants:
        if participant not in results:
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
      state = addWavewatchers(event, wavelet)
      updateIndex(event, wavelet, state)
      logging.info("publishWave Completed")
    if "chuckNorris" in event.blip.text:
      if event.modified_by not in WAVEWATCHERS_ALL:
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
        reply = wavelet.reply("\nOoooh! " + text[0] + " just got Chuck Norris'ed!")   
      else:
        chuckNorris = myRobot.new_wave(wavelet.domain, participants = ["wave-watchers@googlegroups.com", event.modified_by], message = '', submit = True)
        chuckNorrisIndex = myRobot.fetch_wavelet('googlewave.com!w+mTNnWQtAx', WAVELET_ID)
        blip = chuckNorrisIndex.reply("\nA Troll Got Chuck Norris'ed " )
        blip.range(0, len("\nA Troll Got Chuck Norris'ed")).annotate("link/wave", chuckNorris.wave_id)
        chuckNorrisOpQ = chuckNorris.get_operation_queue()
        chuckNorrisOpQ.wavelet_set_title(chuckNorris.wave_id, chuckNorris.wavelet_id, "Chuck Norris just kicked a troll's ASS!")
        reply = wavelet.reply("\nOoooh! A troll just got Chuck Norris'ed!")
      reply.range(0, 7).annotate("link/wave", chuckNorris.wave_id)
      #wavelet.root_blip.append(element.Image(url = 'http://lh4.ggpht.com/_21nXtfYRLLQ/S8TWNljJD3I/AAAAAAAABqk/KbMTcXE27GA/chuckwave.png',caption = 'Your  conquerer'))
      chuckNorris.root_blip.append(element.Image(url = 'http://lh4.ggpht.com/_21nXtfYRLLQ/S8TWNljJD3I/AAAAAAAABqk/KbMTcXE27GA/chuckwave.png',caption = 'Your  conquerer'))
      myRobot.submit(chuckNorrisIndex)
      myRobot.submit(chuckNorris)
    if "addMember(" in event.blip.text:
      addWaveWatcher(event, wavelet, event.blip.text.split("addMember(")[1].split(")")[0], 2)
    if "addOwner(" in event.blip.text:
      addWaveWatcher(event, wavelet, event.blip.text.split("addOwner(")[1].split(")")[0], 1)
    if "addTrusted(" in event.blip.text:
      addWaveWatcher(event, wavelet, event.blip.text.split("addTrusted(")[1].split(")")[0], 3)
    if "addRobot(" in event.blip.text:
      addWaveWatcher(event, wavelet, event.blip.text.split("addRobot(")[1].split(")")[0], 4)
    if "blacklist(" in event.blip.text:
      addBadUser(event, wavelet, event.blip.text.split("blacklist(")[1].split(")")[0], 1)
    if "greylist(" in event.blip.text:
      addBadUser(event, wavelet, event.blip.text.split("greylist(")[1].split(")")[0], 2)
  logging.info("OnBlipSubmitted Completed")
  
def OnWaveletCreated(event, wavelet):
  logging.critical("OnWaveletCreated Called") #Even after a hard-reset, I still don't get this called. Level set as CRITICAL for easy spotting.

def OnWaveletTitleChanged(event, wavelet):
  logging.critical("OnWaveletTitleChanged Called") #Even after a hard-reset, I still don't get this called. Level set as CRITICAL for easy spotting.
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

def OnWaveletParticipantsChanged(event, wavelet):
  logging.debug("OnWaveletParticipantsChanged Called")
  opQ = wavelet.get_operation_queue() #Gets operation queue for tagging the wavelet.
  unsafe = False #Creates a variable for determining if the wave is safe or not.
  results = WAVEWATCHERS_ALL
  for participant in wavelet.participants:
    if participant not in results:
        unsafe = True 
  if unsafe:
    if "not-safe" not in wavelet.tags:
        opQ.wavelet_modify_tag(wavelet.wave_id, wavelet.wavelet_id, "not-safe") #Tags the wavelet
    if "is-safe" in wavelet.tags:
        opQ.wavelet_modify_tag(wavelet.wave_id, wavelet.wavelet_id, "is-safe", modify_how = "remove") #Removes a tag.
  else:
    if "is-safe" not in wavelet.tags:
        opQ.wavelet_modify_tag(wavelet.wave_id, wavelet.wavelet_id, "is-safe")
    if "not-safe" in wavelet.tags:
        opQ.wavelet_modify_tag(wavelet.wave_id, wavelet.wavelet_id, "not-safe", modify_how = "remove")
  logging.info("OnWaveletParticipantsChanged Completed")

if __name__ == '__main__':
  myRobot = robot.Robot("WaveWatcherBot", 
  image_url='http://wave-watchers.appspot.com/Wave-Watchers.png',
  profile_url='http://groups.google.com/group/wave-watchers')
  import verify
  myRobot.register_handler(events.WaveletSelfAdded, OnWaveletSelfAdded)
  myRobot.register_handler(events.WaveletTitleChanged, OnWaveletTitleChanged)
  myRobot.register_handler(events.GadgetStateChanged, OnGadgetStateChanged)
  myRobot.register_handler(events.WaveletCreated, OnWaveletCreated)
  myRobot.register_handler(events.BlipSubmitted, OnBlipSubmitted)
  myRobot.register_handler(events.WaveletParticipantsChanged, OnWaveletParticipantsChanged)
  myRobot.setup_oauth(verify.consumerKey, verify.consumerSecret, server_rpc_base='http://gmodules.com/api/rpc')
  appengine_robot_runner.run(myRobot)

