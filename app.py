from classes import Page
from dfseo import RestClient
import base64
import pandas as pd
import streamlit as st

def generate_meta_tags(url_argument, username, password):
    content = Page(url_argument).content()
    client = RestClient(username, password)
    post_data = dict()
    post_data[len(post_data)] = dict(
        text=content[0:1800],
        creativity=0.9)
#     response = client.post("https://sandbox.dataforseo.com/v3/content_generation/generate_meta_tags/live", post_data)
    response = client.post("/v3/content_generation/generate_meta_tags/live", post_data)
    title = response["tasks"][0]["result"][0]["title"]
    description = response["tasks"][0]["result"][0]["description"]
    return url_argument, title, len(title), description, len(description)

st.set_page_config(layout="wide", page_title="Description Generator")
with st.form(key='Meta Tag Bulk Generator'):
    col1, col2 = st.columns(2)
    with col1:
        st.header("***Meta Tag Bulk Generator***", anchor=None)
        url_input = st.text_area("Enter full URLs. Maximum of 500 URLs.", height=300, placeholder="https://currentdomain.com/current-page")
        url_input = url_input.split()
    with col2:
        st.header("An App by Francis Angelo Reyes of [Lupage Digital](https://www.lupagedigital.com/?utm_source=streamlit&utm_medium=referral&utm_campaign=metatag)")
        api_username = st.text_input("Enter API username here", placeholder="yourcredentials@email.com")
        api_password = st.text_input("Enter API password here",placeholder="1234xx5x6xxx7x80")
        st.markdown("Get your API credentials from [DataForSEO](https://dataforseo.com/?aff=124940). You can find the credentials under the navgitation bar: API Settings > API access.")
    submit_button = st.form_submit_button(label='Generate Meta Tags')

data_for_dataframe = []
count = 0
my_bar = st.progress(count)

if submit_button:    
    if len(url_input) > 500:
        st.warning("Enter up to 500 URLs only")
    else:
        for element in url_input:
            data_for_dataframe.append(generate_meta_tags(element, api_username, api_password))
            count += 1 / len(url_input)
            my_bar.progress(round(count,3))

    df = pd.DataFrame(data=data_for_dataframe)
    df.columns = ["URL", "Title", "Title length", "Description", "Description length"]
    df.index = df.index + 1
    st.table(df)
    csv = df.to_csv()
    b64 = base64.b64encode(csv.encode()).decode()
    st.markdown('### **⬇️ Download output CSV File **')
    href = f"""(Don't left-click. Instead, right-click, select "Save link as...", then save as "download.csv".) <a href="data:file/csv;base64,{b64}">Download CSV File</a> """
    st.markdown(href, unsafe_allow_html=True)
