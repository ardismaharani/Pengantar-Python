
import streamlit as st
import pandas as pd
import matplotlib as plt
import seaborn as sns
from wordcloud import WordCloud
import plotly.express as px

# Menginput data
df = pd.read_csv("sentimentdataset.csv", sep=None, engine="python")

# Membersihkan kolom
df.columns = df.columns.str.strip()
df['Sentiment'] = df['Sentiment'].str.strip()
df['Country'] = df['Country'].str.strip()
df['Platform'] = df['Platform'].str.strip()

# Menormalisasikan fitur filter
df['Country'] = df['Country'].str.title()
df['Platform'] = df['Platform'].str.title()
df['Sentiment'] = df['Sentiment'].str.capitalize()

# Tema dashboard
st.set_page_config(page_title="Dashboard Sentimen Media Sosial", layout="wide")
st.markdown("""
    <style>
    body { background-color: #f5ecdc; color: #4e3d31; }
    .stApp { background-color: #f5ecdc; }
    .sidebar .sidebar-content { background-color: #e9d5b5; color: #4e3d31; }
    .css-1v3fvcr, .css-1d391kg, .css-qbe2hs, .css-1v0mbdj { color: #4e3d31; }
    h1, h2, h3, h4, h5, h6 { color: #5a4531; }
    .stDataFrame, .stDataFrame div, .stDataFrame th, .stDataFrame td { color: #4e3d31 !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("Dashboard Media Sosial")

# Sidebar Filters
st.sidebar.markdown("""
    <style>
    .css-1d391kg { background-color: #e9d5b5; color: #4e3d31; }
    </style>
    """, unsafe_allow_html=True)
st.sidebar.header("🔍 Filter Data")
selected_platform = st.sidebar.multiselect("🎯 Platform", df['Platform'].unique(), default=df['Platform'].unique())
selected_country = st.sidebar.multiselect("🌍 Negara", df['Country'].unique(), default=df['Country'].unique())
selected_sentiment = st.sidebar.multiselect("💬 Sentimen", df['Sentiment'].unique(), default=df['Sentiment'].unique())

# Filter data
df_filtered = df[
    df['Platform'].isin(selected_platform) &
    df['Country'].isin(selected_country) &
    df['Sentiment'].isin(selected_sentiment)
]

# Sentiment Distribution
st.subheader("Distribusi Sentimen")
sentiment_counts = df_filtered['Sentiment'].value_counts()
fig = px.pie(
    values=sentiment_counts.values,
    names=sentiment_counts.index,
    title='Sentiment Breakdown',
    color_discrete_sequence=["#75644f", "#a98965", "#dab98f", "#eddbc4", "#f8f2e7"]
)
st.plotly_chart(fig)

# Likes & Retweets berdasarkan Sentimen
st.subheader("Rata-rata Likes & Retweets berdasarkan Sentimen")
avg_metrics = df_filtered.groupby("Sentiment")[['Likes', 'Retweets']].mean().round(2)
st.dataframe(avg_metrics)

# Plot Time Series
st.subheader("Frekuensi Postingan per Hari")
df_filtered['Timestamp'] = pd.to_datetime(df_filtered['Timestamp'], errors='coerce')
df_time = df_filtered.set_index('Timestamp').resample('D').size()
st.line_chart(df_time)

# WordCloud Hashtags
st.subheader("Hashtag Word Cloud")
all_hashtags = ' '.join(df_filtered['Hashtags'].dropna().astype(str))
if all_hashtags:
    wc = WordCloud(width=800, height=300, background_color='#f8f2e7', colormap='copper').generate(all_hashtags)
    st.image(wc.to_array(), use_column_width=True)
else:
    st.info("No hashtags available to generate WordCloud.")

# Contoh postingan
st.subheader("Contoh Postingan")
st.dataframe(df_filtered[['Text', 'Sentiment', 'Platform', 'Likes', 'Retweets']].head(10))
