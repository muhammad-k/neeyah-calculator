from datetime import datetime, timedelta
import streamlit as st
import pandas as pd

class PricingDetails:
    def __init__(self, home_price, down_payment_amount, initial_rental_rate, rental_increase_percentage, home_increase_percentage):
        self.home_price = home_price
        self.down_payment_amount = down_payment_amount
        self.initial_rental_rate = initial_rental_rate
        self.rental_increase_percentage = rental_increase_percentage
        self.home_increase_percentage = home_increase_percentage


    def __str__(self):
        return f"Home Price: {self.home_price} | Down Payment Amount: {self.down_payment_amount} | Initial Rental Rate {self.initial_rental_rate} | Rental Increase Percentage: {self.rental_increase_percentage} | Home Value Increase Percentage: {self.home_increase_percentage}"

def header():
    st.title("Neeyah Payment Calculator 💸")
    st.markdown('''
    [Neeyah](https://neeyah.com/) is an alternative to conventional mortgages for Muslim home buyers through the use of a technique called [Musharakah](https://en.wikipedia.org/wiki/Profit_and_loss_sharing#Musharakah). Since this method of home ownership is not common in the United States, this calculator was created to help home buyers better understand a potential payment structure.

    Input specific information about your potential home purchase to calculate a payment schedule.
    ''')

def neeyah_description():
    st.write('''
        ### How Does Home Ownership with Neeyah Work?
        1. **Identify and Purchase a Home with Neeyah**
        Buy a minimum 20% and Neeyah buys the rest.
        2. **Make Monthly Payments**
        Pay rent for the portion of the home you don't own yet, while Neeyah pays for its fair share of home expenses. *Anything you pay in excess of your rental percentage is what is used to purchase Neeyah's share of the home.*
        3. **Sell anytime or reach 100% ownership.**
        You decide when to sell the home, or reach sole ownership. *You can pay more to increase your equity in the home and reach sole ownership sooner *
    ''')

def get_purchase_details():
    st.write("### Home Information")
    with st.form("pricing-details"):
        home_price = st.number_input("**🏡 Home Asking Price**", min_value=100000, value=300000, step=1)
        down_payment_amount = st.number_input("**⬇️ Down Payment Amount**\n\n*Minimum 20% of home value.*", min_value=20000, value=60000, step=1)
        initial_rental_rate = st.number_input("**🤔 Initial Monthly Rent on Property**\n\n*You can use [US Gov's HUD Fair Market Rents Documentation System](https://www.huduser.gov/portal/datasets/fmr/fmrs/FY2024_code/select_Geography.odn) to find a market rate for properties in your area.*", step=1, value=1500)
        rental_increase_percentage = st.number_input("**🎢 Rent Percentage Increase YoY**\n\n*The default value of 5% comes is from Neeyah's upper limit on rental increases per year.*", max_value=5.0, min_value=0.01, value=5.0)
        home_increase_percentage = st.number_input("**🛝 Home Value Increase YoY**\n\n*The default value of 5% comes is from Neeyah's upper limit on home value increases per year.*", max_value=5.0, min_value=0.01, value=5.0)
        
        submitted = st.form_submit_button("Submit")
        if submitted:
            if down_payment_amount < home_price * .2:
                st.warning(f"Down payment is less than 20% of home price.\n\nPlease update down payment value and resubmit.", icon="⚠️")
                return
            home_purchase_details = PricingDetails(home_price=home_price, down_payment_amount=down_payment_amount, initial_rental_rate=initial_rental_rate, rental_increase_percentage=rental_increase_percentage, home_increase_percentage=home_increase_percentage) 
            return home_purchase_details

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

def footer():
    st.markdown('''
    :gray[*We are not affiliated, associated, authorized, endorsed by, or in any way officially connected with Neeyah, or any of its subsidiaries or its affiliates. Any information about Neeyah can be found at their website https://neeyah.com/, or by speaking to an official Neeyah representative .*]

    :gray[*The name Neeyah well as related names, marks, emblems and images are registered trademarks of their respective owners.*]
    ''')

if __name__ == '__main__':
    header()
    
    home_purchase_details = get_purchase_details() 
    calculate_payment_schedule(home_purchase_details)

    neeyah_description()
    footer()