"""
   Story functions
"""
from rooms import PropPart

# Story actions and dialogues are kept here

EVENTS = set()

CHECKPOINT = []

ACTIONS = {}

SPEECH = {}


def chapter_setup(_, n):
    module = CHAPTER_MODULES[n-1]
    ACTIONS.update(module.ChapterActions)
    SPEECH.update(module.ChapterSpeech)

def try_again(gamestate,*events_removed):
    r,g,e = CHECKPOINT
    global EVENTS
    EVENTS = e-set(events_removed)
    change_room(gamestate,r,g)

def change_room(gamestate, room, gate):
    gamestate.quit = room, gate
    global CHECKPOINT
    CHECKPOINT = [room,gate,set(EVENTS)]

def key_check(gamestate, keynames, room, gate, status, fail_text):
    if bool(set(keynames) & EVENTS) == status:
        change_room(gamestate,room,gate)
    else:
        gamestate.footer_text(fail_text)

def do_ifelse(gamestate, true_conditions, false_conditions, win_action, fail_action):
    f = false_conditions
    if true_conditions.issubset(EVENTS) and (not f.issubset(EVENTS) or not f):
        o,a = win_action
    else:
        o,a = fail_action
    action_for_object(gamestate,o,a)

def turn_actor(gamestate, name, angle, ms=1000):
    actor = gamestate[name]
    actor.turn_to_angle(angle, ms)

def move_actor(gamestate, name, pos, ms=2000):
    actor = gamestate[name]
    actor.move_to(pos, ms)

def face_player(gamestate, name, ms=500):
    actor = gamestate[name]
    actor.turn_to_face(gamestate.player, ms)

def chapter_end(gamestate, fadecolour, chapter):
    gamestate.fade_to(fadecolour, chapter, "begin")

def take_object(gamestate,item,event,text):
    o = gamestate["Room"][item]
    gamestate["Room"].remove(o)
    EVENTS.add(event)
    gamestate.footer_text(text)

def foot_text(gamestate,text):
    gamestate.footer_text(text)

def begin_speech(gamestate,conversation):
    t,o = SPEECH[conversation]
    gamestate.open_speech(conversation,t,o)

def show_image(gamestate, conversation, size=(400,400)):
    t, o = SPEECH[conversation]
    gamestate.show_picture(conversation,t,o,size=size)

def add_prop(gamestate,p,onceonly):
    """ parameters: a tuple of (name,model,pos,angle,text,material) """
    s = p[0]+" spawned"
    if not onceonly or s not in EVENTS:
        if p[5]:
            m = p[5]+".mtl"
        else:
            m = p[5]
        prop = PropPart(p[0],_obj_filename=p[1]+".obj",_pos=p[2],_angle=p[3],_mat_filename=m)
        prop.text = p[4]
        prop.prepare()
        gamestate["Room"].append(prop)
        EVENTS.add(s)

def cause_event(gamestate,event):
    EVENTS.add(event)

def move_2ab(gamestate,room,gate):
    c = "room2 first"
    if c not in EVENTS:
        EVENTS.add(("room2 first",))
    change_room(gamestate,room,gate)

import story_ch1, story_ch2, story_ch3, story_ch4, story_ch5
import story_ch6, story_ch7, story_ch8, story_ch9

CHAPTER_MODULES = [
    story_ch1, story_ch2, story_ch3, 
    story_ch4, story_ch5, story_ch6, 
    story_ch7, story_ch8, story_ch9 ]

def action_for_object(gamestate, objectID, action):
    """ Perform an action on an object, which may cause effects in
    a specified GameState

    These effects may include:
    change room  (sets gamestate.quit)
    get item (adds an item to the item bar)
    drop item (removes an item from the item bar)
    clear items (drops everything from the item bar)
    
    """
    actions = ACTIONS.get((objectID, action))
    if actions:
        if type(actions) is tuple:
            actions = [actions]
        for actiontuple in actions:
            fn = actiontuple[0]
            args = actiontuple[1:]
            fn(gamestate, *args)
    return bool(actions)

