import math
import tkinter as tk
from tkinter import *
from pynput import keyboard

x_speed=0
y_speed=0
z_speed=0
camera_xrs=0
camera_yrs=0
w_pressed=False
s_pressed=False
d_pressed=False
a_pressed=False

def on_press(key):
    global y_speed
    global camera_xrs
    global camera_yrs
    global w_pressed
    global s_pressed
    global d_pressed
    global a_pressed
    try:
        if key.char=='w':
         w_pressed=True
        elif key.char=='s':
         s_pressed=True
        elif key.char=='d':
         d_pressed=True
        elif key.char=='a':
         a_pressed=True
        elif key.char=='e':
         y_speed=0.05
        elif key.char=='q':
         y_speed=-0.05
        elif key.char=='l':
         camera_xrs=0.05
        elif key.char=='j':
         camera_xrs=-0.05
        elif key.char=='i':
         camera_yrs=-0.05
        elif key.char=='k':
         camera_yrs=0.05
    except AttributeError:
        pass

def on_release(key):
    global y_speed
    global camera_xrs
    global camera_yrs
    global w_pressed
    global s_pressed
    global d_pressed
    global a_pressed
    try:
        if key.char=='w':
         w_pressed=False
        elif key.char=='s':
         s_pressed=False
        elif key.char=='d':
         d_pressed=False
        elif key.char=='a':
         a_pressed=False
        elif key.char=='e':
         y_speed=0
        elif key.char=='q':
         y_speed=0
        elif key.char=='l':
         camera_xrs=0
        elif key.char=='j':
         camera_xrs=0
        elif key.char=='i':
         camera_yrs=0
        elif key.char=='k':
         camera_yrs=0
    except AttributeError:
        pass

    
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)

polygons=[]
rendered_polys=[]

screen_y=768
screen_x=720

camera_fovy=1
camera_fovx=screen_x/screen_y*camera_fovy
camera_x=0
camera_y=0
camera_z=1
camera_xrotation=0
camera_yrotation=0

