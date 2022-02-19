from tkinter import *
from math import sin, cos, pi
from random import choice
from tkinter.messagebox import showinfo

class Cube:
    def __init__(self, x, y, width):
        self.width= width
        self.make_points(x, y, width)
        self.polygon_id = None

    def __lt__(self, other):
        return self.__cmp__(other) == -1

    def __le__(self, other):
        return self.__cmp__(other) != 1

    def __eq__(self, other):
        return self.__cmp__(other) == 0

    def __ne__(self, other):
        return self.__cmp__(other) != 0

    def __gt__(self, other):
        return self.__cmp__(other) == 1

    def __ge__(self, other):
        return self.__cmp__(other) != -1
    
    def __cmp__(self, other):
        min_x, min_y = self.xy
        other_min_x, other_min_y = other.xy
        if min_y < other_min_y:
            return 1
        elif min_y > other_min_y:
            return -1
        elif min_x > other_min_x:
            return 1
        elif min_x < other_min_x:
            return -1
        else:
            return 0
        
    @property
    def xy(self):
        min_x, min_y = self._points[0]
        for x, y in self._points[1:]:
            min_x = min(min_x, x)
            min_y = min(min_y, y)
        return (min_x, min_y)

    @property
    def dxy(self):
        max_x, max_y = self._points[0]
        for x, y in self._points[1:]:
            max_x = max(max_x, x)
            max_y = max(max_y, y)
        return (max_x, max_y)
        
    def reset(self, points):
        self._points = points

    def copy(self):
        cube = Cube(0, 0, 0)
        cube.reset(self._points.copy())
        return cube
        
    @property
    def points(self):
        polygon_points = []
        for point in self._points:
            polygon_points.extend(point)
        return polygon_points
    
    def make_points(self, x, y, width):
        self._points = [(x,y), (x+width-1, y), (x+width-1, y+width-1), (x, y+width-1)]

    def rotate(self, x, y):
        new_points = []
        for point in self._points:
            newx = y - point[1]+ x
            newy = point[0] - x + y
            new_points.append((newx, newy))
        self._points = new_points

    def move(self, deltax, deltay):
        new_points = []
        for point in self._points:
            newx = point[0] + deltax
            newy = point[1] + deltay
            new_points.append((newx, newy))
        self._points = new_points

    def hit_test(self, cube):
        min_x, min_y = self.xy
        max_x, max_y = self.dxy
        for x, y in cube._points:
            if min_x <= x <= max_x and min_y <= y <= max_y:
                return True
        return False
            
class BaseCube:
    count = 0
    # color = ["#0d44e0", "#d83c3c", "#dc1395", "#9a9c0c", "#11a1c2", "#187f8a"]
    color = ["#0d44e0"]
    def __init__(self):
        self.cubes = []
        self.center_x = 0
        self.center_y = 0
        self.tag = self.get_tag()
        self.draw_color = choice(BaseCube.color)
        self.rotate_adjust = [(-1, 0), (0, -1), (1, 0), (0, 1)]

    def create_cube(self, x, y, width):
        self.cubes.append(Cube(x, y, width))
        
    def get_tag(self):
        BaseCube.count = BaseCube.count + 1
        return f"cube_{BaseCube.count}"
    
    def draw(self, canvas):
        for cube in self.cubes:
            cube.polygon_id = canvas.create_polygon(cube.points, fill=self.draw_color, tag=self.tag)
        return self.tag
    
    def move(self, deltax, deltay):
        for cube in self.cubes:
            cube.move(deltax, deltay)
        self.center_x  = self.center_x  + deltax
        self.center_y = self.center_y + deltay

    def copy(self):
        cube = self.__class__(0, 0, 0)
        cube.cubes = [cube.copy() for cube in self.cubes]
        cube.center_x = self.center_x
        cube.center_y = self.center_y
        self.rotate_adjust =  self.rotate_adjust.copy()
        return cube
            
    def rotate(self, canvas=None):
        for cube in self.cubes:
            cube.rotate(self.center_x, self.center_y)
        self.move(*self.rotate_adjust[0])
        self.rotate_adjust.append(self.rotate_adjust.pop(0))
        if canvas:
            canvas.delete(self.tag)
            self.draw(canvas)

