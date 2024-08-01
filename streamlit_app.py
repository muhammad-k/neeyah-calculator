from datetime import datetime, timedelta
import streamlit as st
import pandas as pd
from neeyah import *

'''
def calculate_payment_schedule(home_purchase_details):

    try:
        home_value = home_purchase_details.home_price
        down_payment = home_purchase_details.down_payment_amount
        rent_increase_percent = home_purchase_details.rental_increase_percentage / 100
        home_increase_percent = home_purchase_details.home_increase_percentage / 100
        rental_rate = home_purchase_details.initial_rental_rate 
                
        current_date = datetime.now()
        start_date = current_date

        neeyah_equity = home_value - down_payment
        personal_equity = down_payment
        total_cost = 0
        total_neeyah_rent = 0

        month = 1
        year = 1

        month_and_year_list = []
        neeyah_equity_list = []
        home_value_list = []  
        neeyah_percent_equity_list = []
        personal_equity_list = []
        personal_percent_equity_list = []
        rental_rate_list = []
        neeyah_rental_payment_list = []
        personal_rental_payment_list = []
        personal_percent_equity = 0
        
        while personal_percent_equity <= 1:

            # Calculating equity
            neeyah_percent_equity = neeyah_equity/home_value
            personal_percent_equity = 1 - neeyah_percent_equity

            # Calculating rental payments based on equity
            neeyah_rental_payment = neeyah_percent_equity * rental_rate
            personal_rental_payment = rental_rate - neeyah_rental_payment

            month_and_year_list.append(f"{year}.{month}") 
            home_value_list.append(home_value)


            if personal_percent_equity > 1:
                neeyah_equity_list.append(0)
                personal_equity_list.append(home_value)
                neeyah_percent_equity_list.append(0)
                personal_percent_equity_list(100)
                rental_rate_list.append(home_value - personal_equity)
                neeyah_rental_payment_list.append(0)
                personal_rental_payment_list.append(home_value - personal_equity) 
                break

            # Equity values and percentages
            neeyah_equity_list.append(neeyah_equity)
            personal_equity_list.append(personal_equity)
            neeyah_percent_equity_list.append(neeyah_percent_equity * 100)
            personal_percent_equity_list.append(round(personal_percent_equity * 100,2))
            
            # Rental Values
            rental_rate_list.append(rental_rate)
            neeyah_rental_payment_list.append(neeyah_rental_payment)
            personal_rental_payment_list.append(personal_rental_payment) 

            # Calculating equity and ongoing totals
            personal_equity += personal_rental_payment
            neeyah_equity -= personal_rental_payment
            total_cost += rental_rate
            total_neeyah_rent += neeyah_percent_equity * rental_rate

            # Increase rent by percentage every year except on first month
            if month == 1 and year != 1: 
                rental_rate = rental_rate * (1 + rent_increase_percent)
                home_value = home_value * (1 + home_increase_percent)
            
            # Resetting for the year
            month += 1
            if month == 13:
                month = 1
                year += 1


        data = {
            "Home Value" : home_value_list,
            "Neeyah Equity" : neeyah_equity_list,
            "Personal Equity" : personal_equity_list,
            "Neeyah Equity %" : neeyah_percent_equity_list,
            "Personal Equity %": personal_percent_equity_list,
            "Total Rental Payment": rental_rate_list,
            "Neeyah Share of Rental Payment" : neeyah_rental_payment_list,
            "Personal Share of Rental Payment" : personal_rental_payment_list
        }


        df = pd.DataFrame(data, index=month_and_year_list)
        print(df)
        st.write("### Payment Schedule")
        st.dataframe(df)
        st.write(f"**Total Rent Paid to Neeyah:** ${round(sum(neeyah_rental_payment_list),2)}")
        st.write(f"**Total Cost with Equity:** ${round(total_cost,2)}")
        
    except:
        pass
    return ""
'''

if __name__ == '__main__':
    header()
    home_purchase_details = get_purchase_details()
    if home_purchase_details: print(home_purchase_details)
    # calculate_payment_schedule(home_purchase_details)
    neeyah_description()
    footer()