from imports import pd, st
st.set_page_config(layout="wide", )

@st.cache_data
def load_data():
    columns = ['Symbol', 'Shortname', 'Currency', 'Previousclose', 'Open', 'Daylow',
       'Dayhigh', 'Regularmarketpreviousclose', 'Regularmarketopen',
       'Regularmarketdaylow', 'Regularmarketdayhigh', 'Dividendrate',
       'Dividendyield', 'Fiveyearavgdividendyield', 'Beta', 'Trailingpe',
       'Forwardpe', 'Volume', 'Marketcap', 'Fiftytwoweeklow',
       'Fiftytwoweekhigh', 'Pricetosalestrailing12months', 'Fiftydayaverage',
       'Twohundreddayaverage', 'Profitmargins', 'Bookvalue', 'Pricetobook',
       'Earningsquarterlygrowth', 'Netincometocommon', 'Trailingeps',
       'Forwardeps', 'Enterprisetorevenue', 'Enterprisetoebitda',
       '52weekchange', 'Ebitda', 'Totaldebt', 'Quickratio', 'Currentratio',
       'Totalrevenue', 'Debttoequity', 'Revenuepershare', 'Returnonassets',
       'Returnonequity', 'Grossprofits', 'Freecashflow', 'Operatingcashflow',
       'Earningsgrowth', 'Revenuegrowth', 'Grossmargins', 'Ebitdamargins',
       'Operatingmargins', 'Trailingpegratio']
    default_columns = ["Symbol", "Shortname", "Marketcap", "Volume", "Previousclose", "Dividendyield", "Trailingpe",
                     "Returnonequity", "Grossprofits", "Freecashflow", "Earningsgrowth", "Revenuegrowth", 
                     "Pricetobook", "Totalrevenue", "Debttoequity", "Revenuepershare", "Profitmargins", "Ebitdamargins"]
    return pd.read_csv("stocksData.csv"), columns, default_columns
data, columns, default_columns = load_data()

if "columns_to_show" not in st.session_state:
    st.session_state["columns_to_show"] = default_columns
    
columns_to_show = []
buttons = [
    {"id": "peter_lynch", "title": "Peter Lynch", "subtitle": "Copying Peter Lynch"},
    {"id": "swing_trade", "title": "Possible Swing Trade", "subtitle": "Stocks that can be used for swing trades"},
    {"id": "growth_stocks", "title": "Growth Stocks", "subtitle": "Stocks with high growth potential"}]

def handle_button_click(button_id):
    queries = {"peter_lynch": "Trailingpe < 15 & Returnonequity > 20 & Debttoequity < 1",
               "swing_trade": "Fiftydayaverage > Twohundreddayaverage & Fiftydayaverage < Previousclose & Fiftydayaverage < Fiftytwoweekhigh",
               "growth_stocks": "Earningsgrowth > 20 & Revenuegrowth > 20 & Profitmargins > 10"}
    print(queries[button_id])
    st.write(f"🚀  Function triggered for: {button_id}")
    filtered_df = data.query(queries[button_id])
    data_to_show = filtered_df[st.session_state["columns_to_show"]]
    st.session_state["result_table_example"] = pd.DataFrame(data_to_show)

def submitQuery():
    raw_query = st.session_state.rawQuery
    queries = [i.strip("\n") for i in raw_query.split("&")]
    # for query in queries:
    #     print(query.strip())
    query = " & ".join(queries)
    print(query)
    if raw_query != "":
        filtered_df = data.query(query)
        data_to_show = filtered_df[st.session_state["columns_to_show"]]
        st.session_state["result_table"] = pd.DataFrame(data_to_show)

def autocomplete():
    pass
    

#   Start of the main page elements.
st.title("Stock Screener")
left, right = st.columns([0.6, 0.4], gap="medium", 
                         vertical_alignment='top', border=True)

with right:
    columns_to_show = st.multiselect("Select columns to display:", 
                                     columns, default=default_columns,
                                     key='columns_to_show')
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
        placeholder="Type your query here", 
        height=200)
    st.button("Show Results", key="submit", on_click=submitQuery)

#   Conditionally display the table below the button
if "result_table" in st.session_state:
    st.write("Results:")
    st.dataframe(st.session_state["result_table"], 
                 height=min(700, 45*len(st.session_state["result_table"])),
                 hide_index=True)

st.markdown('''
                **Marketcap**: In order of 1 Billion USD.    
                **Previousclose**: In USD.  
                **Revenuegrowth, Earningsgrowth, Profitmargins**: are in percentage.  
                **Operatingcashflow, Freecashflow, Totalrevenue**: In order of 1 Billion USD.''')

cols = st.columns(len(buttons))  # Create columns for each button

for i, button in enumerate(buttons):
    with cols[i]:  # Place each button in its respective column
        if st.button(f"""{button['title']}  
                     {button['subtitle']}""", key=button["id"]):
            st.session_state["selected_button"] = button["id"]

if "selected_button" in st.session_state:
    handle_button_click(st.session_state["selected_button"])
    if "result_table_example" in st.session_state:
        st.write("Results:")
        st.dataframe(st.session_state["result_table_example"], 
                    height=min(700, 45*len(st.session_state["result_table_example"])),
                    hide_index=True)