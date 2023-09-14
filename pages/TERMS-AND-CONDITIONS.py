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

## General Terms and Condition and Pricing

Our pricing is determined by the complexity of the job and the estimated time required to complete the service. We take into consideration factors such as the size of the area to be cleaned, the level of dirt or grime buildup, and any special requirements or requests you may have. Our goal is to provide you with an accurate and fair price that reflects the complexity of the job and the level of service you expect from us.

We reserve the right to adjust our initial quotation if upon inspection of the property or during the cleaning process, we determine that the job will require more time to complete than initially estimated, or if the Customer's original requirements change. Any additional charges for bedrooms larger than 20 square meters and living rooms larger than 40 square meters will be discussed with the Customer before the commencement of the cleaning service. Any revised price will be communicated to the Customer and will have to be accepted before any additional cleaning time is carried out. If any information about the property that may affect the duration or cost of the cleaning is withheld during the booking, we reserve the right to adjust the quotation to include it in the price. We will communicate any changes to the Customer as soon as possible and obtain their approval before proceeding with the cleaning services.

If the Customer is more than 30 minutes late for the scheduled cleaning service, the Company reserves the right to cancel the service or impose a late fee of £20.

### Cancellations and Reschedule

The Customer may cancel their booking without incurring any charges if they provide notice of cancellation at least 48 hours prior to the scheduled start time of the service. However, if the Customer cancels their booking within 48 hours of the scheduled start time, they will be subject to a cancellation fee of 20% of the total booking amount. The Company reserves the right to waive the cancellation fee at its discretion in exceptional circumstances.

We reserve the right to cancel or reschedule a service in cases where an accident or other unexpected event has affected the assigned cleaning team. If such an event occurs, we will make every effort to inform you as soon as possible and offer alternative arrangements that suit your needs.

We request a 24-hour notice for rescheduling your booking so that we can make alternative arrangements and avoid any inconvenience. For amendments in less than 24 hours, there is a 10% fee payable.

The Customer can reschedule or cancel the appointment over the phone or in writing by email.

## IMPORTANT ITEMS

- **During the booking process**, it is imperative that you inform us of any expensive items, such as furniture, that may necessitate specialist treatment or chemicals. This includes, but is not limited to, parquet and oak flooring, as well as wooden work surfaces. Please note that we will not be liable for any damage caused to such items if we have not been notified of their presence or specific requirements; this must be communicated to the Company at the time of booking in the additional information section.

## END OF TENANCY

- The Customer must ensure that all personal belongings are removed before the commencement of the cleaning service. Failure to do so may result in an additional charge, which will be communicated to the Customer prior to the cleaning service.

- Any cleaning guarantee offered by the Company will not apply to areas where personal belongings are present.

- Cleaning of walls, mold on walls and ceilings is not included in the end of tenancy cleaning service checklist. If the Customer requires these items to be cleaned, this must be communicated to the Company at the time of booking in the additional information section.

- Cleaning of vacuum cleaners, ironing boards, curtains, and other items left in storage cupboards is not included in the end of tenancy cleaning service checklist. If the Customer requires these items to be cleaned, this must be communicated to the Company at the time of booking in the additional information section.

- Rubbish or waste removal is not included in the end of tenancy cleaning service and will incur an additional charge. This charge will be communicated to the Customer prior to the commencement of the cleaning service.

- The Customer is responsible for ensuring that hot running water and electricity are provided, and that there are no blocked drains. Any additional charges for unblocking drains will be communicated to the Customer prior to the commencement of the cleaning service. If the Customer fails to provide hot running water or electricity, the Company reserves the right to cancel the service and will not be liable, under any circumstances, for any costs associated with the cleaning service not being carried out.

- To ensure the best possible cleaning results, we kindly request that customers empty and defrost their fridges and freezers before our arrival. Additionally, please turn off the appliances so we can clean them thoroughly. We cannot be held responsible for cleaning freezers that have not been defrosted, and we will not be liable for any costs associated with incomplete cleaning of the fridge and freezer service. We will make every effort to ensure that your appliances are cleaned to the best of our ability. However, we cannot be held responsible for ingrained dirt that has accumulated over a long period, and that cannot be removed using standard cleaning chemicals.

