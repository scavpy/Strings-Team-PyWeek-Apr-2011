"""
  Story elements for Chapter1

"""
from story_functions import *


def take_artefact(gamestate):
    """ Adds item to inventory and spawns a cultist behind you.
    Removes ability to walk."""
    gp = gamestate.player
    take_object(gamestate,"Artefact","caught stealing",
                "You take the artefact only to hear a slam and a click behind you.")
    add_prop(gamestate,("CultistA","cultist-threaten",(4,6,0),-90,"Cultist","cultist-1900"),True)
    gamestate["Room"].walktiles.remove((4,6))
    gp.watching_me = gamestate["CultistA"]
    gp.turn_to_face(gamestate["CultistA"],250)

def martin_scare(gamestate):
    gp = gamestate.player
    gp.turn(-180)
    gamestate.footer_text("Nothing. You are disappointed. Relieved, but disappointed.")


ChapterActions = {
# Doors
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
    ("AHLeftDoor", "click"):(change_room, "street", "ah"),
    ("AHRightDoor", "click"):(change_room, "street", "ah"),
    ("InMartDoor", "click"):(change_room, "street", "marthouse"),

# Chapter Intro
    ("Chapter1", "begin"):(begin_speech,"BeginChapter1"),
    ("BeginChapter1",1):(change_room, "hotelroom1", "begin"),
    ("BeginChapter1",2):[(chapter_setup, 2), (change_room, "Chapter2", "begin")],

# Chapter 1 events
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
    ("EndChapter1",1):[(chapter_setup, 2), (chapter_end, (0.5,0,0,1), "Chapter2")],
}

ChapterSpeech = {
    "CultA1":('"What are you doing? Give me that!"',["Did you kill Martin?","OK","No"]),
    "CultA2":('"Hah! Fool. You should have stayed away. [He shoots you.]"',["Try again", "Game Over"]),
    "CultA3":('"No? Are you mad? Give me it or I will shoot you!"\n'
              '[What will you do? He seems to be very nervous. The artefact must be precious to him.]',
              ["Destroy the artefact","Get shot"]),
    "CultA4":('"Martin? What does it matter when- No! You don\'t ask me questions! Give me the artefact!"',
              ["No","OK"]),
    "CultA5":('"What have you done!? Oh Gods!\n[He panics. There is a rumbling outside.]"',
              ["What's that noise?"]),

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
    "DLady7":('"Certainly sir! Now let\'s see, which was his room?"\n'
              '[She examines the number on a key]\n'
              '"Ah yes. Your message will be delivered sir."',
              ["Thank you very much madam."]),

    "BedsideOpt":("This is the cultists bedside table.\n"
                  "You highly doubt anything is inside but maybe it\'s worth checking.",
                  ["Open it.","Attempt and succeed to fail to open it."]),
    "MartinOpt":("Oh God ... Martin... What will you do?",
                 ["Check for a pulse","Check wounds","Remove the head in case of zombie plague",
                  "Look ... behind ... you"]),
    "MartinOpt1":("You do so but there's almost no point. He's most definately dead.",["Well then..."]),
    "MartinOpt2":("The wounds were caused by a knife. Stabbed in the gut. He's holding something here...",
                  ["Examine it"]),
    "MartinExamine":("Two documents are here. The first is something about a dark artefact.\n"
                     "It describes a ritual it seems, though you can't read the language.\n"
                     "There is also an image of nine pillars, each more crumbling and ruined than the last."
                     " The artefact is mounted atop the first.",["And the other document..."]),
    "MartinExamine2":("...is a brochure for an auction at the auction house next door."
                      " One of the items appears to be the artefact in the occult text."
                      " Unfortunately the auction was yesterday. Someone has this in their possession"
                      " and you need to find them before they leave Saint-Pierre.",["Go and investigate"]),
    "MartinOpt3":("Certainly not! You couldn't bear to. Besides, the cliche doesn't exist yet, it's 1902.",
                  ["Well then..."]),

    "AHsmalltalk":('"Oh hello... Umm, you\'re a little early for the auction..."',
                   ["Sorry. I just wanted to ask if you know a Martin DuPont?",
                    "Oh sorry... Umm, I'd best be off. "]),
    "AHmartin":('"Martin? Umm, yes I think he lives next door in the uh, white house."',
                ["Thank you. Goodbye.","Does he often come here?"]),
    "AHoften":('"Often? Er, no not really. He was in here umm, yesterday though.'
               ' He only bid on one item and umm, he was outbid by quite a large umm, summ."',
               ["I see. Well thank you. Goodbye."]),
    "AHartefact":('"Oh hello. Umm, you\'re a little early for the auction..."',
                  ["Yes I know. Can you tell what this item is?"]),
    "AHartefact2":('"Umm, that\'s umm... well no I\'m not sure. You could try, er, asking the'
                   ' gentleman who purchased it yesterday. He umm, seemed quite determined to'
                   ' get his hands on it."',["And what gentleman was this?"]),
    "AHartefact3":('"Oo, um, let me, er, see I... I never caught his name. All I remember is'
                   ' that he wore a brown shirt and had a rather large moustache.'
                   ' I think he stays at the umm, Santa Maria hotel."',
                   ["Thank you, you've been most UMM-helpful..."]),
 
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
}
