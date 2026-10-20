"""Conditional 3-point pupil arc inverse; feature-level only."""
import math

def circle_radius(a,s):
    if not a>0 or not 0<s<=a: raise ValueError("minor circular arc required")
    return (a*a+s*s)/(2*s)

def radius_interval(a,observed_s,epsilon):
    if a<=0 or epsilon<0: raise ValueError("invalid input")
    lo=max(0.0,observed_s-epsilon)
    hi=min(a,observed_s+epsilon)
    if hi<=0 or lo>hi: return None
    return circle_radius(a,hi), math.inf if lo<=0 else circle_radius(a,lo)

def arc_geometry(radius,span_deg):
    if radius<=0 or not 0<span_deg<=180: raise ValueError("invalid arc")
    angle=math.radians(span_deg/2)
    return radius*math.sin(angle),radius*(1-math.cos(angle))

def finite_identifiability_angle(radius,epsilon):
    if not 0<epsilon<radius: raise ValueError("invalid inputs")
    return 2*math.degrees(math.acos(1-epsilon/radius))

def relative_upper_error_angle(radius,epsilon,tolerance):
    if not(radius>0 and 0<epsilon<radius and tolerance>0):
        raise ValueError("invalid inputs")
    c=(tolerance*radius**2-tolerance*radius*epsilon-epsilon**2/2)/(tolerance*radius**2+radius*epsilon)
    if c<0: return None
    return 2*math.degrees(math.acos(min(1,max(-1,c))))

def pupil_iris_interval(a,observed_s,epsilon,iris_radius,m_min,m_max):
    if not(iris_radius>0 and 0<m_min<=m_max): raise ValueError("invalid optics")
    b=radius_interval(a,observed_s,epsilon)
    return None if b is None else (b[0]/(m_max*iris_radius),b[1]/(m_min*iris_radius))

def certify_increase(before,after):
    return after[0]>before[1]
