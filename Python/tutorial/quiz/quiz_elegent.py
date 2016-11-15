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
   'South Carolina': 'Columbia', 'South Dakota': 'Pierre', 'Tennessee': 'Nashville', 'Texas': 'Austin', 'Utah': 'Salt Lake City', 'Vermont':
   'Montpelier', 'Virginia': 'Richmond', 'Washington': 'Olympia', 'West Virginia': 'Charleston', 'Wisconsin': 'Madison', 'Wyoming': 'Cheyenne'}



#assign the key-answer pair in list to give it an order


# a function to generate a set of 30 questions at a time
def generate_choices():
    question = []
    answer = []
    choices = []
    for question_num in range(50):
        # generate random states list
        states = list(capitals.keys())
        random.shuffle(states)
        # generate 1 Q
        question.append(states[question_num])
        # find the right answer
        answer.append(capitals[question[question_num]])
        # list all the potential answers
        wrong_answers = list(capitals.values())
        # remove the correct one
        del wrong_answers[wrong_answers.index(answer[question_num])]
        wrong_answers = random.sample(wrong_answers,3)
        choices.append(wrong_answers + [answer[question_num]])  # convert string in to a list
        random.shuffle(choices[question_num])
        
    return question, answer, choices
        

    
# create questions and answers
for quiz_num in range(35):
    quiz_file = open('capitalsquiz{}.txt'.format(quiz_num + 1), 'w+')
    answer_file = open('capitalsquiz_answers{}.txt'.format(quiz_num + 1), 'w+')

# Write out the header for the quiz.
    quiz_file.write('welcome to test, number{} friend \n'.format(quiz_num+1))
    answer_file.write('the answers for number{} friend \n'.format(quiz_num+1))
    #write down Q and A in 2 files
    question, answer, choices = generate_choices()
    for question_num in range(50):
        quiz_file.write('Q{} the capital of {} is ? \n'.format(question_num+1, question[question_num]))
        for i in range(4):
            quiz_file.write('{} {}\n'.format('ABCD'[i],choices[question_num][i]))
            
        right_choice = choices[question_num].index(answer[question_num])
        answer_file.write('{} {} {} \n'.format(question_num+1,'ABCD'[right_choice], answer[question_num]))

# 
quiz_file.close()
answer_file.close()
    
    
    

   