- We want to ensure that our customers are aware that we will do our best to address any concerns you may have regarding pet odors or cigarette smoke during the cleaning process. However, we cannot guarantee the complete removal of these odors. If you have any concerns regarding pet odors or cigarette smoke, please inform us prior to booking your appointment so that we can discuss the options available to you. Please note that we will not be liable for any costs associated with incomplete cleaning of pet odors or cigarette smoke service.

- To ensure the safety and efficiency of our cleaning services, we reserve the right to refuse cleaning your property if a third party is present, such as builders, handymen, or inspectors. If we proceed with the cleaning despite the presence of a third party, please note that the guarantee for the service will not be valid. We appreciate your cooperation in ensuring a safe and seamless cleaning experience.

## CARPET AND UPHOLSTERY CLEANING

- Please note that the company cannot be held liable for any shrinkage of carpets that may occur due to poor fitting. We recommend ensuring that your carpets are properly fitted prior to our cleaning services to avoid any potential issues.

- Please note that the company cannot be held responsible for any damage that may occur as a result of the Customer placing furniture on a carpet that has not completely dried after our cleaning services. We strongly advise waiting until the carpet is fully dry before moving any furniture back onto it.

- We cannot guarantee the complete removal of pre-existing stains or discoloration from your carpets. While we will make every effort to identify and treat all spots and stains, we cannot guarantee their complete removal. Certain stains, such as those caused by tannins, rust, or DIY spotting agents, may be particularly difficult to remove. Additionally, we cannot accept liability for any color run or migration caused by non-colorfast dyes or markers used in the manufacturing of frames, trimmings, padding, stuffing, piping, sewing threads, linings, or valances.

## COMPLAINTS, CUSTOMER SATISFACTION AND RE-CLEAN

- Once the service has been completed, the Customer must visit the premises and check that they are satisfied with the service provided. If the Customer is not available for an inspection, they must inform us before the commencement of the service.

- If the Customer is not satisfied with the service provided, they must inform us immediately. We will arrange for a re-clean to be carried out at the same time or within 48 hours of the original service, free of charge.

- If the Customer fails to notify us of any issues within 24 hours of the service being completed, we will assume that the service was carried out to their satisfaction.

- If the Customer is more than 30 minutes late for an appointment without notifying us, we reserve the right to cancel the appointment and charge the full amount for the service booked. And in the event that the Customer is late for the inspection appointment by more than 30 minutes, additional charges £20 will be incurred.

- To ensure complete satisfaction, we request that customers allow us to revisit and re-clean any areas/items in dispute before engaging a third party or refusing to pay for the service. This is to ensure that we have had an opportunity to rectify any issues and meet your expectations. If access to the property is denied for a re-clean, or if the customer refuses, we will not be held responsible for any costs incurred as a result. Additionally, we will require full payment for the service provided. It is important to note that denying access for a re-clean may result in the inability to rectify any issues or concerns. Therefore, we kindly request that customers allow us the opportunity to revisit and address any issues promptly.

- We want to assure you that we take full responsibility for any damage that may occur to your property or items during our cleaning service. To process a claim, we require full proof or photographic evidence that supports your claim of damage. Please note that claims without evidence cannot be accepted. If your claim is approved, you will need to fix or replace the damaged item first and return it to our company if applicable. After that, please send us photographic evidence along with the receipt for the fixed damage or replaced item and your bank details. We will then reimburse you the full cost within 3-5 working days of receiving the requested details. Please keep in mind that it may take up to 3-5 working days for us to investigate the claim. Rest assured that we will do everything we can to ensure that the process is as smooth and efficient as possible.
### PARKING
- To ensure smooth cleaning services, we kindly request our customers to arrange for a parking space or a valid permit for one vehicle. 
In the absence of a designated parking spot, the customer shall be responsible for paying the metered parking fees. 
Any parking penalties incurred due to the customer's error or lack of information will be borne entirely by the customer.
- Furthermore, in the case where the property to be cleaned is located within the congestion charging zone, 
the customer shall be liable for the payment of the congestion charge.







"""

# Display custom HTML with CSS
st.markdown(custom_css, unsafe_allow_html=True)
st.markdown(terms_and_conditions, unsafe_allow_html=True)
