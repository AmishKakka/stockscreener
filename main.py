from imports import pd, st

def submitQuery():
    raw_query = st.session_state.rawQuery
    queries = raw_query.split("&")
    for query in queries:
        print(query.strip())
    if raw_query != "":
        st.session_state["result_table"] = pd.DataFrame(data_to_show)
    
#   Start of the main page elements.
st.title("Stock Screener")
left, right = st.columns(2, gap="large", 
                         vertical_alignment='top', border=True)

data = pd.read_csv("stocksData.csv")
data_to_show = data[["Symbol", "Shortname", "Marketcap", "Volume", "Previousclose", "Dividendyield", "Trailingpe",
                     "Returnonequity", "Grossprofits", "Freecashflow", "Earningsgrowth", "Revenuegrowth", 
                     "Pricetobook", "Totalrevenue", "Debttoequity", "Revenuepershare", "Profitmargins", "Ebitdamargins"]]

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
    st.dataframe(st.session_state["result_table"],
                 width=2000, height=1000)
    