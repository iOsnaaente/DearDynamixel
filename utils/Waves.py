
import dearpygui.dearpygui as dpg 
import math

from urllib3 import Retry


class Wave: 
    x         : list = [] 
    length    : int  = 0 

    def __init__(self, length : int = 100, amplitude : float = 180.0, period : float = 1.0, omega : float = 90, offset : float = 180, no_set_x : bool = False ) -> None:
        self.A  = amplitude
        self.T  = period 
        self.L  = length
        self.O  = omega 
        self.A0 = offset 
        if not no_set_x: 
            for i in range( length  ): 
                self.append_x( i )

    @property 
    def frequency(self):
        return 1/self.T if self.T != 0 else 0
    
    @property
    def W(self):
        return 2*math.pi*self.frequency 
    
    @property
    def y_sin(self):
        if self.x: 
            return [ self.A0 + self.A*math.sin( self.W * t + self.O ) for t in self.x ] 
        else: 
            return [] 

    @property
    def y_cos(self):
        if self.x:
            return [ self.A0 + self.A*math.cos( self.W * t + self.O ) for t in self.x ]
        else: 
            return [] 

    @property
    def first_x(self):
        if self.x: 
            return self.x[0]
        else: 
            return 0

    @property
    def last_x(self):
        if self.x:
            return self.x[-1]
        else: 
            return 0 

    @property
    def last_y( self ):
        return self.y_sin()[-1]

    def set_period( self, period ): 
        self.T = period 

    def set_amplitude(self, amplitude):
        self.A = amplitude

    def append_x(self, val ): 
        self.x.append( val )
        while len(self.x) > self.L:
            self.x.pop(0)

if __name__ == '__main__': 
    sin = Wave( 360, 180, 10, 90, 180 )