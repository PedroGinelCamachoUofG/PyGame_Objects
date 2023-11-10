import pygame as py
import math

"""
Basic Objects
"""
class Window:

    def __init__(self, caption, window_dimensions) -> None:
        py.init()
        py.display.set_caption(caption)
        self.win = py.display.set_mode(window_dimensions)
        self.objects = {}

    # Place objects in a circle around the a given location in the screen
    def place_circular(self, x, y, radius) -> None:
        for i,obj in enumerate(self.objects.values()):
            obj.set_pos(x + math.cos(((2*math.pi)/len(self.objects))*i)*100, y + math.sin(((2*math.pi)/len(self.objects))*i)*100)
            # note that arrow and line objects do not have a set_pos method

    def draw(self) -> None:
        self.win.fill((245,245,245))
        for obj in reversed(list(self.objects.values())):
            obj.draw(self.win)
        py.display.update()

class Text:

    def __init__(self, x, y, text, font):
        self.text = text
        self.x = x
        self.y = y
        self.font = font

    def change_text(self, text):
        self.text = text

    def add_text(self,char):
        self.text += char

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def is_over(self, pointer):
        if (self.x < pointer.get_pos()[0] < self.font.size(self.text)[0]+self.x) and (self.y < pointer.get_pos()[1] < self.font.size(self.text)[1]+self.y):
            return True
        return False

    def draw(self, win):
        win.blit(self.font.render(self.text, True, (0,0,0)), (self.x, self.y))


"""
Input Objects
"""
class Button:
    def __init__(self, x, y, static_image=None, hover_image=None, width=None, height=None, color=None):
        self.current_image = static_image
        self.static_image = static_image
        self.hover_image = hover_image
        self.x = x
        self.y = y
        if self.current_image is not None:
            self.width = self.current_image.get_width()
            self.height = self.current_image.get_height()
        else:
            self.width = width
            self.height = height
        if color is None:
            self.color = (255,0,0)
        else:
            self.color = color
        self.object = py.Rect(self.x, self.y, self.width, self.height)
        self.actions = [] #functions mus take no args currently

    def draw(self, win):
        if self.current_image is not None:
            win.blit(self.current_image, (self.x, self.y))
        else:
            py.draw.rect(win, self.color, self.object)

    def is_over(self, pointer):
        if self.object.collidepoint(pointer.get_pos()):
            self.current_image = self.hover_image
            return True
        self.current_image = self.static_image
        return False

    def exe_all(self):
        for func in self.actions:
            func()

    def set_pos(self, x, y):
        self.x = x
        self.y = y
        self.object = py.Rect(self.x, self.y, self.width, self.height)

class InputBox:
    """
    Code for giving the input box textures has been commented out
    """
    def __init__(self, x, y, width, height, font, default_text=''):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = Text(self.x, self.y, default_text, font)
        self.object = py.Rect((self.x, self.y), (self.width, self.height))
        self.active = False


        # self.currentImage = staticImage
        # self.staticImage = staticImage
        # self.hoverImage = hoverImage
        #self.wid = self.currentImage.get_width()
        #self.hei = self.currentImage.get_height()
        #self.active = False


    def write(self, char):
        if len(self.text.text) < 35:
            self.text.add_text(char)

    def delete_one(self):
        self.text.change_text(self.text.text[:-1])

    def delete_all(self):
        self.text.change_text('')

    def is_over(self, pointer):
        if self.object.collidepoint(pointer.get_pos()):
            return True
        return False

    def select(self):
        self.active = True

    def unselect(self):
        self.active = False

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def draw(self, win):
        py.draw.rect(win, py.Color(255, 255, 255), self.object)
        self.text.draw(win)
        #win.blit(self.currentImage, (self.x, self.y))

