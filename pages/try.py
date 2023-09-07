import streamlit as st
import pandas as pd
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE
import re
    #from google.cloud import storage
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import requests
from streamlit_lottie import st_lottie
import time  
import webbrowser

import stripe
from streamlit_option_menu import option_menu
import os






@st.cache_data()
def loading_data():
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(r'C:\Users\d\Downloads\service_account.json', scope)
    client = gspread.authorize(credentials)
    
    # Fetch data from prop_type sheet
    prop_type_sheet = client.open('db_try').worksheet('prop_type')
    prop_type_values = prop_type_sheet.col_values(1)
    prop_type = [value for value in prop_type_values if value]
    
    # Fetch data from service_type sheet
    service_type_sheet = client.open('db_try').worksheet('service_type')
    service_type_values = service_type_sheet.col_values(1)
    service_type = [value for value in service_type_values if value]
    
    # Fetch data from options sheet
    options_sheet = client.open('db_try').worksheet('private')
    options_values = options_sheet.col_values(1)
    options = [value for value in options_values if value]
    
    # Fetch data from kitchen_opt sheet
    kitchen_opt_sheet = client.open('db_try').worksheet('kitchen_opt')
    kitchen_opt_values = kitchen_opt_sheet.col_values(1)
    kitchen_opt = [value for value in kitchen_opt_values if value]

    service_type1_sheet = client.open('db_try').worksheet('service_type1')
    service_type1_values = service_type1_sheet.col_values(1)
    service_type1 = [value for value in service_type1_values if value]

    commercial_prop_sheet = client.open('db_try').worksheet('commercial_prop')
    commercial_prop_values = commercial_prop_sheet.col_values(1)
    commercial_prop = [value for value in commercial_prop_values if value]

    sofa_upsterly_types_sheet = client.open('db_try').worksheet('sofa_upsterly_types')
    sofa_upsterly_types_values = sofa_upsterly_types_sheet.col_values(1)
    sofa_upsterly_types = [value for value in sofa_upsterly_types_values if value]

    prices_sheet = client.open('db_try').worksheet('prices')
    prices_values = prices_sheet.get_all_values()
    prices = pd.DataFrame(prices_values[1:], columns=prices_values[0])

    # Return the fetched data as a list of lists
    return [prop_type, service_type, options, kitchen_opt, service_type1, commercial_prop, sofa_upsterly_types, prices]
# Call the function to get the data
[prop_type, service_type, options, kitchen_opt, service_type1,commercial_prop,sofa_upsterly_types, prices] = loading_data()


yesno=['Yes','no']


selected_days = []
check_list=[]
selected_options=[]
selected_options_extr=[]
selected_options_comm=[]
selected_price=[]
carpet_cleaning=[]
condition_toilet=[]
selected_choice=[]
selected_quantity=[]
selected_unitprice=[]
receipt =['hi','hey']


name_list=[]
address_list=[]
email_list=[]
num_list=[]
payment_method_list=[]


#______________________________________________________________________________________________
inv_name_list=[]
inv_address_list=[]
inv_email_list=[]

index=1

if 'selected_options_extr' not in st.session_state:
    st.session_state.selected_options_extr = []



def display_extras():
    # Display form for name, address, and number input
    quantities={}

    for sub_option in selected_options:
            quantity_su = st.number_input(f'Quantity for {sub_option}:', min_value=0, value=0, step=1)
            if quantity_su > 0:
                    quantities[f'{sub_option}'] = quantity_su
    
    return quantities


def display_appliances():
    quantities={}
 

    ttt=['oven', 'microwave']
    if 'Kitchen' in selected_options:
        for sub_option in ttt:
            quantity_su = st.number_input(f'Quantity for {sub_option}:', min_value=0, value=0, step=1)
            if quantity_su > 0:
                    quantities[f'{sub_option}'] = quantity_su

    return quantities




# Define your options with associated Font Awesome icons
options_with_icons = {
    'Kitchen': '🍳',
    'Bathroom': '🚿',
    'Living Room': '🛋️',
    'Bedroom': '🛏️',
    'Garage': '🚗',
    'Outdoor Area': '🌳',
}



# Create a dictionary to store the state of each option
option_states = {}

st.write("Select the areas of the property that need cleaning:")
quantity_su=0

with st.container():
    # Add custom CSS to adjust the width of the number input
    

    right_col1, left_col1 = st.columns(2)

    with right_col1:
        for option, icon in options_with_icons.items():
            option_states[option] = st.checkbox(f"{icon} {option}")
        selected_options = [option for option, state in option_states.items() if state]
    
    with left_col1:
        quantity_su=display_extras()


st.write('---')

display_appliances()



for option, quantity in quantity_su.items():

    if quantity > 0:
            
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        unitprice = prices.loc[prices['Item'] == option, 'Price'].values[0]
    selected_options_extr.append(f'{option} x ({quantity}) - £{unitprice}) - ({timestamp})')
    st.session_state.selected_options_extr = selected_options_extr


item_list_ext=[]
for item in st.session_state.selected_options_extr:
    match = re.search(r'\b(' + '|'.join(prices['Item']) + r')\b', item)
    if match:
        item_list_ext.append(match.group())        

# Create an empty list to store the extracted prices
extracted_values_ext = []
for x in item_list_ext:
    unitprice1 = prices.loc[prices['Item'] == x, 'Price'].values[0]
    extracted_values_ext.append(int(unitprice1))



extracted_quantity_ext = []

for eachquantity in st.session_state.selected_options_extr:
    # Extract the value using regular expressions to find the numbers inside parentheses
    match_quantity = re.search(r'\((\d+)\)', eachquantity)
    if match_quantity:
        extracted_quant = match_quantity.group(1)
        extracted_quantity_ext.append(int(extracted_quant))



new_df_ext = pd.DataFrame({'Item': item_list_ext,'unit_price': extracted_values_ext, 'quantity': extracted_quantity_ext})
st.write(new_df_ext)
for option in st.session_state.selected_options_extr:
    st.sidebar.write(f'- {option}')

# Get the selected options

st.write('You selected:', selected_options)
