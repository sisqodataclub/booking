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


custom_css = """
<style>
    /* Add your CSS styles here */
    body {
        font-family: Arial, sans-serif;
        line-height: 1.6;
        margin: 20px;
    }
    
    h2 {
        color: #333;
        font-size: 24px;
        margin-top: 20px;
    }

    p {
        color: #666;
        font-size: 16px;
    }

    ul {
        list-style: disc;
        margin-left: 20px;
    }

    /* Add more styles as needed */
</style>
"""

# Markdown content
terms_and_conditions = """
# Terms and Conditions

Welcome to the Terms and Conditions policy for D deep Cleaning services. We are committed to providing high-quality cleaning services to our valued customers, and this policy outlines the terms and conditions that govern our services. By using our services, via email, phone, or online booking, you agree to be bound by these terms and conditions, so please read them carefully before placing an order.

We take our legal obligations seriously and are committed to ensuring that our policies and procedures are in compliance with all applicable UK laws and regulations. If you have any questions or concerns about our policy or its compliance with UK law, please do not hesitate to contact us.

## Service Terms and Conditions

### General Terms and Condition and Pricing

Our pricing is determined by the complexity of the job and the estimated time required to complete the service. We take into consideration factors such as the size of the area to be cleaned, the level of dirt or grime buildup, and any special requirements or requests you may have. Our goal is to provide you with an accurate and fair price that reflects the complexity of the job and the level of service you expect from us.

We reserve the right to adjust our initial quotation if upon inspection of the property or during the cleaning process, we determine that the job will require more time to complete than initially estimated, or if the Customer's original requirements change. Any additional charges for bedrooms larger than 20 square meters and living rooms larger than 40 square meters will be discussed with the Customer before the commencement of the cleaning service. Any revised price will be communicated to the Customer and will have to be accepted before any additional cleaning time is carried out. If any information about the property that may affect the duration or cost of the cleaning is withheld during the booking, we reserve the right to adjust the quotation to include it in the price. We will communicate any changes to the Customer as soon as possible and obtain their approval before proceeding with the cleaning services.

If the Customer is more than 30 minutes late for the scheduled cleaning service, the Company reserves the right to cancel the service or impose a late fee of £20.

### Cancellations and Reschedule

The Customer may cancel their booking without incurring any charges if they provide notice of cancellation at least 48 hours prior to the scheduled start time of the service. However, if the Customer cancels their booking within 48 hours of the scheduled start time, they will be subject to a cancellation fee of 20% of the total booking amount. The Company reserves the right to waive the cancellation fee at its discretion in exceptional circumstances.

We reserve the right to cancel or reschedule a service in cases where an accident or other unexpected event has affected the assigned cleaning team. If such an event occurs, we will make every effort to inform you as soon as possible and offer alternative arrangements that suit your needs.

We request a 24-hour notice for rescheduling your booking so that we can make alternative arrangements and avoid any inconvenience. For amendments in less than 24 hours, there is a 10% fee payable.

The Customer can reschedule or cancel the appointment over the phone or in writing by email.
"""

# Display custom HTML with CSS
st.markdown(custom_css, unsafe_allow_html=True)
st.markdown(terms_and_conditions, unsafe_allow_html=True)