class SquareCube(BaseCube):
    def __init__(self, x, y, width):
        BaseCube.__init__(self)
        self.create_cube(x, y, width)
        self.create_cube(x+width, y, width)
        self.create_cube(x+width, y+width, width)
        self.create_cube(x, y+width, width)
        self.center_x = x + width
        self.center_y = y + width
            
class OneCube(BaseCube):
    def __init__(self, x, y, width):
        BaseCube.__init__(self)
        self.create_cube(x, y, width)
        self.create_cube(x, y+width, width)
        self.create_cube(x, y+2*width, width)
        self.create_cube(x, y+3*width, width)
        self.center_x = x
        self.center_y = y + 2 * width

class TCube(BaseCube):
    def __init__(self, x, y, width):
        BaseCube.__init__(self)
        self.create_cube(x, y, width)
        self.create_cube(x+width, y, width)
        self.create_cube(x+2*width, y, width)
        self.create_cube(x+width, y+width, width)
        self.center_x = x + width
        self.center_y = y + width

class SCube(BaseCube):
    def __init__(self, x, y, width):
        BaseCube.__init__(self)
        self.create_cube(x, y, width)
        self.create_cube(x, y+width, width)
        self.create_cube(x+width, y+width, width)
        self.create_cube(x+width, y+2*width, width)
        self.center_x = x + width
        self.center_y = y + width
        
class ZCube(BaseCube):
    def __init__(self, x, y, width):
        BaseCube.__init__(self)
        self.create_cube(x, y, width)
        self.create_cube(x, y+width, width)
        self.create_cube(x-width, y+width, width)
        self.create_cube(x-width, y+2*width, width)
        self.center_x = x
        self.center_y = y + width

class LCube(BaseCube):
    def __init__(self, x, y, width):
        BaseCube.__init__(self)
        self.create_cube(x, y, width)
        self.create_cube(x, y+width, width)
        self.create_cube(x, y+2*width, width)
        self.create_cube(x+width, y+2*width, width)
        self.center_x = x
        self.center_y = y + width
        
class JCube(BaseCube):
    def __init__(self, x, y, width):
        BaseCube.__init__(self)
        self.create_cube(x, y, width)
        self.create_cube(x, y+width, width)
        self.create_cube(x, y+2*width, width)
        self.create_cube(x-width, y+2*width, width)
        self.center_x = x
        self.center_y = y + width
                   
