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
        filtered_df['Symbol'] = filtered_df['Symbol'].apply(
            lambda x: f'<a href="https://finance.yahoo.com/quote/{x}" target="_blank">{x}</a>')
        data_to_show = filtered_df[columns_to_show]
        st.session_state["result_table"] = pd.DataFrame(data_to_show)
    

#   Start of the main page elements.
st.set_page_config(layout="wide")
st.title("Stock Screener")
left, right = st.columns(2, gap="large", 
                         vertical_alignment='top', border=True)

data = pd.read_csv("stocksData.csv")
columns_to_show = ["Symbol", "Shortname", "Marketcap", "Volume", "Previousclose", "Dividendyield", "Trailingpe",
                     "Returnonequity", "Grossprofits", "Freecashflow", "Earningsgrowth", "Revenuegrowth", 
                     "Pricetobook", "Totalrevenue", "Debttoequity", "Revenuepershare", "Profitmargins", "Ebitdamargins"]

with right:
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
        placeholder="Type your query here")
    st.button("Show Results", key="submit", on_click=submitQuery)

#   Conditionally display the table below the button
if "result_table" in st.session_state:
    st.write("Results:")
    with st.container(border=True,height=700):
        st.markdown(st.session_state["result_table"].to_html(escape=False), unsafe_allow_html=True)
    