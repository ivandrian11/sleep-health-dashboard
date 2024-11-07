import pandas as pd
import streamlit as st
import streamlit_shadcn_ui as ui

from func import calculate_metrics
from visualization import create_pie_chart, create_treemap, create_funnel_chart, create_plot_average_by_group

# Load the data
df = pd.read_csv('data/sleep_health.csv')

# Set the page layout to wide
st.set_page_config(layout="wide")

# Sidebar for filtering based on sleep disorders
sleep_disorder = df["sleep_disorder"].unique().tolist()
with st.sidebar:
    st.text("Total Population:")
    ui.badges(badge_list=[(f"{len(df)}", "secondary")], key="total_data")
    selected_data = st.multiselect("Select Data Based on Sleep Disorder", sleep_disorder, sleep_disorder)

# Filter the dataframe based on the selected sleep disorders
filtered_df = df[df["sleep_disorder"].isin(selected_data)]

# Get the metrics
metrics = calculate_metrics(filtered_df)

# Display the metrics dynamically
cols = st.columns(len(metrics))
for i, metric in enumerate(metrics):
    with cols[i]:
        ui.metric_card(
            title=metric["title"],
            content=metric["content"],
            description=metric["trend"],
            key=f"metric-{i+1}"
        )

# Display first visual column
first_visual = st.columns(3)
first_visual[0].plotly_chart(create_pie_chart(filtered_df, "gender", "Gender", hole=0.4))
first_visual[1].plotly_chart(create_funnel_chart(filtered_df, column="blood_pressure_category", label="Blood Pressure"))
first_visual[2].plotly_chart(create_pie_chart(filtered_df, "bmi_category", "BMI"))

# Display second visual column
second_visual = st.columns(2)
gender_icons = {
    'Female': 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/66/Venus_symbol.svg/120px-Venus_symbol.svg.png',
    'Male': 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/Mars_symbol.svg/120px-Mars_symbol.svg.png'
}
df_visual = filtered_df.copy()
df_visual["gender"] = df_visual["gender"].map(gender_icons)
df_visual["sleep_disorder"] = df_visual["sleep_disorder"].apply(lambda x: True if x != "No Issue" else False)
df_visual.drop(["age_group", "blood_pressure_category"], axis=1, inplace=True)

second_visual[0].plotly_chart(create_treemap(filtered_df, "occupation", "Job"))
with second_visual[1]:
    st.markdown("**DataFrame Version**")
    st.dataframe(df_visual, column_config={
        "gender": st.column_config.ImageColumn(),
        "sleep_disorder": st.column_config.CheckboxColumn(disabled=True),
        "quality_of_sleep": st.column_config.ProgressColumn(
            format="%f",
            min_value=0,
            max_value=10,
        ),
        "stress_level": st.column_config.ProgressColumn(
            format="%f",
            min_value=0,
            max_value=10,
        ),
    }, hide_index=True)

# Display third visual column
third_visual = st.columns(2)
third_visual[0].plotly_chart(create_plot_average_by_group(filtered_df, group_column="age_group", value_column="daily_steps"))
third_visual[1].plotly_chart(create_plot_average_by_group(filtered_df, group_column="age_group", value_column="sleep_duration"))