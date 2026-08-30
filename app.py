from pathlib import Path
from io import BytesIO
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from analysis import (
    load_data,
    clean_data,
    dataset_info,
    basic_analysis,
    competition_answers,
)

from ai_explanation import explain_findings


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Food Delivery Analytics",
    page_icon="🍔",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# PREMIUM MUTED PALETTE
# =========================================================

MUTED_BLUE = "#718096"
MUTED_SAGE = "#879A8B"
MUTED_TERRACOTTA = "#B07A6A"
MUTED_TAUPE = "#A69B8D"
MUTED_SLATE = "#667085"
MUTED_PLUM = "#8C7B8B"
MUTED_BLUE_GREY = "#78909C"


# =========================================================
# MATPLOTLIB SETTINGS
# =========================================================

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["axes.titleweight"] = "bold"
plt.rcParams["axes.titlecolor"] = MUTED_SLATE
plt.rcParams["axes.labelcolor"] = MUTED_SLATE
plt.rcParams["xtick.color"] = MUTED_SLATE
plt.rcParams["ytick.color"] = MUTED_SLATE


# =========================================================
# APP HEADER
# =========================================================

st.title("🍔 Food Delivery Analytics")

st.subheader(
    "Turning delivery data into operational insights"
)

st.write(
    "A Python + Pandas analytics dashboard for understanding "
    "delivery performance, traffic impact, route distance, "
    "weather conditions, and operational bottlenecks."
)

st.info(
    "🐍 Python + Pandas  |  📊 Data Analytics  |  "
    "📈 Statistical Analysis  |  🤖 AI Insights  |  "
    "🚫 No Machine Learning"
)


# =========================================================
# LOAD DATASET
# =========================================================

DATA_PATH = Path(__file__).parent / "food_delivery_dataset.csv"

try:
    df_raw = load_data(DATA_PATH)
except Exception as e:
    st.error(f"Unable to load the dataset: {e}")
    st.stop()


# =========================================================
# DATA CLEANING
# =========================================================

raw_info = dataset_info(df_raw)

try:
    df = clean_data(df_raw)
except Exception as e:
    st.error(f"Unable to clean the dataset: {e}")
    st.stop()

# =========================================================
# INTERACTIVE FILTERS
# =========================================================

