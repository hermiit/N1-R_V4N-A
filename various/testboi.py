# Modules
import time
import math

# Variables
sin = math.sin
pi = math.pi

frm = 1/60
frm2 = 1/30

# Functions
def UV(alpha=0.5):
   return sin((pi/2)*alpha)

for i in range(0,10):
   newi = i/10
   print(UV(newi))