"""
Story controller

Full of spoilers!


Determines the possible actions on each unique named object in terms
of story transitions, inventory etc.

"""
from rooms import PropPart

# Action functions

def change_room(gamestate, room, gate):
    gamestate.quit = room, gate

def key_check(gamestate, keyname, room, gate, status, fail_text):
    if (keyname in EVENTS) == status:
        change_room(gamestate,room,gate)
    else:
        tpan = gamestate["text"]
        tpan.text = fail_text
        tpan.prepare()

def do_ifelse(gamestate, true_conditions, false_conditions, win_action, fail_action):
    f = false_conditions
    if true_conditions.issubset(EVENTS) and (not f.issubset(EVENTS) or not f):
        o,a = win_action
    else:
        o,a = fail_action
    action_for_object(gamestate,o,a)
        

def take_artefact(gamestate):
    """ Adds item to inventory and spawns a cultist behind you.
    Removes ability to walk."""
    gp = gamestate.player
    gp.angle = gp.langle = -90
    gp.move_cam(gamestate.camera)
    take_object(gamestate,"Artefact","caught stealing","You take the artefact only to hear a slam and a click behind you.")
    add_prop(gamestate,("CultistA","cultist-threaten",(4,6,0),-90,"Cultist","cultist-1900"),True)
    gamestate["Room"].walktiles.remove((4,6))

def martin_scare(gamestate):
    gp = gamestate.player
    gp.angle -= 180
    gp.move_cam(gamestate.camera)
    tpan = gamestate["text"]
    tpan.text = "Nothing. You are disappointed. Relieved, but disappointed."
    tpan.prepare()

def take_object(gamestate,item,event,text):
    o = gamestate["Room"][item]
    gamestate["Room"].remove(o)
    EVENTS.add(event)
    tpan = gamestate["text"]
    tpan.text = text
    tpan.prepare()

def begin_speech(gamestate,conversation):
    t,o = SPEECH[conversation]
    gamestate.open_speech(conversation,t,o)

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

# All story actions in the whole game

EVENTS = set()

