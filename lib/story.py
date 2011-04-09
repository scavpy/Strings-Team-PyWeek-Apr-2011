"""
Story controller

Full of spoilers!


Determines the possible actions on each unique named object in terms
of story transitions, inventory etc.

"""
from rooms import PropPart


# Action functions

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

def take_artefact(gamestate):
    """ Adds item to inventory and spawns a cultist behind you.
    Removes ability to walk."""
    gp = gamestate.player
    take_object(gamestate,"Artefact","caught stealing","You take the artefact only to hear a slam and a click behind you.")
    add_prop(gamestate,("CultistA","cultist-threaten",(4,6,0),-90,"Cultist","cultist-1900"),True)
    gamestate["Room"].walktiles.remove((4,6))
    gp.watching_me = gamestate["CultistA"]
    gp.turn_to_face(gamestate["CultistA"],250)

def martin_scare(gamestate):
    gp = gamestate.player
    gp.turn(-180)
    gamestate.footer_text("Nothing. You are disappointed. Relieved, but disappointed.")

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

# All story actions in the whole game

EVENTS = set()

CHECKPOINT = []

ACTIONS = {
# ---> Doors
    ("SPRoomDoor", "click"):(change_room, "hotelhall", "yourroom"),
    ("SPCultDoor", "click"):(key_check, ["caught stealing"],
                             "hotelhall", "cultroom", False,
                             "You can't leave. The cultist is blocking the door."),
    ("SPHRoomDoor", "click"):(change_room, "hotelroom1", "door"),
    ("SPHCultDoor", "click"):(key_check, ["cult key"], "hotelroom2", "door",True,
                              "The door is locked. You'll need the key."),
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

    ("CabinDoor", "click"):(key_check,["cultists onboard"], "titanbar", "deck",True,
                            "You see no reason to head inside yet. You decide to stay and chat."),
    ("DeckDoor", "click"):(do_ifelse, set(["go time"]), set(), ("DeckDoor", "late"), ("DeckDoor", "early")),
    ("DeckDoor", "early"):(change_room, "titandeck", "door"),
    ("DeckDoor", "late"):(change_room, "titandecklater", "door"),
    ("HallDoor", "click"):(change_room, "titanhall", "bar"),
    ("BarDoor", "click"):(change_room, "titanbar", "hall"),

    ("TTEnterR1", "click"):(change_room, "titanroom1", "door"),
    ("TTEnterR2", "click"):(key_check,["drunk lifted"], "titanroom2", "door",True,
                            "You don't know who\'s room this is but you don\'t have the key."),
    ("TTLeaveR1", "click"):(change_room, "titanhall", "yourroom"),
    ("TTLeaveR2", "click"):(key_check,["drunk bedded","go time"], "titanhall", "cultroom",True,
                            "You are not going to carry him around the whole ship. Just put him on the bed and rummage through his stuff."),
    ("ArkHDoor", "click"):(key_check,["lawyer in"], "arkroom1", "street",True,
                           "You should speak to Reginald, your lawyer, first."),
    ("ArkR1to2", "click"):[(change_room, "arkroom2", "room1"),(cause_event,"door lock")],
    ("ArkR1to3", "click"):(key_check, ["door lock"], "arkroom3", "room1",True,
                           "Reg is in the way. You should check out the other room."),
    ("ArkHtoStreet", "click"):(key_check, ["door lock"], "arkham", "door",False,
                               "It's locked. Strange... You certainly didn't lock it."),
    ("ArkR2to1", "click"):(change_room, "arkroom1", "room2"),
    ("ArkR2to3", "click"):(change_room, "arkroom3", "room2"),
    ("ArkR3to1", "click"):(change_room, "arkroom1", "room3"),
    ("ArkR3to2", "click"):(change_room, "arkroom2", "room3"),

    ("ArkR1ato2a", "click"):(move_2ab, "arkroom2a", "room1"),
    ("ArkR1ato3a", "click"):(change_room, "arkroom3a", "room1"),
    ("ArkR2ato1a", "click"):(change_room, "arkroom1a", "room2"),
    ("ArkR2ato3a", "click"):(change_room, "arkroom3a", "room2"),
    ("ArkR3ato1a", "click"):(change_room, "arkroom1a", "room3"),
    ("ArkR3ato2a", "click"):(move_2ab, "arkroom2a", "room3"),

    ("ArkR1bto2b", "click"):(move_2ab, "arkroom2b", "room1"),
    ("ArkR1bto3b", "click"):(change_room, "arkroom3b", "room1"),
    ("ArkR2bto1b", "click"):(change_room, "arkroom1b", "room2"),
    ("ArkR2bto3b", "click"):(change_room, "arkroom3b", "room2"),
    ("ArkR3bto1b", "click"):(change_room, "arkroom1b", "room3"),
    ("ArkR3bto2b", "click"):(move_2ab, "arkroom2b", "room3"),

#---> Chapter intros
    ("Chapter1", "begin"):(begin_speech,"BeginChapter1"),
    ("BeginChapter1",1):(change_room, "hotelroom1", "begin"),
    ("BeginChapter1",2):(change_room, "Chapter2", "begin"),
    ("Chapter2", "begin"):(begin_speech,"BeginChapter2"),
    ("BeginChapter2",1):(change_room, "titandeck", "begin"),
    ("BeginChapter2",2):(begin_speech,"Tough"),
    ("BeginChapter2",3):(change_room,"Chapter3","begin"),
    ("Chapter3", "begin"):(begin_speech,"BeginChapter3"),
    ("BeginChapter3",1):(change_room,"arkham","begin"),
    ("Tough",1):(change_room, "titandeck", "door"),

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
    ("DLady7",1):[
        (add_prop,("CultKey","key",(8.2,9.7,0.7),90,"A key.",None),False),
        (turn_actor, "HotelDeskLady", 90)],
    ("CultKey","click"):(take_object,"CultKey","cult key",
                         "You casually pocket the key to the cultists room."),

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

    ("Auctioneer","click"):(do_ifelse,set(("artefact known",)),set(),
                            ("Auctioneer","artefact"),("Auctioneer","smalltalk")),
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
    ("CultA2",1):(try_again,"caught stealing","Artefact spawned"),
    ("CultA2",2):(chapter_end, (0.5,0,0,1), "GameOver"),
    ("CultA4",1):(begin_speech,"CultA3"),
    ("CultA4",2):(begin_speech,"CultA2"),
    ("CultA3",1):(begin_speech,"CultA5"),
    ("CultA3",2):(begin_speech,"CultA2"),
    ("CultA5",1):(begin_speech,"EndChapter1"),
    ("EndChapter1",1):(chapter_end, (0.5,0,0,1), "Chapter2"),

#---> Titanic events
    ("Sailor1","click"):[(face_player, "Sailor1"), (do_ifelse,set(("go time",)),set(),("Sailor","tellon"),("Sailor","talk1"))],
    ("Sailor2","click"):[(face_player, "Sailor2"), (do_ifelse,set(("go time",)),set(),("Sailor","tellon"),("Sailor","talk2"))],
    ("Sailor","talk1"):(begin_speech,"S1"),
    ("Sailor","talk2"):(begin_speech,"S2"),
    ("Sailor","tellon"):(begin_speech,"STell"),
    ("STell",1):(begin_speech,"SLose"),
    ("STell",2):(begin_speech,"SWin"),
    ("SWin",1):(begin_speech,"EndChapter2"),
    ("EndChapter2",1):(chapter_end, (0.5,0,0,1), "Chapter3"),
    ("Man","click"):[(face_player, "Man"), (begin_speech,"Man")],
    ("Lady","click"):[(face_player, "Lady"), (begin_speech,"Lady")],
    ("SuspiciousMan","click"):(begin_speech,"CultB1"),
    ("CultB1",1):[(turn_actor,"SuspiciousMan",-45),(begin_speech,"CultB2")],
    ("CultB2",1):(begin_speech,"CultB3"),
    ("CultB3",1):(cause_event,"cultists onboard"),
    ("NoteBook","click"):(show_image,"CultNote"),
    ("CultNote",1):(begin_speech,"CultNote2"),
    ("CultNote2",1):(cause_event,"cult discovered"),
    ("titanbar","begin"):(do_ifelse, set(), set(["drunk lifted"]), ("titanbar","add drunk"), ("DO","NOTHING")),
    ("titanbar","add drunk"):(add_prop,("Drunk","drunk-sit",(4,9.6,0),90,"Drunk man",None), False),
    ("Drunk","click"):(do_ifelse,set(("cult discovered",)),set(),("Drunk","cult"),("Drunk","smalltalk")),
    ("Drunk","cult"):(begin_speech,"Drunk1"),
    ("Drunk","smalltalk"):(begin_speech,"Drunktalk"),
    ("Drunktalk",1):(begin_speech,"Drunkwhat"),
    ("Drunk1",1):(begin_speech,"Drunk2"),
    ("Drunk2",1):(begin_speech,"Drunk3"),
    ("Drunk3",1):(begin_speech,"Drunk4"),
    ("Drunk4",1):(begin_speech,"Drunk5"),
    ("Drunk5",1):(take_object,"Drunk","drunk lifted","You help the cultist up and prepare to sneak into and investigate his room. A sense of deja vu overcomes you for a moment."),

    ("DrunkBed","click"):[(add_prop,("DrunkC","drunk-lie",(1,0.4,0),0,"Drunk Cultist",None),True),
                          (cause_event,"drunk bedded")],
    ("Suitcase1","click"):(begin_speech,"CaseOpt"),
    ("CaseOpt",1):[(take_object,"Suitcase1","privacy invaded",
                               "You proficiently invade his privacy and the contents of his suitcase are revealed"),
                   (add_prop,("Suitcase2","suitcase-open",(6.4,2,0.73),0,"Open suitcase",None),True)],
    ("Suitcase2","click"):(begin_speech,"CaseOpt2"),
    ("CaseOpt2",1):[(begin_speech,"CaseOptParch"),(cause_event,"go time")],
    ("CaseOpt2",2):[(begin_speech,"CaseOptGun"),(cause_event,"gun get")],
    ("CaseOptParch",1):[(begin_speech,"CaseOptParch2"),(cause_event,"gun get")],
    ("CaseOptGun",1):[(begin_speech,"CaseOptGun2"),(cause_event,"go time")],

    ("SuspiciousMan2","click"):(begin_speech,"SM2confront"),
    ("SM2confront",1):(do_ifelse,set(("gun get",)),set(),("SM2","gun"),("SM2","nogun")),
    ("SM2","gun"):(begin_speech,"SM2withgun"),
    ("SM2","nogun"):(begin_speech,"SM2nogun"),

    ("SM2withgun",1):(begin_speech,"SM2tellon"),
    ("SM2nogun",1):(begin_speech,"SM2tellon"),
    ("SM2withgun",2):(begin_speech,"SM2threaten"),
    ("SM2nogun",2):(begin_speech,"SM2press"),
    ("SM2withgun",3):(begin_speech,"SM2press"),
    ("SM2threaten",1):(begin_speech,"FailChapter2"),
    ("FailChapter2",1):(try_again,),
    ("FailChapter2",2):(chapter_end, (0,0,0,0), "GameOver"),
    ("EndChapter2",1):(chapter_end, (0,0.2,0.1,1), "Chapter3"),

#---> Arkham
    ("arkham","begin"):(do_ifelse,set(),set(("lawyer in",)),("arkham","AddLawyer"),("DO","NOTHING")),
    ("arkham","AddLawyer"):(add_prop,("Lawyer","man",(10,20,0),-90,"Reg.D, lawyer","lawyer"),False),
    ("Lawyer","click"):(do_ifelse,set(("lawyer talked",)),set(),("Lawyer","vanish"),("Lawyer","talk")),
    ("Lawyer","talk"):(begin_speech,"Lawyer1"),
    ("Lawyer1",1):[(cause_event,"lawyer talked"),
                   (turn_actor,"Lawyer",0),],
    ("Lawyer","vanish"):[(cause_event, "lawyer in"),
                         (move_actor, "Lawyer", (14,20,0)),
                         (foot_text,"Reg heads inside the house."),],
    ("arkroom1","begin"):(do_ifelse,set(),set(("door lock",)),("arkroom1","AddLawyer"),("DO","NOTHING")),
    ("arkroom1","AddLawyer"):(add_prop,("Lawyer2","man",(0,6,0),0,"Reg.D, lawyer","lawyer"),False),
    ("Lawyer2","click"):(begin_speech,"Lawyer2"),
    ("arkroom2","begin"):(do_ifelse,set(("wind placed",)),set(("wind stolen",)),("arkroom2","AddWind"),("DO","NOTHING")),
    ("arkroom2","AddWind"):(add_prop,("WindSumm2","painting",(-0.98,0,-0.4),90,
                                      "'The Summoning of Wind'. You\'re glad it\'s here to complete the set.",
                                      "windsummon"),False),
    ("BloodSumm","click"):(do_ifelse,set(("wind taken",)),set(("wind placed",)),("BloodSumm","put"),("BloodSumm","text")),
    ("BloodSumm","put"):(begin_speech,"WindPlace"),
    ("BloodSumm","text"):(begin_speech,"WindWhere"),
    ("WindPlace",1):[(begin_speech,"WindNice"),(cause_event,"wind placed"),(add_prop,("WindSumm2","painting",
                                                                                      (-0.98,0,-0.4),90,
                                      "'The Summoning of Wind'. You\'re glad it\'s here to complete the set.",
                                      "windsummon"),False)],
    ("WindNice",1):(begin_speech,"WindCrash"),
    ("WindCrash",1):[(take_object,"ArkR2to3","dswitch","Something's wrong..."),
                     (take_object,"ArkR2to1","dswitch","Something's wrong..."),
                     (add_prop,("ArkR2to1a","door",(10,6,0),180,"Door",None),False),
                     (add_prop,("ArkR2to3b","door",(2,8,0),-90,"Door",None),False),
                     ],
    ("ArkR2to1a","click"):(change_room,"arkroom1a","room2"),
    ("ArkR2to3b","click"):(change_room,"arkroom3b","room2"),
    ("arkroom3","begin"):(do_ifelse,set(),set(("lawyer call",)),("arkroom3","AddLawyer"),("DO","NOTHING")),
    ("arkroom3","AddLawyer"):(add_prop,("Lawyer3","man",(0,4,0),180,"Reg.D, lawyer","lawyer"),False),
    ("Lawyer3","click"):[(face_player,"Lawyer3"),(begin_speech,"Lawyer3")],
    ("Lawyer3",1):(begin_speech,"Lawyer4"),
    ("Lawyer4",1):(take_object,"Lawyer3","lawyer call","He seems in a hurry to use the phone. What was he looking at?"),
    ("WindSumm1","click"):(begin_speech,"WindOpt"),
    ("WindOpt",1):(begin_speech,"WindEx"),
    ("WindOpt",2):(begin_speech,"WindTk"),
    ("WindEx",1):(begin_speech,"WindTk"),
    ("WindTk",1):(take_object,"WindSumm1","wind taken",
                  "You lift the frame from the wall in order to move it into the other room."),

    ("arkroom2a","begin"):(do_ifelse,set(),set(("room2 first",)),("2a","first"),("DO","NOTHING")),
    ("2a","first"):(foot_text,"Whoever or whatever is in here seems to have gone upstairs. And they've taken the Summoning of Wind with them. The door is locked, you are not getting out of here alive. The least you can do is stop any future Summonings from happening."),
                   
}

