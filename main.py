from imports import pd, st

def submitQuery():
    raw_query = st.session_state.rawQuery
    queries = [i.strip("\n") for i in raw_query.split("&")]
    # for query in queries:
    #     print(query.strip())
    query = " & ".join(queries)
    print(query)
    if raw_query != "":
        filtered_df = data.query(query)
        # filtered_df['Symbol'] = filtered_df['Symbol'].apply(
        #     lambda x: f'<a href="https://finance.yahoo.com/quote/{x}" target="_blank">{x}</a>')
        data_to_show = filtered_df[columns_to_show]
        st.session_state["result_table"] = pd.DataFrame(data_to_show)
    

#   Start of the main page elements.
st.set_page_config(layout="wide")
st.title("Stock Screener")
left, middle, right = st.columns([0.5, 0.2, 0.3], gap="medium", 
                         vertical_alignment='top', border=True)

data = pd.read_csv("stocksData.csv")
columns_to_show = ["Symbol", "Shortname", "Marketcap", "Volume", "Previousclose", "Dividendyield", "Trailingpe",
                     "Returnonequity", "Grossprofits", "Freecashflow", "Earningsgrowth", "Revenuegrowth", 
                     "Pricetobook", "Totalrevenue", "Debttoequity", "Revenuepershare", "Profitmargins", "Ebitdamargins"]

with right:
    st.markdown('''
                **Marketcap**: In order of 100 Million USD. 
                **Previousclose**: In USD.  
                **Revenuegrowth, Earningsgrowth, Profitmargins**: are in percentage.  
                **Operatingcashflow, Freecashflow, Totalrevenue**: are in 100 Million USD.''')

with middle:
    st.write("Example query:")
    multi = '''
    Marketcap > 1000 &  
    Previousclose > 10 &  
    Profitmargins > 10 &  
    Earningsgrowth > 10    
    '''
    st.markdown(multi)
    
with left:
    #   Text area for query input
    st.text_area(
        "Enter your query:",
        key="rawQuery",
        placeholder="Type your query here", height=85)
    st.button("Show Results", key="submit", on_click=submitQuery)

#   Conditionally display the table below the button
if "result_table" in st.session_state:
    st.write("Results:")
    st.dataframe(st.session_state["result_table"], 
                 height=min(700, 35*len(st.session_state["result_table"])),
                 hide_index=True)

