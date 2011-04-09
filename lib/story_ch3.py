"""
  Story elements for Chapter1

"""
from story_functions import *

ChapterActions = {
# Doors
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

# Chapter Intro
    ("Chapter3", "begin"):(begin_speech,"BeginChapter3"),
    ("BeginChapter3",1):(change_room,"arkham","begin"),

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
    ("Lawyer4",1):(take_object,"Lawyer3","lawyer call",
                   "He seems in a hurry to use the phone. What was he looking at?"),
    ("WindSumm1","click"):(begin_speech,"WindOpt"),
    ("WindOpt",1):(begin_speech,"WindEx"),
    ("WindOpt",2):(begin_speech,"WindTk"),
    ("WindEx",1):(begin_speech,"WindTk"),
    ("WindTk",1):(take_object,"WindSumm1","wind taken",
                  "You lift the frame from the wall in order to move it into the other room."),
    ("arkroom2a","begin"):(do_ifelse,set(),set(("room2 first",)),("2a","first"),("DO","NOTHING")),
    ("2a","first"):(foot_text,"Whoever or whatever is in here seems to have gone upstairs. And they've taken the Summoning of Wind with them. The door is locked, you are not getting out of here alive. The least you can do is stop any future Summonings from happening."),

}

ChapterSpeech = {
    "BeginChapter3":(
        "Your father set out on the Titanic when you were only little yet never returned. Unable to articulate who he"
        " was, he has remained in a Massachusets mental hospital ever since.\n"
        "When you finally discover his whereabouts, you take the long trip to visit him. Upon arrival, he speaks"
        " gibberish about some fantasy cult responsible for the sinking of the Titanic. Unable to believe him"
        " or persuade the doctors to release him, you decide you can at least finish what he started and visit"
        " the old Arkham house.\n"
        "You decide to engage a lawyer and claim ownership of the ancient building.", ["Begin"]),
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
