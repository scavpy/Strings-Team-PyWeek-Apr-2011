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

def take_artifact(gamestate):
    """ Adds item to inventory and spawns a cultist behind you.
    Removes ability to walk."""
    pass

def add_prop(gamestate,p):
    """ parameters: a tuple of (name,model,pos,angle,text) """
    s = p[0]+" spawned"
    if s not in EVENTS:
        prop = PropPart(p[0],_obj_filename=p[1]+".obj",_pos=p[2],_angle=p[3])
        prop.text = p[4]
        prop.prepare()
        gamestate["Room"].append(prop)
        EVENTS.add(s)


# All story actions in the whole game

EVENTS = set()

ACTIONS = {
    ("SPRoomDoor", "click"):(change_room, "hotelhall", "yourroom"),
    ("SPCultDoor", "click"):(change_room, "hotelhall", "cultroom"),
    ("SPHRoomDoor", "click"):(change_room, "hotelroom1", "door"),
    ("SPHCultDoor", "click"):(change_room, "hotelroom2", "door"),
    ("SPHLobbyDoor", "click"):(change_room, "hotellobby", "hallway"),
    ("SPHallDoor", "click"):(change_room, "hotelhall", "lobby"),
    ("SPHRightDoor", "click"):(change_room, "street", "hotel"),
    ("SPHLeftDoor", "click"):(change_room, "street", "hotel"),

    ("HotelDoors", "click"):(change_room, "hotellobby", "street"),
    ("AHDoors", "click"):(change_room, "auctionhouse", "door"),
    ("MartDoor", "click"):(change_room, "marthouse", "door"),

    ("Boat", "click"):(change_room, "titandeck", "door"),
    ("House", "click"):(change_room, "arkham", "begin"),

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

    ("CultBedside", "click"):(add_prop, ("Artefact","artefact",(6.7,3,0.55),90,"This is the artefact.") ),
    
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

