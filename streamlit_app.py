from datetime import datetime, timedelta
import streamlit as st
import pandas as pd

class PricingDetails:
    def __init__(self, home_price, initial_rental_rate, rental_increase_percentage):
    # def __init__(self, home_price, initial_rental_rate, rental_increase_percentage, mortgage_monthly_payment, use_mortgage_max_monthly_payment=False):
        self.home_price = home_price
        self.initial_rental_rate = initial_rental_rate
        self.rental_increase_percentage = rental_increase_percentage
        # self.use_mortgage_max_monthly_payment = use_mortgage_max_monthly_payment
        # self.mortgage_monthly_payment = mortgage_monthly_payment

    def __str__(self):
        return f"Home Price: {self.home_price} | Rental Increase Percentage {self.rental_increase_percentage} | Initial Rental Rate {self.initial_rental_rate}"

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
        home_price = st.number_input("**Home Asking Price**", min_value=300000, step=1)
        initial_rental_rate = st.number_input("**Initial Monthly Rent on Property**\n\n*You can use [US Gov's HUD Fair Market Rents Documentation System](https://www.huduser.gov/portal/datasets/fmr/fmrs/FY2024_code/select_Geography.odn) to find a market rate for properties in your area.*", step=1, value=1500)
        rental_increase_percentage = st.number_input("**Rent Percentage Increase YoY**\n\n*The default value of 5% comes is from Neeyah's upper limit on rental increases per year.*", max_value=5.0, min_value=0.01, value=5.0)
        
        submitted = st.form_submit_button("Submit")
        if submitted:
            home_purchase_details = PricingDetails(home_price, initial_rental_rate, rental_increase_percentage) 
            return home_purchase_details

def calculate_payment_schedule(home_purchase_details):
    try:
        home_value = home_purchase_details.home_price
        rent_increase_percent = home_purchase_details.rental_increase_percentage / 100
        rental_rate = home_purchase_details.initial_rental_rate 
                
        current_date = datetime.now()
        start_date = current_date

        neeyah_equity = .8 * home_value
        personal_equity = .2 * home_value
        total_cost = 0
        total_neeyah_rent = 0

        month_and_year_list = []
        neeyah_equity_list = []
        neeyah_percent_equity_list = []
        personal_equity_list = []
        personal_percent_equity_list = []
        rental_rate_list = []
        neeyah_rental_payment_list = []
        personal_rental_payment_list = []

        while personal_equity < home_value:
            
            month_and_year = current_date.strftime("%B %Y")

            # Calculating equity
            neeyah_percent_equity = round(neeyah_equity/home_value, 2)
            personal_percent_equity = round(1 - neeyah_percent_equity, 2)
            
            # Calculating rental payments based on equity
            personal_rental_payment = round(personal_percent_equity * rental_rate, 2)
            neeyah_rental_payment = round(neeyah_percent_equity * rental_rate, 2)

            month_and_year_list.append(month_and_year) # index
            neeyah_equity_list.append(round(neeyah_equity, 2))
            neeyah_percent_equity_list.append(round(neeyah_percent_equity * 100, 2))
            
            personal_equity_list.append(round(personal_equity, 2))
            personal_percent_equity_list.append(round(personal_percent_equity * 100,2))
            
            rental_rate_list.append(rental_rate)
            neeyah_rental_payment_list.append(neeyah_rental_payment)
            personal_rental_payment_list.append(personal_rental_payment) 

            # Calculating equity and ongoing totals
            personal_equity += personal_rental_payment
            neeyah_equity -= personal_rental_payment
            total_cost += rental_rate
            total_neeyah_rent += neeyah_percent_equity * rental_rate


            # Increase rent by percentage every year
            if current_date.month == start_date.month and start_date.month != current_date.month: 
                rental_rate = round(rental_rate * (1 + rent_increase_percent),2)
            
            #Increae time by 1 month
            current_date = current_date + timedelta(days=1 * (365/12))

        data = {
            "Neeyah Equity" : neeyah_equity_list,
            "Personal Equity" : personal_equity_list,
            "Neeyah Equity %" : neeyah_percent_equity_list,
            "Personal Equity %": personal_percent_equity_list,
            "Total Rental Payment": rental_rate_list,
            "Neeyah Share of Rental Payment" : neeyah_rental_payment_list,
            "Personal Share of Rental Payment" : personal_rental_payment_list
        }


        df = pd.DataFrame(data, index=month_and_year_list)
        
        st.write("### Payment Schedule")
        st.dataframe(df)
        st.write(f"**Total Rent Paid to Neeyah:** ${round(total_neeyah_rent,2)}")
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

