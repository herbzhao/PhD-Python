import numpy as np
CNC = (1.51, 1.59)
layer_parameters_set = {
            'n': [CNC,CNC,CNC], 
            'pitch': [300e-9,300e-9,300e-9], 
            'thickness': [600e-9,600e-9,600e-9], 
            'rotation': np.linspace(0,60,3)}

name_set = ['test1','test2','test3']

headings = (list(layer_parameters_set))
n_list = layer_parameters_set['n']
pitch_list = layer_parameters_set['pitch']
thickness_list = layer_parameters_set['thickness']
rotation_list = layer_parameters_set['rotation']

zipped_list = list(zip(n_list,pitch_list,thickness_list,rotation_list))
print(zipped_list)
parameters_set_collection = {}


for i in range(len(name_set)):
    parameters_set_collection[name_set[i]] = {}


for i in range(len(name_set)):
    print(i)
    parameters_set_collection[name_set[i]]['n'] = zipped_list[i][0]
    parameters_set_collection[name_set[i]]['pitch'] = zipped_list[i][1]
    parameters_set_collection[name_set[i]]['thickness'] = zipped_list[i][2]
    parameters_set_collection[name_set[i]]['rotation'] = zipped_list[i][3]

    #parameters_set_collection[name_set[i]] = zipped_list[i]

print(parameters_set_collection)
# output goal
#layer1_parameters_set['test1'] = {'n': CNC, 'pitch': 300e-9, 'thickness': 600e-9, 'rotation': 0}

#print(layer_parameters_set)


