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



st.write('You selected')