"""
Shapes
"""
class Rectangle:
    """
    This class is meant for any image or anything that has a rectangular shape
    """
    def __init__(self, x, y, width, height, image=None, color=None):
        self.x = x
        self.y = y
        self.image = image
        if image is not None:
            self.width = image.get_width()
            self.height = image.get_height()
        else:
            self.width = width
            self.height = height
        self.object = py.Rect((self.x, self.y), (self.width, self.height))
        if color is None:
            self.color = (255,0,0)
        else:
            self.color = color
        self.info = []

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def is_over(self, pointer):
        if self.x < pointer.get_pos()[0] < self.x+self.width and self.y < pointer.get_pos()[1] < self.y+self.height:
            return True
        return False

    def draw(self, win):
        if self.image is not None:
            win.blit(self.image, (self.x, self.y))
        else:
            py.draw.rect(win, self.color, self.object)

class Arrow:

    def __init__(self, start, end, color=None):
        if color is None:
            self.color = (255,0,0)
        else:
            self.color = color
        self.point = end
        self.length = int(math.sqrt(((start[0]-end[0])**2)+((start[1]-end[1])**2)))
        self.direction = [(end[0] - start[0]), (end[1] - start[1])]
        #make direction unitary
            #this to avoid division by 0 if the line is parallel
        if self.direction[0] == 0 or self.direction[1] == 0:
            self.direction[0] = 1
            self.direction[1] = 1
        self.direction = (self.direction[0]/math.sqrt((self.direction[0]**2)+(self.direction[1]**2)),
                          self.direction[1]/math.sqrt((self.direction[0]**2)+(self.direction[1]**2)))
        self.tangent = (-self.direction[1], self.direction[0])
        """points:    c\ 
        a-------------b  \point
        f-------------e  /
                      d/
        """
        self.a = (start[0]+(self.tangent[0]*5), start[1]+(self.tangent[1]*5))
        self.f = (start[0]-(self.tangent[0] * 5), start[1]-(self.tangent[1] * 5))
        self.b = (self.a[0]+(self.direction[0]*(self.length-10))), (self.a[1]+(self.direction[1]*(self.length-10)))
        self.e = (self.f[0]+(self.direction[0]*(self.length-10))), (self.f[1]+(self.direction[1]*(self.length-10)))
        self.c = (self.b[0]+self.tangent[0]*5, self.b[1]+self.tangent[1]*5)
        self.d = (self.e[0]-self.tangent[0]*5, self.e[1]-self.tangent[1]*5)

    def draw(self, win):
        py.draw.polygon(win, (255,0,0), [self.a, self.b, self.c, self.point, self.d, self.e, self.f])

class Line:

    def __init__(self, start, end, color=None) -> None:
        self.start = start
        self.end = end
        if not color:
            self.color = (0,0,0)
        else:
            self.color = color
        self.length = int(math.sqrt(((start[0]-end[0])**2)+((start[1]-end[1])**2)))
        self.direction = [(end[0] - start[0]), (end[1] - start[1])]
        #this to avoid division by 0 if the line is parallel
        if self.direction[0] == 0 or self.direction[1] == 0:
            self.direction[0] = 1
            self.direction[1] = 1
        self.direction = (self.direction[0]/math.sqrt((self.direction[0]**2)+(self.direction[1]**2)), self.direction[1]/math.sqrt((self.direction[0]**2)+(self.direction[1]**2)))
        self.tangent = (-self.direction[1], self.direction[0])
        """
        Points
        a ----------------- b
        |                   |
        c ----------------- d
        """
        self.a = (start[0]+(self.tangent[0]*5), start[1]+(self.tangent[1]*5))
        self.b = (self.a[0]+(self.direction[0]*(self.length-10))), (self.a[1]+(self.direction[1]*(self.length-10)))
        self.c = (start[0]-(self.tangent[0] * 5), start[1]-(self.tangent[1] * 5))
        self.d = (self.c[0]+(self.direction[0]*(self.length-10))), (self.c[1]+(self.direction[1]*(self.length-10)))

    def draw(self, win) -> None:
        py.draw.polygon(win, self.color, [self.a, self.b, self.d, self.c])