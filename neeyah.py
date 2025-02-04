import streamlit as st

class PricingDetails:
    def __init__(self, home_purchase_price, down_payment_amount, local_property_tax_rate, initial_rental_rate, annual_rental_increase_percentage, annual_home_value_appreciation_percentage, annual_equity_purchase_rate,):
        self.home_purchase_price = home_purchase_price
        self.down_payment_amount = down_payment_amount
        self.local_property_tax_rate = local_property_tax_rate 
        self.initial_rental_rate = initial_rental_rate
        self.annual_rental_increase_percentage = annual_rental_increase_percentage
        self.annual_home_value_appreciation_percentage = annual_home_value_appreciation_percentage
        self.annual_equity_purchase_rate = annual_equity_purchase_rate

    def __str__(self):
        return f"Home Price: {self.home_purchase_price} \nDown Payment Amount: {self.down_payment_amount} \nLocal Property Tax Rate: {self.local_property_tax_rate} \n--------------------\nInitial Rental Rate: {self.initial_rental_rate} \nRental Increase Percentage: {self.annual_rental_increase_percentage} \n--------------------\nAnnual Home Value Appreciation Percentage: {self.annual_home_value_appreciation_percentage} \nAnnual Equity Purchase Rate: {self.annual_equity_purchase_rate}"

class ScheduleDetails:
    def __init__(self, simplified_df, full_df, annual_equity_purchase_rate, rental_expense_list, personal_tax_burden_list, year, month):
        self.simplified_df = simplified_df
        self.full_df = full_df
        self.annual_equity_purchase_rate = annual_equity_purchase_rate
        self.rental_expense_list = rental_expense_list
        self.personal_tax_burden_list = personal_tax_burden_list
        self.year = year
        self.month = month


def header():
    st.title("Neeyah Payment Calculator 💸")
    st.markdown('''
    [Neeyah](https://neeyah.com/) is an alternative to conventional mortgages for Muslim home buyers through the use of a technique called [Musharakah](https://en.wikipedia.org/wiki/Profit_and_loss_sharing#Musharakah). Since this method of home ownership is not common in the United States, this calculator aims to help home buyers better understand a potential payment structure.

    Input specific information about your potential home purchase to calculate a payment schedule.
    ''')

def get_purchase_details():
    with st.form("pricing-details"):
        st.markdown('''### 🏡 Home Information''')
        home_purchase_price = st.number_input("**Home Purchase Price**", min_value=100000, value=350000, step=1)
        down_payment_amount = st.number_input("**Down Payment Amount**\n\n*Minimum 20% of home value.*", min_value=20000, value=70000, step=1)
        local_property_tax_rate = st.number_input("**Local Property Tax Rate**\n\n*You can use [SmartAsset's Property Tax Calculator](https://smartasset.com/taxes/property-taxes) to find the property tax rates in your area.*", max_value=5.0, min_value=0.01, value=1.25)
        st.markdown("""---""")

        st.markdown('''### 💵 Rental Information''')
        initial_rental_rate = st.number_input("**Initial Monthly Rent on Property**\n\n*You can use [US Gov's HUD Fair Market Rents Documentation System](https://www.huduser.gov/portal/datasets/fmr/fmrs/FY2024_code/select_Geography.odn) to find a market rate for properties in your area.*", step=1, value=2000)
        annual_rental_increase_percentage = st.number_input("**Rent Percentage Increase YoY**\n\n*5% is Neeyah's upper limit on rental increases per year.*", max_value=5.0, min_value=0.01, value=3.0)
        st.markdown("""---""")

        st.markdown('''### 📈 Home Value Growth''')
        annual_home_value_appreciation_percentage = st.number_input("**Home Value Increase YoY**\n\n*5% is Neeyah's upper limit on home value increases per year.*", max_value=5.0, min_value=0.01, value=3.0)
        annual_equity_purchase_rate = st.number_input("**Equity Percent Purchase YoY**\n\n*The amount of equity you would like to gain from the total home value every year.*", max_value=5.0, min_value=0.01, value=5.0)

        submitted = st.form_submit_button("Submit")
        if submitted:
            if down_payment_amount < home_purchase_price * .2:
                st.warning(f"#### Down payment is less than 20% of home price.\n\nPlease update down payment value and resubmit.")
                return
            home_purchase_details = PricingDetails(home_purchase_price=home_purchase_price, down_payment_amount=down_payment_amount, local_property_tax_rate=local_property_tax_rate, initial_rental_rate=initial_rental_rate, annual_rental_increase_percentage=annual_rental_increase_percentage, annual_home_value_appreciation_percentage=annual_home_value_appreciation_percentage, annual_equity_purchase_rate=annual_equity_purchase_rate)
            return home_purchase_details
        

def display_df(schedule_info: ScheduleDetails):
    if schedule_info is None:
        return
    
    simplified_df = schedule_info.simplified_df
    full_df = schedule_info.full_df
    annual_equity_purchase_rate = schedule_info.annual_equity_purchase_rate
    rental_expense_list = schedule_info.rental_expense_list
    personal_tax_burden_list = schedule_info.personal_tax_burden_list
    year = schedule_info.year
    month = schedule_info.month

    st.write("### Payment Schedule")
    st.write(f"This is a payment schedule that assumes you purchase {int(annual_equity_purchase_rate * 100)}% of Neeyah's equity per year.\n\nIt would take you **{year} years and {month} {'month' if month == 1 else 'months'}** to complete the payments.\n\nBy the end of the term you would have paid **\${round(sum(rental_expense_list),2)}** in rental payments to Neeyah and **${round(sum(personal_tax_burden_list),2)}** in taxes.")

    # TODO figure out toggle for full and simplfied view
    st.write("#### Simplified Columns")
    st.dataframe(simplified_df)

    st.write("#### Full Columns")
    st.dataframe(full_df)



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

def footer():
    st.markdown('''
    :gray[*We are not affiliated, associated, authorized, endorsed by, or in any way officially connected with Neeyah, or any of its subsidiaries or its affiliates. Any information about Neeyah can be found at their website https://neeyah.com/, or by speaking to an official Neeyah representative .*]

    :gray[*The name Neeyah well as related names, marks, emblems and images are registered trademarks of their respective owners.*]
    ''')