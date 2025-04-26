import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("final_housing_data.csv", parse_dates=["observation_date"])
    return df

df = load_data()

# Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Housing vs Mortgage", "CPI vs Unemployment", "Income and GDP", "Housing Starts", "Correlation Heatmap", "Scatter Matrix", "Monthly Trends", "Yearly Boxplot", "GDP vs Housing"])

# Line chart colors
colors = {
    "Home_Price_Index": "blue",
    "Mortgage_Rate": "red",
    "CPI": "orange",
    "Unemployment_Rate": "green",
    "Median_Income": "purple",
    "Housing_Starts": "brown",
    "Real_GDP": "teal"
}

# Shared year filter
years = df["Year"].unique()
start_year, end_year = st.sidebar.select_slider("Select Year Range", options=sorted(years), value=(min(years), max(years)))
filtered_df = df[(df["Year"] >= start_year) & (df["Year"] <= end_year)]

# HOME PAGE
if page == "Home":
    st.title("\U0001F3E1 HOME.LLC: US Housing and Economic Analysis Dashboard")
    st.markdown("""
    Welcome to **HOME.LLC** — an interactive data science dashboard exploring the key factors that have influenced **US home prices** nationally over the past 20 years.

    **Key Metrics Explored:**
    - Home Price Index vs Mortgage Rate
    - Consumer Price Index (CPI) vs Unemployment Rate
    - Median Household Income and Real GDP
    - Monthly Housing Starts

    Use the **sidebar navigation** to explore different analyses and visualizations!
    """)


    # Show two main charts on home page
    st.subheader("\U0001F4C8 Home Price Index vs Mortgage Rate")
    fig1 = px.line(filtered_df, x="observation_date", y=["Home_Price_Index", "Mortgage_Rate"],
                   color_discrete_map={k: colors[k] for k in ["Home_Price_Index", "Mortgage_Rate"]})
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("\U0001F4CA CPI and Unemployment Rate")
    fig2 = px.line(filtered_df, x="observation_date", y=["CPI", "Unemployment_Rate"],
                   color_discrete_map={k: colors[k] for k in ["CPI", "Unemployment_Rate"]})
    st.plotly_chart(fig2, use_container_width=True)

# PAGE: Housing vs Mortgage
elif page == "Housing vs Mortgage":
    st.title("Housing Price Index vs Mortgage Rate")
    fig = px.line(filtered_df, x="observation_date", y=["Home_Price_Index", "Mortgage_Rate"],
                  color_discrete_map={k: colors[k] for k in ["Home_Price_Index", "Mortgage_Rate"]})
    st.plotly_chart(fig, use_container_width=True)

# PAGE: CPI vs Unemployment
elif page == "CPI vs Unemployment":
    st.title("CPI and Unemployment Rate")
    fig = px.line(filtered_df, x="observation_date", y=["CPI", "Unemployment_Rate"],
                  color_discrete_map={k: colors[k] for k in ["CPI", "Unemployment_Rate"]})
    st.plotly_chart(fig, use_container_width=True)

# PAGE: Income and GDP
elif page == "Income and GDP":
    st.title("Median Income and Real GDP")
    fig = px.line(filtered_df, x="observation_date", y=["Median_Income", "Real_GDP"],
                  color_discrete_map={k: colors[k] for k in ["Median_Income", "Real_GDP"]})
    st.plotly_chart(fig, use_container_width=True)

# PAGE: Housing Starts
elif page == "Housing Starts":
    st.title("Monthly Housing Starts")
    fig = px.bar(filtered_df, x="observation_date", y="Housing_Starts", color_discrete_sequence=[colors["Housing_Starts"]])
    st.plotly_chart(fig, use_container_width=True)

# PAGE: Correlation Heatmap
elif page == "Correlation Heatmap":
    st.title("Correlation Heatmap")
    corr = filtered_df.drop(columns=["Year", "Month", "Day"]).corr()
    fig_corr, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
    st.pyplot(fig_corr)

# PAGE: Scatter Matrix
elif page == "Scatter Matrix":
    st.title("Pairwise Scatter Plot Matrix")
    selected_vars = st.multiselect("Choose variables to explore:", options=df.columns[1:-3],
                                    default=["Home_Price_Index", "Mortgage_Rate", "CPI"])
    if len(selected_vars) >= 2:
        fig_pair = sns.pairplot(filtered_df[selected_vars])
        st.pyplot(fig_pair)
    else:
        st.info("Please select at least 2 variables.")

# PAGE: Monthly Trends
elif page == "Monthly Trends":
    st.title("Monthly Average Trends Over Time")
    monthly_avg = df.groupby("Month").mean(numeric_only=True)
    fig = px.line(monthly_avg.reset_index(), x="Month", y=["Home_Price_Index", "Mortgage_Rate", "CPI"],
                  color_discrete_map=colors)
    fig.update_layout(xaxis=dict(tickmode='linear'), legend_title="Metric")
    st.plotly_chart(fig, use_container_width=True)

# PAGE: Yearly Boxplot
elif page == "Yearly Boxplot":
    st.title("Yearly Distribution of Home Price Index")
    fig = px.box(filtered_df, x="Year", y="Home_Price_Index", color_discrete_sequence=["skyblue"])
    st.plotly_chart(fig, use_container_width=True)

# PAGE: GDP vs Housing
elif page == "GDP vs Housing":
    st.title("Real GDP vs Housing Starts")
    fig = px.scatter(filtered_df, x="Real_GDP", y="Housing_Starts",
                     color="Year", size="Home_Price_Index",
                     color_continuous_scale="Viridis")
    st.plotly_chart(fig, use_container_width=True)