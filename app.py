import altair as alt
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="US Funds Dashboard",
    page_icon="🌍",
    layout="wide",
)

st.sidebar.title("US Funds Dashboard")
horizon = st.sidebar.selectbox("Horizon", ("3 Years", "5 Years", "10 Years"))
quote = st.sidebar.selectbox("Quote type", ("None", "ETF", "Mutual Fund"))
investment = st.sidebar.selectbox(
    "Investment type", ("None", "Value", "Growth", "Blend")
)
size = st.sidebar.selectbox("Size type", ("None", "Large", "Medium", "Small"))


@st.cache
def load_data():
    data = pd.read_parquet("data/data.parquet")
    return data


@st.cache
def load_source(data, quote, investment, size):
    if quote != "None":
        data = data.loc[data.quote_type == quote.replace(" ", "")]
    if investment != "None":
        data = data.loc[data.investment_type == investment]
    if size != "None":
        data = data.loc[data.size_type == size]
    return data


def plot_risk_return(source, horizon):
    horizon = horizon.replace(" ", "").lower()
    return (
        alt.Chart(source)
        .mark_circle(size=20)
        .encode(
            x=f"fund_stdev_{horizon}",
            y=f"fund_return_{horizon}",
            tooltip=[
                "fund_symbol",
                f"fund_stdev_{horizon}",
                f"fund_return_{horizon}",
                "asset_bonds",
                "asset_stocks",
                "investment_type",
                "size_type",
            ],
        )
        .interactive()
    )


def plot_alpha_beta(source, horizon):
    horizon = horizon.replace(" ", "").lower()
    return (
        alt.Chart(source)
        .mark_circle(size=20)
        .encode(
            x=f"fund_alpha_{horizon}",
            y=f"fund_beta_{horizon}",
            tooltip=[
                "fund_symbol",
                f"fund_alpha_{horizon}",
                f"fund_beta_{horizon}",
                "asset_bonds",
                "asset_stocks",
                "investment_type",
                "size_type",
            ],
        )
        .interactive()
    )


def load_symbols(source):
    return source.fund_symbol.to_list()


def load_metrics(source, symbol, horizon):
    source = source.loc[source.fund_symbol == symbol, :].iloc[0]
    horizon = horizon.replace(" ", "").lower()
    fund_name = source["fund_long_name"]
    fund_risk = source[f"fund_stdev_{horizon}"]
    fund_return = source[f"fund_return_{horizon}"]
    fund_alpha = source[f"fund_alpha_{horizon}"]
    fund_beta = source[f"fund_beta_{horizon}"]
    investment_type = source["investment_type"]
    size_type = source["size_type"]
    asset_bonds = source["asset_bonds"]
    asset_stocks = source["asset_stocks"]
    return (
        fund_name,
        fund_risk,
        fund_return,
        fund_alpha,
        fund_beta,
        investment_type,
        size_type,
        asset_bonds,
        asset_stocks,
    )

def plot_symbol_risk_return(source, horizon, symbol):
    horizon = horizon.replace(" ", "").lower()
    return (
        alt.Chart(source)
        .mark_circle(size=20)
        .encode(
            x=f"fund_stdev_{horizon}",
            y=f"fund_return_{horizon}",
            color=alt.condition(
                alt.datum.fund_symbol == symbol,
                alt.value("#1f77b4"),
                alt.value("lightgrey"),
            ),
            tooltip=[
                "fund_symbol",
                f"fund_stdev_{horizon}",
                f"fund_return_{horizon}",
                f"fund_alpha_{horizon}",
                f"fund_beta_{horizon}",
                "asset_bonds",
                "asset_stocks",
                "investment_type",
                "size_type",
            ],
        )
        .interactive()
    )

def plot_symbol_alpha_beta(source, horizon, symbol):
    horizon = horizon.replace(" ", "").lower()
    return (
        alt.Chart(source)
        .mark_circle(size=20)
        .encode(
            x=f"fund_alpha_{horizon}",
            y=f"fund_beta_{horizon}",
            color=alt.condition(
                alt.datum.fund_symbol == symbol,
                alt.value("#1f77b4"),
                alt.value("lightgrey"),
            ),
            tooltip=[
                "fund_symbol",
                f"fund_alpha_{horizon}",
                f"fund_beta_{horizon}",
                "asset_bonds",
                "asset_stocks",
                "investment_type",
                "size_type",
            ],
        )
        .interactive()
    )

data = load_data()
source = load_source(data, quote, investment, size)

symbol = st.sidebar.selectbox("Symbol", ["None"] + load_symbols(source))

if symbol != "None":
    (
        fund_name,
        fund_risk,
        fund_return,
        fund_alpha,
        fund_beta,
        investment_type,
        size_type,
        asset_bonds,
        asset_stocks,
    ) = load_metrics(source, symbol, horizon)

    col_1, col_2 = st.columns([1, 8])
    col_1.metric(label="Symbol", value=symbol)
    col_2.metric(label="Name", value=fund_name)

    col_1, col_2, col_3, col_4, col_5, col_6, col_7, col_8 = st.columns(8)
    col_1.metric(label="Investment Type", value=f"{investment_type}")
    col_2.metric(label="Size Type", value=f"{size_type}")
    col_3.metric(label="Bond Allocation", value=f"{asset_bonds:.0%}")
    col_4.metric(label="Stock Allocation", value=f"{asset_stocks:.0%}")
    col_5.metric(label="Risk", value=f"{fund_risk:.2f}")
    col_6.metric(label="Return", value=f"{fund_return:.0%}")
    col_7.metric(label="Alpha", value=f"{fund_alpha:.2f}")
    col_8.metric(label="Beta", value=f"{fund_beta:.2f}")

    col_1, col_2 = st.columns(2)
    with col_1:
        st.altair_chart(plot_symbol_risk_return(source, horizon, symbol), use_container_width=True)
    with col_2:
        st.altair_chart(plot_symbol_alpha_beta(source, horizon, symbol), use_container_width=True)
else:
    col_1, col_2 = st.columns(2)
    with col_1:
        st.altair_chart(plot_risk_return(source, horizon), use_container_width=True)
    with col_2:
        st.altair_chart(plot_alpha_beta(source, horizon), use_container_width=True)
