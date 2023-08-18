# IMPORT LIBRARIES
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

#####################################################################################################################
#PAGE SETUP


st.set_page_config(page_title='BOOKING SPACE', layout='wide')
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

# ---- LOAD ASSETS ----
#lottie_coding = load_lottieurl("https://lottie.host/4bcf69c4-1e8b-486c-a53f-c1790547bdb5/XNiyLI7esJ.json")
lottie_pic = load_lottiefile("images/display.json")  # replace link to local lottie file
lottie_pic1 = load_lottiefile("images/calendar.json")  # replace link to local lottie file

#_________________________________________________________________________________________________________________

with st.container():
    left_col, right_col, mid_col=st.columns(3)
    with left_col:
        
        st_lottie(lottie_pic1, height=150, width=200, key="coding")
    with right_col:
        st.title("BOOK NOW/GET QUOTE")
    with mid_col:
        st_lottie(lottie_pic, height=150, width=200, key="")

##########################################################################################################################################
#LOAD DATA




# Authorize with the credentials


@st.cache_data()
def loading_data():
    # Get the JSON key from the secret
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(service_account, scope)
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
    
    # Return the fetched data as a list of lists
    return [prop_type, service_type, options, kitchen_opt]
# Call the function to get the data
[prop_type, service_type, options, kitchen_opt] = loading_data()



##############################################################################################################
scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(r'C:\Users\d\Downloads\service_account.json', scope)
client = gspread.authorize(credentials)

yesno = ['Yes','No']
bar_checklist=['TABLE: Wipe Down tables','BAR: Wipe Down the Bar',
                'FLOORS: Sweep and mop floors','BINS: Empty and sanitize trash cans']

prices_dict = {'Item': ['House', 'Flat', 'Bungalow', 'Pub/Restaurant/Club', 'One Off cleaning', 
                        'Regular cleaning', 'Bedroom','Bathroom','Seperate Toilet','Diningroom','Livingroom','Kitchen',
            'Study/Utility Room', 'Staircases', 'Garage','Conservatory','Balcony', 'FRIDGE/FREEZER','FRIDGE','FREEZER','AMERICAN STYLE FRIDGE (LARGE FRIDGE)','SINGLE OVEN',
              'DOUBLE OVEN','RANGE COOKER OVEN','AGA OVEN','MICROWAVE','WASHING MACHINE',
              'DISH WASHER','HOB','HOB EXTRACTOR HOODS','1 seat','2 Seat', 'L-Shape'], 
            'Price': [5, 10, 5,1,10,5,20,30,10,25,25,25,10,5,15,15,10,15,10,5,20,25,35,25,25,5,5,5,5,5,10,20,25]}
prices = pd.DataFrame(prices_dict)

service_type1=['End of Tenancy/Moving in', 'One-off deep cleaning(Living in)']
commercial_prop=['Bar/Pub/Restaurant', 'Takeway', 'Offices', 'Other']
sofa_upsterly_types=['1 seat', '2 Seat', 'L-Shape']
paym =['Card','Bank Transfer', 'Cash']


#########################################################################################################################################


#DEFINE FUNCTIONS


#=============================================================================================================================================
def popup_message(message):
    st.markdown(
        f"""
        <div style="
            display: flex;
            justify-content: center;
            align-items: center;
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            padding: 20px;
            background-color: #f0f0f0;
            border: 1px solid #ccc;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            z-index: 1000;
        ">
            {message}
        </div>
        """,
        unsafe_allow_html=True,
    )



def popup_message5(message):
    st.markdown(
        f"""
        <div style="
            display: flex;
            justify-content: center;
            align-items: center;
            position: fixed;
            top: 7%;
            left: 20px; /* Adjust this value to position the pop-up message next to the sidebar */
            transform: translate(0, -50%);
            padding: 20px;
            background-color: #f0f0f0;
            border: 1px solid #ccc;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            z-index: 1000;
        ">
            {message}
        </div>
        """,
        unsafe_allow_html=True,
    )

#===================================================================================================================================
#DATE AND TIME SELECTION FUNCTIONS

def select_time_and_date():
    st.title('TIME AND DATE SELECTION')

    # Create two columns to display the start and end time inputs side by side
    date_col, time_col = st.columns(2)

    # Add the start time input to the first column
    start_date = date_col.date_input(f'SELECT PREFERRED DATE:', value=datetime.date.today())

    # Add the end time input to the second column
    start_time = time_col.time_input(f'SELECT PREFERRED TIME:', value=datetime.time(hour=10, minute=0))

    # Convert selected date and time to strings
    start_date_str = start_date.strftime("%Y-%m-%d")
    start_time_str = start_time.strftime("%H:%M:%S")

    return start_date_str, start_time_str


def select_start_time_and_date():
    st.title('TIME AND DATE SELECTION')

    # Create two columns to display the start and end time inputs side by side
    date_col, time_col = st.columns(2)

    # Add the start time input to the first column
    start_date = date_col.date_input(f'SELECT STARTING DATE:', value=datetime.date.today())

    # Add the end time input to the second column
    start_time = time_col.time_input(f'SELECT STARTING TIME:', value=datetime.time(hour=10, minute=0))

    # Convert selected date and time to strings
    start_date_str1 = start_date.strftime("%Y-%m-%d")
    start_time_str1 = start_time.strftime("%H:%M:%S")

    return start_date_str1, start_time_str1

# shift preferences function to display the 
def shift_preferences():
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    shift_options = ['weekly', 'every 2 weeks', 'every 3 weeks', 'every 4 weeks']

    preferences_list = []

    selected_days = st.multiselect("Select Days you need your property cleaning", days)

    # Create lists to store data for each field
    day_list = []
    start_time_list = []
    end_time_list = []
    shift_prefs_list = []

    # Loop through each day of the week
    for day in selected_days:
        st.write(f"### {day}")

        # Create two columns to display the start and end time inputs side by side
        start_col, end_col = st.columns(2)

        # Add the start time input to the first column
        start_time = start_col.time_input(f'Start time for {day}:', value=datetime.time(hour=9, minute=0))
    # Convert time object to a string
        start_time_str = start_time.strftime("%H:%M:%S")

        start_time_list.append(start_time_str)

        # Add the end time input to the second column
        end_time = end_col.time_input(f'End time for {day}:', value=datetime.time(hour=17, minute=0))
        end_time_str = end_time.strftime("%H:%M:%S")
        end_time_list.append(end_time_str)

        # Add a multiselect to choose the preferred shift(s) for the day
        shift_prefs = start_col.selectbox(f"Select preferred shift(s) for {day}:", shift_options)
        shift_prefs_list.append(shift_prefs)

        # Append the day to the day list
        day_list.append(day)

    # Create a DataFrame using the collected data
    preferences_df = pd.DataFrame({
        'Day': day_list,
        'Start Time': start_time_list,
        'End Time': end_time_list,
        'Shift Preferences': shift_prefs_list
    })

    return preferences_df


#=============================================================================================================================================


def generate_unique_id(email):
    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    first_letter = email[0]
    unique_id = f"{current_time}{first_letter}"
    return unique_id

#=============================================================================================================================================

quantity_su=0
def display_extras():
    st.write('---')

    st.title('EXTRA SERVICES')

    # Display form for name, address, and number input
    st.write("Extra Services")
    quantities={}
    
    rubbish_rem = st.radio('DO YOU WANT US TO GET RID OF ALL RUBBISH BAG AT THE END OF THE CLEANING', yesno, index=1)
    sofa_clean = st.radio('DO YOU NEED YOUR SOFA/UPHOKSTERY CLEANED', yesno, index=1)
    if sofa_clean == 'Yes':
        for sub_option in sofa_upsterly_types:
            quantity_su = st.number_input(f'Quantity for {sub_option}:', min_value=0, value=0, step=1)
            if quantity_su > 0:
                    quantities[f'{sub_option}'] = quantity_su
    
    return rubbish_rem, sofa_clean, quantities
rubbish_rem_price = 0
#=============================================================================================================================================

def display_quote():
    # Display form for name, address, and number input
    st.write("Please enter your name, property address, and email:")
    inv_name = st.text_input("Provide Name")
    inv_address = st.text_input("Property Address")
    inv_email = st.text_input("Email to receive quote")
    return inv_name, inv_address, inv_email

def display_book():
    # Display form for name, address, and number input
    st.write("Please enter your name(company name), address, email and contact number:")
    name = st.text_input("Name")
    address = st.text_input("Address")
    post_code = st.text_input("Post Code")
    email = st.text_input("email")
    num = st.text_input("Contact Number")
    payment_method= st.selectbox('Prefered payment method', paym)
    terms_and_conditions = st.checkbox("I agree to the Terms and Conditions")


    return name, address, post_code,email, num, payment_method, terms_and_conditions

def display_book_reg():
    # Display form for name, address, and number input
    st.write("Please enter your name(company name), address, email and contact number:")
    name_reg = st.text_input("Name")
    address_reg = st.text_input("Address")
    email_reg = st.text_input("email")
    num_reg = st.text_input("Contact Number")
    payment_method_reg= st.selectbox('Prefered payment method for your first charge.', paym)
    terms_and_conditions_reg = st.checkbox("I agree to the Terms and Conditions")


    return name_reg, address_reg, email_reg, num_reg, payment_method_reg, terms_and_conditions_reg

