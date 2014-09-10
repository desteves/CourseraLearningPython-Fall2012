http://www.codeskulptor.org/#user7-m7ef0Wz9rA-1.py
http://www.codeskulptor.org/#user7-m7ef0Wz9rA-#######.py  #######24
http://www.codeskulptor.org/#user7-G9vUfsC33JXfNe8.py

# program template for Spaceship

################################
# file: Spaceship.py
# author: DWE
# date: 05DEC2012
# brief: Mini-project #7
# link: http://www.codeskulptor.org/# 
################################
import simplegui
import math
import random

# globals for user interface
width = 800
height = 600
score = 0
lives = 3
time = 0

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0]-q[0])**2+(p[1]-q[1])**2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.c_const = .04 #friction    
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()        
        self.radius = info.get_radius()
        
    def draw(self,canvas):        
        #draws the ship as an image
        canvas.draw_image(self.image, self.image_center, self.image_size, 
                                      self.pos, self.image_size, self.angle)
        #wrap around effect
        #ship's position wraps to the other side of the screen when it crosses the edge of the screen
        self.pos[0] %=  width
        self.pos[1] %=  height
    def shoot(self):
        global a_missile
        fwd = angle_to_vector(self.angle) 
        #missile spawns at the tip of the ship's gun
        a_missile = Sprite([self.pos[0] + fwd[0]*self.radius,  
                            self.pos[1] + fwd[1]*self.radius],   
                           #The missile's velocity is the sum of the ship's velocity
                           #and a multiple of its forward vector.
                          [self.vel[0] + fwd[0]*3,  
                           self.vel[1] + fwd[1]*3],  
                           self.angle, 0, missile_image, missile_info, missile_sound)
        
    # Used to change the acceleration due to the user  
    def reset_vel(self):
        #self.vel = angle_to_vector(self.angle)	
        pass
    def set_key_thr(self, t):
        self.thrust = t           
    def set_key_vel(self, v):
        self.angle_vel = v        
    def update(self):        
        # ship's orientation is independent of its velocity
        self.angle += self.angle_vel
        # Updates the angle_vel using the acceleration.       
        #update position -- ship flies in a straight line when not under thrust        
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]    
        #update friction
        #ship's velocity slows to zero while the thrust is not being applied
        self.vel[0] *= (1 - self.c_const)
        self.vel[1] *= (1 - self.c_const)        
        if self.thrust: 
            # draws the ship with thrusters on when the up arrow is held down
            self.image_center[0] = self.image_size[0] + self.image_size[0]/2
            # plays the thrust sound only when the up arrow key is held down
            ship_thrust_sound.play()               
            #update velocity
            fwd = angle_to_vector(self.angle)
            # accelerates in its forward direction when the thrust key is held down
            self.vel[0] += fwd[0]
            self.vel[1] += fwd[1]
        else:
            self.image_center[0] = self.image_size[0]/2;
            ship_thrust_sound.pause()
# Sprite class
class Sprite:    
    def __init__(self,pos, vel, ang, ang_vel,image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()   #plays the missile firing sound when the missile is spawned
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, 
                                      self.pos, self.image_size, self.angle)
        #canvas.draw_circle(self.pos, self.radius, 1, "Red", "Red")    
    def update(self):        
        self.angle += self.angle_vel
        # Updates the angle_vel using the acceleration.       
        #update position
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]    
        
def draw(canvas):
    global time    
    # animiate background
    time += 1
    center = debris_info.get_center()
    size = debris_info.get_size()
    wtime = (time / 8) % center[0]
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [width/2, height/2], [width, height])
    canvas.draw_image(debris_image, [center[0]-wtime, center[1]], [size[0]-2*wtime, size[1]], 
                                [width/2+1.25*wtime, height/2], [width-2.5*wtime, height])
    canvas.draw_image(debris_image, [size[0]-wtime, center[1]], [2*wtime, size[1]], 
                                [1.25*wtime, height/2], [2.5*wtime, height])
    # draws appropriate text for lives on the upper left portion of the screen
    canvas.draw_text(str(lives), [50, 50], 30, "White")
    # draws appropriate text for score on the upper right portion of the screen
    canvas.draw_text(str(score), [width-50, 50], 30, "White")
    
    # draw ship and sprites    
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    a_missile.draw(canvas)    
    # update ship and sprites
    my_ship.update()
    a_rock.update()
    a_missile.update()

# timer handler that spawns a rock    
def rock_spawner():
    global a_rock 
    # randomly generated
    # rock travels in a straight line at a constant velocity.
    # rock is respawned once every second by a timer.
    # rock has a random spawn position, spin direction and velocity
    a_rock = Sprite([random.randrange(0, width),random.randrange(0, height)],
                    [random.random() * random.choice([-1, 1]) * 2 ,
                     random.random() * random.choice([-1, 1]) * 2], 
                     random.random() * random.choice([-1, 1]) * .1,
                     random.random() * random.choice([-1, 1]) * .1,
                    asteroid_image, asteroid_info)    
# initialize frame
frame = simplegui.create_frame("Asteroids", width, height)
# initialize ship and two sprites
my_ship = Ship([width / 2, height / 2], [0, 0], 0, ship_image, ship_info)
# randomly generated
a_rock = Sprite([random.randrange(0, width),random.randrange(0, height)],
                [random.random() * random.choice([-1, 1]) * 2 ,
                 random.random() * random.choice([-1, 1]) * 2], 
                 random.random() * random.choice([-1, 1]) * .1,
                 random.random() * random.choice([-1, 1]) * .1,
                 asteroid_image, asteroid_info)
a_missile = Sprite([0, 0], [-1,1], 0, 0, missile_image, missile_info, missile_sound)

# Sets the key_acc of the stick depending on 
#	the keys pressed.
def keydown_handler(key):
    vel = .02
    # counter clockwise direction when the left arrow key is held down
    if key == simplegui.KEY_MAP['left']:
        my_ship.set_key_vel(-vel)
    #  clockwise direction when the right arrow key is held down
    elif key == simplegui.KEY_MAP['right']:
        my_ship.set_key_vel(vel)
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_key_thr(True)  
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
        #my_ship.set_res_vel(0)
def keyup_handler(key):    
    my_ship.set_key_vel(0)
    my_ship.set_key_thr(False)    
    my_ship.reset_vel()
# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown_handler)
frame.set_keyup_handler(keyup_handler)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()

