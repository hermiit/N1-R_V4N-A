# uhhhh
import math

class Vector2:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def mag(self):
        hyp = math.sqrt(pow(self.x,2) + pow(self.y,2))
        return hyp

    def rem(self,ovec):
        sdif = Vector2(self.x - ovec.x, self.y - ovec.y)
        return sdif

    def scal(self,alp):
        scalvec = Vector2(self.x*alp, self.y*alp)
        return scalvec

    def components(self):
        print("(%.3f,%.3f)" % (self.x,self.y))
