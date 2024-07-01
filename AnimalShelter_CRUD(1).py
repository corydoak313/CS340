#!/usr/bin/env python
# coding: utf-8

# In[7]:


from Animal_Shelter import AnimalShelter
from bson.objectid import ObjectId


class AnimalShelterCRUD(object):
    animals = AnimalShelter()

    data = {
      'age_upon_outcome': '1 year',
      'animal_id': 'TEST',
      'animal_type': 'Dog',
      'breed': 'Domestic',
      'color': 'Black',
      'date_of_birth': '2023-06-02',
      'datetime': '2024-05-06 10:49:00',
      'monthyear': '2024-05-06T10:49:00',
      'name': 'Steve',
      'outcome_subtype': '',
      'outcome_type': 'Transfer',
      'sex_upon_outcome': 'Spayed Female',
      'location_lat': 30.6525984560118,
      'location_long': -97.7419963476254,
      'age_upon_outcome_in_weeks': 52.9215277777778}

    #testing no data
    #REMOVE HASH
    #data = none

    #calling for create fucntionality
    if animals.create(data):
        print("New Animal Added")

    #calling for read funcitonality
    request = animals.read({'name' : 'Steve'})
    for animal in request:
        print(animal)

    #calling for update fuctionality
    updateAnimal = animals.update({'name' : 'Steve'}, {'outcome_type' : 'Adopted '})
    print(updateAnimal)

    #calling for delete functionality
    deleteAnimal = animals.delete({'name' : 'Steve'})
    print(deleteAnimal)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




