# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 11:06:00 2018

@author: tpkl2
"""

import numpy as np

def dict2parameterset(name_set,dictionary):
    """
    INPUT:
    takes a dictionary with structure {'key': [entry1,entry2,entry3,...]}
    and a name_set with structure ['name1','name2','name3',...]
    OUTPUT:
    transforms them into the required nested format for simulation parameters
    {'name1': {'key': entry1}, 'name2': {'key': entry2}, ...}
    """
    key_set,entry_superset = dict_transpose(dictionary)
    parameters_set = make_nested_dict(name_set,key_set,entry_superset)
    return parameters_set


def dict_transpose(dictionary):
    """
    takes a dictionary with structure {'key': entry_set_by_key}
    where entry_set_by_key is a list of entries associated with a single key
    and splits it into a key_set and entry_superset
    (a name_set need not be provided)
    """
    
    key_set = []
    entry_superset_by_key = []
    # go through the dictionary
    for key, entry_set_by_key in dictionary.items():
        # fill key_set (list) with keys (elements)
        key_set.append(key)        
        # fill entry_superset_by_key (2D list) with entry_set_by_key (rows)
        entry_superset_by_key.append(entry_set_by_key)
    
    entry_superset = np.transpose(entry_superset_by_key)
    
    return key_set,entry_superset


def make_nested_dict(name_set,key_set,entry_superset):
    """
    make a nested dictionary with structure {'name': dictionary}
    where the top level is referenced by names from name_set
    and each name is associated with a dictionary {'key': entry_set_by_name}
    
    entry_superset is sliced into entry_sets and passed to make_dict
    
    each name in name_set corresponds to an entry_set_by_name
    each key in key_set has a corresponding entry in each entry_set_by_name
    """
    
    entry_superset_array = np.asarray(entry_superset)
    assert entry_superset_array.shape[0] == len(name_set)
    assert entry_superset_array.shape[1] == len(key_set)
    
    dictionary_set = []
    # slice entry_superset to get an entry_set
    for entry_set_by_name in entry_superset:
        # make a dictionary from key_set and entry_set
        new_dict = make_dict(key_set,entry_set_by_name)
        # construct a dictionary_set
        dictionary_set.append(new_dict)
    
    # make nested dictionary
    nested_dict = make_dict(name_set,dictionary_set)
    
    return nested_dict


def make_dict(key_set,entry_set):
    """
    make a dictionary {'key': entry}
    where each entry from entry_set
    is assigned to a key from key_set
    """
    
    assert len(key_set) == len(entry_set)
    
    new_dict = {}
    for idx,key in enumerate(key_set):
        new_dict[key] = entry_set[idx]
    
    return new_dict


CNC = (1.51, 1.59)

npoints = 4
x_list = np.linspace(0e-9,1000e-9,npoints)
# sine_list = np.sin(x_list/200e-9 * 2*np.pi)

name_set = [('test'+str(n)) for n in range(npoints)]
layer1_dictionary = {'n': [CNC] * npoints,
                     'pitch': [185e-9] * npoints,
                     'thickness': 1000e-9 - x_list,
                     'rotation': 2*np.pi/100e-9 * x_list}
layer2_dictionary = {'n': [CNC] * npoints,
                     'pitch': [185e-9] * npoints,
                     'thickness': x_list,
                     'rotation': 2*np.pi/100e-9 * x_list}
interface_parameters_set = None
layer1_parameters_set = dict2parameterset(name_set,layer1_dictionary)
layer2_parameters_set = dict2parameterset(name_set,layer2_dictionary)

print(layer1_parameters_set)
print()
print(layer2_parameters_set)