with st.sidebar:

    st.divider()

    st.header("🎛️ Filters")

    filtered_df = df.copy()

    # Weather filter
    if "Weather_conditions" in df.columns:

        weather_options = sorted(
            df["Weather_conditions"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_weather = st.multiselect(
            "🌦️ Weather",
            weather_options,
            default=weather_options,
        )

        if selected_weather:
            filtered_df = filtered_df[
                filtered_df["Weather_conditions"]
                .astype(str)
                .isin(selected_weather)
            ]

    # Traffic filter
    if "Road_traffic_density" in df.columns:

        traffic_options = sorted(
            df["Road_traffic_density"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_traffic = st.multiselect(
            "🚦 Traffic",
            traffic_options,
            default=traffic_options,
        )

        if selected_traffic:
            filtered_df = filtered_df[
                filtered_df["Road_traffic_density"]
                .astype(str)
                .isin(selected_traffic)
            ]

    # Vehicle condition filter
    if "Vehicle_condition" in df.columns:

        vehicle_options = sorted(
            df["Vehicle_condition"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_vehicle = st.multiselect(
            "🚗 Vehicle Condition",
            vehicle_options,
            default=vehicle_options,
        )

        if selected_vehicle:
            filtered_df = filtered_df[
                filtered_df["Vehicle_condition"]
                .astype(str)
                .isin(selected_vehicle)
            ]

    # City filter
    if "City" in df.columns:

        city_options = sorted(
            df["City"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_city = st.multiselect(
            "🏙️ City",
            city_options,
            default=city_options,
        )

        if selected_city:
            filtered_df = filtered_df[
                filtered_df["City"]
                .astype(str)
                .isin(selected_city)
            ]

    # Order type filter
    if "Type_of_order" in df.columns:

        order_options = sorted(
            df["Type_of_order"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_order = st.multiselect(
            "📦 Order Type",
            order_options,
            default=order_options,
        )

        if selected_order:
            filtered_df = filtered_df[
                filtered_df["Type_of_order"]
                .astype(str)
                .isin(selected_order)
            ]

    st.caption(
        f"Showing **{len(filtered_df):,}** "
        f"of **{len(df):,}** deliveries"
    )

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("🍔 Analytics Dashboard")

    st.caption(
        "Food Delivery Analytics Challenge"
    )

    st.divider()

    st.write("### Dataset")

    st.write(
        f"📦 Raw records: **{len(df_raw):,}**"
    )

    st.write(
        f"🧹 Clean records: **{len(df):,}**"
    )

    st.write(
        f"📋 Columns: **{len(df_raw.columns)}**"
    )

    st.write(
        f"🔁 Duplicate rows: "
        f"**{raw_info['duplicate_records']:,}**"
    )

    st.divider()

    st.write("### Technology")

    st.write("🐍 Python")
    st.write("🐼 Pandas")
    st.write("📊 Matplotlib")
    st.write("🎈 Streamlit")
    st.write("🤖 Gemini AI")

    st.divider()

    st.caption(
        "Analytics dashboard built for the "
        "Food Delivery Analytics Challenge."
    )


# =========================================================
# DATASET OVERVIEW
# =========================================================

st.header("📦 Dataset Overview")

st.caption(
    "A quick look at the size, structure, and quality "
    "of the original dataset."
)


# =========================================================
# DATASET METRICS
# =========================================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Raw Records",
    f"{len(df_raw):,}",
)

col2.metric(
    "Clean Records",
    f"{len(df):,}",
)

col3.metric(
    "Original Columns",
    f"{len(df_raw.columns)}",
)

col4.metric(
    "Duplicate Rows",
    f"{raw_info['duplicate_records']:,}",
)

st.caption(
    f"{len(df_raw):,} raw records loaded → "
    f"{len(df):,} records after cleaning"
)


# =========================================================
# DATA PREVIEW
# =========================================================

with st.expander("📋 Preview Dataset", expanded=True):

    st.dataframe(
        df_raw.head(10),
        use_container_width=True,
        hide_index=True,
    )


# =========================================================
# COLUMN NAMES
# =========================================================

with st.expander("📝 Original Column Names"):

    columns_df = pd.DataFrame(
        {
            "Column Number": range(
                1,
                len(df_raw.columns) + 1,
            ),
            "Column Name": df_raw.columns,
        }
    )

    st.dataframe(
        columns_df,
        use_container_width=True,
        hide_index=True,
    )


# =========================================================
# DATA TYPES
# =========================================================

with st.expander("🔤 Data Types"):

    dtype_table = pd.DataFrame(
        {
            "Column": df_raw.columns,
            "Data Type": df_raw.dtypes.astype(str).values,
        }
    )

    st.dataframe(
        dtype_table,
        use_container_width=True,
        hide_index=True,
    )


# =========================================================
# MISSING VALUES
# =========================================================

with st.expander("⚠️ Missing Values"):

    missing = (
        df_raw.isna()
        .sum()
        .rename("Missing Values")
    )

    missing_table = missing[
        missing > 0
    ].to_frame()

    if missing_table.empty:

        st.success(
            "✅ No missing values found."
        )

    else:

        st.dataframe(
            missing_table,
            use_container_width=True,
        )


# =========================================================
# CLEANING SUMMARY
# =========================================================

with st.expander("🧹 Cleaning Summary"):

    rows_removed = len(df_raw) - len(df)

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Rows Before",
        f"{len(df_raw):,}",
    )

    c2.metric(
        "Rows After",
        f"{len(df):,}",
    )

    c3.metric(
        "Rows Removed",
        f"{rows_removed:,}",
    )

    st.write(
        f"**Duplicate rows found:** "
        f"{raw_info['duplicate_records']:,}"
    )

    st.write("**Cleaning decisions:**")

    st.write(
        "• Exact duplicate rows were removed."
    )

    st.write(
        "• Relevant numeric columns were converted "
        "to numeric values."
    )

    st.write(
        "• Missing delivery-person age and rating "
        "values were filled using median values."
    )

    st.write(
        "• Invalid or non-positive delivery time "
        "and distance values were removed."
    )

    st.write(
        "• Delivery speed was calculated from "
        "distance and delivery time."
    )


# =========================================================
# BASIC ANALYSIS
# =========================================================

st.header("📊 Basic Analysis")

st.caption(
    "Key performance indicators calculated from "
    "the cleaned dataset."
)

metrics = basic_analysis(filtered_df)


# =========================================================
# KPI ROW 1
# =========================================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "🚚 Total Deliveries",
    f"{metrics['total_deliveries']:,}",
)

col2.metric(
    "⏱️ Avg Delivery Time",
    f"{metrics['average_delivery_time']:.2f} min",
)

col3.metric(
    "📍 Avg Distance",
    f"{metrics['average_delivery_distance']:.2f} km",
)

col4.metric(
    "🚀 Avg Speed",
    f"{metrics['average_delivery_speed']:.2f} km/h",
)


# =========================================================
# KPI ROW 2
# =========================================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "⚡ Minimum Time",
    f"{metrics['minimum_delivery_time']} min",
)

col2.metric(
    "🐢 Maximum Time",
    f"{metrics['maximum_delivery_time']} min",
)

col3.metric(
    "⭐ Avg Rating",
    f"{metrics['average_delivery_person_rating']:.2f}",
)

col4.metric(
    "👤 Avg Driver Age",
    f"{metrics['average_delivery_person_age']:.2f} years",
)


# =========================================================
# COMPETITION QUESTIONS
# =========================================================

st.header("🏆 Questions")

st.caption(
    "Key analytical questions answered using the cleaned dataset."
)


answers = competition_answers(filtered_df)


# =========================================================
# Q1 - TRAFFIC IMPACT
# =========================================================

st.subheader("Q1 • Traffic Impact")

traffic_results = (
    answers["q1_traffic"]
    .rename("Average Delivery Time (min)")
    .round(2)
)

st.dataframe(
    traffic_results,
    use_container_width=True,
    hide_index=False,
)

worst_traffic = answers["q1_traffic"].index[0]

worst_traffic_time = (
    answers["q1_traffic"].iloc[0]
)

st.success(
    f"🏆 **Answer:** {worst_traffic} traffic has the "
    f"highest average delivery time at "
    f"**{worst_traffic_time:.2f} minutes**."
)


# =========================================================
# Q2 - DISTANCE IMPACT
# =========================================================

st.subheader("Q2 • Distance Impact")

correlation = answers["q2_correlation"]

st.metric(
    "Pearson Correlation",
    f"{correlation:.3f}",
)

st.write(
    f"The Pearson correlation between delivery distance "
    f"and delivery time is **{correlation:.3f}**."
)

if correlation > 0:

    st.success(
        "📈 **Positive relationship**"
    )

    st.info(
        "Longer delivery distances generally require "
        "more delivery time."
    )

elif correlation < 0:

    st.warning(
        "📉 **Negative relationship**"
    )

    st.info(
        "Longer delivery distances are associated "
        "with lower delivery time in this dataset."
    )

else:

    st.info(
        "➖ **Little linear relationship**"
    )

    st.info(
        "The correlation is approximately zero, "
        "indicating little linear relationship between "
        "distance and delivery time."
    )


# =========================================================
# Q3 - COMBINED CONDITIONS
# =========================================================

st.subheader("Q3 • Combined Conditions")

weather_traffic_results = (
    answers["q3_weather_traffic"]
    .rename("Average Delivery Time (min)")
    .round(2)
)

st.dataframe(
    weather_traffic_results,
    use_container_width=True,
    hide_index=False,
)

top_combo = answers[
    "q3_weather_traffic"
].iloc[0]

top_weather, top_traffic = answers[
    "q3_weather_traffic"
].index[0]

st.success(
    f"🏆 **Answer:** The highest average delivery "
    f"time occurs under **{top_weather} weather + "
    f"{top_traffic} traffic**, at "
    f"**{top_combo:.2f} minutes**."
)
# =========================================================
# VISUALIZATION
# =========================================================

st.header("📈 Visualization")

st.caption(
    "Premium muted-tone visualizations highlighting "
    "the main drivers of delivery performance."
)


# =========================================================
# CHART 1 + CHART 2
# =========================================================

chart_col1, chart_col2 = st.columns(2)


# =========================================================
# CHART 1: TRAFFIC
# =========================================================

with chart_col1:

    st.subheader("🚦 Delivery Time by Traffic")

    traffic_data = (
        df.groupby(
            "Road_traffic_density"
        )["Time_taken (min)"]
        .mean()
        .sort_values(ascending=False)
    )

    fig1, ax1 = plt.subplots(
        figsize=(5.5, 3.0)
    )

    traffic_colors = [
        MUTED_TERRACOTTA,
        MUTED_TAUPE,
        MUTED_SAGE,
        MUTED_BLUE,
    ]

    bars1 = ax1.bar(
        traffic_data.index.astype(str),
        traffic_data.values,
        color=traffic_colors[
            :len(traffic_data)
        ],
        width=0.55,
        edgecolor="white",
        linewidth=1.2,
    )

    ax1.set_ylabel(
        "Average Time (min)",
        fontsize=8,
    )

    ax1.set_xlabel(
        "Traffic Density",
        fontsize=8,
    )

    ax1.set_title(
        "Average Delivery Time by Traffic",
        fontsize=11,
        fontweight="bold",
        pad=10,
    )

    ax1.tick_params(
        axis="both",
        labelsize=8,
    )

    ax1.grid(
        axis="y",
        linestyle="--",
        linewidth=0.7,
        alpha=0.20,
    )

    for bar in bars1:

        height = bar.get_height()

        ax1.text(
            bar.get_x() + bar.get_width() / 2,
            height + 0.25,
            f"{height:.1f}",
            ha="center",
            va="bottom",
            fontsize=8,
            fontweight="bold",
            color=MUTED_SLATE,
        )

    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)

    ax1.spines["left"].set_alpha(0.2)
    ax1.spines["bottom"].set_alpha(0.2)

    plt.tight_layout()

    st.pyplot(
        fig1,
        use_container_width=True,
    )

    plt.close(fig1)


# =========================================================
# CHART 2: DISTANCE VS TIME
# =========================================================

with chart_col2:

    st.subheader("📍 Distance vs Delivery Time")

    fig2, ax2 = plt.subplots(
        figsize=(5.5, 3.0)
    )

    ax2.scatter(
        df["distance_km"],
        df["Time_taken (min)"],
        alpha=0.20,
        s=10,
        color=MUTED_BLUE,
        edgecolors="none",
    )

    ax2.set_xlabel(
        "Delivery Distance (km)",
        fontsize=8,
    )

    ax2.set_ylabel(
        "Delivery Time (min)",
        fontsize=8,
    )

    ax2.set_title(
        "Delivery Distance vs Delivery Time",
        fontsize=11,
        fontweight="bold",
        pad=10,
    )

    ax2.tick_params(
        axis="both",
        labelsize=8,
    )

    ax2.grid(
        linestyle="--",
        linewidth=0.7,
        alpha=0.20,
    )

    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)

    ax2.spines["left"].set_alpha(0.2)
    ax2.spines["bottom"].set_alpha(0.2)

    plt.tight_layout()

    st.pyplot(
        fig2,
        use_container_width=True,
    )

    plt.close(fig2)


# =========================================================
# CHART 3 + CHART 4
# =========================================================

chart_col3, chart_col4 = st.columns(2)


# =========================================================
# CHART 3: WEATHER
# =========================================================

with chart_col3:

    st.subheader("🌦️ Delivery Time by Weather")

    weather_data = (
        df.groupby(
            "Weather_conditions"
        )["Time_taken (min)"]
        .mean()
        .sort_values(ascending=False)
    )

    fig3, ax3 = plt.subplots(
        figsize=(5.5, 3.0)
    )

    bars3 = ax3.bar(
        weather_data.index.astype(str),
        weather_data.values,
        color=MUTED_BLUE,
        width=0.55,
        edgecolor="white",
        linewidth=1.2,
    )

    ax3.set_ylabel(
        "Average Time (min)",
        fontsize=8,
    )

    ax3.set_xlabel(
        "Weather Condition",
        fontsize=8,
    )

    ax3.set_title(
        "Average Delivery Time by Weather",
        fontsize=11,
        fontweight="bold",
        pad=10,
    )

    ax3.tick_params(
        axis="both",
        labelsize=8,
    )

    ax3.tick_params(
        axis="x",
        rotation=25,
    )

    ax3.grid(
        axis="y",
        linestyle="--",
        linewidth=0.7,
        alpha=0.20,
    )

    for bar in bars3:

        height = bar.get_height()

        ax3.text(
            bar.get_x() + bar.get_width() / 2,
            height + 0.25,
            f"{height:.1f}",
            ha="center",
            va="bottom",
            fontsize=8,
            fontweight="bold",
            color=MUTED_SLATE,
        )

    ax3.spines["top"].set_visible(False)
    ax3.spines["right"].set_visible(False)

    ax3.spines["left"].set_alpha(0.2)
    ax3.spines["bottom"].set_alpha(0.2)

    plt.tight_layout()

    st.pyplot(
        fig3,
        use_container_width=True,
    )

    plt.close(fig3)


# =========================================================
# CHART 4: VEHICLE CONDITION
# =========================================================

with chart_col4:

    st.subheader("🚗 Delivery Time by Vehicle")

    vehicle_data = (
        df.groupby(
            "Vehicle_condition"
        )["Time_taken (min)"]
        .mean()
        .sort_values(ascending=False)
    )

    fig4, ax4 = plt.subplots(
        figsize=(5.5, 3.0)
    )

    bars4 = ax4.bar(
        vehicle_data.index.astype(str),
        vehicle_data.values,
        color=MUTED_SAGE,
        width=0.55,
        edgecolor="white",
        linewidth=1.2,
    )

    ax4.set_ylabel(
        "Average Time (min)",
        fontsize=8,
    )

    ax4.set_xlabel(
        "Vehicle Condition",
        fontsize=8,
    )

    ax4.set_title(
        "Average Delivery Time by Vehicle Condition",
        fontsize=11,
        fontweight="bold",
        pad=10,
    )

    ax4.tick_params(
        axis="both",
        labelsize=8,
    )

    ax4.grid(
        axis="y",
        linestyle="--",
        linewidth=0.7,
        alpha=0.20,
    )

    for bar in bars4:

        height = bar.get_height()

        ax4.text(
            bar.get_x() + bar.get_width() / 2,
            height + 0.25,
            f"{height:.1f}",
            ha="center",
            va="bottom",
            fontsize=8,
            fontweight="bold",
            color=MUTED_SLATE,
        )

    ax4.spines["top"].set_visible(False)
    ax4.spines["right"].set_visible(False)

    ax4.spines["left"].set_alpha(0.2)
    ax4.spines["bottom"].set_alpha(0.2)

    plt.tight_layout()

    st.pyplot(
        fig4,
        use_container_width=True,
    )

    plt.close(fig4)


# =========================================================
# AI-POWERED EXPLANATION
# =========================================================

st.header("🤖 AI-Powered Explanation")

st.caption(
    "Gemini interprets the calculated results and "
    "translates them into practical business meaning."
)


summary = (
    f"Total deliveries: "
    f"{metrics['total_deliveries']}. "

    f"Average delivery time: "
    f"{metrics['average_delivery_time']:.2f} minutes. "

    f"Minimum delivery time: "
    f"{metrics['minimum_delivery_time']} minutes. "

    f"Maximum delivery time: "
    f"{metrics['maximum_delivery_time']} minutes. "

    f"Average delivery distance: "
    f"{metrics['average_delivery_distance']:.2f} km. "

    f"Average delivery speed: "
    f"{metrics['average_delivery_speed']:.2f} km/h. "

    f"Average delivery-person rating: "
    f"{metrics['average_delivery_person_rating']:.2f}. "

    f"Average delivery-person age: "
    f"{metrics['average_delivery_person_age']:.2f} years. "

    f"Highest traffic average delivery time: "
    f"{worst_traffic} traffic = "
    f"{worst_traffic_time:.2f} minutes. "

    f"Distance/time Pearson correlation: "
    f"{correlation:.3f}. "

    f"Worst weather + traffic combination: "
    f"{top_weather} weather + "
    f"{top_traffic} traffic = "
    f"{top_combo:.2f} minutes."
)


try:

    with st.spinner(
        "🤖 Gemini is analyzing the findings..."
    ):

        explanation = explain_findings(
            summary
        )

    if explanation:

        st.success(
            "✅ AI analysis generated successfully."
        )

        st.info(
            explanation
        )

    else:

        st.warning(
            "The AI returned an empty response."
        )

except Exception as e:

    st.error(
        "AI explanation could not be generated."
    )

    st.caption(
        f"Error: {e}"
    )

# =========================================================
# AI BUSINESS RECOMMENDATIONS
# =========================================================

st.header("💡 AI Business Recommendations")

st.caption(
    "AI-generated operational recommendations based only "
    "on the calculated analytics."
)


recommendation_summary = (
    f"Total deliveries analyzed: "
    f"{metrics['total_deliveries']}. "

    f"Average delivery time: "
    f"{metrics['average_delivery_time']:.2f} minutes. "

    f"Average distance: "
    f"{metrics['average_delivery_distance']:.2f} km. "

    f"Average delivery speed: "
    f"{metrics['average_delivery_speed']:.2f} km/h. "

    f"Highest traffic delay: "
    f"{worst_traffic} traffic with "
    f"{worst_traffic_time:.2f} minutes. "

    f"Distance-time correlation: "
    f"{correlation:.3f}. "

    f"Worst weather and traffic combination: "
    f"{top_weather} weather + "
    f"{top_traffic} traffic with "
    f"{top_combo:.2f} minutes."
)


def generate_recommendations(summary):

    import os

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return (
            "AI recommendations are unavailable because "
            "GEMINI_API_KEY is not configured."
        )

    try:

        from google import genai

        client = genai.Client(
            api_key=api_key
        )

        prompt = (
            "You are a senior food-delivery business analyst. "
            "Based ONLY on the calculated results below, "
            "provide 3 practical business recommendations. "
            "Do not invent data. "
            "Keep the response under 150 words. "
            "Format the answer as exactly 3 numbered recommendations. "
            "Each recommendation should contain a short action "
            "and explain why it matters.\n\n"
            + summary
        )

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )

        return response.text.strip()

    except Exception as exc:

        return (
            f"AI recommendations could not be generated: "
            f"{exc}"
        )


try:

    with st.spinner(
        "🤖 Gemini is generating business recommendations..."
    ):

        recommendations = generate_recommendations(
            recommendation_summary
        )

    if recommendations:

        st.success(
            "✅ Business recommendations generated"
        )

        st.write(
            recommendations
        )

except Exception as e:

    st.warning(
        "AI recommendations could not be generated."
    )

    st.caption(
        f"Technical detail: {e}"
    )

# =========================================================
# KEY TAKEAWAYS
# =========================================================

st.header("🎯 Key Takeaways")

st.caption(
    "The most important findings from the food delivery analysis."
)

takeaway_col1, takeaway_col2, takeaway_col3 = st.columns(3)


# =========================================================
# TAKEAWAY 1
# =========================================================

with takeaway_col1:

    st.subheader("🚦 Traffic Bottleneck")

    st.metric(
        "Highest Average Time",
        f"{worst_traffic_time:.2f} min",
    )

    st.write(
        f"**{worst_traffic} traffic** produces the highest "
        "average delivery time."
    )

    st.caption(
        "Traffic congestion is an important operational "
        "factor affecting delivery speed."
    )


# =========================================================
# TAKEAWAY 2
# =========================================================

with takeaway_col2:

    st.subheader("📍 Distance Matters")

    st.metric(
        "Distance-Time Correlation",
        f"{correlation:.3f}",
    )

    st.write(
        "Delivery distance has a positive relationship "
        "with delivery time."
    )

    st.caption(
        "Longer routes generally require more time, "
        "although distance is not the only factor."
    )


# =========================================================
# TAKEAWAY 3
# =========================================================

with takeaway_col3:

    st.subheader("🌦️ Worst Conditions")

    st.metric(
        "Highest Average Time",
        f"{top_combo:.2f} min",
    )

    st.write(
        f"**{top_weather} weather + {top_traffic} traffic** "
        "creates the slowest delivery conditions."
    )

    st.caption(
        "Combined environmental and traffic conditions "
        "can significantly increase delivery delays."
    )


# =========================================================
# FINAL BUSINESS CONCLUSION
# =========================================================

st.divider()

st.subheader("💡 Business Conclusion")

st.info(
    f"Delivery performance is most affected by operational "
    f"conditions rather than distance alone. {worst_traffic} "
    f"traffic increases average delivery time to "
    f"{worst_traffic_time:.2f} minutes, while the combination "
    f"of {top_weather} weather and {top_traffic} traffic "
    f"produces the highest average time of {top_combo:.2f} "
    f"minutes. These findings suggest that managing traffic "
    f"and adverse operating conditions should be a priority "
    f"for improving delivery efficiency."
)

# =========================================================
# DOWNLOADABLE PDF REPORT
# =========================================================

st.header("📄 Download Analysis Report")

st.caption(
    "Generate a concise PDF report containing the "
    "key analytical findings."
)


def create_pdf_report():

    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.enums import TA_CENTER
    from reportlab.platypus import (
        SimpleDocTemplate,
        Paragraph,
        Spacer,
        Table,
        TableStyle,
    )
    from reportlab.lib import colors

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    title_style.alignment = TA_CENTER

    heading_style = styles["Heading2"]
    body_style = styles["BodyText"]

    story = []

    # -----------------------------------------------------
    # TITLE
    # -----------------------------------------------------

    story.append(
        Paragraph(
            "Food Delivery Analytics Report",
            title_style,
        )
    )

    story.append(
        Spacer(1, 20)
    )

    story.append(
        Paragraph(
            "Python + Pandas Analytics | No Machine Learning",
            body_style,
        )
    )

    story.append(
        Spacer(1, 20)
    )

    # -----------------------------------------------------
    # DATASET SUMMARY
    # -----------------------------------------------------

    story.append(
        Paragraph(
            "Dataset Summary",
            heading_style,
        )
    )

    story.append(
        Spacer(1, 8)
    )

    dataset_table = Table(
        [
            ["Metric", "Value"],
            [
                "Raw Records",
                f"{len(df_raw):,}",
            ],
            [
                "Clean Records",
                f"{len(df):,}",
            ],
            [
                "Columns",
                f"{len(df_raw.columns)}",
            ],
            [
                "Duplicate Rows",
                f"{raw_info['duplicate_records']:,}",
            ],
        ],
        colWidths=[250, 150],
    )

    dataset_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#667085"),
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.lightgrey,
                ),
                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
            ]
        )
    )

    story.append(
        dataset_table
    )

    story.append(
        Spacer(1, 20)
    )

    # -----------------------------------------------------
    # KPI SUMMARY
    # -----------------------------------------------------

    story.append(
        Paragraph(
            "Key Performance Indicators",
            heading_style,
        )
    )

    story.append(
        Spacer(1, 8)
    )

    kpi_table = Table(
        [
            ["Metric", "Result"],
            [
                "Total Deliveries",
                f"{metrics['total_deliveries']:,}",
            ],
            [
                "Average Delivery Time",
                f"{metrics['average_delivery_time']:.2f} min",
            ],
            [
                "Average Distance",
                f"{metrics['average_delivery_distance']:.2f} km",
            ],
            [
                "Average Speed",
                f"{metrics['average_delivery_speed']:.2f} km/h",
            ],
            [
                "Average Rating",
                f"{metrics['average_delivery_person_rating']:.2f}",
            ],
        ],
        colWidths=[250, 150],
    )

    kpi_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#879A8B"),
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.lightgrey,
                ),
                (
                    "PADDING",
                    (0, 0),
                    (-1, -1),
                    7,
                ),
            ]
        )
    )

    story.append(
        kpi_table
    )

    story.append(
        Spacer(1, 20)
    )

    # -----------------------------------------------------
    # COMPETITION ANSWERS
    # -----------------------------------------------------

    story.append(
        Paragraph(
            "Competition Questions",
            heading_style,
        )
    )

    story.append(
        Spacer(1, 8)
    )

    story.append(
        Paragraph(
            f"<b>Q1 - Traffic Impact:</b> "
            f"{worst_traffic} traffic has the highest "
            f"average delivery time at "
            f"{worst_traffic_time:.2f} minutes.",
            body_style,
        )
    )

    story.append(
        Spacer(1, 8)
    )

    story.append(
        Paragraph(
            f"<b>Q2 - Distance Impact:</b> "
            f"The Pearson correlation between delivery "
            f"distance and delivery time is "
            f"{correlation:.3f}.",
            body_style,
        )
    )

    story.append(
        Spacer(1, 8)
    )

    story.append(
        Paragraph(
            f"<b>Q3 - Combined Conditions:</b> "
            f"{top_weather} weather + {top_traffic} traffic "
            f"has the highest average delivery time at "
            f"{top_combo:.2f} minutes.",
            body_style,
        )
    )

    story.append(
        Spacer(1, 20)
    )

    # -----------------------------------------------------
    # BUSINESS CONCLUSION
    # -----------------------------------------------------

    story.append(
        Paragraph(
            "Business Conclusion",
            heading_style,
        )
    )

    story.append(
        Spacer(1, 8)
    )

    conclusion = (
        f"Traffic congestion and adverse weather conditions "
        f"are important operational bottlenecks. "
        f"{worst_traffic} traffic results in an average "
        f"delivery time of {worst_traffic_time:.2f} minutes, "
        f"while {top_weather} weather combined with "
        f"{top_traffic} traffic produces the highest "
        f"average delivery time of {top_combo:.2f} minutes. "
        f"Distance also has a positive relationship with "
        f"delivery time, with a Pearson correlation of "
        f"{correlation:.3f}."
    )

    story.append(
        Paragraph(
            conclusion,
            body_style,
        )
    )

    document.build(
        story
    )

    buffer.seek(0)

    return buffer


try:

    pdf_file = create_pdf_report()

    st.download_button(
        label="📥 Download PDF Report",
        data=pdf_file,
        file_name="food_delivery_analysis_report.pdf",
        mime="application/pdf",
    )

except Exception as e:

    st.warning(
        "PDF report could not be generated."
    )

    st.caption(
        f"Technical detail: {e}"
    )

# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🍔 Food Delivery Analytics Challenge • "
    "Python + Pandas • Matplotlib • Gemini AI • "
    "No Machine Learning"
)