SPEECH = {
#---> Saint-Pierre
    "CultA1":('"What are you doing? Give me that!"',["Did you kill Martin?","OK","No"]),
    "CultA2":('"Hah! Fool. You should have stayed away. [He shoots you.]"',["Try again", "Game Over"]),
    "CultA3":('"No? Are you mad? Give me it or I will shoot you!" [What will you do? He seems to be very nervous. The artefact must be precious to him.]',["Destroy the artefact","Get shot"]),
    "CultA4":('"Martin? What does it matter when- No! You don\'t ask me questions! Give me the artefact!"',["No","OK"]),
    "CultA5":('"What have you done!? Oh Gods!\n[He panics. There is a rumbling outside.]"',["What's that noise?"]),

    "DLady1":('"Hello, how may I help you?"',
              ["Do you know where M. Martin DuPont lives?","Nothing, thank you."]),
    "DLady2":('"Alright, good day sir."',[]),
    "DLady3":('"Oh yes, M. DuPont. He lives in the white house on the other side of the road."',
              ["Thank you."]),
    "DLady4":('"Hello, how may I help you?"',
              ["A man with a brown shirt and a large moustache stays here. Can you tell me his room number?",
               "I need to see the man with the large moustache; is he in his room?",
               "I have a message for the man in the brown shirt; can you deliver it for me?"]),
    "DLady5":('"I\'m sorry sir, I\'m afraid I cannot give out room numbers."',["I see ..."]),
    "DLady6":('"I\'m afraid not sir. You could try him again later."',["I see ..."]),
    "DLady7":('"Certainly sir! Now let\'s see, which was his room?" [She examines the number on a key] "Ah yes. Your message will be delivered sir.',
              ["Thank you very much madam."]),

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
        ["Begin","Ch2"]),
    "EndChapter1":(
        "A huge cloud of glowing smoke rushes down from Mont Pelee, burning and sweeping aside everything in its path.\n"
        "Before you die, you have time to wonder what the cultists would have been able to do with the artefact"
        " if you hadn't stopped them..."
        "Your mother and son are left alone in Arkham.", ["End of Chapter 1"]),

    "BeginChapter2":(
        "After your father died in Martinique, your mother moved back from America to Glasgow. She lived well and"
        " died peacefully leaving you a large inheritance.\n"
        "You decide to visit your old house in Arkham and find out more about your father's life. Your wife remains"
        " at home, being unable to travel in her delicate condition.\n"
        "Taking your father's old notes and diaries to read on the long sea voyage,"
        " you book passage on the maiden voyage of the world's greatest ship:\nThe Titanic", 
        ["Begin", "No wait, I can see this isn't going to go well...","Ch. 3"]),
    "Tough":("Tough.\nGet on with it, you've got a world to save.", ["Fine."]),
    "FailChapter2":(
        "You are immediately arrested and thrown in the brig until arrival at New York.\n"
        "As the ship docks, an unnatural tide rises and engulfs the city.  There are... things in the water.\n"
        "Tens of thousands die, and reports come in from other cities that the same terrible"
        " events are repeating across the whole world.\n"
        "You realise as unholy tentacles reach into your prison cell, you have failed.",
        ["Try Again","Game Over"]),
    "EndChapter2":(
        "The 'anarchists' are arrested and thrown in the brig. Late at night you hear drunken chanting"
        " from the next cabin, then a horrible scream.\n"
        "The water beside the ship churns and begins to freeze. Something vast moves beneath the ship and tears it open.\n"
        "Although you make it onto a lifeboat, what you see that night breaks you. You are cared for in a mental"
        " hospital for the remainder of your life.",
        ["End of Chapter 2"]),
    "BeginChapter3":(
        "Your father set out on the Titanic when you were only little yet never returned. Unable to articulate who he"
        " was, he has remained in a Massachusets mental hospital ever since.\n"
        "When you finally discover his whereabouts, you take the long trip to visit him. Upon arrival, he speaks"
        " gibberish about some fantasy cult responsible for the sinking of the Titanic. Unable to believe him"
        " or persuade the doctors to release him, you decide you can at least finish what he started and visit"
        " the old Arkham house.\n"
        "You decide to engage a lawyer and claim ownership of the ancient building.", ["Begin"]),

