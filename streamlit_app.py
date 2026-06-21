# ============================================================================
# BEGINNER STREAMLIT TUTORIAL: CAT FITBIT TRACKER
# ============================================================================
# This is a simple tutorial project to learn Streamlit basics.
# It shows how to:
# 1. Define static data
# 2. Create a DataFrame from that data
# 3. Display data in a table
# 4. Create simple charts
#
# Read through the comments to understand each step!
# ============================================================================

# Step 1: Import the libraries we need
# ----------------------------------
import streamlit as st  # Streamlit - for building web apps
import pandas as pd     # Pandas - for working with data tables
import altair as alt    # Altair - for creating charts

# ============================================================================
# STEP 2: CONFIGURE THE PAGE
# ============================================================================
# This sets the title and icon that appear in the browser tab
st.set_page_config(
    page_title="Cat Fitbit Tracker",  # Browser tab title
    page_icon=":cat:",                 # Browser tab icon (emoji)
)

# ============================================================================
# STEP 3: DEFINE STATIC DATA
# ============================================================================
# This is our data. Each row represents one cat activity.
# Each tuple is: (event_id, activity, start_time, duration_in_minutes)
#
# Think of it like a list of records in a spreadsheet!

cat_activities = [
    (1, 'Sleeping', '2026-01-15 22:00', 480),
    (2, 'Eating', '2026-01-16 08:00', 15),
    (3, 'Purring', '2026-01-16 09:00', 45),
    (4, 'Drinking', '2026-01-16 12:00', 5),
    (5, 'Sleeping', '2026-01-16 13:00', 240),
    (6, 'Playing', '2026-01-16 17:00', 30),
    (7, 'Eating', '2026-01-16 18:00', 10),
    (8, 'Purring', '2026-01-16 19:00', 60),
    (9, 'Drinking', '2026-01-16 20:00', 3),
    (10, 'Sleeping', '2026-01-16 21:00', 540),
]

# ============================================================================
# STEP 4: CREATE A DATAFRAME
# ============================================================================
# A DataFrame is like a spreadsheet table in Python.
# We're converting our list of tuples into a nice table with column names.

df = pd.DataFrame(
    cat_activities,  # Our data from above
    columns=[        # Column names for our table
        "event_id",
        "activity",
        "start_time",
        "event_duration",
    ],
)

# ============================================================================
# STEP 5: DISPLAY CONTENT ON THE WEB PAGE
# ============================================================================

# Add a title to the page
st.title("🐱 Cat Fitbit Tracker")

# Add some descriptive text
st.write("""
This is a simple Streamlit app that displays cat activity data.
Below you can see:
- A table of all activities
- Charts showing activity durations and frequency
""")

# ============================================================================
# Display the data as a table
# ============================================================================
st.subheader("📊 All Cat Activities")
st.dataframe(df)

# ============================================================================
# Display some statistics
# ============================================================================
st.subheader("📈 Statistics")
# st.columns() creates multiple columns side-by-side
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Total Activities",
        value=len(df)  # Count how many rows we have
    )

with col2:
    total_minutes = df['event_duration'].sum()  # Add up all durations
    st.metric(
        label="Total Minutes Tracked",
        value=total_minutes
    )

with col3:
    avg_duration = df['event_duration'].mean()  # Average duration
    st.metric(
        label="Average Duration (mins)",
        value=f"{avg_duration:.1f}"
    )

# ============================================================================
# STEP 6: CREATE A SIMPLE BAR CHART
# ============================================================================
# This chart shows how long each activity lasted
# Altair is a powerful library for creating interactive charts

st.subheader("⏱️ Activity Duration Chart")

# Create a simple bar chart
# .mark_bar() means we want a bar chart
# .encode() tells it which columns to use for what
chart = alt.Chart(df).mark_bar().encode(
    x='event_duration',      # X-axis: duration of activity
    y='activity',             # Y-axis: name of activity
    color='activity',         # Color each activity differently
).properties(
    width=600,
    height=400,
    title="How long did each activity last?"
)

# Display the chart
st.altair_chart(chart, use_container_width=True)

# ============================================================================
# STEP 7: CREATE ANOTHER CHART - Activity Frequency
# ============================================================================
# This chart shows how many times each activity happened

st.subheader("🔄 Activity Frequency")

# Count how many times each activity appears in the data
# .value_counts() counts occurrences of each activity
activity_counts = df['activity'].value_counts().reset_index()
activity_counts.columns = ['activity', 'count']

# Create a bar chart of activity frequency
frequency_chart = alt.Chart(activity_counts).mark_bar().encode(
    x='count',
    y='activity',
    color=alt.Color('count', scale=alt.Scale(scheme='viridis')),  # Nice colors!
).properties(
    width=600,
    height=300,
    title="How many times did the cat do each activity?"
)

st.altair_chart(frequency_chart, use_container_width=True)

# ============================================================================
# Done! That's the basics of Streamlit!
# ============================================================================
#
# KEY CONCEPTS YOU LEARNED:
# 1. st.title() - Add a title
# 2. st.write() - Add text
# 3. st.dataframe() - Display a table
# 4. st.subheader() - Add a section heading
# 5. st.metric() - Show a single metric
# 6. st.columns() - Create side-by-side columns
# 7. st.altair_chart() - Display a chart
# 8. pd.DataFrame() - Create a table from data
# 9. alt.Chart() - Create an interactive chart
#
# NEXT STEPS TO LEARN:
# - Try st.slider() to filter data
# - Try st.selectbox() to pick activities
# - Try st.line_chart() for line charts
# - Read the Streamlit documentation at streamlit.io
# ============================================================================
