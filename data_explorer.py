import pandas as pd
import streamlit as st
import plotly.express as px

st.title("Kickbase Analyzer")

players_df = pd.read_csv("player_data_sample.csv")
players_df.date = pd.to_datetime(players_df.date)
players_df.date = players_df.date.dt.date
players_df["full_name"] = players_df["first_name"] + " " + players_df["last_name"]
# players_df = players_df.sort_values(by="last_name")

with st.sidebar:
    start = st.date_input("Start", value=players_df["date"].min())
    end = st.date_input("Ende", value=players_df["date"].max())
    top_n = st.number_input("Show top n players", min_value=1, max_value=players_df.full_name.unique().shape[0], value=10)    

players_df = players_df[(players_df["date"] >= start) & (players_df["date"] <= end)]
# players_df = players_df[players_df["full_name"].isin(players_selection)]
pre_agg_df = players_df[["last_name", "first_name", "team_id", "id", "market_value"]]

agg_df = pre_agg_df.groupby(by=["last_name", "first_name", "team_id", "id"]) \
    .aggregate(["min", "max", "mean"]) \
    .reset_index()

agg_df = pd.merge(right=players_df.loc[players_df["date"] == start, ["first_name", "last_name", "market_value"]], left=agg_df, on=["last_name", "first_name"])
agg_df = pd.merge(right=players_df.loc[players_df["date"] == end, ["first_name", "last_name", "market_value"]], left=agg_df, on=["last_name", "first_name"])
agg_df = agg_df.rename(columns={"market_value_x":"market_value_start", "market_value_y":"market_value_end"})
agg_df["value_development"] = (agg_df["market_value_start"] - agg_df["market_value_end"]) / agg_df["market_value_end"] * 100
agg_df["value_development"] = agg_df["value_development"].apply(lambda x: str(x) + " %")

with st.sidebar:
    show_columns = st.multiselect("Show columns", agg_df.columns, default=["first_name", "last_name", "value_development", "market_value_start", "market_value_end"])
    order_by = st.multiselect("Order by", agg_df.columns)
    ascendig = st.selectbox("Sort ascending", [True, False])
    players_selection = st.multiselect("Select players for plot", players_df["full_name"].unique())

agg_df = agg_df[show_columns]
agg_df = agg_df.sort_values(by=order_by, ascending=ascendig)
agg_df = agg_df.head(top_n)

st.dataframe(agg_df)

filtered_df = players_df.loc[players_df["full_name"].isin(players_selection)]
filtered_df["date_num"] = filtered_df.groupby(by=["first_name", "last_name"]).cumcount()
fig = px.scatter(filtered_df, x="date_num", y="market_value", color='full_name', trendline="ols", hover_data=["market_value", "date"])
st.plotly_chart(fig)