class Game:
    def __init__(self, canvas, x, y, width, height, speed, cube_width=20):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.cube_width = cube_width
        self.start_x = self.x + self.width/2 - cube_width - (self.x + self.width/2 - cube_width)%cube_width
        self.start_y = y
        self.down_cube = None
        self.down_cube_id = None
        self.pause_down_cube = None
        self.pause_down_cube_id = None
        self.make_edges()
        
    def get_random_cube(self):
        return choice([SquareCube, OneCube, TCube, SCube, ZCube, LCube, JCube])(self.start_x,  self.start_y, self.cube_width)
    
    def draw_cubes(self):
        for y in range(self.y, self.y+self.height-1, self.cube_width):
            for x in range(self.x, self.x+self.width-1, self.cube_width):
                self.canvas.create_polygon(Cube(x, y, self.cube_width).points, fill="#a3cecc")

    def make_edges(self):
        self.edges = []
        for y in range(self.y, self.y+self.height+1, self.cube_width):
            self.edges.append((Cube(self.x-self.cube_width, y, self.cube_width), "solid"))
            self.edges.append((Cube(self.x + self.width, y, self.cube_width), "solid"))
        for x in range(self.x, self.x+self.width+1, self.cube_width):
            self.edges.append((Cube(x, self.y + self.height, self.cube_width), "solid"))

    def erase_lines(self):
        self.edges.sort(key=lambda x: x[0])
        loop = True
        while loop:
            loop = False
            line_cube = []
            continous = False
            move_down = False
            delete_start = delete_end = None
            for edge_index, (cube_v, cube_t) in enumerate(self.edges):
                if cube_t == "solid":
                    continue
                if move_down:
                    self.canvas.move(cube_v.polygon_id, 0, self.cube_width)
                    cube_v.move(0, self.cube_width)
                    continue
                cube_vx, cube_vy = cube_v.xy
                if cube_vx == self.x:
                    line_cube = []
                    delete_start = edge_index
                    line_cube.append(cube_v)
                    continous = True
                    next_x = cube_vx + cube_v.width
                    next_y = cube_vy
                    continue
                if not continous:
                    continue
                if next_x != cube_vx or next_y != cube_vy:
                    continous = False
                    continue
                line_cube.append(cube_v)
                next_x = cube_vx + cube_v.width
                if next_x == self.x + self.width:
                    delete_end = edge_index
                    for cube_i in line_cube:
                        self.canvas.delete(cube_i.polygon_id)
                    move_down = True
                    loop = True
            if loop:
                del self.edges[delete_start:delete_end+1] 
                    
    def auto_down_cube(self):
        if self.down_cube_id:
            self.canvas.update()
            cube = self.down_cube.copy()
            cube.move(0, self.cube_width)
            if self.hit_test(cube):
                for cube_1 in self.down_cube.cubes:
                    self.edges.append((cube_1, ""))
                self.erase_lines()
                if self.check_end():
                    showinfo("Game Over", "Game Over")
                    self.start()
                    return
                else:
                    self.down_cube = self.get_random_cube()
                    self.down_cube_id = self.down_cube.draw(self.canvas)
            else:
                self.canvas.move(self.down_cube_id, 0, self.cube_width)
                self.down_cube.move(0, self.cube_width)
        self.canvas.after(self.speed, self.auto_down_cube)
                           
    def left_move_cube(self, event):
        if self.down_cube_id:
            cube = self.down_cube.copy()
            cube.move(-self.cube_width, 0)
            if not self.hit_test(cube):
                self.canvas.move(self.down_cube_id, -self.cube_width, 0)
                self.down_cube.move(-self.cube_width, 0)

    def right_move_cube(self, event):
         if self.down_cube_id:
            cube = self.down_cube.copy()
            cube.move(self.cube_width, 0)
            if not self.hit_test(cube):
                self.canvas.move(self.down_cube_id, self.cube_width, 0)
                self.down_cube.move(self.cube_width, 0)
            
    def down_move_cube(self, event):
        if self.down_cube_id:
            cube = self.down_cube.copy()
            cube.move(0, self.cube_width)
            if not self.hit_test(cube):
                self.canvas.move(self.down_cube_id, 0, self.cube_width)
                self.down_cube.move(0, self.cube_width)

    def rotate_cube(self, event):
        if self.down_cube_id:
            cube = self.down_cube.copy()
            cube.rotate()
            if not self.hit_test(cube):
                self.down_cube.rotate(self.canvas)
    
    def hit_test(self, cube):
        for cube in cube.cubes:
            for cube_v, cube_t in self.edges:
                if cube_v.hit_test(cube):
                    return True
        return False

    def check_end(self):
        for cube_v, cube_t in self.edges:
            if cube_t  != "solid":
                for x, y in cube_v._points:
                    if y == self.y:
                        return True
        return False
    
    def start(self):
        self.canvas.delete("all")
        self.draw_cubes()
        self.edges = [(cube_v, cube_t ) for cube_v, cube_t in self.edges if cube_t  == "solid"]
        self.down_cube = self.get_random_cube()
        self.down_cube_id = self.down_cube.draw(self.canvas)
        self.canvas.after(self.speed, self.auto_down_cube)

    def toogle(self):
        if self.down_cube_id or self.pause_down_cube_id:
            if not self.pause_down_cube_id:
                self.pause_down_cube_id = self.down_cube_id
                self.pause_down_cube = self.down_cube
                self.down_cube_id = None
                self.down_cube = None
            else:
                self.down_cube_id = self.pause_down_cube_id
                self.down_cube = self.pause_down_cube
                self.pause_down_cube_id = None
                self.pause_down_cube = None

root = Tk()
game_width =  600
game_height = 800
canvas = Canvas(root, width=game_width, height=game_height, borderwidth=0)
canvas.pack(padx=10, pady=10)
game = Game(canvas, 0, 0, game_width, game_height, 300)
root.bind("<Left>", game.left_move_cube)
root.bind("<Right>", game.right_move_cube)
root.bind("<Down>", game.down_move_cube)
root.bind("<Up>", game.rotate_cube)
root.bind("<KeyPress-p>", lambda event: game.toogle())
game.start()
mainloop()
