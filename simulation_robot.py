import pyglet
from pyglet.window import key
import random

window = pyglet.window.Window()
def draw_background():
    pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON, ('v2f', (0,0, 640,0, 640, 480, 0, 480)),  ('c3B', (179, 213, 193, 147, 213, 201, 165, 226, 183, 194, 236, 183)) )

def draw_obstacles():
    pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON, ('v2f', (100,100, 150,100, 150,150, 100,150)),  ('c3B', (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)) )

    
@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.SPACE:
        print('Starting a thing') # Space bar
    
@window.event
def on_draw():
    window.clear()
    draw_background()
    draw_obstacles()
    
pyglet.app.run()
    
