import pandas as pd
import numpy as np
import datetime
import os
import random
import itertools
import json

# https://contrib.scikit-learn.org/categorical-encoding/index.html
import category_encoders as ce



def gen_sphere(x,y,z, radius):
    sphere = {'x': x, 'y': y, 'z': z, 'size': radius}
    return sphere

def distance(x0, y0, z0, x1, y1, z1):
    sqr_distance = (x0 - x1)**2 + (y0 - y1)**2 + (z0- z1)**2
    return sqr_distance**(1/2)
 
def check_boundary_condition(boundary_condition, x, y, z, radius):
    x = [x - radius, x + radius]
    y = [y - radius, y + radius]
    z = [z - radius, z + radius]
    # generate all possible combinations

    boundary_points = list(itertools.product(x, y, z))
    for point in boundary_points:
        if not boundary_condition(point[0], point[1], point[2]):
            return False
            
    return True

            
def gen_random_spheres(boundary_radius, number=50, radius=3, wall=0):
    spheres = []
    boundary_condition = lambda x,y,z: x**2 + y**2 + z**2 < boundary_radius**2
    
    for i in range(number):
        # check whether the x,y follows the boundary condition
        trial = 0
        while True:
            trial += 1
            x = np.random.uniform(-boundary_radius, boundary_radius)
            y = np.random.uniform(-boundary_radius, boundary_radius)
            z = np.random.uniform(-boundary_radius, boundary_radius)

            #print('produced x, y: {} {}'.format(x, y))
            if check_boundary_condition(boundary_condition, x, y, z, radius):
                #print('it is within the boundary')
                # check overlapping
                #print('checking overlapping')
                overlapping = False
                for old_sphere in spheres:
                    old_x = old_sphere['x']
                    old_y = old_sphere['y']
                    old_z = old_sphere['z']
            
                    # if there is a thin wall in between, dist will be distance + width
                    if distance(old_x, old_y, old_z, x, y, z) < (radius+wall)*2:
                        overlapping = True
                if not overlapping:
                    break
                    
            # force stop if the trial is too large, probably filled enough space
            if trial > 500:
                #print('cannot find space to fit in more circle')
                break
        if trial <= 500:
            spheres.append(gen_sphere(x, y, z, radius))
            
    return spheres


if __name__ == "__main__":
    boundary_radius = 10
    radius = 1
    wall = 0

    spheres = gen_random_spheres(boundary_radius=boundary_radius, number=500, radius=radius, wall=wall)
    x = [sphere['x'] for sphere in spheres]
    y = [sphere['y'] for sphere in spheres]
    z = [sphere['z'] for sphere in spheres]
    size = [sphere['size'] for sphere in spheres]
    with open("balls.json", "w") as json_file:
        json.dump(spheres, json_file)

    with open("balls.json", "r") as json_file:
        spheres = json.load(json_file)
    print(spheres)
    print(len(spheres))