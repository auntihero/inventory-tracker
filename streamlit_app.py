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
    (1, '2026-06-01', 'Monday', 'Sleeping', '22:00', 480),
    (2, '2026-06-01', 'Monday', 'Eating', '08:00', 15),
    (3, '2026-06-01', 'Monday', 'Purring', '09:00', 45),
    (4, '2026-06-01', 'Monday', 'Drinking', '12:00', 5),
    (5, '2026-06-01', 'Monday', 'Sleeping', '13:00', 240),
    (6, '2026-06-01', 'Monday', 'Playing', '17:00', 30),
    (7, '2026-06-01', 'Monday', 'Eating', '18:00', 10),
    (8, '2026-06-01', 'Monday', 'Purring', '19:00', 60),
    (9, '2026-06-01', 'Monday', 'Drinking', '20:00', 3),
    (10, '2026-06-02', 'Tuesday', 'Sleeping', '21:00', 240),
    (11, '2026-06-02', 'Tuesday', 'Sleeping', '22:00', 480),
    (12, '2026-06-02', 'Tuesday', 'Eating', '08:00', 15),
    (13, '2026-06-02', 'Tuesday', 'Purring', '09:00', 45),
    (14, '2026-06-02', 'Tuesday', 'Drinking', '12:00', 5),
    (15, '2026-06-02', 'Tuesday', 'Sleeping', '13:00', 240),
    (16, '2026-06-02', 'Tuesday', 'Playing', '17:00', 30),
    (17, '2026-06-02', 'Tuesday', 'Eating', '18:00', 10),
    (18, '2026-06-02', 'Tuesday', 'Purring', '19:00', 60),
    (19, '2026-06-02', 'Tuesday', 'Drinking', '20:00', 3),
    (20, '2026-06-02', 'Tuesday', 'Sleeping', '21:00', 240),
    (21, '2026-06-03', 'Wednesday', 'Eating', '08:00', 30),
    (22, '2026-06-03', 'Wednesday', 'Purring', '09:00', 15),
    (23, '2026-06-03', 'Wednesday', 'Drinking', '12:00', 55),
    (24, '2026-06-03', 'Wednesday', 'Sleeping', '13:00', 100),
    (25, '2026-06-03', 'Wednesday', 'Playing', '17:00', 150),
    (26, '2026-06-03', 'Wednesday', 'Eating', '18:00', 60),
    (27, '2026-06-03', 'Wednesday', 'Purring', '19:00', 60),
    (28, '2026-06-03', 'Wednesday', 'Drinking', '20:00', 30),
    (29, '2026-06-03', 'Wednesday', 'Sleeping', '21:00', 90),
    (30, '2026-06-04', 'Thursday', 'Eating', '08:00', 30),
    (31, '2026-06-04', 'Thursday', 'Purring', '09:00', 15),
    (32, '2026-06-04', 'Thursday', 'Drinking', '12:00', 55),
    (33, '2026-06-04', 'Thursday', 'Sleeping', '13:00', 100),
    (34, '2026-06-04', 'Thursday', 'Playing', '17:00', 150),
    (35, '2026-06-04', 'Thursday', 'Eating', '18:00', 60),
    (36, '2026-06-04', 'Thursday', 'Purring', '19:00', 60),
    (37, '2026-06-04', 'Thursday', 'Drinking', '20:00', 30),
    (38, '2026-06-04', 'Thursday', 'Sleeping', '21:00', 90),
    (39, '2026-06-05', 'Friday', 'Eating', '08:00', 30),
    (40, '2026-06-05', 'Friday', 'Purring', '09:00', 15),
    (41, '2026-06-05', 'Friday', 'Drinking', '12:00', 55),
    (42, '2026-06-05', 'Friday', 'Sleeping', '13:00', 100),
    (43, '2026-06-05', 'Friday', 'Playing', '17:00', 150),
    (44, '2026-06-05', 'Friday', 'Eating', '18:00', 60),
    (45, '2026-06-05', 'Friday', 'Purring', '19:00', 60),
    (46, '2026-06-05', 'Friday', 'Drinking', '20:00', 30),
    (47, '2026-06-05', 'Friday', 'Sleeping', '21:00', 90),
    (48, '2026-06-06', 'Saturday', 'Eating', '08:00', 30),
    (49, '2026-06-06', 'Saturday', 'Purring', '09:00', 15),
    (50, '2026-06-06', 'Saturday', 'Drinking', '12:00', 55),
    (51, '2026-06-06', 'Saturday', 'Sleeping', '13:00', 100),
    (52, '2026-06-06', 'Saturday', 'Playing', '17:00', 150),
    (53, '2026-06-06', 'Saturday', 'Eating', '18:00', 60),
    (54, '2026-06-06', 'Saturday', 'Purring', '19:00', 60),
    (55, '2026-06-06', 'Saturday', 'Drinking', '20:00', 30),
    (56, '2026-06-06', 'Saturday', 'Sleeping', '21:00', 90),
    (57, '2026-06-07', 'Sunday', 'Eating', '08:00', 30),
    (58, '2026-06-07', 'Sunday', 'Purring', '09:00', 15),
    (59, '2026-06-07', 'Sunday', 'Drinking', '12:00', 55),
    (60, '2026-06-07', 'Sunday', 'Sleeping', '13:00', 100),
    (61, '2026-06-07', 'Sunday', 'Playing', '17:00', 150),
    (62, '2026-06-07', 'Sunday', 'Eating', '18:00', 60),
    (63, '2026-06-07', 'Sunday', 'Purring', '19:00', 60),
    (64, '2026-06-07', 'Sunday', 'Drinking', '20:00', 30),
    (65, '2026-06-07', 'Sunday', 'Sleeping', '21:00', 90),
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
        "event_date",
        "event_weekday_name",
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

# Try making a slider to filter the chart by day name
day_filter = st.select_slider(
    "Filter by Day of the Week",
    options=df['event_weekday_name'].unique().tolist(),
    value=df[['event_weekday_name']].iloc[0, 0]
)

# Create a chart to show how the cat spent their day like a gant chart

st.bar_chart(
    df, 
    x='start_time', 
    y='activity', 
    use_container_width=True,
    x_label='Day',
    y_label='Activity',
    color='activity',
    stack=True
    )
# ============================================================================
# STEP 7: CREATE ANOTHER CHART - Activity Frequency
# ============================================================================
# This chart shows how many times each activity happened
st.subheader("Weekly Activity Frequency")
# Make a bar chart which shows the total duration of each activity per weekday
st.bar_chart(
    df,
    x='event_weekday_name',
    y='event_duration',
    x_label='Weekday',
    y_label='Total Duration (mins)',
    color='activity',
    sort='event_date',
    horizontal=True
)


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