#---> Titanic
    "S1":('"The weather looks fine. It should be a smooth journey."',[]),
    "S2":('"There\'s a bar through that door over there. Feel free to head inside and get a drink."',[]),
    "Man":('"Did you know that they say that even God couldn\'t sink this ship? I certainly feel safe."',[]),
    "Lady":('"I can\'t wait to meet my fiance in New York. We\'re getting married there."',[]),
    "CultB1":('"Oh don\'t bother me."',["I\'m Sorry"]),
    "CultB2":('"I\'m not in the mood for chat."',["[Where have I seen that tattoo before ...]"]),
    "CultB3":('You remember seeing the tattoo before in your father\'s notes which you have left in your cabin.',["Go and investigate"]),
    "Drunktalk":('"I\'ll show them... I\'ll show them all..."',["Show them what?"]),
    "Drunkwhat":('"Show them... ... what?"',["Never mind. Enjoy your drink(s)."]),
    "Drunk1":('"I\'ll show them... I\'ll... My glass is empty..."',["Then I\'ll buy you a drink. If you\'ll tell me about your tattoo."]),
    "Drunk2":('"Oh no I can\'t tell you about that. The others told me to keep quiet ... always pushing me around ... telling me what to do."',["Terrible. Have another drink. Who are the other?"]),
    "Drunk3":('"Haha! Wouldn\'t you like to know...(hic)...know. No. They\'d be angry if I spoiled our plans to you."',
              ["Of course. They\'d be furious. Another drink? What plans are these?"]),
    "Drunk4":('"We\'re going to make something. We\'re going to make it in New York. If we can make it there, we can make it anywhere"',["I see. Well good evening sir."]),
    "Drunk5":('"No wait. Please. I can\'t stand up. Would you help me to my room? It\'s the third on the left."',["Certainly sir. I\'ll just take your key to get in."]),

    "CultNote":("tattoo.png",["The tattoo..."]),
    "CultNote2":("You remember now. This drawing was sent to you by your father before he died. It was a symbol painted in blood above the body of a man named Martin. So the men on board are likely to be members of the same cult your father was investigating. You need to find out what they\'re up to before they do something dreadful.",["Go and investigate"]),

    "CaseOpt":("This is the cultists case. It may contain vital clues.",["Open it","Unsuccessfully fail to respect his privacy."]),
    "CaseOpt2":("There are a few banal items in here but a few that pique your interest. Namely an ancient looking scroll of parchment, and a gun.",["Look at the parchment","Take the gun"]),
    "CaseOptParch":("It\'s a scroll written in an ancient language you can\'t comprehend. It depicts a tentacled horror. Even this crude drawing makes you uneasy. You need to stop whatever they\'re up to. This drunk is obviously not a threat, but his probable superior up on the deck definately seems to be. It\'s time you confronted him.",["Take the gun","Get moving"]),
    "CaseOptGun":("Oh you\'re taking the gun.",["View parchment"]),
    "CaseOptParch2":("Oh you\'re taking the gun.",["Get moving"]),
    "CaseOptGun2":("It\'s a scroll written in an ancient language you can\'t comprehend. It depicts a tentacled horror. Even this crude drawing makes you uneasy. You need to stop whatever they\'re up to. This drunk is obviously not a threat, but his probable superior up on the deck definately seems to be. It\'s time you confronted him.",["Get moving"]),

    "SM2confront":('"I\'ve warned you. I don\'t care for chat."',["I know what you\'re doing here."]),
    "SM2withgun":('"Heh heh. I don\'t know what you\'re talking about.',
                  ["I\'ll tell the captain about your cult.",
                   "I\'ve got a gun and I\'ll use it to stop you if I have to.",
                   "I know about the ritual."]),
    "SM2nogun":('"Heh heh. I don\'t know what you\'re talking about.',
                ["I\'ll tell the captain about your cult.",
                 "I know about the ritual."]),
    "SM2tellon":('"What will you tell him? You will sound like a mad-man."',["I\'ll stop you whatever it takes."]),
    "SM2threaten":('"You\'re going to shoot me? You can\'t shoot us all and there are more of us in New York."',
                   ["[Shoot him]","Damn. He\'s right..."]),
    "SM2press":('"You know nothing. Earth, Water, Wind and Flame. Blood, Poison, Monstrosity and Plague. And then the final summoning. There is nothing you can do."',["[He looks insane. What will you do?]"]),

    "STell":('"Evening sir. Problems?"',["Yes. That man over there is a member of a evil cult.",
                                         "Yes. That man over there is a member of a group of anarchists."]),
    "SLose":('"Of course sir. I think you may have had a little too much to drink."',[]),
    "SWin":('"Are you sure? Hmm, his tattoo is suspicious. I will alert the Captain and we\'ll search the ship."',
            ["Thank you."]),

