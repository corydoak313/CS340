#!/usr/bin/env python
# coding: utf-8

# In[4]:


from pymongo import MongoClient
from bson.objectid import ObjectId

class AnimalShelter (object):
    """CRUD operations for Animal collection in MongoDB"""
    
    def __init__(self, user, password):
        #Initializing Mongo CLient helps access Mongo databases and collections. 
        
        USER = 'aacuser'
        PASSWORD = 'SNHU1234'
        HOST = 'nv-desktop-services.apporto.com'
        PORT = 31580
        DB = 'AAC'
        COL = 'animals'
        #
        #initialize connection
        #
        self.client = MongoClient('mongodb://%s:%s@localHost:31580/AAC' % (user, password))
        self.database = self.client['AAC' % (DB)]
        self.collection = self.database['%s' % (COL)]

    #Method to implement the C in CRUD
    def create(self, data):
        if data is not None:
            insertStatus = self.database.animals.insert(data)
            if insertStatus != 0:
                return True
            else:
                return False
        else:
            raise Exception("Nothing to save, because data parameter is empty")

    #Method to implement R in CRUD
    def read(self, readData):
        if searchData:
            inputData = self.database.animals.find(readData, {"_id": False})
        else:
            inputData = self.database.animals.find({}, {"_id": False})
            
        return inputData
    
    #Method to implement U in CRUD
    def update(self, searchData, updateData):
        #Return dataset or else let error flow
        if searchData is not None:
            result = self.database.animals.update_many(searchData, {"$set": updateData})
        else:
            raise Exception("Nothing to update")
        #getting amount of objects modified
        return len(updateData)
        
    
    #Method to implement D in CRUD
    def delete(self, deleteData):
        if deleteData is not None:
            result = self.database.animals.delete_many(delete_data)
        else:
            raise Exception("Nothing to Delete")
        #getting number of objects deleted
        return len(delete_data)
       
    
    
            


# In[ ]:




