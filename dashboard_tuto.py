import streamlit as st
import pandas as pd
from pympler.util.bottle import app
import numpy as np
import plotly.express as px
import time
import plotly.graph_objects as go
#from plotly.subplots import make_subplots as ms
st.set_page_config(page_title='SWAST - Handover Delays',  layout='wide')
t1, t2 = st.columns((0.07, 1))
t1.image('R.jpeg', width=120)
t2.title("My Marketing Dashboard")
t2.markdown("This app is created by Moussa Fall as a academic project")
st.balloons()

def merge_data(data_files):
    if len(data_files) < 2:
        return {'error': 'Please provide at least two data files.'}

    data_frames = []
    for file in data_files:
        if file.name.endswith('.csv'):
            data_frames.append(pd.read_csv(file))
        elif file.name.endswith('.xlsx'):
            data_frames.append(pd.read_excel(file))
        else:
            return {'error': 'Unsupported file format. Please use CSV or Excel files.'}

    merged_data = data_frames[0]
    for df in data_frames[1:]:
        merged_data = pd.merge(merged_data, df, on="cookie_id")
    return merged_data

def main():
    st.sidebar.title("Merge data")
    st.sidebar.write("Please select at least two data files for merging.")

    data_files = st.sidebar.file_uploader("Load data files", accept_multiple_files=True)
    if data_files:
        data = merge_data(data_files)
        st.write("Merged data:")
        st.write(data)
    st.sidebar.markdown("Here, I wanted to highlight another automatic way to download and merge datasets. Thus, I created a function that preloads and merges the datasets from two files. However, this method is also limited as it would require adapting the variable names to visualize the graphs if we were to change the data.")

if __name__ == "__main__":
    main()

#Loading the data
def load_data():
    impressions = pd.read_csv("impressions.csv", parse_dates=['timestamp'])
    achats = pd.read_csv("achats.csv", parse_dates=['timestamp'])
    clics = pd.read_csv("clics.csv", parse_dates=['timestamp'])
    merged_data1 = pd.merge(impressions, clics, on='cookie_id', how='left')
    merged_data = pd.merge(merged_data1, achats, on='cookie_id', how='left')
    merged_data = pd.DataFrame(merged_data)
    return merged_data

base=load_data()
basefinale = pd.DataFrame(base)

toggle = st.checkbox("To view data", value=True, help="Untick if you wanna see data.")
click = st.button("Data", disabled=bool(toggle))
if click:
    st.write(basefinale)

with st.spinner('Wait for it...'):
    time.sleep(10)


campaign_filter = st.selectbox("Select the campaign id", pd.unique(basefinale['campaign_id']))


# creating a single-element container.
placeholder = st.empty()

# dataframe filter

df = basefinale[basefinale['campaign_id'] == campaign_filter]



for seconds in range(20):


#creating KPIs
    avg_age = np.mean(df['age'])
    avg_age_global = np.mean(basefinale['age'])
    avg_ages = df.groupby('product_id')['age'].mean().reset_index()

    turnover_by_campaign = int(df["price"].sum())

    nb_achats = df['timestamp_y'].count()

    chiffre_affaires = int(basefinale['price'].sum())

with placeholder.container():

    # create three columns
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    # fill in those three columns with respective metrics or KPIs
    kpi1.metric(label="Age ⏳", value=round(avg_age), delta=round(avg_age_global))
    kpi2.metric(label="Turnover by campaign in €", value=round(turnover_by_campaign))
    kpi3.metric(label="Total achats by campaign", value=(nb_achats))
    with kpi4:
        st.markdown("Total turnover")
        st.write(f"<span style='color:red; font-size:25px;'> {chiffre_affaires} € </span>", unsafe_allow_html=True)

fig_col01, fig_col02 = st.columns(2)
with fig_col01:
    fig = px.box(df, x='product_id', y='age')
    fig.update_layout(
        xaxis_title='Products',
        yaxis_title="Age",
        title="Age and Products by campaign")
    st.plotly_chart(fig, use_container_width=True)

with fig_col02:
    fig2 = px.bar(data_frame=avg_ages, x="product_id", y="age")
    fig.update_layout(
        xaxis_title='Product_id',
        yaxis_title="Average age",
        title="Average ages by product")
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("#### Below are the overall results, i.e., for the entire three advertising campaigns.")

fig_col1, fig_col2 = st.columns(2)
with fig_col1:
    nb_clics = int(basefinale['timestamp_x'].count())
    nb_achats = basefinale['timestamp_y'].count()
    nb_impressions = basefinale['timestamp'].count()
    fig2 = go.Figure(
        go.Funnel(
            y=['Clics', 'Achats', 'Impressions'],
            x=[nb_clics, nb_achats, nb_impressions]
        )
    )

    fig2.update_layout(
        title="Conversion funnel"
    )

    st.plotly_chart(fig2, use_container_width=True)
with fig_col2:
    fig2 = px.histogram(data_frame=base, y='price', x='gender')
    fig2.update_layout(
        title="Sales by gender")
    st.plotly_chart(fig2, use_container_width=True)

fig_col1, fig_col2 = st.columns(2)
with fig_col1:
    fig = px.box(basefinale, x='product_id', y='age')
    fig.update_layout(
        xaxis_title='Products',
        yaxis_title="Âge",
        title="Relationship between Age and Products")
    st.plotly_chart(fig, use_container_width=True)

    with fig_col2:
        fig2 = px.bar(data_frame=basefinale, x="campaign_id", y="price")
        fig2.update_layout(
            xaxis_title='campaign_id',
            yaxis_title="price",
            title="Average ages by product")
        st.plotly_chart(fig2, use_container_width=True)

st.markdown("### Detailed Data View")
st.write(base)
with st.expander("Contact us"):
    with st.form(key='contact', clear_on_submit=True):
        email = st.text_input('Contact Email')
        st.text_area("Query", "Please fill in all the information or we may not be able to process your request")

        submit_button = st.form_submit_button(label='Send Information')

if __name__ == '__dashboard_tuto__':
    app.run(debug=True)



