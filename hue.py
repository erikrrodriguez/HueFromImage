from qhue import Bridge
from dev_settings import ip, key
import math
from collections import namedtuple

# Represents a CIE 1931 XY coordinate pair.
XYPoint = namedtuple('XYPoint', ['x', 'y'])

# LivingColors Iris, Bloom, Aura, LightStrips
GamutA = (
    XYPoint(0.704, 0.296),
    XYPoint(0.2151, 0.7106),
    XYPoint(0.138, 0.08),
)

# Hue A19 bulbs
GamutB = (
    XYPoint(0.675, 0.322),
    XYPoint(0.4091, 0.518),
    XYPoint(0.167, 0.04),
)

# Hue BR30, A19 (Gen 3), Hue Go, LightStrips plus
GamutC = (
    XYPoint(0.692, 0.308),
    XYPoint(0.17, 0.7),
    XYPoint(0.153, 0.048),
)


class HueLights():
    def __init__(self):
        self.b = Bridge(ip, key)

        self.Red = GamutB[0]
        self.Lime = GamutB[1]
        self.Blue = GamutB[2]

    def change_all_lights(self, circles, transtime):
        for i, circle in enumerate(circles):
            r, g, b, a = circle.color.getRgb()
            self.change_light_xy(bulb=i+1, r=r/255, g=g/255, b=b/255, transitiontime=transtime)

    def change_light_xy(self, bulb, r, g, b, transitiontime):
        x, y = self.rgb_to_xy(r, g, b)
        self.b.lights[bulb].state(xy=[x,y], transitiontime=transitiontime)

    def rgb_to_xy(self, red, green, blue):
        r = ((red + 0.055) / (1.0 + 0.055))**2.4 if (red > 0.04045) else (red / 12.92)
        g = ((green + 0.055) / (1.0 + 0.055))**2.4 if (green > 0.04045) else (green / 12.92)
        b = ((blue + 0.055) / (1.0 + 0.055))**2.4 if (blue > 0.04045) else (blue / 12.92)

        X = r * 0.664511 + g * 0.154324 + b * 0.162028
        Y = r * 0.283881 + g * 0.668433 + b * 0.047685
        Z = r * 0.000088 + g * 0.072310 + b * 0.986039

        if (X+Y+Z) == 0:
            cx = 0
            cy = 0
        else:
            cx = X / (X + Y + Z)
            cy = Y / (X + Y + Z)

        # Check if the given XY value is within the colourreach of our lamps.
        xy_point = XYPoint(cx, cy)
        in_reach = self.check_point_in_lamps_reach(xy_point)

        if not in_reach:
            xy_point = self.get_closest_point_to_point(xy_point)

        return xy_point

    def check_point_in_lamps_reach(self, p):
        """Check if the provided XYPoint can be recreated by a Hue lamp."""
        v1 = XYPoint(self.Lime.x - self.Red.x, self.Lime.y - self.Red.y)
        v2 = XYPoint(self.Blue.x - self.Red.x, self.Blue.y - self.Red.y)

        q = XYPoint(p.x - self.Red.x, p.y - self.Red.y)
        s = self.cross_product(q, v2) / self.cross_product(v1, v2)
        t = self.cross_product(v1, q) / self.cross_product(v1, v2)

        return (s >= 0.0) and (t >= 0.0) and (s + t <= 1.0)

    def get_closest_point_to_line(self, A, B, P):
        """Find the closest point on a line. This point will be reproducible by a Hue lamp."""
        AP = XYPoint(P.x - A.x, P.y - A.y)
        AB = XYPoint(B.x - A.x, B.y - A.y)
        ab2 = AB.x * AB.x + AB.y * AB.y
        ap_ab = AP.x * AB.x + AP.y * AB.y
        t = ap_ab / ab2

        if t < 0.0:
            t = 0.0
        elif t > 1.0:
            t = 1.0

        return XYPoint(A.x + AB.x * t, A.y + AB.y * t)

    def get_closest_point_to_point(self, xy_point):
        # Color is unreproducible, find the closest point on each line in the CIE 1931 'triangle'.
        pAB = self.get_closest_point_to_line(self.Red, self.Lime, xy_point)
        pAC = self.get_closest_point_to_line(self.Blue, self.Red, xy_point)
        pBC = self.get_closest_point_to_line(self.Lime, self.Blue, xy_point)

        # Get the distances per point and see which point is closer to our Point.
        dAB = self.get_distance_between_two_points(xy_point, pAB)
        dAC = self.get_distance_between_two_points(xy_point, pAC)
        dBC = self.get_distance_between_two_points(xy_point, pBC)

        lowest = dAB
        closest_point = pAB

        if (dAC < lowest):
            lowest = dAC
            closest_point = pAC

        if (dBC < lowest):
            lowest = dBC
            closest_point = pBC

        # Change the xy value to a value which is within the reach of the lamp.
        cx = closest_point.x
        cy = closest_point.y

        return XYPoint(cx, cy)

    def get_distance_between_two_points(self, one, two):
        """Returns the distance between two XYPoints."""
        dx = one.x - two.x
        dy = one.y - two.y
        return math.sqrt(dx * dx + dy * dy)

    def cross_product(self, p1, p2):
        """Returns the cross product of two XYPoints."""
        return (p1.x * p2.y - p1.y * p2.x)