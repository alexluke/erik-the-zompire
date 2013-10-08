import pygame, os

"""
resource.py
A caching resource loader
License: Public Domain
Author: David Clark (silenus at telus.net)

This module wraps pygame's resource loading functions.  It ensures that only
one copy of any given resource will be in memory at any time - further requests
for that same resource will get a reference to the loaded copy.  This behavoir
can be overridden by specifying that the resource loading be forced - all
clients of that resource will then refer to the new version.  The resource can
be manually removed from memory with the clear_* set of functions.

This code might be useful if a game is going to be loading many copies of a
given disk resource.  Most of the time, you'd write your own cache; now you
can just use this one.

Remember to call the 'set path' functions before trying to load anything;
otherwise, you'll get a ValueError.


"""



__images = {}
__actions = {}
__fonts = {}
__sounds = {}
__sound_actions = {}

__images_path = 'data'
__fonts_path = None
__sounds_path = os.path.join('data','sound')

class NoneSound:
    def play(self): pass

def get_image(filename, colorkey = None, force_reload = 0):
    """
    get_image(filename, colorkey = None, force_reload = 1) --> surface
    Call this function instead of pygame.image.load - it will load the image
    from the disk the first time, then just return a reference to the copy each
    subsequent time.  This function does no colorkey setting or pixel format
    conversion; you'll have to do that manually, if you wish.
    """
    
    if not __images_path:
        raise ValueError, "resources.set_images_path() not called yet."
    if (force_reload == 1 or filename not in __images.keys()):
        try:
            surface = pygame.image.load(os.path.join(__images_path, filename))            
        except pygame.error:
            raise IOError, "File " + filename + " not found."
        if colorkey is not None:
            if colorkey is -1:
                 colorkey = surface.get_at((0,0))
            surface.set_colorkey(colorkey, pygame.locals.RLEACCEL)
        __images[filename] = surface
        return surface
    else:
        return __images[filename]

def has_image(filename):
    """
    has_image(filename) --&gt; Boolean
    Returns true if the image is in memory, false if it has to be loaded from
    disk.
    """
    return __images.has_key(filename)

def clear_image(filename):
    """
    clear_image(filename) --&gt; Boolean
    Eliminates the image from memory.  Subsequent calls will load it from the
    disk.  Returns True if the resource was found in memory, False if it
    Wasn't.  Use this to reduce the memory footprint, if you're sure you won't
    be needing the resource again.
    """
    
    try:
        del __images[filename]
        return 1
    except KeyError:
        return 0

def get_action(who, what, direction):
    global __actions
    if not __actions.has_key(who):
        __actions[who] = {}
    if not __actions[who].has_key(what):
        __actions[who][what] = {}
        for directions in ('n','ne','e','se','s','sw','w','nw'):
            __actions[who][what][directions] = load_direction(who, what, directions)
    return __actions[who][what][direction]
                

def load_direction(who, what, direction):
    images = []
    num = 0
    while 1:
        filename = os.path.join(who, ' '.join((what, direction))+ \
                                               '000'+str(num) + '.bmp')
        try:
            newimage = get_image(filename, -1)
            images.append(newimage)
        except IOError:
            break        
        num = num + 1
    if len(images) == 0:
        raise IOError, "Did not find any tiles for " + who + "_" + what + "_" + direction
    return images

def get_font(filename, size, force_reload = 0):
    """ 
    get_font(filename, size, force_reload = 1) --&gt; surface
    Call this function instead of pygame.font.Font - it will load the font
    from the disk the first time, then just return a reference to the copy each 
    subsequent time.
    """
    if not __fonts_path:
        raise ValueError, "resources.set_fonts_path() not called yet."
    if (force_reload == 1 or filename not in __fonts.keys()):
        try:
            font = pygame.font.Font(os.path.join(__fonts_path, filename), size)
        except pygame.error:
            raise IOError, "File " + filename + " not found."
        __fonts[filename] = font
        return font
    else:
        return __fonts[filename]

def has_font(filename):
    """
    has_font(filename) --&gt; Boolean
    Returns true if the font is in memory, false if it has to be loaded from
    disk.
    """
    return __fonts.has_key(filename)

