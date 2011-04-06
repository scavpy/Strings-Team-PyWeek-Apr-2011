"""
Story controller

Full of spoilers!


Determines the possible actions on each unique named object in terms
of story transitions, inventory etc.

"""
import data


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
    return ["examine", "take"]

def action_for_object(gamestate, objectID, action):
    """ Perform an action on an object, which may cause effects in
    a specified GameState

    These effects may include:
    change room  (sets gamestate.quit)
    get item (adds an item to the item bar)
    drop item (removes an item from the item bar)
    clear items (drops everything from the item bar)

    """
    print "object:", objectID, "action:", action
