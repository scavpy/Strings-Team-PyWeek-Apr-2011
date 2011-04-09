"""
  Story elements for Chapter2

"""
from story_functions import *

ChapterActions = {
# Doors
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

# Chapter Intro
    ("Chapter2", "begin"):(begin_speech,"BeginChapter2"),
    ("BeginChapter2",1):(change_room, "titandeck", "begin"),
    ("BeginChapter2",2):(begin_speech,"Tough"),
    ("BeginChapter2",3):[(chapter_setup, 3), (change_room,"Chapter3","begin")],
    ("Tough",1):(change_room, "titandeck", "door"),

# Actions
    ("Sailor1","click"):[(face_player, "Sailor1"), (do_ifelse,set(("go time",)),set(),("Sailor","tellon"),("Sailor","talk1"))],
    ("Sailor2","click"):[(face_player, "Sailor2"), (do_ifelse,set(("go time",)),set(),("Sailor","tellon"),("Sailor","talk2"))],
    ("Sailor","talk1"):(begin_speech,"S1"),
    ("Sailor","talk2"):(begin_speech,"S2"),
    ("Sailor","tellon"):(begin_speech,"STell"),
    ("STell",1):(begin_speech,"SLose"),
    ("STell",2):(begin_speech,"SWin"),
    ("SWin",1):(begin_speech,"EndChapter2"),
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
    ("EndChapter2",1):[(chapter_setup, 3), (chapter_end, (0,0.2,0.1,1), "Chapter3")],
}

ChapterSpeech = {
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
}
