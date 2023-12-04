import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide", page_icon=":bar_chat:",
                   page_title="Data driven")


@st.cache_data
def read_data_from_excel():
    df = pd.read_excel(
        io="./data/supermarkt_sales.xlsx",
        engine="openpyxl",
        sheet_name="Sales",
        skiprows=3,
        usecols="B:R",
        nrows=1000
    )
    df["hour"] = pd.to_datetime(
        df["Time"], format="%H:%M:%S").dt.hour
    df['month'] = pd.to_datetime(df["Date"], format="%b %d %Y").dt.month
    return df


# password = stauth.Hasher(["testing890"]).generate()
# print(password)
credentials = {
    "usernames": {
        "testing101": {
            "name": "testing101@gmail.com",
            "password": "$2b$12$/XuBJOXuPYp7XNGfhIeIluvkfeNjXjz3pj41RNEPL7wptzdAqc8CS",
        },
        "testing102": {
            "name": "testing102@gmail.com",
            "password": "$2b$12$/XuBJOXuPYp7XNGfhIeIluvkfeNjXjz3pj41RNEPL7wptzdAqc8CS",
        },
    }
}
authenticator = stauth.Authenticate(
    credentials, cookie_name="streamlit", key="abcdef", cookie_expiry_days=30)
name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Invalid user credentials")
if authentication_status is None:
    st.warning("Please fill in the required fields")
if authentication_status:
    # st.balloons()

    st.sidebar.markdown(f"<h3> Hi {username}", unsafe_allow_html=True)
    authenticator.logout("Logout", "sidebar")
    df = read_data_from_excel()

    st.sidebar.header("Please Filter here")

    city = st.sidebar.multiselect(
        "Select City:",
        options=df['City'].unique(),
        default=df["City"].unique()
    )
    customer_type = st.sidebar.multiselect(
        "Select Customer Type:",
        options=df['Customer_type'].unique(),
        default=df["Customer_type"].unique()
    )
    gender = st.sidebar.multiselect(
        "Select Gender:",
        options=df['Gender'].unique(),
        default=df["Gender"].unique()
    )

    df_selected = df.query(
        "City== @city & Customer_type== @customer_type & Gender== @gender")

    st.title(":bar_chart: Sales Dashboard")
    st.markdown("##")
    total_sales = int(df_selected["Total"].sum())
    average_rating = round(df_selected["Rating"].mean(), 1)

    star_rating = ":star:" * int(round(average_rating, 0))
    average_sales_by_transaction = round(df_selected["Total"].mean(), 2)
    # st.dataframe(df_selected)

    left_column, middle_column, right_column = st.columns(3)

    with left_column:
        st.subheader("Total Sales")
        st.subheader(f"US $ {total_sales:,}")

    with middle_column:
        st.subheader("Average Rating")
        st.subheader(f"{average_rating} {star_rating}")

    with right_column:
        st.subheader("Average Sales Per Transaction")
        st.subheader(f"US $ {average_sales_by_transaction:,}")

    st.markdown("---")

    sales_by_product_line = (
        df_selected.groupby(by=["Product line"])[
            ["Total"]].sum().sort_values("Total")
    )

    fig_product_sales = px.bar(
        sales_by_product_line,
        x="Total",
        y=sales_by_product_line.index,
        orientation="h",
        title="<b> Sales By Product Line <b>",
        color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
        template="plotly_white"

    )
    fig_product_sales.update_layout(
        plot_bgcolor="rgba(0, 0, 0, 0)",
        xaxis=(dict(showgrid=False))
    )

    st.plotly_chart(fig_product_sales)

    # Sales by hour

    sales_by_hour = df_selected.groupby(
        "hour")[["Total"]].sum().sort_values("Total")
    fig_hour_sales = px.bar(
        sales_by_hour,
        y="Total",
        x=sales_by_hour.index,
        title="<b> Sales By Hour <b>",
        color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
        template="plotly_white"

    )
    fig_hour_sales.update_layout(
        xaxis=dict(tickmode="linear"),
        plot_bgcolor="rgba(0, 0, 0, 0)",
        yaxis=(dict(showgrid=False))
    )

    st.plotly_chart(fig_hour_sales)

    # Sales by month
    monthly_sales = df_selected.groupby(
        "month")[["Total"]].sum().sort_values("Total")
    fig_monthly_sales = px.bar(
        monthly_sales,
        y="Total",
        x=monthly_sales.index,
        title="<b> Sales By Month <b>",
        color_discrete_sequence=["#0083B8"] * len(monthly_sales),
        template="plotly_white"

    )
    fig_monthly_sales.update_layout(
        xaxis=dict(tickmode="linear"),
        plot_bgcolor="rgba(0, 0, 0, 0)",
        yaxis=(dict(showgrid=False))
    )

    st.plotly_chart(fig_monthly_sales)

    # sales by payment methods
    sales_by_payment_method = df_selected.groupby(
        "Payment")[["Total"]].sum().sort_values("Total")
    fig_payment_method = px.bar(
        sales_by_payment_method,
        y="Total",
        x=sales_by_payment_method.index,
        title="<b> Sales By Payment Method <b>",
        color_discrete_sequence=["#0083B8"] * len(sales_by_payment_method),
        template="plotly_white"

    )
    fig_payment_method.update_layout(
        xaxis=dict(tickmode="linear"),
        plot_bgcolor="rgba(0, 0, 0, 0)",
        yaxis=(dict(showgrid=False))
    )

    st.plotly_chart(fig_payment_method)

    # The most selling branch

    most_selling_branch = df_selected.groupby(
        "Branch")[["Total"]].sum().sort_values("Total")
    fig_selling_branch = px.bar(
        most_selling_branch,
        y="Total",
        x=most_selling_branch.index,
        title="<b> Sales By Branch <b>",
        color_discrete_sequence=["#0083B8"] * len(most_selling_branch),
        template="plotly_white"

    )
    fig_selling_branch.update_layout(
        xaxis=dict(tickmode="linear"),
        plot_bgcolor="rgba(0, 0, 0, 0)",
        yaxis=(dict(showgrid=False))
    )

    st.plotly_chart(fig_selling_branch)
