# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 22:38:49 2016

@author: herbz
"""

import random

capitals = {'Alabama': 'Montgomery', 'Alaska': 'Juneau', 'Arizona': 'Phoenix',
   'Arkansas': 'Little Rock', 'California': 'Sacramento', 'Colorado': 'Denver',
   'Connecticut': 'Hartford', 'Delaware': 'Dover', 'Florida': 'Tallahassee',
   'Georgia': 'Atlanta', 'Hawaii': 'Honolulu', 'Idaho': 'Boise', 'Illinois':
   'Springfield', 'Indiana': 'Indianapolis', 'Iowa': 'Des Moines', 'Kansas':
   'Topeka', 'Kentucky': 'Frankfort', 'Louisiana': 'Baton Rouge', 'Maine':
   'Augusta', 'Maryland': 'Annapolis', 'Massachusetts': 'Boston', 'Michigan':
   'Lansing', 'Minnesota': 'Saint Paul', 'Mississippi': 'Jackson', 'Missouri':
   'Jefferson City', 'Montana': 'Helena', 'Nebraska': 'Lincoln', 'Nevada':
   'Carson City', 'New Hampshire': 'Concord', 'New Jersey': 'Trenton', 'New Mexico': 'Santa Fe', 'New York': 'Albany', 'North Carolina': 'Raleigh',
   'North Dakota': 'Bismarck', 'Ohio': 'Columbus', 'Oklahoma': 'Oklahoma City',
   'Oregon': 'Salem', 'Pennsylvania': 'Harrisburg', 'Rhode Island': 'Providence',
   'South Carolina': 'Columbia', 'South Dakota': 'Pierre', 'Tennessee':
   'Nashville', 'Texas': 'Austin', 'Utah': 'Salt Lake City', 'Vermont':
   'Montpelier', 'Virginia': 'Richmond', 'Washington': 'Olympia', 'West Virginia': 'Charleston', 'Wisconsin': 'Madison', 'Wyoming': 'Cheyenne'}


capital_list = []
#assign the key-answer pair in list to give it an order
for state, city in capitals.items():
    capital_list.append((state,city))



def generate_questions():
    question, choices, answer= [],[],[]
    k = random.randint(0,36)
    x =[0,1,2,3]
    random.shuffle(x)
    question = capital_list[k][0]
    answer = capital_list[k][1]

    
    
    choices = '{'+str(x[0])+r'}   '+'{'+str(x[1])+'}   '+'{'+str(x[2])+'}   '+'{'+str(x[3])+'}'
    choices = choices.format(capital_list[random.randint(0,36)][1], capital_list[random.randint(0,36)][1], capital_list[random.randint(0,36)][1], capital_list[k][1])
    return question, answer, choices

    
    
# create questions and answers
for quiz_num in range(35):
    quiz_file = open('capitalsquiz{}.txt'.format(quiz_num + 1), 'w+')
    answer_file = open('capitalsquiz_answers{}.txt'.format(quiz_num + 1), 'w+')

# Write out the header for the quiz.
    quiz_file.write('welcome to test, number{} friend \n'.format(quiz_num+1))
    answer_file.write('the answers for number{} friend \n'.format(quiz_num+1))
    for question_num in range(10):
        question, answer, choices = generate_questions()
        quiz_file.write('Q{}   '.format(question_num)+ str(question)+'\n'+str(choices)+'\n')
        answer_file.write(str(question_num) + '.'+ str(answer) + '\n')
    
# TODO: Shuffle the order of the states.
    

    quiz_file.close()
    answer_file.close()
    
# TODO: Loop through all 50 states, making a question for each.



   