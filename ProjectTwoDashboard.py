#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Setup the Jupyter version of Dash
from jupyter_dash import JupyterDash

# Configure the necessary Python module imports for dashboard components
import dash_leaflet as dl
from dash import dcc
from dash import html
import plotly.express as px
from dash import dash_table
from dash.dependencies import Input, Output, State
import base64

# Configure OS routines
import os

# Configure the plotting routines
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#### FIX ME #####
# change animal_shelter and AnimalShelter to match your CRUD Python module file name and class name
from AnimalShelter_CRUD import AnimalShelterCRUD

###########################
# Data Manipulation / Model
###########################
# FIX ME update with your username and password and CRUD Python module name

username = "aacuser"
password = "SNHU1234"
shelter = AnimalShelter(username, password)
hostname = 'nv-desktop-services.apporto.com'
port = 31580


# Connect to database via CRUD Module
db = AnimalShelter(username, password)

# class read method must support return of list object and accept projection json input
# sending the read method an empty document requests all documents be returned
df = pd.DataFrame.from_records(db.read({}))

# MongoDB v5+ is going to return the '_id' column and that is going to have an 
# invlaid object type of 'ObjectID' - which will cause the data_table to crash - so we remove
# it in the dataframe here. The df.drop command allows us to drop the column. If we do not set
# inplace=True - it will reeturn a new dataframe that does not contain the dropped column(s)
df.drop(columns=['_id'],inplace=True)

## Debug
# print(len(df.to_dict(orient='records')))
# print(df.columns)


#########################
# Dashboard Layout / View
#########################
app = JupyterDash(__name__)

#FIX ME Add in Grazioso Salvare’s logo
image_filename = 'Cory_D_Grazioso.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

#FIX ME Place the HTML image tag in the line below into the app.layout code according to your design
#FIX ME Also remember to include a unique identifier such as your name or date
#html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))

app.layout = html.Div([
    #html.Div(id='hidden-div', style={'display':'none'}),
    html.Center(html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))),
    html.Center(html.B(html.H1('Cory Doak - CS-340 Dashboard'))),
    html.Hr(),
    html.Div(
        dcc.RadioItems(
            id= 'filter-type',
            #Grazioso Requirements
            options = [
                {'label': 'Water Rescue', 'value':'WR'},
                {'label': 'Mountain or Wilderness Rescue', 'value': 'M/WR'},
                {'label': 'Disaster Rescue or Individual Training', 'value': 'DR/IT'},
                {'label': 'Reset - Return to unfiltered state', 'value': 'RESET'}
            ],
            value = 'RESET',
            labelStyle = {'display': 'inline-block'}
        )
    ),
    html.Hr(),
    dash_table.DataTable(id='datatable-id',
                         columns=[{"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns],
                         data=df.to_dict('records'),
#FIXME: Set up the features for your interactive data table to make it user-friendly for your client
#If you completed the Module Six Assignment, you can copy in the code you created here 
                        editable = False,
                        filter_action = 'native',
                        sort_action = 'native',
                        sort_mode = 'multi',
                        column_selectable = False,
                        row_selectable = 'single',
                        row_deletable = False,
                        selected_columns = [],
                        selected_rows = [],
                        page_action = 'native',
                        page_current = 0,
                        page_size = 10,

                        ),
    html.Br(),
    html.Hr(),
#This sets up the dashboard so that your chart and your geolocation chart are side-by-side
    html.Div(className='row',
         style={'display' : 'flex'},
             children=[
        html.Div(
            id='graph-id',
            className='col s12 m6',

            ),
        html.Div(
            id='map-id',
            className='col s12 m6',
            )
        ])
])

#############################################
# Interaction Between Components / Controller
#############################################



    
@app.callback(Output('datatable-id','data'),
              [Input('filter-type', 'value')])
