import streamlit as st
import yfinance as yf


st.set_page_config(page_icon=":bar_chart", page_title="Home")


def app():
    st.write(
        """
    # Simple Stock price App 
    
    Shown are the stock **closing price** and the **volume price** of Google
    """
    )

    tickerSimbol = "GOOGL"
    tickerData = yf.Ticker(tickerSimbol)
    tickerDf = tickerData.history(
        period="1d", start="2010-05-31", end="2020-05-31")

    st.write("""
        ## Closing Price      
    """)
    st.line_chart(tickerDf.Close)
    st.write("""
        ## Volume Price      
    """)
    st.line_chart(tickerDf.Volume)


if __name__ == "__main__":
    app()