ACTIONS = {
# ---> Doors
    ("SPRoomDoor", "click"):(change_room, "hotelhall", "yourroom"),
    ("SPCultDoor", "click"):(key_check, "caught stealing",
                             "hotelhall", "cultroom", False,"You can't leave. The cultist is blocking the door."),
    ("SPHRoomDoor", "click"):(change_room, "hotelroom1", "door"),
    ("SPHCultDoor", "click"):(key_check, "cult key", "hotelroom2", "door",True,"The door is locked. You'll need the key."),
    ("SPHLobbyDoor", "click"):(change_room, "hotellobby", "hallway"),
    ("SPHallDoor", "click"):(change_room, "hotelhall", "lobby"),
    ("SPHRightDoor", "click"):(change_room, "street", "hotel"),
    ("SPHLeftDoor", "click"):(change_room, "street", "hotel"),

    ("HotelDoors", "click"):(change_room, "hotellobby", "street"),
    ("AHDoors", "click"):(change_room, "auctionhouse", "door"),
    ("MartDoor", "click"):(change_room, "marthouse", "door"),

    ("Boat", "click"):(change_room, "titandeck", "door"),
    ("House", "click"):(change_room, "arkham", "begin"),
    ("ToyBarrel", "click"):(change_room, "warehousehall", "door"),

    ("AHLeftDoor", "click"):(change_room, "street", "ah"),
    ("AHRightDoor", "click"):(change_room, "street", "ah"),
    ("InMartDoor", "click"):(change_room, "street", "marthouse"),

    ("CabinDoor", "click"):(change_room, "titanbar", "deck"),
    ("DeckDoor", "click"):(change_room, "titandeck", "door"),
    ("HallDoor", "click"):(change_room, "titanhall", "bar"),
    ("BarDoor", "click"):(change_room, "titanbar", "hall"),

    ("TTEnterR1", "click"):(change_room, "titanroom1", "door"),
    ("TTEnterR2", "click"):(change_room, "titanroom2", "door"),
    ("TTLeaveR1", "click"):(change_room, "titanhall", "yourroom"),
    ("TTLeaveR2", "click"):(change_room, "titanhall", "cultroom"),

    ("ArkHDoor", "click"):(change_room, "arkroom1", "street"),
    ("ArkR1to2", "click"):(change_room, "arkroom2", "room1"),
    ("ArkR1to3", "click"):(change_room, "arkroom3", "room1"),
    ("ArkHtoStreet", "click"):(change_room, "arkham", "door"),
    ("ArkR2to1", "click"):(change_room, "arkroom1", "room2"),
    ("ArkR2to3", "click"):(change_room, "arkroom3", "room2"),
    ("ArkR3to1", "click"):(change_room, "arkroom1", "room3"),
    ("ArkR3to2", "click"):(change_room, "arkroom2", "room3"),

#---> Intro
    ("Chapter1", "begin"):(begin_speech,"BeginChapter1"),
    ("BeginChapter1",1):(change_room, "hotelroom1", "begin"),

#---> Saint-Pierre events
    ("HotelDeskLady", "click"):(do_ifelse,set(("cultist IDed",)),set(("cult key",)),
                                ("HotelDeskLady","askcult"),("HotelDeskLady","askmart")),
    ("HotelDeskLady", "askmart"):(begin_speech,"DLady1"),
    ("HotelDeskLady", "askcult"):(begin_speech,"DLady4"),
    ("DLady1",1):(begin_speech,"DLady3"),
    ("DLady1",2):(begin_speech,"DLady2"),
    ("DLady4",1):(begin_speech,"DLady5"),
    ("DLady4",2):(begin_speech,"DLady6"),
    ("DLady4",3):(begin_speech,"DLady7"),
    ("DLady7",1):(add_prop,("CultKey","key",(8,9.5,0.7),90,"A key.",None),False),
    ("CultKey","click"):(take_object,"CultKey","cult key","You subtly pocket the key to the cultists room."),

    ("CultBedside", "click"):(begin_speech,"BedsideOpt"),
    ("BedsideOpt",1):(add_prop, ("Artefact","artefact",(6.7,3,0.55),90,"This is the artefact.",None),True),
    ("Artefact", "click"):(take_artefact,),
    ("CultistA", "click"):(begin_speech,"CultA1"),

    ("Martin","click"):(begin_speech,"MartinOpt"),
    ("MartinOpt",1):(begin_speech,"MartinOpt1"),
    ("MartinOpt",2):(begin_speech,"MartinOpt2"),
    ("MartinOpt",3):(begin_speech,"MartinOpt3"),
    ("MartinOpt1",1):(begin_speech,"MartinOpt"),
    ("MartinOpt3",1):(begin_speech,"MartinOpt"),
    ("MartinOpt",4):(martin_scare,),

    ("MartinOpt2",1):(begin_speech,"MartinExamine"),
    ("MartinExamine",1):(begin_speech,"MartinExamine2"),
    ("MartinExamine2",1):(cause_event,"artefact known"),

    ("Auctioneer","click"):(do_ifelse,set(("artefact known",)),set(),("Auctioneer","artefact"),("Auctioneer","smalltalk")),
    ("Auctioneer","smalltalk"):(begin_speech,"AHsmalltalk"),
    ("Auctioneer","artefact"):(begin_speech,"AHartefact"),

    ("AHsmalltalk",1):(begin_speech,"AHmartin"),
    ("AHmartin",2):(begin_speech,"AHoften"),

    ("AHartefact",1):(begin_speech,"AHartefact2"),
    ("AHartefact2",1):(begin_speech,"AHartefact3"),
    ("AHartefact3",1):(cause_event,"cultist IDed"),

    ("CultA1",1):(begin_speech,"CultA4"),
    ("CultA1",2):(begin_speech,"CultA2"),
    ("CultA1",3):(begin_speech,"CultA3"),
    ("CultA4",1):(begin_speech,"CultA3"),
    ("CultA4",2):(begin_speech,"CultA2"),
    ("CultA3",1):(begin_speech,"CultA5"),
    ("CultA3",2):(begin_speech,"CultA2"),

#---> Titanic events
    
}