def update_dashboard(filter_type):
## FIX ME Add code to filter interactive data table with MongoDB queries
    #Reads if filter type is Water Rescue (WR)
    if filter_type == 'WR':
        df = pd.DataFrame(list(shelter.read({'$and': [{'sex_upon_outcome': 'Intact Female'},
                                                      {'$or': [
                                                          {'breed': 'Labrador-Retriever Mix'},
                                                          {'breed': 'Chesa Bay Retr Mix'},
                                                          {'breed': 'Newfoundland'}],                                                    
                                                      },
                                                      {'$and': [
                                                          {'age_upon_outcome_in_weeks': {'@gte': 26}},
                                                          {'age_upon_outcome_in_weeks': {'@lte': 156}}]
                                                      }
                                                     ]
                                            }
                                           )
                              )
                         )
    
    
    #Reads if filter type is Mountain or Wilderness Rescue (M/WR)
    elif filter_type == 'M/WR':
        df = pd.DataFrame(list(shelter.read({'$and': [{'sex_upon_outcome': 'Intact Male'}, 
                                                      {'$or': [
                                                          {'breed': 'German Shepherd'},
                                                          {'breed': 'Alaskan Malamute'},
                                                          {'breed': 'Old English Sheepdog'},
                                                          {'breed': 'Siberian Husky'},
                                                          {'breed': 'Rottweiler'}]
                                                      },
                                                      {'$and': [
                                                          {'age_upon_outcome_in_weeks': {'@gte': 26}},
                                                          {'age_upon_outcome_in_weeks': {'@lte': 156}}]
                                                     }
                                                     ]
                                            }
                                           )
                              )
                         )
                                                    
        
    #Reads if filter type is Disaster Rescue or Individual Training(DR/IT)
    elif filter_type == 'DR/IT':
        df = pd.DataFrame(list(shelter.read({'$and': [{'sex_upon_outcome': 'Intact Male'}, 
                                                      {'$or': [
                                                          {'breed': 'Doberman Pinscher'},
                                                          {'breed': 'German Shepherd'},
                                                          {'breed': 'Golden Retriever'},
                                                          {'breed': 'Bloodhound'},
                                                          {'breed': 'Rottweiler'}]
                                                      },
                                                      {'$and': [
                                                          {'age_upon_outcome_in_weeks': {'@gte': 20}},
                                                          {'age_upon_outcome_in_weeks': {'@lte': 300}}]
                                                     }
                                                     ]
                                            }
                                           )
                              )
                         )
        
    #Reads if search filter is needs to be RESET
    elif filter_type == 'RESET':
        df = pd.DataFrame.from_records(shelter.read({}))
        

        
        columns=[{"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns]
        data=df.to_dict('records')

        return (data,columns)

# Display the breeds of animal based on quantity represented in
# the data table
@app.callback(
    Output('graph-id', "children"),
    [Input('datatable-id', "derived_virtual_data")])

def update_graphs(viewData):
    ###FIX ME ####
    # add code for chart of your choice (e.g. pie chart) #
    dff = pd.DataFrame.from_dict(viewData)
    
    #creating needed values
    names = dff['breed'].value_counts().keys().tolist()
    values = dff['breed'].value_counts().tolist()

    return [
        dcc.Graph(            
            figure = px.pie(
                title = 'Preferred Animals',
                data_frame = dff,
                values = values,
                names = 'breed',
                color_discrete_sequence = px.colors.sequential.RdBu,
                height = 450,
                width = 700 
            )
        )    
    ]
    
#This callback will highlight a cell on the data table when the user selects it
@app.callback(
    Output('datatable-id', 'style_data_conditional'),
    [Input('datatable-id', 'selected_columns')]
)
def update_styles(selected_columns):
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]


# This callback will update the geo-location chart for the selected data entry
# derived_virtual_data will be the set of data available from the datatable in the form of 
# a dictionary.
# derived_virtual_selected_rows will be the selected row(s) in the table in the form of
# a list. For this application, we are only permitting single row selection so there is only
# one value in the list.
# The iloc method allows for a row, column notation to pull data from the datatable
@app.callback(
    Output('map-id', "children"),
    [Input('datatable-id', "derived_virtual_data"),
     Input('datatable-id', "derived_virtual_selected_rows")])
def update_map(viewData, index):  
    if viewData is None:
        return
    elif index is None:
        return
    
    dff = pd.DataFrame.from_dict(viewData)
    # Because we only allow single row selection, the list can be converted to a row index here
    if index is None:
        row = 0
    else: 
        row = index[0]
        
    # Austin TX is at [30.75,-97.48]
    return [
        dl.Map(style={'width': '1000px', 'height': '500px'}, center=[30.75,-97.48], zoom=10, children=[
            dl.TileLayer(id="base-layer-id"),
            # Marker with tool tip and popup
            # Column 13 and 14 define the grid-coordinates for the map
            # Column 4 defines the breed for the animal
            # Column 9 defines the name of the animal
            dl.Marker(position=[dff.iloc[row,13],dff.iloc[row,14]], children=[
                dl.Tooltip(dff.iloc[row,4]),
                dl.Popup([
                    html.H1("Animal Name"),
                    html.P(dff.iloc[row,9])
                ])
            ])
        ])
    ]



app.run_server(debug=True)


# In[ ]:





# In[ ]:




