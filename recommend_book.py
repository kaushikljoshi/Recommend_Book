# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 22:43:28 2019

@author: kaushik Joshi

"""
import sys
import operator
import utility_functions

class Book:
    def __init__(self,book_data):
        self.isbn = book_data[0]
        self.title = book_data[1]
        self.author = book_data[2]

class User:
    
    def __init__(self):
        self.value_flag = 0
        self.book_data = {}
        self.book_list = []
        self.ratings_list = []
    
    def set_values(self,user_data):
        self.id = int(user_data[0])
        self.location = user_data[1]
        self.value_flag = 1
        if (len(user_data) > 2):
            self.age = int(user_data[2])
        else:
            self.age = -1

class Recommend:
  
    def __init__(self,user_name,num):
        self.item_name = user_name
        self.num_neighbors = num
        self.user_list = []
        self.items = {}
        self.book_list = []
        self.descriptors = {}
        self.user_ids = []
        self.nearest_list = {}
    
    def read_user_data(self,filename):
        nlines = 0
        data_lines = []
        with open(filename,'r') as file:
            for line in file:
                data_lines.append(line)
                nlines = nlines + 1
                #print ('%s %s'%(nlines,line))
                if (nlines > 1):
                    data = line.split(';')                
                    size = len(data)
                    if (size == 3 and data[0].strip('"').isnumeric() ): #eliminates empty strings and non-numeric user ids
                        self.user_ids.append(int(data[0].strip('"')))
                        item_data = []
                        utility_functions.parse_string(line,item_data)
                        self.items[item_data[0]] = User()
                        self.items[item_data[0]].set_values(item_data)
        
        print ('Finished reading user data')
    
    def read_book_data(self,filename):       
        nlines = 0
        with open(filename,'r') as file:
            for line in file:
                nlines = nlines + 1
                if (nlines == 1):
                    #its a header line
                    data = line.split(';')
                    size = len(data)
                else:
                    data = line.split(';')
                    if (len(data) == size):
                        book_data = []
                        book_data.append(data[0].strip('"'))
                        book_data.append(data[1].strip('"'))
                        book_data.append(data[2].strip('"'))
                        
                        self.descriptors[book_data[0]] = Book(book_data) #isbn is key
        print ('Finished reading book data')
    
    def read_ratings_data(self,filename):
         nlines = 0
         with open(filename,'r') as file:
            for line in file:
                nlines = nlines + 1
                #print (nlines)
                if (nlines == 1):
                    #its a header line
                    data = line.split(';')
                    size = len(data)
                else:
                    data = line.split(';')
                    if (len(data) == size and data[0].strip('"').isnumeric()):
                        ratings_data = []
                        for i1 in range(0,size):
                            if (i1 < size-1):
                                ratings_data.append(data[i1].strip('"'))
                            else:
                                ratings_data.append(data[i1].strip().strip('"'))
                        if ratings_data[0] in self.items:
                            self.items[ratings_data[0]].book_data[ratings_data[1]] = float(ratings_data[2])
         print ('Finished reading ratings data')
    
    def find_nearest_neighbor(self):
        if (self.item_name in self.items):
            item_book_data = self.items[self.item_name].book_data.copy()
        else:
            print ('User name does not exist in provided data. Hence exiting')
            sys.exit()
        #Need to write a part for a condition for which item has not rated any book
        neigh_ratings = {}
        for key in self.items:
            if (key != self.item_name):
                #neigh_ratings[key] = utility_functions.get_cosine_similarity(item_book_data,self.items[key].book_data) 
                neigh_ratings[key] = utility_functions.get_Pearson(item_book_data,self.items[key].book_data) 
        
        sorted_neighs = sorted(neigh_ratings.items(),key=operator.itemgetter(1),reverse=True)
        recommendations = {}
        
        total = 0.0
        for i1 in range(0,self.num_neighbors):
            total = total + sorted_neighs[i1][1]
        
        print ('Total is %f'%(total))
        print ('Sorted neighbors contain %d elements'%len(sorted_neighs))
        
        for i1 in range(0,self.num_neighbors):
            wt = sorted_neighs[i1][1]/total
            
            neigh_data = self.items[sorted_neighs[i1][0]].book_data
            print ('Length of sorted_neigh element %s is %d'%(sorted_neighs[i1][0],len(neigh_data)))
            for key in neigh_data:
                if key not in item_book_data:
                    if key not in recommendations:
                        recommendations[key] = wt*neigh_data[key]
                    else:
                        recommendations[key] = recommendations[key] + wt*neigh_data[key]
        
        recomm_list = sorted(recommendations.items(),key=operator.itemgetter(1),reverse=True)
        for i1 in range(0,5):
            print (recomm_list[i1][0],recomm_list[i1][1],self.descriptors[recomm_list[i1][0]].title)
            

user_name = '171118'
#user_name = '276747'
input_file_names = ['BX-Users.csv','BX-Books.csv','BX-Book-Ratings.csv']

for i1 in range(0,len(input_file_names)):
    if not (utility_functions.check_file(input_file_names[i1])):
        print('%s file does exist'%(input_file_names[i1]))
        sys.exit()

make_rec = Recommend(user_name,5)
make_rec.read_user_data(input_file_names[0])
make_rec.read_book_data(input_file_names[1])
make_rec.read_ratings_data(input_file_names[2])
make_rec.find_nearest_neighbor()

if '0060139145' in make_rec.items[user_name].book_data:
    print ('I have rated this book')
else:
    print ('I have not rated this book')