name, address, email, num, inv_name, inv_address, inv_email, name_reg, address_reg, email_reg, num_reg, payment_method_reg, terms_and_conditions_reg = "", "","", "","","","","", "","", "","",""

stripe.api_key = "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" 


def create_payment_link(amount, currency="gbp", success_url=None, cancel_url=None):
    try:
        line_items = [{
            'price_data': {
                'currency': currency,
                'unit_amount': amount,
                'product_data': {
                    'name': 'Payment'
                    },
                    },
                    'quantity': 1,
        }]
        payment_link = stripe.checkout.Session.create(
            success_url=success_url,
            cancel_url=cancel_url,
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
        )

                # Retrieve the payment link URL
        link_url = payment_link.url

        return link_url

    except stripe.error.StripeError as e:
                # Handle any errors that occur during payment link creation
        print(f"Error creating payment link: {e}")
        return None

######################################################################################################################################

#DESIGN MENU

menu = option_menu(None, ["ONE-OFF CLEANING", "REGULAR CLEANING"], 
    icons=['house', 'cloud-upload'], 
    menu_icon="cast", default_index=0, orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "15px"}, 
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "green"},
    }
)

st.sidebar.success('BOOKING SUMMARY')

#insert a divider
st.write('---')
#####################################################################################################################
#First part
#________________________________________________________________________________________________________
st.title('PROPERTY DETAILS')

# Create two columns to display the start and end time inputs side by side
# Display content based on selected option

with st.container():

    right_col1, left_col1 = st.columns(2)
    option_services1=None
    option_services2=None

    with right_col1:
        option_services = st.radio("Select a property type:", prop_type)
    with left_col1:
        if option_services in ['Commercial Property', 'Other']:
            option_services1= st.radio("Select Business Type", commercial_prop)
        else:
            option_services2= st.radio("Select Service type", service_type1)

st.write('---')

###################################################################################################################################


#-------------------------------------------------------------------------------------------------------
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
receipt =[]


name_list=[]
address_list=[]
email_list=[]
num_list=[]
payment_method_list=[]
post_code_list=[]
#______________________________________________________________________________________________
inv_name_list=[]
inv_address_list=[]
inv_email_list=[]

index=1

#____________________________________________________________________________________________________________

if 'selected_options' not in st.session_state:
    st.session_state.selected_options = []

if 'selected_options_extr' not in st.session_state:
    st.session_state.selected_options_extr = []

popup_message5("Click arrow to View Summary!")


