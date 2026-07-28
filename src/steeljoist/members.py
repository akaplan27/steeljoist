from dataclasses import dataclass
from typing import Optional
from functools import cached_property
from math import nan, inf, pi, ceil, sin, cos, dist, sqrt, radians
from libdenavit.section import DoubleAngle, Angle
from sectionproperties.pre.library import angle_section
from shapely import Polygon
from sectionproperties.pre import Geometry
from sectionproperties.analysis import Section


# Testing for use of SectionProperties with Crimped Angle
# https://www.desmos.com/calculator/mxb7esj14w
# b = 1.25
# t = 1/8

# k = abs((0.375 * sqrt(2) * t) + (0.25 * sqrt(2) * b))

# polyL = Polygon([(0, k), 
#                 (b / sqrt(2), k - (b / sqrt(2))),
#                 ((b - t) / sqrt(2), k - ((b + t) / sqrt(2))),
#                 (0, k - (t * sqrt(2))), 
#                 ((t - b) / sqrt(2), k - ((b + t) / sqrt(2))),
#                 (-b / sqrt(2), k - (b / sqrt(2)))
#                 ])

# geom = Geometry(geom=polyL)
# geom.create_mesh(mesh_sizes=20)
# sec = Section(geometry=geom)
# sec.calculate_geometric_properties()
# sec.calculate_warping_properties()
# sec.calculate_plastic_properties()
# sec.display_results()



@dataclass(frozen=True)
class JoistRound:
    D: float
    A: Optional[float] = None

    def __post_init__(self):       
        if self.A is None:
            object.__setattr__(self, "A", pi/4*D**2)

    @property
    def r(self):
        return self.D/4

    def MASTAN2_sect_info(self):
        A = pi/4*self.D**2
        return [
            A,
            pi/64*self.D**4,        # Ix
            pi/64*self.D**4,        # Iy
            pi/32*self.D**4,        # J
            0,                      # Cw
            1/6*self.D**3,          # Zx
            1/6*self.D**3,          # Zy
            0.9*A,                  # Asy
            0.9*A,                  # Asz
            1, 1, 1, 1,
            0, 0, 0, 0, 0, 0, 0,
        ]

    def in_plane_depth(self):
        return self.D
        
    def slenderness(self,L):
        return L/self.r


    
'''
class JoistRound:
    def __init__(self, D):
        self.D = D

    def MASTAN2_sect_info(self):
        A = pi/4*self.D**2
        I = pi/64*self.D**4
        J = pi/32*self.D**4
        Cw = 0
        Z = 1/6*self.D**3
        As = 0.9*A
        return [A, I , I, J, Cw, Z, Z, As, As, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]        
    
    def in_plane_depth(self):
        return self.D

    def slenderness(self,L):
        return L/(self.D/4)
'''

@dataclass(frozen=True)
class JoistDoubleAngle:
    b: float
    t: float
    s: float
    number_of_fillers: Optional[int] = 0
    d: Optional[float] = None
    A: Optional[float] = None

    def __post_init__(self):
        if self.d is None:
            object.__setattr__(self, "d", self.b)
        
        obj = DoubleAngle(self.d, self.b, self.t, self.s)
        if self.A is None:
            object.__setattr__(self, "A", obj.A)

    @cached_property
    def _double_angle(self):
        return DoubleAngle(self.d, self.b, self.t, self.s)

    @property
    def y_bar(self):
        return self._double_angle.y_bar

    @property
    def Ix(self):
        return self._double_angle.Ix

    @property
    def rx(self):
        return self._double_angle.rx

    @property
    def ry(self):
        return self._double_angle.ry

    @property
    def rz_single(self):
        return Angle(self.d, self.b, self.t).rz

    def MASTAN2_sect_info(self):
        return [
            self._double_angle.A,
            self._double_angle.Ix,
            self._double_angle.Iy,
            self._double_angle.J,
            0,                      # Cw
            self._double_angle.Zx,
            self._double_angle.Zy,
            2 * self.d * self.t,    # Asy
            2 * self.b * self.t,    # Asz
            1, 1, 1, 1,
            0, 0, 0, 0, 0, 0, 0,
        ]

    def in_plane_depth(self):
        return self.b
        
    def slenderness(self,L):
        l_over_rx = L/self.rx
        l_over_ry = L/self.ry
        l_over_rz = L/(self.number_of_fillers+1)/self.rz_single
        return max(l_over_rx,l_over_ry,l_over_rz)
        
    def check_strength_at_panel_point(self,basis,P,M,Fy):
        fa = P/self.A
        fb = M*(self.b-self.y_bar)/self.Ix

        if basis == 'LRFD':
            f_limit = 0.9*Fy
        else:
            raise ValueError(f'Unknown basis: {basis}')

        print(f'Strength Evaluation at Panel Point:')
        print(f'  fa = {fa/psi:,.0f} psi')
        print(f'  fb = {fb/psi:,.0f} psi')
        if (fa+fb) <= f_limit:
            print(f'  PASS') 
        else:
            print(f'  FAIL')