SPEECH = {
#---> Saint-Pierre
    "CultA1":('"What are you doing? Give me that!"',["Did you kill Martin?","OK","No"]),
    "CultA2":('"Hah! Fool. You should have stayed away. [Shot dead]"',[]),
    "CultA3":('"No? Are you mad? Give me it or I will shoot you!" [What will you do? He seems to be very nervous. The artefact must be precious to him.]',["Destroy the artefact","Get shot"]),
    "CultA4":('"Martin? What does it matter when- No! You don\'t ask me questions! Give me the artefact!"',["No","OK"]),
    "CultA5":('"What have you done!? Oh Gods! [He panicks. You have no clue. Mount Pelee erupts. You get a TKO by volcano but still die. On to the Titanic]"',[]),

    "DLady1":('"Hello, how may I help you?"',["Do you know where M. Martin DuPont lives?","Nothing, thank you."]),
    "DLady2":('"Alright, good day sir."',[]),
    "DLady3":('"Oh yes, M. DuPont. He lives in the white house on the other side of the road."',["Thank you."]),
    "DLady4":('"Hello, how may I help you?"',
              ["A man with a brown shirt and a large moustache stays here. Can you tell me his room number?",
               "I need to see the man with the large moustache; is he in his room?",
               "I have a message for the man in the brown shirt; can you deliver it for me?"]),
    "DLady5":('"I\'m sorry sir, I\'m afraid I cannot give out room numbers."',["I see ..."]),
    "DLady6":('"I\'m afraid not sir. You could try him again later."',["I see ..."]),
    "DLady7":('"Certainly sir! Now let\'s see, which was his room?" [She examines the number on a key] "Ah yes. Your message will be delivered sir.',["Thank you very much madam."]),

    "BedsideOpt":("This is the cultists bedside table. You highly doubt anything is inside but maybe it\'s worth checking.",["Open it.","Attempt and succeed to fail to open it."]),
    "MartinOpt":("Oh God ... Martin... What will you do?",["Check for a pulse","Check wounds","Remove the head in case of zombie plague","Look ... behind ... you"]),
    "MartinOpt1":("You do so but there's almost no point. He's most definately dead.",["Well then..."]),
    "MartinOpt2":("The wounds were caused by a knife. Stabbed in the gut. He's holding something here...",["Examine it"]),
    "MartinExamine":("Two documents are here. The first is something about a dark artefact. It describes a ritual it seems, though you can't read the language. There is also an image of nine pillars, each more crumbling and ruined than the last. The artefact is mounted atop the first.",["And the other document..."]),
    "MartinExamine2":("...is a brochure for an auction at the auction house next door. One of the items appears to be the artefact in the occult text. Unfortunately the auction was yesterday. Someone has this in their possession and you need to find them before they leave Saint-Pierre.",["Go and investigate"]),
    "MartinOpt3":("Certainly not! You couldn't bear to. Besides, the cliche doesn't exist yet, it's 1902.",["Well then..."]),

    "AHsmalltalk":('"Oh hello... Umm, you\'re a little early for the auction..."',["Sorry. I just wanted to ask if you know a Martin DuPont?","Oh sorry... Umm, I'd best be off. "]),
    "AHmartin":('"Martin? Umm, yes I think he lives next door in the uh, white house."',["Thank you. Goodbye.","Does he often come here?"]),
    "AHoften":('"Often? Er, no not really. He was in here umm, yesterday though. He only bid on one item and umm, he was outbid by quite a large umm, summ."',["I see. Well thank you. Goodbye."]),
    "AHartefact":('"Oh hello. Umm, you\'re a little early for the auction..."',["Yes I know. Can you tell what this item is?"]),
    "AHartefact2":('"Umm, that\'s umm... well no I\'m not sure. You could try, er, asking the gentleman who purchased it yesterday. He umm, seemed quite determined to get his hands on it."',["And what gentleman was this?"]),
    "AHartefact3":('"Oo, um, let me, er, see I... I never caught his name. All I remember is that he wore a brown shirt and had a rather large moustache. I think he stays at the umm, Santa Maria hotel."',["Thank you, you've been most UMM-helpful..."]),
 
    "BeginChapter1":(
        "You have spent many years investigating supernatural phenomena (without success). But you keep finding"
        " references to one particular ancient cult with disturbing beliefs.\n"
        "Recently you received a letter from an old friend Martin DuPont, which leads you to believe the cult"
        " are active on the caribbean island of Martinique, so you go to see what they are up to.",
        ["Begin"]),
    }
def save_story(filename=".9nm"):
    """ save story state in a file """
    pass

def load_story(filename=".9nm"):
    """ load story state and return tuple of room,spawnpoint for where
    the player is standing """
    return "hotelroom1","begin"

def menu_for_object(objectID):
    """ Returns a list of strings giving the menu choices
    for interactive objects.
    An empty list means the object has no useful actions """
    return []

def action_for_object(gamestate, objectID, action):
    """ Perform an action on an object, which may cause effects in
    a specified GameState

    These effects may include:
    change room  (sets gamestate.quit)
    get item (adds an item to the item bar)
    drop item (removes an item from the item bar)
    clear items (drops everything from the item bar)
    
    """
    actiontuple = ACTIONS.get((objectID, action))
    if actiontuple:
        fn = actiontuple[0]
        args = actiontuple[1:]
        fn(gamestate, *args)
        return True
    else:
        return False

