from datetime import datetime, timedelta
import streamlit as st
import pandas as pd
from neeyah import *
import csv

def calculate_payment_schedule_by_percent(home_purchase_details):
    if home_purchase_details is not None:
        home_purchase_price = home_purchase_details.home_purchase_price
        down_payment_amount = home_purchase_details.down_payment_amount
        local_property_tax_rate = home_purchase_details.local_property_tax_rate / 100
        initial_rental_rate = home_purchase_details.initial_rental_rate
        annual_rental_increase_percentage = home_purchase_details.annual_rental_increase_percentage / 100
        annual_home_value_appreciation_percentage = home_purchase_details.annual_home_value_appreciation_percentage / 100
        annual_equity_purchase_rate = home_purchase_details.annual_equity_purchase_rate / 100
                
        personal_equity = down_payment_amount
        rental_rate = initial_rental_rate

        month = 1
        year = 1
        month_and_year_list = [f"{month}.{year}"]

        home_value = home_purchase_price
        personal_equity = down_payment_amount
        personal_equity_percentage = personal_equity / home_value
        
        equity_investment_payment = (home_value * annual_equity_purchase_rate) / 12
        monthly_tax_rate = (home_value * local_property_tax_rate) / 12

        home_value_list = []
        neeyah_equity_list = []
        personal_equity_list = []
        neeyah_equity_percent_list = []
        personal_equity_percent_list = []
        rental_rate_list = []
        rental_expense_list = []
        equity_investment_payment_list = []
        total_tax_burden_list = []
        personal_tax_burden_list = []
        total_monthly_payment_list = []

        # TODO handle weird/infinite values 
        while personal_equity_percentage <= 1:
            # At start of the year, 
            # increase rent, home values and calculate monthly tax rate and equity investment payment
            if month == 1 and year != 1: 
                home_value = home_value * (1 + annual_home_value_appreciation_percentage)
                rental_rate = rental_rate * (1 + annual_rental_increase_percentage)
                monthly_tax_rate = (home_value * local_property_tax_rate) / 12
                equity_investment_payment = (home_value * annual_equity_purchase_rate) / 12

            # Calculating equities
            neeyah_equity = home_value - personal_equity
            personal_equity_percentage = personal_equity / home_value
            neeyah_equity_percentage = 1 - personal_equity_percentage

            # Calculating rental and tax burdens and monthly payment
            rental_expense = neeyah_equity_percentage * rental_rate
            personal_tax_burden = neeyah_equity_percentage * monthly_tax_rate
            total_monthly_payment = rental_expense + equity_investment_payment + personal_tax_burden

            # if total_monthly_payment > neeyah_equity:
            # TODO Handle final month here 

            # Increasing equity
            personal_equity += equity_investment_payment

            home_value_list.append(home_value)
            personal_equity_list.append(personal_equity)
            personal_equity_percent_list.append(personal_equity_percentage)
            neeyah_equity_list.append(neeyah_equity)
            neeyah_equity_percent_list.append(neeyah_equity_percentage)
            rental_rate_list.append(rental_rate)
            rental_expense_list.append(rental_expense)
            equity_investment_payment_list.append(equity_investment_payment)
            total_tax_burden_list.append(monthly_tax_rate)
            personal_tax_burden_list.append(personal_tax_burden)
            total_monthly_payment_list.append(total_monthly_payment)
            
            # TODO Handle adding extra month here
            # Resetting for the year
            month = (month % 12) + 1
            month_and_year_list.append(f"{year}.{month}")
            if month == 1: year += 1

        if len(month_and_year_list) > (12*45):
            st.warning(f"#### Payment schedule is longer than 50 years.\n\nPlease update values and resubmit.")
            return


        data = {
            "Home Value" : [f"${str(int(value))}" for value in home_value_list],
            "Neeyah Equity" : [f"${str(int(value))}" for value in neeyah_equity_list],
            "Personal Equity" : [f"${str(int(value))}" for value in personal_equity_list],
            "Neeyah Equity %" : [f"{round((value*100), 1)}%" for value in neeyah_equity_percent_list],
            "Personal Equity %": [f"{round((value*100), 1)}%" for value in personal_equity_percent_list],
            "Rental Rate": [f"${str(int(value))}" for value in rental_rate_list],
            "Rental Payment" : [f"${str(int(value))}" for value in rental_expense_list],
            "Equity Payment" : [f"${str(int(value))}" for value in equity_investment_payment_list],
            "Total Tax Burden" : [f"${str(int(value))}" for value in total_tax_burden_list],
            "Personal Tax Burden" : [f"${str(int(value))}" for value in personal_tax_burden_list],
            "Total Monthly Payment": [f"${str(int(value))}" for value in total_monthly_payment_list]
        }

        df = pd.DataFrame(data, index=month_and_year_list[:-1])
        st.write("### Payment Schedule")
        st.dataframe(df)
        
if __name__ == '__main__':
    header()
    home_purchase_details = get_purchase_details()
    calculate_payment_schedule_by_percent(home_purchase_details)
    neeyah_description()
    footer()