#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 22:00:40 2020

@author: oyewunmi
"""
# importing packages
import GetOldTweets3 as got
import MySQLdb as sql

# connecting to the user profile that we want to read from
user1 = got.manager.TweetCriteria().setUsername('OweYoruba')
user2 = got.manager.TweetCriteria().setUsername('oweyorubadotnet')

# getting all the tweets fo user one and two
tweet_1 = got.manager.TweetManager.getTweets(user1)
tweet_2 = got.manager.TweetManager.getTweets(user2)
container, container2 = [],[]

for i in tweet_1:
   container.append(i.text)   
for j in tweet_2:
    container2.append(j.text)

# creating database object and connecting to it
db = sql.connect('localhost', 'root', 'claudia', 'OweYorubas')
cursor = db.cursor()

# dropping the table if it has been existing before and recreating it 
cursor.execute('drop table if exists proverbs')

# creating table
command='create table proverbs(proverbs char(150),translation char(255))'
cursor.execute(command)  

# inserting values into the database
# formatting and inserting the user1 values into the database
getter = []
for lines in container:
    lines = lines.split('. ')
    getter.append(lines)
    for line in getter:
        if len(line) > 1 and len(line) < 3:
            cursor.execute('insert into proverbs values (%s,%s)',(line[0],line[1])) 
        elif len(line) > 2 and len(line) < 3:
            cursor.execute('insert into proverbs values (%s,%s)',(line[0],line[1]+line[2])) 
        else:
            cursor.execute('insert into proverbs values (%s, %s)',(line[0], 'translation not provided'))
    db.commit()
# formatting and inserting the user2 values into the database
getter2 = []    
for lines in container2:
    lines = lines.split('/')
    getter2.append(lines)
    for line in getter2:
        if len(line) == 1:
            cursor.execute('insert into proverbs values (%s,%s)',(line[0],'translation not included')) 
        elif len(line) == 2:
            cursor.execute('insert into proverbs values (%s,%s)',(line[0], line[1]))
        elif len(line) > 2:
            cursor.execute('insert into proverbs values (%s,%s)',(line[0], 'translation not provided or error in format'))
    db.commit()
# there is an issue with the data as some are in different ways of writing...
# one would need to use regular expression to match their pattern...but this has been skipped by me
            