'''
class JoistDoubleAngle:
    def __init__(self, b, t, s, d=None, A=None):       
        self.b = b
        self.t = t
        self.s = s
        if d is None:
            self.d = b
        else:
            self.d = d
        self._A = A

    def y_bar(self):
        obj = DoubleAngle(self.d, self.b, self.t, self.s)
        return obj.y_bar

    def area(self):
        if self._A is None:
            obj = DoubleAngle(self.d, self.b, self.t, self.s)
            return obj.A
        else:
            return self._A
        
    def Ix(self):
        obj = DoubleAngle(self.d, self.b, self.t, self.s)
        return obj.Ix   
        
    def rx(self):
        obj = DoubleAngle(self.d, self.b, self.t, self.s)
        return obj.rx    
        
    def ry(self):
        obj = DoubleAngle(self.d, self.b, self.t, self.s)
        return obj.ry     
        
    def rz_single(self):
        obj = Angle(self.d, self.b, self.t)
        return obj.rz
        
    def MASTAN2_sect_info(self):
        obj = DoubleAngle(self.d, self.b, self.t, self.s)
        A = obj.A
        Ix = obj.Ix
        Iy = obj.Iy
        J = obj.J
        Cw = 0
        Zx = obj.Zx
        Zy = obj.Zy
        Asy = 2 * obj.d * obj.t
        Asz = 2 * obj.b * obj.t
        return [A, Ix , Iy, J, Cw, Zx, Zy, Asy, Asz, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]

    def inPlaneDepth(self):
        return self.b
'''

class JoistCrimpedAngle:
    def __init__(self, b, t): 
        # Assume always equal leg angle
        self.b = b
        self.d = b
        self.t = t

    def MASTAN2_sect_info(self):
        obj = Angle(self.b, self.d, self.t)
        A = (obj.d + obj.b - obj.t)*obj.t
        Ixx = (obj.Ix + obj.Iy)/2 + obj.Ixy
        Iyy = (obj.Ix + obj.Iy)/2 - obj.Ixy
        J = obj.J
        Cw = 0
        Zx = 0.5
        Zy = 0.5 # @todo: crimped angle Zx and Zy
        # come up with equation for Zx and Zy then use sectionproperties to verify accuracy
        Asy = inf #inf A_sy
        Asz = inf # inf A_sx
        return [A, Ixx , Iyy, J, Cw, Zx, Zy, Asy, Asz, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]

    def in_plane_depth(self):
        return self.b * cos(45)

    def slenderness(self,L):
        return L/self.rz

    @property
    def A(self):
        obj = Angle(self.b, self.d, self.t)
        return obj.A  

    @property
    def rx(self):
        obj = Angle(self.b, self.d, self.t)
        return obj.rx 
        
    @property
    def ry(self):
        obj = Angle(self.b, self.d, self.t)
        return obj.ry         

    @property
    def rz(self):
        obj = Angle(self.b, self.d, self.t)
        return obj.rz    

class ColdFormedChannel:
    # https://www.desmos.com/calculator/9dkjawcosb
    def __init__(self, w, h, t, ri, n=10):
        self.w = w
        self.h = h
        self.t = t
        self.ri = ri
        self.ro = ri + t
        self.n = n

    def MASTAN2_sect_info(self):
        leftInner  = []
        leftOuter  = []
        rightInner = []
        rightOuter = []
        for a in range(self.n)[1:]:
            leftInner.append((-0.5 * self.w + self.t + self.ri * (1 - cos(radians(90 * a / self.n))), -self.h + self.ro - (self.ri * sin(radians(90 * a / self.n)))))
            rightInner.append((0.5 * self.w - self.t - self.ri * (1 - cos(radians(90 * (self.n-a) / self.n))), -self.h + self.ro - self.ri * sin(radians(90 * (self.n-a) / self.n))))
            rightOuter.append((0.5 * self.w - self.ro * (1 - cos(radians(90 * a / self.n))), -self.h + self.ro * (1 - sin(radians(90 * a / self.n)))))
            leftOuter.append((-0.5 * self.w + self.ro * (1 - cos(radians(90 * (self.n-a) / self.n))), -self.h + self.ro * (1-sin(radians(90 * (self.n-a) / self.n)))))

        polyU = Polygon([(-self.w / 2, 0),
                 (self.t - 0.5 * self.w, 0),
                 (self.t - 0.5 * self.w, self.ro - self.h)] +  
                 leftInner +
                 [(0.5 * self.w - self.ro, self.t - self.h)] +
                 rightInner +
                 [(0.5 * self.w - self.t, 0),
                 (0.5 * self.w, 0),
                 (0.5 * self.w, self.ro - self.h)] +
                 rightOuter +                
                 [(self.ro - 0.5 * self.w, -self.h)] +
                 leftOuter)
        geom = Geometry(geom=polyU)
        # geom.plot_geometry()
        geom.create_mesh(mesh_sizes=20)
        sec = Section(geometry=geom)
        sec.calculate_geometric_properties()
        sec.calculate_warping_properties()
        sec.calculate_plastic_properties()
        # sec.display_results()
        
        A = float(sec.get_area())
        Ixx = float(sec.get_ig()[0])
        Iyy = float(sec.get_ig()[1])
        J = float(sec.get_j())
        Cw = float(sec.get_gamma()) # gamma
        Zx = 0 # determine by calculating for crimped angle then comparing which is correct
        Zy = 0 # @todo: crimped angle Zx and Zy
        Asy = inf #inf
        Asz = inf # inf
        return [A, Ixx , Iyy, J, Cw, Zx, Zy, Asy, Asz, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]

    def in_plane_depth(self):
        return self.w # @todo: is this correct?