class polygon():
 def __init__(self, points):
  self.points=points
  global polygons
  polygons.append(self)
 def rotatey(self,x2,z2,deg):
  for i in range(3):
   if x2==self.points[i][0]:
    if z2>self.points[i][2]:
     self.points[i][0]=math.cos(-math.pi/2+deg)*(z2-self.points[i][2])+x2
     self.points[i][2]=math.sin(-math.pi/2+deg)*(z2-self.points[i][2])+z2
    elif z2<self.points[i][2]:
     self.points[i][0]=math.cos(math.pi/2+deg)*(z2-self.points[i][2])+x2
     self.points[i][2]=math.sin(math.pi/2+deg)*(z2-self.points[i][2])+z2
   else:
    length=((x2-self.points[i][0])**2+(z2-self.points[i][2])**2)**0.5
    angle=math.atan((z2-self.points[i][2])/(x2-self.points[i][0]))
    if x2>self.points[i][0]:
     self.points[i][0]=math.cos(angle+math.pi+deg)*length+x2
     self.points[i][2]=math.sin(angle+math.pi+deg)*length+z2
    elif x2<self.points[i][0]:
     self.points[i][0]=math.cos(angle+deg)*length+x2
     self.points[i][2]=math.sin(angle+deg)*length+z2
     
 def rotatez(self,y2,x2,deg):
  for i in range(3):
   if y2==self.points[i][1]:
    if x2>self.points[i][0]:
     self.points[i][1]=math.cos(-math.pi/2+deg)*(x2-self.points[i][0])+y2
     self.points[i][0]=math.sin(-math.pi/2+deg)*(x2-self.points[i][0])+x2
    elif x2<self.points[i][2]:
     self.points[i][1]=math.cos(math.pi/2+deg)*(x2-self.points[i][0])+y2
     self.points[i][0]=math.sin(math.pi/2+deg)*(x2-self.points[i][0])+x2
   else:
    length=((y2-self.points[i][1])**2+(x2-self.points[i][0])**2)**0.5
    angle=math.atan((x2-self.points[i][0])/(y2-self.points[i][1]))
    if y2>self.points[i][1]:
     self.points[i][1]=math.cos(angle+math.pi+deg)*length+y2
     self.points[i][0]=math.sin(angle+math.pi+deg)*length+x2
    elif y2<self.points[i][1]:
     self.points[i][1]=math.cos(angle+deg)*length+y2
     self.points[i][0]=math.sin(angle+deg)*length+x2

 def rotatex(self,z2,y2,deg):
  for i in range(3):
   if z2==self.points[i][2]:
    if y2>self.points[i][1]:
     self.points[i][2]=math.cos(-math.pi/2+deg)*(y2-self.points[i][1])+z2
     self.points[i][1]=math.sin(-math.pi/2+deg)*(y2-self.points[i][1])+y2
    elif y2<self.points[i][1]:
     self.points[i][2]=math.cos(math.pi/2+deg)*(y2-self.points[i][1])+z2
     self.points[i][1]=math.sin(math.pi/2+deg)*(y2-self.points[i][1])+y2
   else:
    length=((z2-self.points[i][2])**2+(y2-self.points[i][1])**2)**0.5
    angle=math.atan((y2-self.points[i][1])/(z2-self.points[i][2]))
    if z2>self.points[i][2]:
     self.points[i][2]=math.cos(angle+math.pi+deg)*length+z2
     self.points[i][1]=math.sin(angle+math.pi+deg)*length+y2
    elif z2<self.points[i][2]:
     self.points[i][2]=math.cos(angle+deg)*length+z2
     self.points[i][1]=math.sin(angle+deg)*length+y2
     
 def render(self):
  global camera_xrotation
  global camera_yrotation
  global camera_fovx
  global camera_fovy
  global camera_x
  global camera_y
  global camera_z
  global screen_x
  global screen_y
  var=0
  x_angles=[]
  y_angles=[]
  for i in range(3):
   if camera_x==self.points[i][0]:
    if camera_z>self.points[i][2]:
     x=math.cos(-math.pi/2+camera_xrotation)*(camera_z-self.points[i][2])+camera_x
     z=math.sin(-math.pi/2+camera_xrotation)*(camera_z-self.points[i][2])+camera_z
    elif camera_z<self.points[i][2]:
     x=math.cos(math.pi/2+camera_xrotation)*(camera_z-self.points[i][2])+camera_x
     z=math.sin(math.pi/2+camera_xrotation)*(camera_z-self.points[i][2])+camera_z
   else:
    length=((camera_x-self.points[i][0])**2+(camera_z-self.points[i][2])**2)**0.5
    angle=math.atan((camera_z-self.points[i][2])/(camera_x-self.points[i][0]))
    if camera_x>self.points[i][0]:
     x=math.cos(angle+math.pi+camera_xrotation)*length+camera_x
     z=math.sin(angle+math.pi+camera_xrotation)*length+camera_z
    elif camera_x<self.points[i][0]:
     x=math.cos(angle+camera_xrotation)*length+camera_x
     z=math.sin(angle+camera_xrotation)*length+camera_z
    
   if camera_z==z:
    if camera_y>self.points[i][1]:
     self.z=math.cos(-math.pi/2+camera_yrotation)*(camera_y-self.points[i][1])+camera_z
     self.y=math.sin(-math.pi/2+camera_yrotation)*(camera_y-self.points[i][1])+camera_y
    elif camera_y<self.points[i][1]:
     z=math.cos(math.pi/2+camera_yrotation)*(camera_y-self.points[i][1])+camera_z
     y=math.sin(math.pi/2+camera_yrotation)*(camera_y-self.points[i][1])+camera_y
   else:
    length=((camera_z-z)**2+(camera_y-self.points[i][1])**2)**0.5
    angle=math.atan((camera_y-self.points[i][1])/(camera_z-z))
    if camera_z>z:
     z=math.cos(angle+math.pi+camera_yrotation)*length+camera_z
     y=math.sin(angle+math.pi+camera_yrotation)*length+camera_y
    elif camera_z<z:
     z=math.cos(angle+camera_yrotation)*length+camera_z
     y=math.sin(angle+camera_yrotation)*length+camera_y
   
   distance_y=((z-camera_z)**2+(y-camera_y)**2)**0.5
   distance_x=((z-camera_z)**2+(x-camera_x)**2)**0.5
   if distance_y==0:
    y_angles.append(0)
   if distance_x==0:
    x_angles.append(0)

   y_angles.append(math.asin((y-camera_y)/distance_y))
   x_angles.append(math.asin((x-camera_x)/distance_x))
   if z<camera_z:
    x_angles[i]+=math.pi
   if x_angles[i]>camera_fovx or x_angles[i]<-camera_fovx or y_angles[i]>camera_fovy or y_angles[i]<-camera_fovy:
    var=1
    break
   

  if var==0:
   x1=math.tan(x_angles[0])/(2*math.tan(camera_fovx))*screen_x+screen_x/2
   y1=1-(math.tan(y_angles[0])/(2*math.tan(camera_fovy)))*screen_y+screen_y/2
   x2=math.tan(x_angles[1])/(2*math.tan(camera_fovx))*screen_x+screen_x/2
   y2=1-(math.tan(y_angles[1])/(2*math.tan(camera_fovy)))*screen_y+screen_y/2
   x3=math.tan(x_angles[2])/(2*math.tan(camera_fovx))*screen_x+screen_x/2
   y3=1-(math.tan(y_angles[2])/(2*math.tan(camera_fovy)))*screen_y+screen_y/2
   tk.canvas.create_line(x1,y1,x2,y2)
   tk.canvas.create_line(x2,y2,x3,y3)
   tk.canvas.create_line(x3,y3,x1,y1)

