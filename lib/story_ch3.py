"""
  Story elements for Chapter3

"""
from story_functions import *

def setup_room_3(gamestate, ms):
    if "moved clock" in EVENTS:
        take_object(gamestate, "Painting1", "", "...")
        take_object(gamestate, "Painting2", "", "Two very strange paintings are exposed")
        add_prop(gamestate, ("FireSumm", "painting", (-.98,4,-0.4),90,
                             "'The Summoning of Fire' A painting of what? Some kind of creature?", 
                             "firesummon"), False)
        add_prop(gamestate, ("BloodSumm", "painting", (-.98,4,-0.9),90,
                             "'The Summoning of Blood'. Very disturbing. A twisted, discoloured figure.",
                             "bloodsummon"), False)
        move_actor(gamestate, "GrandfatherClock", (0,5,0), ms)
        if "cultists coming" in EVENTS:
            take_object(gamestate, "ArkR3to1","","Something is wrong...")
            take_object(gamestate, "ArkR3to2","","Something is wrong...")
            add_prop(gamestate, ("ArkR3to1a","door",(8,4,0),180,"",None),False)
            add_prop(gamestate, ("ArkR3to2a","door",(4,0,0),90,"",None),False)
            begin_speech(gamestate,"BreakIn")

ChapterActions = {
# Doors
    ("ArkHDoor", "click"):(key_check,["lawyer in"], "arkroom1", "street",True,
                           "You should speak to Reginald, your lawyer, first."),
    ("ArkR1to3", "click"):[(change_room, "arkroom3", "room1"),(cause_event,"door lock")],
    ("ArkR1to2", "click"):(key_check, ["door lock"], "arkroom2", "room1",True,
                           "Reg is in the way. You should check out the other room."),
    ("ArkHtoStreet", "click"):(key_check, ["door lock"], "arkham", "door",False,
                               "It's locked. Strange... You certainly didn't lock it."),
    ("ArkR2to1", "click"):(change_room, "arkroom1", "room2"),
    ("ArkR2to3", "click"):(change_room, "arkroom3", "room2"),
    ("ArkR3to1", "click"):(change_room, "arkroom1", "room3"),
    ("ArkR3to2", "click"):(change_room, "arkroom2", "room3"),

    ("ArkR1to2a", "click"):(change_room, "arkroom2a", "room1"),
    ("ArkR2to1a", "click"):(change_room, "arkroom1a", "room2"),
    ("ArkR1to3a", "click"):(change_room, "arkroom3a", "room1"),
    ("ArkR2to3a", "click"):(change_room, "arkroom3a", "room2"),
    ("ArkR3to1a", "click"):(change_room, "arkroom1a", "room3"),
    ("ArkR3to2a", "click"):(change_room, "arkroom2a", "room3"),

# Chapter Intro
    ("Chapter3", "begin"):(begin_speech,"BeginChapter3"),
    ("BeginChapter3",1):(change_room,"arkham","begin"),
    ("BeginChapter3",2):[(chapter_setup, 4), (chapter_end, (1,1,0,1), "Chapter4")],

# Actions
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
    ("arkroom1","AddLawyer"):(add_prop,("Lawyer2","man",(0,2,0),0,"Reg.D, lawyer","lawyer"),False),
    ("Lawyer2","click"):(begin_speech,"Lawyer2"),
    ("arkroom2","begin"):(do_ifelse,set(),set(("lawyer call",)),("arkroom2","AddLawyer"),("DO","NOTHING")),
    ("arkroom2","AddLawyer"):(add_prop,("Lawyer3","man",(0,6,0),180,"Reg.D, lawyer","lawyer"),False),
    ("arkroom3", "begin"):(setup_room_3, 1),
    ("Lawyer3","click"):[(face_player,"Lawyer3"),(begin_speech,"Lawyer3")],
    ("Lawyer3",1):(begin_speech,"Lawyer4"),
    ("Lawyer4",1):(take_object,"Lawyer3","lawyer call",
                   "He seems in a hurry to use the phone. What was he looking at?"),
    ("GrandfatherClock","click"):(do_ifelse,set(),set(("moved clock",)),("GClock","talk"),("DO","NOTHING")),
    ("GClock","talk"):(begin_speech, "GClockPuzzle"),
    ("GClockPuzzle",1):(foot_text, "You don't know anything about clocks"),
    ("GClockPuzzle",2):(foot_text, "Are you kidding? It weighs a ton."),
    ("GClockPuzzle",3):[(cause_event, "moved clock"), (setup_room_3, 3000)],
    ("WindSumm","click"):(begin_speech, "WindSumm"),
    ("WindSumm",1):(cause_event, "cultists coming"),
    ("StaircaseA","click"):(begin_speech,"BloodStairs"),
    ("BloodStairs",1):(begin_speech,"StopThem"),
    ("BloodStairs",2):(begin_speech,"GetAway"),
    ("Painting1a","click"):(begin_speech,"TakeFire"),
    ("Painting2a","click"):(begin_speech,"TakeBlood"),
    ("arkroom3a","begin"):[(do_ifelse,set(),set(("fire taken",)),("fire","place"),("DO","NOTHING")),
                           (do_ifelse,set(),set(("blood taken",)),("blood","place"),("DO","NOTHING"))],
    ("fire","place"):(add_prop,("Painting1a","painting",(-0.98,4,-0.4),90,
                                "The Summoning of Fire","firesummon"),False),
    ("blood","place"):(add_prop,("Painting2a","painting",(-0.98,4,-0.9),90,
                                "The Summoning of Blood","bloodsummon"),False),
    ("TakeFire",1):[(begin_speech,"TookFire"),(take_object,"Painting1a","fire taken","You now carry the Summoning of Fire.")],
    ("TakeBlood",1):[(begin_speech,"TookBlood"),(take_object,"Painting2a","blood taken","You now carry the Summoning of Blood.")],
    ("FireplaceA","click"):(do_ifelse,set(("blood taken","fire taken")),set(),("FireplaceA","burn"),("DO","NOTHING")),
    ("FireplaceA","burn"):(begin_speech,"BurnThem"),
    ("BurnThem",1):(begin_speech,"BloodBurn"),
    ("BurnThem",2):(begin_speech,"FireBurn"),
    ("BloodBurn",1):(begin_speech,"FireBurn"),
    ("FireBurn",1):(begin_speech,"EndChapter3"),
    ("EndChapter3",1):[(chapter_setup, 4), (chapter_end, (1,1,0,1), "Chapter4")],


}