def clear_font(filename):
    """
    clear_font(filename) --&gt; Boolean
    Eliminates the font from memory.  Subsequent calls will load it from the
    disk.  Returns True if the resource was found in memory, False if it
    Wasn't.  Use this to reduce the memory footprint, if you're sure you won't
    be needing the resource again.
    """
    try:
        del __fonts[filename]
        return 1
    except KeyError:
        return 0

def get_sound(filename, force_reload = 0):
    """
    get_sound(filename, force_reload = 1) --&gt; sound
    Call this function instead of pygame.mixer.Sound - it will load the sound
    from the disk the first time, then just return a reference to the copy each 
    subsequent time.  
    """
    if not __sounds_path:
        raise ValueError, "resources.set_sounds_path() not called yet."
    if (force_reload == 1 or filename not in __fonts.keys()):
        try:
            sound = pygame.mixer.Sound(os.path.join(__sounds_path, filename))
        except pygame.error:
            raise IOError, "File " + filename + " not found."
        __sounds[filename] = sound
        return sound
    else:
        return __sounds[filename]
    
def get_action_sound(who, what):
    global __sounds
    if not __actions.has_key(who):
        __actions[who] = {}
    if not __actions[who].has_key(what):
        __actions[who][what] = []
        num = 1
        while 1:
            filename = '_'.join((who, what, str(num)))+'.wav'
            try:
                newsound = get_sound(filename)
                __actions[who][what].append(newsound)
            except IOError:
                break
            num = num + 1
        if len(__actions[who][what]) == 0:
            #print "Did not find any sounds for " + who + "_" + what
            __actions[who][what].append(NoneSound())
    return __actions[who][what]

def has_sound(filename):
    """
    has_sound(filename) --&gt; Boolean
    Returns true if the sound is in memory, false if it has to be loaded from
    disk.
    """
    return __sounds.has_key(filename)

def clear_sound(filename):
    """
    clear_sound(filename) --&gt; Boolean
    Eliminates the sound from memory.  Subsequent calls will load it from the
    disk.  Returns True if the resource was found in memory, False if it
    Wasn't.  Use this to reduce the memory footprint, if you're sure you won't
    be needing the resource again.
    """
    try:
        del __sounds[filename]
        return 1
    except KeyError:
        return 0

def set_images_path(path):
    """
    set_images_path(path) --&gt; Boolean
    Set the path you'll be loading the images off of.  Pass the string
    representation of the new path.  Raises an exception if the path doesn't
    exist, otherwise it returns True.
    """
    if not os.access(path, os.F_OK):
        raise IOError, path + " not found."
    if path.endswith(os.sep):
        path = path[:-1]
    global __images_path
    __images_path = path
    return 1

def set_fonts_path(path):
    """
    set_fonts_path(path) --&gt; Boolean
    Set the path you'll be loading the fonts off of.  Pass the string
    representation of the new path.  Raises an exception if the path doesn't
    exist, otherwise it returns True.
    """
    if not os.access(path, os.F_OK):
        raise IOError, path + " not found."
    if path.endswith(os.sep):
        path = path[:-1]
    global __fonts_path
    __fonts_path = path
    return 1

def set_sounds_path(path):
    """
    set_sounds_path(path) --&gt; Boolean
    Set the path you'll be loading the sounds off of.  Pass the string
    representation of the new path.  Raises an exception if the path doesn't
    exist, otherwise it returns True.
    """
    if not os.access(path, os.F_OK):
        raise IOError, path + " not found."
    if path.endswith(os.sep):
        path = path[:-1]
    global __sounds_path
    __sounds_path = path
    return 1

    
def get_images_path():
    """
    get_images_path() --&gt; String
    Returns the current value of the images path, or None if it hasn't been
    set yet.
    """
    return __images_path

def get_fonts_path():
    """
    get_fonts_path() --&gt; String
    Returns the current value of the fonts path, or None if it hasn't been
    set yet.
    """
    return __fonts_path

def get_sounds_path():
    """
    get_sounds_path() --&gt; String
    Returns the current value of the sounds path, or None if it hasn't been
    set yet.
    """
    return __sounds_path
