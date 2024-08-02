from datetime import datetime, timedelta
import streamlit as st
import pandas as pd
from neeyah import *
import csv

def calculate_payment_schedule_by_percent(home_purchase_details):
    if home_purchase_details is None:
        return
    
    home_purchase_price = home_purchase_details.home_purchase_price
    down_payment_amount = home_purchase_details.down_payment_amount
    local_property_tax_rate = home_purchase_details.local_property_tax_rate / 100
    initial_rental_rate = home_purchase_details.initial_rental_rate
    annual_rental_increase_percentage = home_purchase_details.annual_rental_increase_percentage / 100
    annual_home_value_appreciation_percentage = home_purchase_details.annual_home_value_appreciation_percentage / 100
    annual_equity_purchase_rate = home_purchase_details.annual_equity_purchase_rate / 100
            
    personal_equity = down_payment_amount
    neeyah_equity = home_purchase_price - down_payment_amount
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

    while personal_equity_percentage <= 1:
        # At start of the year, increase rent, home values 
        # and calculate monthly tax rate and equity investment payment
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
        personal_tax_burden = personal_equity_percentage * monthly_tax_rate
        total_monthly_payment = rental_expense + equity_investment_payment + personal_tax_burden

        # Increasing equity
        personal_equity += equity_investment_payment

        # Incrementing time and checking for length of payments
        month_and_year_list.append(f"{year}.{month}")
        month = (month % 12) + 1
        if month == 1: year += 1

        if len(month_and_year_list) > (12*50):
            st.warning(f"#### Payment schedule is longer than 50 years.\n\nPlease update values and resubmit.")
            return
        
        # Handles calculation of final payment
        if neeyah_equity_percentage < 0:
            personal_equity += equity_investment_payment + neeyah_equity
            print(neeyah_equity)
            home_value_list.append(home_value)
            personal_equity_list.append(personal_equity)
            personal_equity_percent_list.append(1)
            neeyah_equity_list.append(0)
            neeyah_equity_percent_list.append(0)
            rental_rate_list.append(rental_rate)
            rental_expense_list.append(0)
            equity_investment_payment_list.append(equity_investment_payment + neeyah_equity)
            total_tax_burden_list.append(monthly_tax_rate)
            personal_tax_burden_list.append(monthly_tax_rate)
            total_monthly_payment_list.append(equity_investment_payment + neeyah_equity + rental_expense + monthly_tax_rate)
            break

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

    full_percent_data = {
        "Home Value" : [f"${str(int(value))}" for value in home_value_list],
        "Neeyah Equity" : [f"${str(int(value))}" for value in neeyah_equity_list],
        "Personal Equity" : [f"${str(int(value))}" for value in personal_equity_list],
        "Neeyah Equity %" : [f"{round((value * 100),2)}%" for value in neeyah_equity_percent_list],
        "Personal Equity %": [f"{round((value * 100),2)}%" for value in personal_equity_percent_list],
        "Rental Rate": [f"${str(int(value))}" for value in rental_rate_list],
        "Rental Payment" : [f"${str(int(value))}" for value in rental_expense_list],
        "Equity Payment" : [f"${str(int(value))}" for value in equity_investment_payment_list],
        "Total Tax Burden" : [f"${str(int(value))}" for value in total_tax_burden_list],
        "Personal Tax Burden" : [f"${str(int(value))}" for value in personal_tax_burden_list],
        "Total Monthly Payment": [f"${str(int(value))}" for value in total_monthly_payment_list]
    }

    simplified_percent_data = {
        "Home Value" : [f"${str(int(value))}" for value in home_value_list],
        "Personal Equity %": [f"{round((value * 100),2)}%" for value in personal_equity_percent_list],
        "Rental Payment" : [f"${str(int(value))}" for value in rental_expense_list],
        "Personal Tax Burden" : [f"${str(int(value))}" for value in personal_tax_burden_list],
        "Equity Payment" : [f"${str(int(value))}" for value in equity_investment_payment_list],
        "Total Monthly Payment": [f"${str(int(value))}" for value in total_monthly_payment_list]
    }
    full_percent_df = pd.DataFrame(full_percent_data, index=month_and_year_list[:-1])
    simplified_percent_df = pd.DataFrame(simplified_percent_data, index=month_and_year_list[:-1])
    
    return ScheduleDetails(simplified_df=simplified_percent_df, full_df=full_percent_df, annual_equity_purchase_rate=annual_equity_purchase_rate, 
                           rental_expense_list=rental_expense_list, personal_tax_burden_list=personal_tax_burden_list, year=year, month=month)
        

if __name__ == '__main__':
    header()
    home_purchase_details = get_purchase_details()
    schedule_info = calculate_payment_schedule_by_percent(home_purchase_details)
    display_df(schedule_info)
    neeyah_description()
    footer()