ChapterSpeech = {
    "BeginChapter3":(
        "Your father set out on the Titanic when you were only little yet never returned. Unable to articulate who he"
        " was, he has remained in a Massachusets mental hospital ever since.\n"
        "When you finally discover his whereabouts, you take the long trip to visit him. Upon arrival, he speaks"
        " gibberish about some fantasy cult responsible for the sinking of the Titanic. Unable to believe him"
        " or persuade the doctors to release him, you decide you can at least finish what he started and visit"
        " the old Arkham house.\n"
        "You decide to engage a lawyer and claim ownership of the ancient building.", ["Begin","Ch4 skip"]),
    "Lawyer1":('"Well sir, here\'s the place. Shall we head inside and take a look?"',["After you."]),
    "Lawyer2":('"Here we are then. Let me know when you\'ve finished looking around."',["OK. I will."]),
    "Lawyer3":('"Oh... Er, hello."',["Hi. Did you find anything interesting?"]),
    "Lawyer4":('"Oh yes, yes indeed. It\'s all very interesting.'
               ' Would you excuse me? I need to make a phonecall."',
               ["Of couse."]),
    "GClockPuzzle":("This must be your grandfather's clock, ironically enough. It's not ticking",
                    ["Try to wind it", "Try to lift it", "Try to push it", "Leave it alone"]),
    "WindSumm":("There is some weird writing on the picture. It looks very old.\n"
                "Maybe it's valuable. Perhaps there are many such things in this old house.\n",
                ["Possibly in your grandfather's study..."]),
    "WindCrash":('You suddenly hear a crash! It sounds like breaking glass. You also hear an angry shout. Not the investigating type, you decide to get out of here.',["As soon as possible..."]),
    "BloodStairs":('There\'s blood everywhere and you can hear chanting upstairs. On top of this, the Summoning of Wind is missing. What are they doing up there? Maybe your father was right about these people ... the cult.',["I must stop them","I must get away"]),
    "BreakIn":("You hear a loud smash followed by muffled cursing. Someone has broken in to the house.",[]),
    "StopThem":("But how? There must be more than one person upstairs. And God knows what else. The Summoning of Wind, whatever it is, is presumably in progress. You must prevent them from getting the other two",["Why me?"]),
    "GetAway":("Good luck with that.",["...Thanks"]),
    "TakeFire":("It\'s the Summoning of Fire. Will you take it?",["Take it","No"]),
    "TakeBlood":("It\'s the Summoning of Blood. Will you take it?",["Take it","No"]),
    "TookFire":("You lift the Summoning of Fire off its nail.",[]),
    "TookBlood":("You lift the Summoning of Blood off its nail.",[]),
    "BurnThem":("The rising wind outside roars across the chimney, causing the flames to flicker and sway.",["Burn the Blood Summoning","Burn the Fire Summoning"]),
    "BloodBurn":("You feed the Summoning of Blood into the flames. It crackles and almost seems to bubble as it crumbles away.",["Burn the Fire one now"]),
    "FireBurn":("You throw the Summoning, frame and all, into the fire. The second the flames meet the parchment the fire leaps high. Sparks and embers fly from the burning parchment, sprouting new infernos where they land. In a matter of seconds, the entire sitting-room is ablaze. There is no time to escape. Eventually, the entire building is consumed. ",["End of Chapter 3"]),
    "EndChapter3":("The Summoning of Wind hit Arkham as a category 5 hurricane. Hundreds of people were killed"
                   " throughout New England. The Summonings of Blood and Fire, through your actions, were delayed"
                   " for decades.\n"
                   "Nobody knew how grateful they should be for the desperate actions of a lone hero, least"
                   " of all your only daughter. She grew up knowing nothing of the darkness in her family"
                   " history.", ["Epilogue..."]),
}