if menu == "ONE-OFF CLEANING":

    right_col2, left_col2 =st.columns(2)

        #option = st.selectbox("Select an option", ["Option 1", "Option 2"])
    if option_services not in ['Commercial Property', 'Other']:

        quantities = {}
        quantity_carpet = None
        toilet_condition = None  
        with right_col2:
            option_pro = st.selectbox('Select areas of the property that needs cleaning', options)
            #quantity = st.number_input(f'Quantity for {option_pro}:', key=f'{option_pro}_quantity', min_value=0, value=0, step=1)
            #quantity_carpet= st.radio(f'Do you want carpet wash and dry {option_pro}:', yesno, key=f'{option_pro}_carpet')
        if option_pro:
            with left_col2:
                quantity = st.number_input(f'Quantity for {option_pro}:', min_value=0, value=0, step=1)
            quantities[option_pro] = quantity

            if option_pro == 'Kitchen':
                
                for sub_option in kitchen_opt:
                    sub_quantity = st.number_input(f'Quantity for {sub_option}:', min_value=0, value=0, step=1)
                    if sub_quantity > 0:
                        quantities[f'{sub_option}'] = sub_quantity

            elif option_pro in ['Bathroom', 'Seperate Toilet']:
                toilet_condition= st.radio(f'Presence of feces outside the toilet {option_pro}:', yesno)
                condition_toilet.append(toilet_condition)


            else:
                quantity_carpet= st.radio(f'Do you want carpet wash and dry in the {option_pro}:', yesno)
                carpet_cleaning.append(quantity_carpet)

                    
            submit_button = st.button('Add option')
            if submit_button:
                selected_options = st.session_state.get('selected_options', [])
                selected_choice = st.session_state.get('selected_choice', [])
                selected_quantity =st.session_state.get('selected_quantity', [])
                selected_unitprice= st.session_state.get('selected_unitprice', [])
                
                for option, quantity in quantities.items():
                    if quantity > 0:
                        unitprice = prices.loc[prices['Item'] == option, 'Price'].values[0]


    # Check if the option already exists in the list
                        # Check if the option already exists in the list

                        # Check if the option already exists in the list
                        
                        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        selected_options.append(f'{option} x ({quantity})  carpet-({quantity_carpet}) - £{unitprice}) human_feces-({toilet_condition}) ({timestamp})')
                        selected_choice.append(f'{option}, {unitprice}')
                        selected_quantity.append(f'{quantity}')
                        selected_unitprice.append(f'{unitprice}')
                                            
                        st.session_state.selected_options = selected_options or [] # initialize with an empty list if it doesn't exist
                        st.session_state.selected_choice = selected_choice or []
                        st.session_state.selected_quantity = selected_quantity
                        st.session_state.selected_unitprice = selected_unitprice

                        sheet=client.open('db_try').worksheet('Sheet1')

                        # Append the data to the Google Sheet
                        data_to_append = list(zip(selected_options, selected_choice, selected_quantity, selected_unitprice))
                        sheet.append_rows(data_to_append)

                        # Optional: Clear the session_state variables after updating the Google Sheet
                        data_to_append = []
                        

                # add receipt data to dataframe            
                


        st.write(f"You selected {st.session_state.selected_options}!")


    #___________________________________________________________________________________________________________________
        rubbish_rem, sofa_clean, quantity_su=display_extras()


        for option, quantity in quantity_su.items():
            if quantity > 0:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


                unitprice = prices.loc[prices['Item'] == option, 'Price'].values[0]
            selected_options_extr.append(f'{option} x ({quantity}) - £{unitprice}) Rubbish Removal-({rubbish_rem}) ({timestamp})')
            st.session_state.selected_options_extr = selected_options_extr
        

        st.session_state.selected_options_extr = selected_options_extr

        #st.write(selected_options_extr)
    ###########################################################################################################################################
        #______________________________________________________________________________________________________________________________________


        removed_options = []

        # Assuming you already have the selected_options in session_state
        selected_options = st.session_state.get('selected_options', [])

        # Create checkboxes for each option to allow the user to select options to remove
        for option in selected_options:
            removed = st.sidebar.checkbox(f"Remove '{option}'", key=f"remove_{option}")
            if removed:
                removed_options.append(option)

        # Remove the selected options from the selected_options list
        selected_options = [option for option in selected_options if option not in removed_options]

        # Update the session_state with the modified selected_options list
        st.session_state.selected_options = selected_options
        st.sidebar.write('---')

    #_______________________________________________________________________________________________________

        st.title('BOOKING SUMMARY')

        discount_code=st.text_input('Insert discount code')

        
        item_list=[]
        for item in st.session_state.selected_options:
            match = re.search(r'\b(' + '|'.join(prices['Item']) + r')\b', item)
            if match:
                item_list.append(match.group())                

        # Create an empty list to store the extracted values
        extracted_values = []
        for x in item_list:
            unitprice1 = prices.loc[prices['Item'] == x, 'Price'].values[0]
            extracted_values.append(int(unitprice1))

        extracted_quantity = []

        for eachquantity in st.session_state.selected_options:
            # Extract the value using regular expressions to find the numbers inside parentheses
            match_quantity = re.search(r'\((\d+)\)', eachquantity)
            if match_quantity:
                extracted_quant = match_quantity.group(1)
                extracted_quantity.append(int(extracted_quant))

        extracted_carpet = []

        for xa in st.session_state.selected_options:
            if 'carpet-(Yes)' in xa:
                match_xa = re.search(r'\b(\d+)\b', xa)
                if match_xa:
                    quantity_xa = match_xa.group(1)
                    extracted_quantity_xa = int(quantity_xa) * 20
                    extracted_carpet.append(extracted_quantity_xa)
            else:
                extracted_carpet.append(int(0))


        extracted_toilet = []

        for xb in st.session_state.selected_options:
            if 'human_feces-(Yes)' in xb:
                match_xa = re.search(r'\b(\d+)\b', xb)
                if match_xa:
                    quantity_xa = match_xa.group(1)
                    extracted_quantity_xa = int(quantity_xa) * 20
                    extracted_toilet.append(extracted_quantity_xa)
            else:
                extracted_toilet.append(int(0))


        #_____________________________________________________________________________________________________________________________

        item_list_ext=[]
        for item in st.session_state.selected_options_extr:
            match = re.search(r'\b(' + '|'.join(prices['Item']) + r')\b', item)
            if match:
                item_list_ext.append(match.group())        

        # Create an empty list to store the extracted values
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

        #_______________________________________________________________________________________________________________________________-
        # Create a new DataFrame using the extracted values list
        new_df = pd.DataFrame({'Item': item_list,'unit_price': extracted_values, 'quantity': extracted_quantity, 'carpet_price': extracted_carpet, 'toilet_condition':extracted_toilet})

        new_df_ext = pd.DataFrame({'Item': item_list_ext,'unit_price': extracted_values_ext, 'quantity': extracted_quantity_ext})


        #____________________________________________________________________________________________________________________________________________________________________________

        #for option in st.session_state.selected_options:
        #    st.sidebar.write(f'- {option}')

        for option in st.session_state.selected_options_extr:

            st.sidebar.write(f'- {option}')

        if option_services in ['House', 'Flat']:

            if rubbish_rem== 'No':

                rubbish_rem_price=0
            
            else:
                rubbish_rem_price=10
                st.sidebar.write(f'- Rubbish Removal-{rubbish_rem} {rubbish_rem_price}')

        #__________________________________________________________________________________________________________________________________


        def calculate_total(new_df):
            total = 0
            for i, row in new_df.iterrows():
                total += (row['unit_price'] * row['quantity']) + row['carpet_price'] 
            return total


        def calculate_total_ext(new_df):
            total_ext = 0
            for i, row in new_df.iterrows():
                total_ext += (row['unit_price'] * row['quantity'])
            return total_ext


        discount_dict = {'discount_code': ['ten', 'twenty'], 
                    'discount_amount': [10, 20]}

        discount_table = pd.DataFrame(discount_dict)


        if discount_code in discount_table['discount_code'].values:
            discount_tot = discount_table.loc[discount_table['discount_code'] == discount_code, 'discount_amount'].values[0]
        else:
            discount_tot = 0


        total = calculate_total(new_df)
        tot_ext = calculate_total_ext(new_df_ext)

        total_amount= total+tot_ext+rubbish_rem_price

        net=total_amount-(discount_tot/100)*total_amount



        st.write(f'<p style="font-size: 34px;">Total: {net:.2f}</p>', unsafe_allow_html=True)

        #for x in st.session_state.new_list:
        #    st.sidebar.write(f'{x}')

        st.sidebar.markdown('### Applied Discount:')


        st.sidebar.markdown(f'**${(discount_tot/100)*total_amount:.2f}**')
        st.sidebar.markdown('### Net Total:')
        st.sidebar.markdown(f'<p style="font-size: 34px;">£{net:.2f}</p>', unsafe_allow_html=True)


        st.write('---')

        # Call the function to display the time and date selection and get the selected values
        start_date_str, start_time_str = select_time_and_date()


        st.write('---')

        st.title('CONTACT DETAILS')

        inv = st.radio("", ["Book Now", "Send Quote by email"])


        if inv == 'Book Now':
            name, address, post_code,email, num, payment_method, terms_and_conditions = display_book() 
        else:
            inv_name, inv_address, inv_email,  = display_quote()

        button_placeholder = st.empty()

    #__________________________________________________________________________________________________________________________________

        if inv == 'Book Now':
            if payment_method == 'Card':
                if button_placeholder.button(f' click to  {inv}'):

                    if not address or not email or not terms_and_conditions:
                        st.warning("Property address and email fields cannot be empty")
                    else:
                        
                        name_list.append(name)
                        address_list.append(address)
                        email_list.append(email)
                        num_list.append(num)
                        payment_method_list.append(payment_method)
                        #option_services1_list.append(option_services1)
                        
                        unique_id = generate_unique_id(email)
                        personal_info_df = pd.DataFrame({'name': name_list,'addeess': address_list, 'email': email_list, 'contact_number': num_list, 'payment_method': payment_method_list, 'id': unique_id, 'date': start_date_str, 'time':start_time_str, 'property_type': option_services, 'service_type': option_services2, 'Rubbish Removal':rubbish_rem, 'Total':net})

                        personal_info_sheet=client.open('db_try').worksheet('personal_info')
                        sheet4=client.open('db_try').worksheet('Sheet4')

                        personal_info_data=personal_info_df.values.tolist()
                        personal_info_sheet.append_rows(personal_info_data)

                        values1 = new_df.values.tolist()
                        values2= new_df_ext.values.tolist()
                        sheet4.append_rows(values1)
                        sheet4.append_rows(values2)


                        html_template = """
                        <html>
                        <head>
                            <style>
                                body {{
                                    font-family: Arial, sans-serif;
                                    font-size: 14px;
                                }}
                                .invoice-container {{
                                    width: 800px;
                                    margin: 0 auto;
                                    border: 1px solid #ccc;
                                    padding: 20px;
                                }}
                                h1 {{
                                    color: #333;
                                    text-align: center;
                                }}
                                h2 {{
                                    color: #333;
                                    text-align: center;
                                }}
                                h3 {{
                                    color: #333;
                                    text-align: center;
                                }}
                                table {{
                                    border-collapse: collapse;
                                    width: 100%;
                                    margin-bottom: 20px;
                                }}
                                th, td {{
                                    padding: 8px;
                                    text-align: left;
                                    border-bottom: 1px solid #ddd;
                                }}
                                th {{
                                    background-color: #f2f2f2;
                                }}
                                td:first-child {{
                                    font-weight: bold;
                                }}
                            </style>
                        </head>
                        <body>
                            <div class="invoice-container">
                                <h1>DDEEP CLEANING INVOICE</h1>
                                <h3>Use the following details for bank transfer payment</h3>
                                <h2>
                                    <p>Account Name: DDEEP CLEANING SERVICES</p>
                                    <p>Account Number: 73946439</p>
                                    <p>Sort Code: 04-03-70</p>
                                </h2>
                                
                                <h3>Customer Information:</h3>
                                <ul>
                                    <li>
                                        Name: {}
                                        <br>
                                        Address: {}
                                        <br>
                                        Email: {}
                                        <br>
                                        Phone Number: {}
                                        <br>
                                        Payment Method: {}
                                        <br>
                                        Rubbish Removal (£5): {}
                                        <br>
                                        TOTAL: {}
                                        <br>

                                    </li>
                                </ul>

                                {}
                            </div>
                        </body>
                        </html>
                        """

                        def df_to_html_table(df):
                            table_html = "<table>"

                            # Add table header row
                            table_html += "<tr>"
                            for col in df.columns:
                                table_html += f"<th>{col}</th>"
                            table_html += "</tr>"
                            
                            for index, row in df.iterrows():
                                table_html += "<tr>"
                                for value in row:
                                    table_html += f"<td>{value}</td>"
                                table_html += "</tr>"
                            
                            table_html += "</table>"
                            return table_html

                        def df_to_html_tables(df, df2, name, address, email, num, payment_method, net, rubbish_rem):
                            table1_html = df_to_html_table(df)
                            table2_html = df_to_html_table(df2)
                            
                            final_html = html_template.format(name, address, email, num, payment_method, rubbish_rem ,net, table1_html + table2_html)
                            return final_html

                        final_html = df_to_html_tables(new_df, new_df_ext, name, address, email, num, payment_method, rubbish_rem,net)

                        smtp_server = "smtp.gmail.com"
                        smtp_port = 587
                        smtp_username = "clean@ddeepcleaningservices.com"
                        smtp_password = "acrmtrkgyezawleg"
                        email_from = "clean@ddeepcleaningservices.com"
                        email_to = 'fd92uk@gmail.com'
                        email_subject = "INVOICE@DDEEP CLEANING SERVICES"
                        email_body = "Thank you for choosing Ddeep Cleaning Services for your cleaning needs. We look forward to serving you again and exceeding your expectations. Please find attached your booking invoice."

                            # Create the email message
                        msg = MIMEMultipart()
                        msg['From'] = email_from
                        msg['To'] = email_to
                        msg['Subject'] = email_subject
                        msg.attach(MIMEText(email_body))

                            # Attach the HTML to the email
                        part = MIMEText(final_html, 'html')
                        part.add_header('Content-Disposition', 'attachment', filename="invoice.html")
                        msg.attach(part)
                        try:
                            smtp = smtplib.SMTP(smtp_server, smtp_port)
                            smtp.ehlo()
                            smtp.starttls()
                            smtp.login(smtp_username, smtp_password)
                            smtp.sendmail(email_from, email_to, msg.as_string())
                            smtp.quit()
                            st.success("Email sent successfully!")
                        except Exception as e:
                            st.error(f"Error sending email: {str(e)}")




                        net_in_stripe_format = int(net * 100)
                        payment_link_url = create_payment_link(net_in_stripe_format, currency="gbp", success_url="https://example.com/success", cancel_url="https://example.com/cancel")  # Replace this with the actual function call to create the payment link
                        
                        button_placeholder.empty()


                        popup_message("Thanks for booking with Ddeep Cleaning Services. You will now be directed to a new page to complete your booking!")
                        time.sleep(5)  # Wait for 5 seconds

                        webbrowser.open_new_tab(payment_link_url)                   
            


            else:

                if button_placeholder.button(f' now  {inv}'):

                    if not address or not email or not terms_and_conditions:
                        st.warning("Terms and Conditions, Property address and email fields cannot be empty")
                    else:
                        
                        name_list.append(name)
                        address_list.append(address)
                        email_list.append(email)
                        num_list.append(num)
                        payment_method_list.append(payment_method)
                        unique_id = generate_unique_id(email)
                        
                        personal_info_df = pd.DataFrame({'name': name_list,'addeess': address_list, 'email': email_list, 'contact_number': num_list, 'payment_method': payment_method_list, 'id': unique_id, 'date': start_date_str, 'time':start_time_str, 'property_type': option_services, 'service_type': option_services2, 'Rubbish_Removal':rubbish_rem, 'Total':net})

                        scope= ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
                        credentials=ServiceAccountCredentials.from_json_keyfile_name(r'C:\Users\d\Downloads\service_account.json', scope)
                        client=gspread.authorize(credentials)

                        personal_info_sheet=client.open('db_try').worksheet('Sheet14')
                        sheet4=client.open('db_try').worksheet('Sheet4')

                        personal_info_data=personal_info_df.values.tolist()
                        personal_info_sheet.append_rows(personal_info_data)

                        values1 = new_df.values.tolist()
                        values2= new_df_ext.values.tolist()
                        sheet4.append_rows(values1)
                        sheet4.append_rows(values2)


                        html_template = """
                        <html>
                        <head>
                            <style>
                                body {{
                                    font-family: Arial, sans-serif;
                                    font-size: 14px;
                                }}
                                .invoice-container {{
                                    width: 800px;
                                    margin: 0 auto;
                                    border: 1px solid #ccc;
                                    padding: 20px;
                                }}
                                h1 {{
                                    color: #333;
                                    text-align: center;
                                }}
                                h2 {{
                                    color: #333;
                                    text-align: center;
                                }}
                                h3 {{
                                    color: #333;
                                    text-align: center;
                                }}
                                table {{
                                    border-collapse: collapse;
                                    width: 100%;
                                    margin-bottom: 20px;
                                }}
                                th, td {{
                                    padding: 8px;
                                    text-align: left;
                                    border-bottom: 1px solid #ddd;
                                }}
                                th {{
                                    background-color: #f2f2f2;
                                }}
                                td:first-child {{
                                    font-weight: bold;
                                }}
                            </style>
                        </head>
                        <body>
                            <div class="invoice-container">
                                <h1>DDEEP CLEANING INVOICE</h1>
                                <h3>Use the following details for bank transfer payment</h3>
                                <h2>
                                    <p>Account Name: DDEEP CLEANING SERVICES</p>
                                    <p>Account Number: 73946439</p>
                                    <p>Sort Code: 04-03-70</p>
                                </h2>
                                
                                <h3>Customer Information:</h3>
                                <ul>
                                    <li>
                                        Name: {}
                                        <br>
                                        Address: {}
                                        <br>
                                        Email: {}
                                        <br>
                                        Phone Number: {}
                                        <br>
                                        Payment Method: {}
                                        <br>
                                        Rubbish Removal (5): {}
                                        <br>
                                        TOTAL: {}
                                        <br>

                                    </li>
                                </ul>

                                {}
                            </div>
                        </body>
                        </html>
                        """

                        def df_to_html_table(df):
                            table_html = "<table>"

                            # Add table header row
                            table_html += "<tr>"
                            for col in df.columns:
                                table_html += f"<th>{col}</th>"
                            table_html += "</tr>"
                            
                            for index, row in df.iterrows():
                                table_html += "<tr>"
                                for value in row:
                                    table_html += f"<td>{value}</td>"
                                table_html += "</tr>"
                            
                            table_html += "</table>"
                            return table_html

                        def df_to_html_tables(df, df2, name, address, email, num, payment_method,  rubbish_rem, net):
                            table1_html = df_to_html_table(df)
                            table2_html = df_to_html_table(df2)
                            
                            final_html = html_template.format(name, address, email, num, payment_method, rubbish_rem ,net, table1_html + table2_html)
                            return final_html


                        

                        final_html = df_to_html_tables(new_df, new_df_ext, name, address, email, num, payment_method, rubbish_rem,net)

                        smtp_server = "smtp.gmail.com"
                        smtp_port = 587
                        smtp_username = "clean@ddeepcleaningservices.com"
                        smtp_password = "acrmtrkgyezawleg"
                        email_from = "clean@ddeepcleaningservices.com"
                        email_to = 'fd92uk@gmail.com'
                        email_subject = "INVOICE@DDEEP CLEANING SERVICES"
                        email_body = "Thank you for choosing Ddeep Cleaning Services for your cleaning needs. We look forward to serving you again and exceeding your expectations. Please find attached your booking invoice."

                            # Create the email message
                        msg = MIMEMultipart()
                        msg['From'] = email_from
                        msg['To'] = email_to
                        msg['Subject'] = email_subject
                        msg.attach(MIMEText(email_body))

                            # Attach the HTML to the email
                        part = MIMEText(final_html, 'html')
                        part.add_header('Content-Disposition', 'attachment', filename="invoice.html")
                        msg.attach(part)
                        try:
                            smtp = smtplib.SMTP(smtp_server, smtp_port)
                            smtp.ehlo()
                            smtp.starttls()
                            smtp.login(smtp_username, smtp_password)
                            smtp.sendmail(email_from, email_to, msg.as_string())
                            smtp.quit()
                            st.success("Email sent successfully!")
                        except Exception as e:
                            st.error(f"Error sending email: {str(e)}")


                        button_placeholder.empty()


                        popup_message("Thanks for booking with Ddeep Cleaning Services. The booking details has been sent to the email you provided!")
                        time.sleep(5)  # Wait for 5 seconds



                        webbrowser.open_new_tab('http://localhost:8502/tc') 
                        

        #_____________________________________________________________________________________________________________________________________

        if inv == 'Send Quote by email':


            if button_placeholder.button(f' now  {inv}'):


                if not inv_email:
                    st.warning("email field cannot be empty")
                else:
                    inv_name_list.append(inv_name)
                    inv_address_list.append(inv_address)
                    inv_email_list.append(inv_email)

                    unique_id = generate_unique_id(inv_email)

                    
                    quote_info_df = pd.DataFrame({'name': inv_name,'addeess': inv_address_list, 'email': inv_email_list, 'id': unique_id, 'date': start_date_str, 'time':start_time_str})



                    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
                    credentials = ServiceAccountCredentials.from_json_keyfile_name(r'C:\Users\d\Downloads\service_account.json', scope)
                    client = gspread.authorize(credentials)

                    quote_info_sheet=client.open('db_try').worksheet('quote_info')
                    quote_summary=client.open('db_try').worksheet('quote_summary')


                    quote_info_data=quote_info_df.values.tolist()
                    quote_info_sheet.append_rows(quote_info_data)

                    values1 = new_df.values.tolist()

                    # Adding the unique ID to each row
                    for row in values1:
                        row.insert(0, unique_id)




                    quote_summary.append_rows(values1)

                    #__________________________________________________________________________________________________________________


                    html_template = """

                    <html>
                    <head>
                        <style>
                            body {{
                                font-family: Arial, sans-serif;
                                font-size: 14px;
                            }}
                            .invoice-container {{
                                width: 800px;
                                margin: 0 auto;
                                border: 1px solid #ccc;
                                padding: 20px;
                            }}
                            h1 {{
                                color: #333;
                                text-align: center;
                            }}
                            h2 {{
                                color: #333;
                                text-align: center;
                            }}
                            h3 {{
                                color: #333;
                                text-align: center;
                            }}
                            table {{
                                border-collapse: collapse;
                                width: 100%;
                                margin-bottom: 20px;
                            }}
                            th, td {{
                                padding: 8px;
                                text-align: left;
                                border-bottom: 1px solid #ddd;
                            }}
                            th {{
                                background-color: #f2f2f2;
                            }}
                            td:first-child {{
                                font-weight: bold;
                            }}
                        </style>
                    </head>
                    <body>
                        <div class="invoice-container">
                            <h1>DDEEP CLEANING INVOICE</h1>
                            <h3>Use the following details for bank transfer payment</h3>
                            <h2>
                                <p>Account Name: DDEEP CLEANING SERVICES</p>
                                <p>Account Number: 73946439</p>
                                <p>Sort Code: 04-03-70</p>
                            </h2>
                            
                            <h3>Customer Information:</h3>
                            <ul>
                                <li>
                                    Name: {}
                                    <br>
                                    Address: {}
                                    <br>
                                    Email: {}
                                    <br>
                                    Phone Number: {}
                                    
                                </li>
                            </ul>

                            {}
                        </div>
                    </body>
                    </html>
                    """

                    def df_to_html_tables(df, name, address, email, num):
                        # Create a table for each column
                        tables_html = ""
                        for col in df.columns:
                            rows = df[col].values.tolist()

                            # Create a new table with multiple rows
                            table_html = """
                            <table>
                                <tr>
                                    <th>{}</th>
                                </tr>
                            """.format(col)

                            for row in rows:
                                table_html += """
                                <tr>
                                    <td>{}</td>
                                </tr>
                                """.format(row)

                            table_html += "</table>"

                            # Append the table to the tables_html string
                            tables_html += table_html

                        # Insert the tables and customer information into the html string
                        final_html = html_template.format(name, address, email, num,  tables_html)

                        return final_html

                    final_html = df_to_html_tables(new_df, name, address, email, num)

                    smtp_server = "smtp.gmail.com"
                    smtp_port = 587
                    smtp_username = "clean@ddeepcleaningservices.com"
                    smtp_password = "acrmtrkgyezawleg"
                    email_from = "clean@ddeepcleaningservices.com"
                    email_to = 'fd92uk@gmail.com'
                    email_subject = "INVOICE@DDEEP CLEANING SERVICES"
                    email_body = "Thank you for choosing Ddeep Cleaning Services for your cleaning needs. We look forward to serving you again and exceeding your expectations. Please find attached your booking invoice."

                        # Create the email message
                    msg = MIMEMultipart()
                    msg['From'] = email_from
                    msg['To'] = email_to
                    msg['Subject'] = email_subject
                    msg.attach(MIMEText(email_body))

                        # Attach the HTML to the email
                    part = MIMEText(final_html, 'html')
                    part.add_header('Content-Disposition', 'attachment', filename="invoice.html")
                    msg.attach(part)
                    try:
                        smtp = smtplib.SMTP(smtp_server, smtp_port)
                        smtp.ehlo()
                        smtp.starttls()
                        smtp.login(smtp_username, smtp_password)
                        smtp.sendmail(email_from, email_to, msg.as_string())
                        smtp.quit()
                        st.success("Email sent successfully!")
                    except Exception as e:
                        st.error(f"Error sending email: {str(e)}")




                    button_placeholder.empty()


                    popup_message("Your quote has been sent to the email address you provided!")
                    time.sleep(5)  # Wait for 5 seconds



                    webbrowser.open_new_tab('http://localhost:8502/tc')   

    ############################################################################################################################################

    else:
        with st.form("example_form2", clear_on_submit=True):
            

            st.write("Please tell us about your property and which areas you need cleaning")

            # Add a text area for customer comments with a larger height
            customer_comment = st.text_area("Tell us about your property:", height=150)
            

            st.write('---')

            selected_start_date, selected_start_time = select_time_and_date()

            st.title('CONTACT DETAILS')



            st.write("Please enter your name, property address, and email:")
            inv_name1 = st.text_input("Enter Name")
            inv_address1 = st.text_input("Enter Property Address")
            inv_email1 = st.text_input("Enter Email to receive quote")
            
            
            additional_info = st.text_input("Please provide additional information")
            
            add_button = st.form_submit_button(label="SUBMIT")

        if add_button:



            if not inv_email1:
                st.warning("email field cannot be empty")
            else:

                inv_name_list1=[]
                inv_address_list1=[]
                inv_email_list1=[]
                customer_comment_list=[]





                inv_name_list1.append(inv_name1)
                inv_address_list1.append(inv_address1)
                inv_email_list1.append(inv_email1)
                customer_comment_list.append(customer_comment)
                unique_id1 = generate_unique_id(inv_email1)

                
                quote_info_df1 = pd.DataFrame({'name': inv_name1,'addeess': inv_address_list1, 'email': inv_email_list1, 'id': unique_id1, 'date': selected_start_date, 'time':selected_start_time, 'det': customer_comment_list})



                scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
                credentials = ServiceAccountCredentials.from_json_keyfile_name(r'C:\Users\d\Downloads\service_account.json', scope)
                client = gspread.authorize(credentials)

                quote_info_sheet=client.open('db_try').worksheet('quote_info_comm')
                #quote_summary=client.open('db_try').worksheet('quote_summary')


                quote_info_data1=quote_info_df1.values.tolist()
                quote_info_sheet.append_rows(quote_info_data1)

                #values1 = new_df.values.tolist()

                # Adding the unique ID to each row
                #for row in values1:
                #    row.insert(0, unique_id)




                #quote_summary.append_rows(values1)


            popup_message("Thanks for booking with Ddeep Cleaning Services. We will contact you shortly with a quote!")
        
            time.sleep(5)  # Wait for 5 seconds

            #webbrowser.open_new_tab(https://www.youtube.com/watch?v=_Um12_OlGgw)                   


    #build dataframe for price calculation






