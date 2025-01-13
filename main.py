import time
import streamlit as st
import pandas as pd

def submitQuery():
    raw_query = st.session_state.rawQuery
    queries = raw_query.split("&")
    for query in queries:
        print(query.strip())
    data = {
        "Column 1": [raw_query, f"{raw_query} + A", f"{raw_query} + B"],
        "Column 2": [1, 2, 3],
        "Column 3": [4, 5, 6],
    }
    st.session_state["result_table"] = pd.DataFrame(data)
    
#   Start of the main page elements.
st.title("Stock Screener")
left, right = st.columns(2, gap="large", 
                         vertical_alignment='top', border=True)

with right:
    st.write("Example query:")
    multi = '''
    market_cap > 1000000 &  
    current price > 10 &  
    Price to Earnings ratio < 15 &  
    Sales growth last 5 years > 10%    
    '''
    st.markdown(multi)
    
with left:
    #   Text area for query input
    st.text_area(
        "Enter your query:",
        key="rawQuery",
        placeholder="Type your query here")
    st.button("Show Results", key="submit", on_click=submitQuery)

#   Conditionally display the table below the button
if "result_table" in st.session_state:
    st.write("Results:")
    st.table(st.session_state["result_table"])
    