def forward():
 global z_speed
 z_speed=0.01

def forward_released():
 global z_speed
 z_speed=0

def back():
 global z_speed
 z_speed=-0.01

def back_released():
 global z_speed
 z_speed=0

def right():
 global x_speed
 x_speed=0.01

def right_released():
 global x_speed
 x_speed=0

def left():
 global x_speed
 x_speed=-0.01

def left_released():
 global x_speed
 x_speed=0

window=tk.Tk()
window.geometry("768x720")
window.title('Thomas')
tk.canvas = Canvas(window, height=768, width=720)
tk.canvas.pack(fill=BOTH)
tk.canvas.create_line(0, 0, 300, 300)

triangle1=polygon([[-1,1,4],[-1,1,2],[1,1,2]])
triangle2=polygon([[-1,1,4],[1,1,4],[1,1,2]])
triangle3=polygon([[-1,1,4],[-1,1,2],[-1,-1,4]])
triangle4=polygon([[-1,1,2],[-1,-1,4],[-1,-1,2]])
triangle5=polygon([[-1,1,2],[1,1,2],[-1,-1,2]])
triangle6=polygon([[-1,-1,2],[1,-1,2],[1,1,2]])
triangle7=polygon([[1,1,2],[1,-1,2],[1,-1,4]])
triangle8=polygon([[1,1,2],[1,1,4],[1,-1,4]])
triangle9=polygon([[-1,1,4],[1,1,4],[-1,-1,4]])
triangle10=polygon([[-1,-1,4],[1,-1,4],[1,1,4]])
triangle11=polygon([[-1,-1,4],[1,-1,4],[-1,-1,2]])
triangle12=polygon([[-1,-1,2],[1,-1,2],[1,-1,4]])

listener.start()
while True:
 if w_pressed==True:
         camera_z+=math.cos(camera_xrotation)*0.05
         camera_x+=math.sin(camera_xrotation)*0.05
 if s_pressed==True:
         camera_z+=math.cos(camera_xrotation)*-0.05
         camera_x+=math.sin(camera_xrotation)*-0.05
 if d_pressed==True:
         camera_x+=math.sin(camera_xrotation+math.pi/2)*0.05
         camera_z+=math.cos(camera_xrotation+math.pi/2)*0.05
 if a_pressed==True:
         camera_x+=math.sin(camera_xrotation+math.pi/2)*-0.05
         camera_z+=math.cos(camera_xrotation+math.pi/2)*-0.05
 camera_y+=y_speed
 camera_xrotation+=camera_xrs
 camera_yrotation+=camera_yrs
 if camera_yrotation>math.pi/2:
  camera_yrotation=math.pi/2
 if camera_yrotation<-math.pi/2:
  camera_yrotation=-math.pi/2
 if camera_xrotation>2*math.pi:
  camera_xrotation-=2*math.pi
 if camera_xrotation<0:
  camera_xrotation+=2*math.pi
 triangle1.rotatey(0,3,math.pi/500)
 triangle1.render()
 triangle2.rotatey(0,3,math.pi/500)
 triangle2.render()
 triangle3.rotatey(0,3,math.pi/500)
 triangle3.render()
 triangle4.rotatey(0,3,math.pi/500)
 triangle4.render()
 triangle5.rotatey(0,3,math.pi/500)
 triangle5.render()
 triangle6.rotatey(0,3,math.pi/500)
 triangle6.render()
 triangle7.rotatey(0,3,math.pi/500)
 triangle7.render()
 triangle8.rotatey(0,3,math.pi/500)
 triangle8.render()
 triangle9.rotatey(0,3,math.pi/500)
 triangle9.render()
 triangle10.rotatey(0,3,math.pi/500)
 triangle10.render()
 triangle11.rotatey(0,3,math.pi/500)
 triangle11.render()
 triangle12.rotatey(0,3,math.pi/500)
 triangle12.render()
 window.update()
 tk.canvas.delete('all')