#---> Arkham
    "Lawyer1":('"Well sir, here\'s the place. Shall we head inside and take a look?"',["After you."]),
    "Lawyer2":('"Here we are then. The sitting room is just through that other door. Let me know when you\'ve finished looking around."',["OK. I will."]),
    "Lawyer3":('"Oh... Er, hello."',["Hi. Did you find anything interesting?"]),
    "Lawyer4":('"Oh yes, yes indeed. It\'s all very interesting. Would you excuse me? I need to make a phonecall."',
["Of couse."]),
    "WindOpt":('A painting of some kind. Weren\'t there a few like it in the sitting room?',["Examine it","Take it"]),
    "WindEx":('Labelled \'The Summoning of Wind\'. It depicts a large vortex it seems.',["Take it"]),
    "WindTk":('It probably belongs with the other two in the sitting room. You should place it right next to the Summoning of Blood.',["Make it so"]),

    "WindPlace":('Yes. You think the Summoning of Wind would look simply adorable next to the Summoning of Blood.',
                 ["Yes indeed. Most tasteful."]),
    "WindNice":('You are an interior decorating genius.',["Without question"]),
    "WindCrash":('You suddenly hear a crash! It sounds like breaking glass. You also hear an angry shout. Not the investigating type, you decide to get out of here.',["As soon as possible..."]),
    "WindWhere":('Labelled \'The Summoning of Blood\'. It shows a blackened, twisted figure. It is most disturbing.'
                 ' It almost seems like there should be a set of three such paintings.'
                 ' You wonder where the other is, if so.',[]),
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
    actions = ACTIONS.get((objectID, action))
    if actions:
        if type(actions) is tuple:
            actions = [actions]
        for actiontuple in actions:
            fn = actiontuple[0]
            args = actiontuple[1:]
            fn(gamestate, *args)
    return bool(actions)