########################################################################################################
########################################################################################################
else:





    right_col2, left_col2 =st.columns(2)

        #option = st.selectbox("Select an option", ["Option 1", "Option 2"])
    if option_services in ['House', 'Flat']:

        quantities = {}
        quantity_carpet = None
        toilet_condition = None  
        with right_col2:
            option_pro = st.selectbox('Select areas of the property that needs cleaning', options)
            #quantity = st.number_input(f'Quantity for {option_pro}:', key=f'{option_pro}_quantity', min_value=0, value=0, step=1)
            #quantity_carpet= st.radio(f'Do you want carpet wash and dry {option_pro}:', yesno, key=f'{option_pro}_carpet')
        if option_pro:
            with left_col2:
                quantity = st.number_input(f'Quantity for {option_pro}:', min_value=0, value=0, step=1)
            quantities[option_pro] = quantity

            if option_pro == 'Kitchen':
                
                for sub_option in kitchen_opt:
                    sub_quantity = st.number_input(f'Quantity for {sub_option}:', min_value=0, value=0, step=1)
                    if sub_quantity > 0:
                        quantities[f'{sub_option}'] = sub_quantity

            elif option_pro in ['Bathroom', 'Seperate Toilet']:
                toilet_condition= st.radio(f'Presence of feces outside the toilet {option_pro}:', yesno)
                condition_toilet.append(toilet_condition)


            else:
                quantity_carpet= st.radio(f'Do you want carpet wash and dry in the {option_pro}:', yesno)
                carpet_cleaning.append(quantity_carpet)

                    
            submit_button = st.button('Add option')
            if submit_button:
                selected_options = st.session_state.get('selected_options', [])
                selected_choice = st.session_state.get('selected_choice', [])
                selected_quantity =st.session_state.get('selected_quantity', [])
                selected_unitprice= st.session_state.get('selected_unitprice', [])

                
                
                for option, quantity in quantities.items():
                    if quantity > 0:
                        unitprice = prices.loc[prices['Item'] == option, 'Price'].values[0]





    # Check if the option already exists in the list
                        # Check if the option already exists in the list

                        # Check if the option already exists in the list
                        
                        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        selected_options.append(f'{option} x ({quantity})  carpet-({quantity_carpet}) - £{unitprice}) human_feces-({toilet_condition}) ({timestamp})')
                        selected_choice.append(f'{option}, {unitprice}')
                        selected_quantity.append(f'{quantity}')
                        selected_unitprice.append(f'{unitprice}')
                                            
                        st.session_state.selected_options = selected_options or [] # initialize with an empty list if it doesn't exist
                        st.session_state.selected_choice = selected_choice or []
                        st.session_state.selected_quantity = selected_quantity
                        st.session_state.selected_unitprice = selected_unitprice

                        scope= ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
                        credentials=ServiceAccountCredentials.from_json_keyfile_name(r'C:\Users\d\Downloads\service_account.json', scope)
                        client=gspread.authorize(credentials)
                        sheet=client.open('db_try').worksheet('Sheet1')

                        # Append the data to the Google Sheet
                        data_to_append = list(zip(selected_options, selected_choice, selected_quantity, selected_unitprice))
                        sheet.append_rows(data_to_append)

                        # Optional: Clear the session_state variables after updating the Google Sheet
                        data_to_append = []
                        

                # add receipt data to dataframe            
                


        st.write(f"You selected {st.session_state.selected_options}!")

    ##################################################################################################################################
    #___________________________________________________________________________________________________________________
        rubbish_rem, sofa_clean, quantity_su=display_extras()


        for option, quantity in quantity_su.items():
            if quantity > 0:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


                unitprice = prices.loc[prices['Item'] == option, 'Price'].values[0]
            selected_options_extr.append(f'{option} x ({quantity}) - £{unitprice}) Rubbish Removal-({rubbish_rem}) ({timestamp})')
            st.session_state.selected_options_extr = selected_options_extr
        

        st.session_state.selected_options_extr = selected_options_extr

        #st.write(selected_options_extr)
    ###########################################################################################################################################
        #______________________________________________________________________________________________________________________________________


        removed_options = []

        # Assuming you already have the selected_options in session_state
        selected_options = st.session_state.get('selected_options', [])

        # Create checkboxes for each option to allow the user to select options to remove
        for option in selected_options:
            removed = st.sidebar.checkbox(f"Remove '{option}'", key=f"remove_{option}")
            if removed:
                removed_options.append(option)

        # Remove the selected options from the selected_options list
        selected_options = [option for option in selected_options if option not in removed_options]

        # Update the session_state with the modified selected_options list
        st.session_state.selected_options = selected_options
        st.sidebar.write('---')

    #___________________________________________________________________________________________________________________________

    #-----------------------------------------------------------------------------------------------------------

    ###############################################################################################################################################
        

        
    #start_date_str = start_date.strftime("%Y-%m-%d")
    #start_time_str = start_time.strftime("%H:%M:%S")


    #_______________________________________________________________________________________________________

        st.title('BOOKING SUMMARY')

        preferences_df1 = shift_preferences()

        # Get the row count using the shape attribute
        row_count = preferences_df1.shape[0]
        st.write(row_count)



        discount_code=st.text_input('Insert discount code')

        
        item_list=[]
        for item in st.session_state.selected_options:
            match = re.search(r'\b(' + '|'.join(prices['Item']) + r')\b', item)
            if match:
                item_list.append(match.group())
        
                

        # Create an empty list to store the extracted values
        extracted_values = []
        for x in item_list:
            unitprice1 = prices.loc[prices['Item'] == x, 'Price'].values[0]
            extracted_values.append(int(unitprice1))

        extracted_quantity = []

        for eachquantity in st.session_state.selected_options:
            # Extract the value using regular expressions to find the numbers inside parentheses
            match_quantity = re.search(r'\((\d+)\)', eachquantity)
            if match_quantity:
                extracted_quant = match_quantity.group(1)
                extracted_quantity.append(int(extracted_quant))

        extracted_carpet = []

        for xa in st.session_state.selected_options:
            if 'carpet-(Yes)' in xa:
                match_xa = re.search(r'\b(\d+)\b', xa)
                if match_xa:
                    quantity_xa = match_xa.group(1)
                    extracted_quantity_xa = int(quantity_xa) * 20
                    extracted_carpet.append(extracted_quantity_xa)
            else:
                extracted_carpet.append(int(0))


        extracted_toilet = []

        for xb in st.session_state.selected_options:
            if 'human_feces-(Yes)' in xb:
                match_xa = re.search(r'\b(\d+)\b', xb)
                if match_xa:
                    quantity_xa = match_xa.group(1)
                    extracted_quantity_xa = int(quantity_xa) * 20
                    extracted_toilet.append(extracted_quantity_xa)
            else:
                extracted_toilet.append(int(0))


        #_____________________________________________________________________________________________________________________________

        item_list_ext=[]
        for item in st.session_state.selected_options_extr:
            match = re.search(r'\b(' + '|'.join(prices['Item']) + r')\b', item)
            if match:
                item_list_ext.append(match.group())        

        # Create an empty list to store the extracted values
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

        #_______________________________________________________________________________________________________________________________-
        # Create a new DataFrame using the extracted values list
        new_df_reg = pd.DataFrame({'Item': item_list,'unit_price': extracted_values, 'quantity': extracted_quantity, 'carpet_price': extracted_carpet, 'toilet_condition':extracted_toilet})

        new_df_ext_reg = pd.DataFrame({'Item': item_list_ext,'unit_price': extracted_values_ext, 'quantity': extracted_quantity_ext})


        #____________________________________________________________________________________________________________________________________________________________________________

        #for option in st.session_state.selected_options:
        #    st.sidebar.write(f'- {option}')

        for option in st.session_state.selected_options_extr:

            st.sidebar.write(f'- {option}')

        if option_services in ['House', 'Flat']:

            if rubbish_rem== 'No':

                rubbish_rem_price=0
            
            else:
                rubbish_rem_price=10
                st.sidebar.write(f'- Rubbish Removal-{rubbish_rem} {rubbish_rem_price}')

        #__________________________________________________________________________________________________________________________________


        def calculate_total(new_df):
            total = 0
            for i, row in new_df.iterrows():
                total += (row['unit_price'] * row['quantity']) + row['carpet_price'] 
            return total


        def calculate_total_ext(new_df):
            total_ext = 0
            for i, row in new_df.iterrows():
                total_ext += (row['unit_price'] * row['quantity'])
            return total_ext






        discount_dict = {'discount_code': ['ten', 'twenty'], 
                    'discount_amount': [10, 20]}

        discount_table = pd.DataFrame(discount_dict)


        if discount_code in discount_table['discount_code'].values:
            discount_tot = discount_table.loc[discount_table['discount_code'] == discount_code, 'discount_amount'].values[0]
        else:
            discount_tot = 0


        total = calculate_total(new_df_reg)
        tot_ext = calculate_total_ext(new_df_ext_reg)



        if row_count== 0:
            total_amount= (total+tot_ext+rubbish_rem_price)
        else:
            total_amount= (total+tot_ext+rubbish_rem_price)*row_count


        

        

        net=total_amount-(discount_tot/100)*total_amount

        if row_count== 0:
            preferences_df1['Amount'] = net
        else:
            preferences_df1['Amount'] = net/row_count


        st.write(preferences_df1)
        st.write(new_df_reg)
        st.write(new_df_ext_reg)
        st.write(f'<p style="font-size: 34px;">FIRST PAYMENT TOTAL: {net:.2f}</p>', unsafe_allow_html=True)

        #for x in st.session_state.new_list:
        #    st.sidebar.write(f'{x}')

        st.sidebar.markdown('### Applied Discount:')


        st.sidebar.markdown(f'**${(discount_tot/100)*total_amount:.2f}**')
        st.sidebar.markdown('### Net Total:')
        st.sidebar.markdown(f'<p style="font-size: 34px;">£{net:.2f}</p>', unsafe_allow_html=True)


        st.write('---')
    #############################################################################################################################################
        
        # Call the function to display the time and date selection and get the selected values
        start_date_str1, start_time_str1 = select_start_time_and_date()

        st.write('---')


    #########################################################################################################################################
        st.write('---')

        st.title('CONTACT DETAILS')

        inv = st.radio("", ["Book Now", "Send Quote by email"])


        if inv == 'Book Now':
            name, address, post_code,email, num, payment_method, terms_and_conditions = display_book() 
        else:
            inv_name, inv_address, inv_email,  = display_quote()



        button_placeholder = st.empty()

    #__________________________________________________________________________________________________________________________________

        if inv == 'Book Now':
            if payment_method == 'Card':
                if button_placeholder.button(f' click to  {inv}'):

                    if not address or not post_code or not email or not terms_and_conditions:
                        st.warning("Property address, post code and email fields cannot be empty")
                    else:
                        
                        name_list.append(name)
                        address_list.append(address)
                        post_code_list.append(post_code)
                        email_list.append(email)
                        num_list.append(num)
                        payment_method_list.append(payment_method)
                        #option_services1_list.append(option_services1)
                        
                        unique_id = generate_unique_id(email)
                        reg_cleaning_pers_df = pd.DataFrame({'name': name_list,'addeess': address_list, 'post_code':post_code_list,'email': email_list, 'contact_number': num_list, 'payment_method': payment_method_list, 'id': unique_id, 'date': start_date_str1, 'time':start_time_str1, 'property_type': option_services, 'service_type': option_services2, 'Rubbish Removal':rubbish_rem, 'Total':net})

    #___________________________________________________________________________________________________________________________________
                                    #write into sheets

                        reg_cleaning_sheet=client.open('db_try').worksheet('reg_cleaning')
                        reg_cleaning_sheet_data = new_df_reg.values.tolist()
                        reg_cleaning_sheet_data2= new_df_ext_reg.values.tolist()
                        reg_cleaning_sheet.append_rows(reg_cleaning_sheet_data)
                        reg_cleaning_sheet.append_rows(reg_cleaning_sheet_data2)

                        reg_cleaning_pers_sheet=client.open('db_try').worksheet('reg_cleaning_pers')
                        reg_cleaning_pers_df_data=reg_cleaning_pers_df.values.tolist()
                        reg_cleaning_pers_sheet.append_rows(reg_cleaning_pers_df_data)


                        reg_cleaning_hours_sheet=client.open('db_try').worksheet('reg_cleaning_hours')
                        reg_cleaning_hours_df_data=preferences_df1.values.tolist()
                        for row in reg_cleaning_hours_df_data:
                            row.insert(0, unique_id)
                        reg_cleaning_hours_sheet.append_rows(reg_cleaning_hours_df_data)

                        


                        html_template = """
                        <html>
                        <head>
                            <style>
                                body {{
                                    font-family: Arial, sans-serif;
                                    font-size: 14px;
                                }}
                                .invoice-container {{
                                    width: 800px;
                                    margin: 0 auto;
                                    border: 1px solid #ccc;
                                    padding: 20px;
                                }}
                                h1 {{
                                    color: #333;
                                    text-align: center;
                                }}
                                h2 {{
                                    color: #333;
                                    text-align: center;
                                }}
                                h3 {{
                                    color: #333;
                                    text-align: center;
                                }}
                                table {{
                                    border-collapse: collapse;
                                    width: 100%;
                                    margin-bottom: 20px;
                                }}
                                th, td {{
                                    padding: 8px;
                                    text-align: left;
                                    border-bottom: 1px solid #ddd;
                                }}
                                th {{
                                    background-color: #f2f2f2;
                                }}
                                td:first-child {{
                                    font-weight: bold;
                                }}
                            </style>
                        </head>
                        <body>
                            <div class="invoice-container">
                                <h1>DDEEP CLEANING INVOICE</h1>
                                <h3>Use the following details for bank transfer payment</h3>
                                <h2>
                                    <p>Account Name: DDEEP CLEANING SERVICES</p>
                                    <p>Account Number: 73946439</p>
                                    <p>Sort Code: 04-03-70</p>
                                </h2>
                                
                                <h3>Customer Information:</h3>
                                <ul>
                                    <li>
                                        Name: {}
                                        <br>
                                        Address: {}
                                        <br>
                                        Post COde: {}
                                        <br>
                                        Email: {}
                                        <br>
                                        Phone Number: {}
                                        <br>
                                        Payment Method: {}
                                        <br>
                                        Rubbish Removal (£5): {}
                                        <br>
                                        TOTAL: {}
                                        <br>

                                    </li>
                                </ul>

                                {}
                            </div>
                        </body>
                        </html>
                        """

                        def df_to_html_table(df):
                            table_html = "<table>"

                            # Add table header row
                            table_html += "<tr>"
                            for col in df.columns:
                                table_html += f"<th>{col}</th>"
                            table_html += "</tr>"
                            
                            for index, row in df.iterrows():
                                table_html += "<tr>"
                                for value in row:
                                    table_html += f"<td>{value}</td>"
                                table_html += "</tr>"
                            
                            table_html += "</table>"
                            return table_html

                        def df_to_html_tables(df, df2, name, address, post_code ,email, num, payment_method, net, rubbish_rem):
                            table1_html = df_to_html_table(df)
                            table2_html = df_to_html_table(df2)
                            
                            final_html = html_template.format(name, address, post_code,email, num, payment_method, rubbish_rem ,net, table1_html + table2_html)
                            return final_html

                        final_html = df_to_html_tables(new_df_reg, preferences_df1, name, address, post_code,email, num, payment_method, net, rubbish_rem)

                        smtp_server = "smtp.gmail.com"
                        smtp_port = 587
                        smtp_username = "clean@ddeepcleaningservices.com"
                        smtp_password = "acrmtrkgyezawleg"
                        email_from = "clean@ddeepcleaningservices.com"
                        email_to = 'fd92uk@gmail.com'
                        email_subject = "INVOICE@DDEEP CLEANING SERVICES"
                        email_body = "Thank you for choosing Ddeep Cleaning Services for your cleaning needs. We look forward to serving you again and exceeding your expectations. Please find attached your booking invoice."

                            # Create the email message
                        msg = MIMEMultipart()
                        msg['From'] = email_from
                        msg['To'] = email_to
                        msg['Subject'] = email_subject
                        msg.attach(MIMEText(email_body))

                            # Attach the HTML to the email
                        part = MIMEText(final_html, 'html')
                        part.add_header('Content-Disposition', 'attachment', filename="invoice.html")
                        msg.attach(part)
                        try:
                            smtp = smtplib.SMTP(smtp_server, smtp_port)
                            smtp.ehlo()
                            smtp.starttls()
                            smtp.login(smtp_username, smtp_password)
                            smtp.sendmail(email_from, email_to, msg.as_string())
                            smtp.quit()
                            st.success("Email sent successfully!")
                        except Exception as e:
                            st.error(f"Error sending email: {str(e)}")

                        net_in_stripe_format = int(net * 100)
                        payment_link_url = create_payment_link(net_in_stripe_format, currency="gbp", success_url="https://example.com/success", cancel_url="https://example.com/cancel")  # Replace this with the actual function call to create the payment link
                        
                        button_placeholder.empty()


                        popup_message("Thanks for booking with Ddeep Cleaning Services. You will now be directed to a new page to complete your booking!")
                        time.sleep(5)  # Wait for 5 seconds

                        webbrowser.open_new_tab(payment_link_url)                   
            

            else:

                if button_placeholder.button(f' click to  {inv}'):


                    if not address or not post_code or not email or not terms_and_conditions:
                        st.warning("Property address, post code and email fields cannot be empty")
                    else:
                        
                        name_list.append(name)
                        address_list.append(address)
                        post_code_list.append(post_code)
                        email_list.append(email)
                        num_list.append(num)
                        payment_method_list.append(payment_method)
                        #option_services1_list.append(option_services1)
                        
                        unique_id = generate_unique_id(email)
                        reg_cleaning_pers_df = pd.DataFrame({'name': name_list,'addeess': address_list, 'post_code':post_code_list,'email': email_list, 'contact_number': num_list, 'payment_method': payment_method_list, 'id': unique_id, 'date': start_date_str1, 'time':start_time_str1, 'property_type': option_services, 'service_type': option_services2, 'Rubbish Removal':rubbish_rem, 'Total':net})

    #___________________________________________________________________________________________________________________________________
                                    #write into sheets

                        reg_cleaning_sheet=client.open('db_try').worksheet('reg_cleaning')
                        reg_cleaning_sheet_data = new_df_reg.values.tolist()
                        reg_cleaning_sheet_data2= new_df_ext_reg.values.tolist()
                        reg_cleaning_sheet.append_rows(reg_cleaning_sheet_data)
                        reg_cleaning_sheet.append_rows(reg_cleaning_sheet_data2)

                        reg_cleaning_pers_sheet=client.open('db_try').worksheet('reg_cleaning_pers')
                        reg_cleaning_pers_df_data=reg_cleaning_pers_df.values.tolist()
                        reg_cleaning_pers_sheet.append_rows(reg_cleaning_pers_df_data)


                        reg_cleaning_hours_sheet=client.open('db_try').worksheet('reg_cleaning_hours')
                        reg_cleaning_hours_df_data=preferences_df1.values.tolist()
                        for row in reg_cleaning_hours_df_data:
                            row.insert(0, unique_id)
                        reg_cleaning_hours_sheet.append_rows(reg_cleaning_hours_df_data)

                        html_template = """
                        <html>
                        <head>
                            <style>
                                body {{
                                    font-family: Arial, sans-serif;
                                    font-size: 14px;
                                }}
                                .invoice-container {{
                                    width: 800px;
                                    margin: 0 auto;
                                    border: 1px solid #ccc;
                                    padding: 20px;
                                }}
                                h1 {{
                                    color: #333;
                                    text-align: center;
                                }}
                                h2 {{
                                    color: #333;
                                    text-align: center;
                                }}
                                h3 {{
                                    color: #333;
                                    text-align: center;
                                }}
                                table {{
                                    border-collapse: collapse;
                                    width: 100%;
                                    margin-bottom: 20px;
                                }}
                                th, td {{
                                    padding: 8px;
                                    text-align: left;
                                    border-bottom: 1px solid #ddd;
                                }}
                                th {{
                                    background-color: #f2f2f2;
                                }}
                                td:first-child {{
                                    font-weight: bold;
                                }}
                            </style>
                        </head>
                        <body>
                            <div class="invoice-container">
                                <h1>DDEEP CLEANING INVOICE</h1>
                                <h3>Use the following details for bank transfer payment</h3>
                                <h2>
                                    <p>Account Name: DDEEP CLEANING SERVICES</p>
                                    <p>Account Number: 73946439</p>
                                    <p>Sort Code: 04-03-70</p>
                                </h2>
                                
                                <h3>Customer Information:</h3>
                                <ul>
                                    <li>
                                        Name: {}
                                        <br>
                                        Address: {}
                                        <br>
                                        Post COde: {}
                                        <br>
                                        Email: {}
                                        <br>
                                        Phone Number: {}
                                        <br>
                                        Payment Method: {}
                                        <br>
                                        Rubbish Removal (£5): {}
                                        <br>
                                        TOTAL: {}
                                        <br>

                                    </li>
                                </ul>

                                {}
                            </div>
                        </body>
                        </html>
                        """

                        def df_to_html_table(df):
                            table_html = "<table>"

                            # Add table header row
                            table_html += "<tr>"
                            for col in df.columns:
                                table_html += f"<th>{col}</th>"
                            table_html += "</tr>"
                            
                            for index, row in df.iterrows():
                                table_html += "<tr>"
                                for value in row:
                                    table_html += f"<td>{value}</td>"
                                table_html += "</tr>"
                            
                            table_html += "</table>"
                            return table_html

                        def df_to_html_tables(df, df2, name, address, post_code ,email, num, payment_method, net, rubbish_rem):
                            table1_html = df_to_html_table(df)
                            table2_html = df_to_html_table(df2)
                            
                            final_html = html_template.format(name, address, post_code,email, num, payment_method, rubbish_rem ,net, table1_html + table2_html)
                            return final_html

                        final_html = df_to_html_tables(new_df_reg, preferences_df1, name, address, post_code,email, num, payment_method, net, rubbish_rem)

                        smtp_server = "smtp.gmail.com"
                        smtp_port = 587
                        smtp_username = "clean@ddeepcleaningservices.com"
                        smtp_password = "acrmtrkgyezawleg"
                        email_from = "clean@ddeepcleaningservices.com"
                        email_to = 'fd92uk@gmail.com'
                        email_subject = "INVOICE@DDEEP CLEANING SERVICES"
                        email_body = "Thank you for choosing Ddeep Cleaning Services for your cleaning needs. We look forward to serving you again and exceeding your expectations. Please find attached your booking invoice."

                            # Create the email message
                        msg = MIMEMultipart()
                        msg['From'] = email_from
                        msg['To'] = email_to
                        msg['Subject'] = email_subject
                        msg.attach(MIMEText(email_body))

                            # Attach the HTML to the email
                        part = MIMEText(final_html, 'html')
                        part.add_header('Content-Disposition', 'attachment', filename="invoice.html")
                        msg.attach(part)
                        try:
                            smtp = smtplib.SMTP(smtp_server, smtp_port)
                            smtp.ehlo()
                            smtp.starttls()
                            smtp.login(smtp_username, smtp_password)
                            smtp.sendmail(email_from, email_to, msg.as_string())
                            smtp.quit()
                            st.success("Email sent successfully!")
                        except Exception as e:
                            st.error(f"Error sending email: {str(e)}")

                        net_in_stripe_format = int(net * 100)
                        payment_link_url = create_payment_link(net_in_stripe_format, currency="gbp", success_url="https://example.com/success", cancel_url="https://example.com/cancel")  # Replace this with the actual function call to create the payment link
                        
                        button_placeholder.empty()
                        popup_message("Thanks for booking with Ddeep Cleaning Services. The booking details has been sent to the email you provided!")
                        time.sleep(5)  # Wait for 5 seconds
                        webbrowser.open_new_tab('http://localhost:8502/tc') 
                    
        #_____________________________________________________________________________________________________________________________________

        if inv == 'Send Quote by email':
            if button_placeholder.button(f' now  {inv}'):
                if not inv_email:
                    st.warning("email field cannot be empty")
                else:
                    inv_name_list.append(inv_name)
                    inv_address_list.append(inv_address)
                    inv_email_list.append(inv_email)

                    unique_id = generate_unique_id(inv_email)
                    quote_info_df = pd.DataFrame({'name': inv_name,'addeess': inv_address_list, 'email': inv_email_list, 'id': unique_id, 'date': start_date_str1, 'time':start_time_str1})

                    quote_info_sheet=client.open('db_try').worksheet('quote_info_reg')
                    quote_info_data=quote_info_df.values.tolist()
                    quote_info_sheet.append_rows(quote_info_data)

                    quote_summary=client.open('db_try').worksheet('quote_summary_reg')
                    values1 = new_df_reg.values.tolist()
                    values2= new_df_ext_reg.values.tolist()

                    # Adding the unique ID to each row
                    for row in values1:
                        row.insert(0, unique_id)
                    
                    for row in values2:
                        row.insert(0, unique_id)

                    quote_summary.append_rows(values1)
                    quote_summary.append_rows(values2)

                    reg_cleaning_hours_quote_sheet=client.open('db_try').worksheet('reg_cleaning_hours_quote')
                    values3=preferences_df1.values.tolist()
                    for row in values3:
                        row.insert(0, unique_id)
                    reg_cleaning_hours_quote_sheet.append_rows(values3)

                    #__________________________________________________________________________________________________________________


                    html_template = """

                    <html>
                    <head>
                        <style>
                            body {{
                                font-family: Arial, sans-serif;
                                font-size: 14px;
                            }}
                            .invoice-container {{
                                width: 800px;
                                margin: 0 auto;
                                border: 1px solid #ccc;
                                padding: 20px;
                            }}
                            h1 {{
                                color: #333;
                                text-align: center;
                            }}
                            h2 {{
                                color: #333;
                                text-align: center;
                            }}
                            h3 {{
                                color: #333;
                                text-align: center;
                            }}
                            table {{
                                border-collapse: collapse;
                                width: 100%;
                                margin-bottom: 20px;
                            }}
                            th, td {{
                                padding: 8px;
                                text-align: left;
                                border-bottom: 1px solid #ddd;
                            }}
                            th {{
                                background-color: #f2f2f2;
                            }}
                            td:first-child {{
                                font-weight: bold;
                            }}
                        </style>
                    </head>
                    <body>
                        <div class="invoice-container">
                            <h1>DDEEP CLEANING INVOICE</h1>
                            <h3>Use the following details for bank transfer payment</h3>
                            <h2>
                                <p>Account Name: DDEEP CLEANING SERVICES</p>
                                <p>Account Number: 73946439</p>
                                <p>Sort Code: 04-03-70</p>
                            </h2>
                            
                            <h3>Customer Information:</h3>
                            <ul>
                                <li>
                                    Name: {}
                                    <br>
                                    Address: {}
                                    <br>
                                    Email: {}
                                    <br>
                                    Rubbish Removal: {}
                                    <br>
                                    Total: {}
                                    <br>
                                    
                                </li>
                            </ul>

                            {}
                        </div>
                    </body>
                    </html>
                    """

                    def df_to_html_table(df):
                            
                            table_html = "<table>"

                            # Add table header row
                            table_html += "<tr>"
                            for col in df.columns:
                                table_html += f"<th>{col}</th>"
                            table_html += "</tr>"
                            
                            for index, row in df.iterrows():
                                table_html += "<tr>"
                                for value in row:
                                    table_html += f"<td>{value}</td>"
                                table_html += "</tr>"
                            
                            table_html += "</table>"
                            return table_html

                    def df_to_html_tables(df, df2, name, address,email,  rubbish_rem, net):
                        table1_html = df_to_html_table(df)
                        table2_html = df_to_html_table(df2)
                        
                        final_html = html_template.format(name, address, email , rubbish_rem, net,table1_html + table2_html)
                        return final_html

                    final_html = df_to_html_tables(new_df_reg, preferences_df1, inv_name, inv_address,inv_email, rubbish_rem, net)

                    smtp_server = "smtp.gmail.com"
                    smtp_port = 587
                    smtp_username = "clean@ddeepcleaningservices.com"
                    smtp_password = "acrmtrkgyezawleg"
                    email_from = "clean@ddeepcleaningservices.com"
                    email_to = 'fd92uk@gmail.com'
                    email_subject = "INVOICE@DDEEP CLEANING SERVICES"
                    email_body = "Thank you for choosing Ddeep Cleaning Services for your cleaning needs. We look forward to serving you again and exceeding your expectations. Please find attached your booking invoice."

                        # Create the email message
                    msg = MIMEMultipart()
                    msg['From'] = email_from
                    msg['To'] = email_to
                    msg['Subject'] = email_subject
                    msg.attach(MIMEText(email_body))

                        # Attach the HTML to the email
                    part = MIMEText(final_html, 'html')
                    part.add_header('Content-Disposition', 'attachment', filename="invoice.html")
                    msg.attach(part)
                    try:
                        smtp = smtplib.SMTP(smtp_server, smtp_port)
                        smtp.ehlo()
                        smtp.starttls()
                        smtp.login(smtp_username, smtp_password)
                        smtp.sendmail(email_from, email_to, msg.as_string())
                        smtp.quit()
                        st.success("Email sent successfully!")
                    except Exception as e:
                        st.error(f"Error sending email: {str(e)}")

                    button_placeholder.empty()
                    popup_message("Your quote has been sent to the email address you provided!")
                    time.sleep(5)  # Wait for 5 seconds

                    webbrowser.open_new_tab('http://localhost:8502/tc')   

    ############################################################################################################################################

    else:
        preferences_df = shift_preferences()
        st.write(preferences_df)

        with st.form("example_form2", clear_on_submit=True):
            

            st.write("Please tell us about your property and which areas you need cleaning")

            # Add a text area for customer comments with a larger height
            customer_comment = st.text_area("Tell us about your property:", height=150)
            

            st.write('---')

            selected_start_date, selected_start_time = select_time_and_date()
            


            st.title('CONTACT DETAILS')



            st.write("Please enter your name, property address, and email:")
            inv_name1 = st.text_input("Enter Name")
            inv_address1 = st.text_input("Enter Property Address")
            inv_email1 = st.text_input("Enter Email to receive quote")
            
            
            additional_info = st.text_input("Please provide additional information")
            
            add_button = st.form_submit_button(label="SUBMIT")

        if add_button: 
            if not inv_email1:
                st.warning("email field cannot be empty")
            else:

                inv_name_list1=[]
                inv_address_list1=[]
                inv_email_list1=[]
                customer_comment_list=[]

                inv_name_list1.append(inv_name1)
                inv_address_list1.append(inv_address1)
                inv_email_list1.append(inv_email1)
                customer_comment_list.append(customer_comment)
                unique_id1 = generate_unique_id(inv_email1)
                quote_info_df1 = pd.DataFrame({'name': inv_name1,'addeess': inv_address_list1, 'email': inv_email_list1, 'id': unique_id1, 'date': selected_start_date, 'time':selected_start_time, 'det': customer_comment_list})

                quote_info_sheet=client.open('db_try').worksheet('quote_info_comm')
                reg=client.open('db_try').worksheet('Sheet16')

                quote_info_data1=quote_info_df1.values.tolist()
                quote_info_sheet.append_rows(quote_info_data1)

                valuesreg = preferences_df.values.tolist()

                # Adding the unique ID to each row
                for row in valuesreg:
                    row.insert(0, unique_id1)

                reg.append_rows(valuesreg)

                popup_message("Thanks for booking with Ddeep Cleaning Services. We will contact you shortly with a quote!")
            
                time.sleep(5)  # Wait for 5 seconds

    


