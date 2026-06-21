from collections import defaultdict
from pathlib import Path
import sqlite3

import streamlit as st
import altair as alt
import pandas as pd


# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title="Testing",
    page_icon=":shopping_bags:",  # This is an emoji shortcode. Could be a URL too.
)


# -----------------------------------------------------------------------------
# Declare some useful functions.


def connect_db():
    """Connects to the sqlite database."""

    DB_FILENAME = Path(__file__).parent / "inventory.db"
    db_already_exists = DB_FILENAME.exists()

    conn = sqlite3.connect(DB_FILENAME)
    db_was_just_created = not db_already_exists

    return conn, db_was_just_created


def initialize_data(conn):
    """Initializes the inventory table with some data."""
    
    cursor = conn.cursor()
    
    cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS inventory (
                    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    activity TEXT
                    start_time TEXT,
                    event_duration INTEGER,
                    activity_date INTEGER,
                    """
    )

    cursor.execute(
        """
        INSERT INTO inventory
            (activity, start_time, event_duration, activity_date)
        VALUES
            -- Beverages
            ('Bottled Water (500ml)', 1.50, 115, 15),
            ('Soda (355ml)', 2.00, 93, 8),
            ('Energy Drink (250ml)', 2.50, 12, 18),
            ('Coffee (hot, large)', 2.75, 11, 14),
            ('Juice (200ml)', 2.25, 11, 9),

            -- Snacks
            ('Potato Chips (small)', 2.00, 34, 16),
            ('Candy Bar', 1.50, 6, 19),
            ('Granola Bar', 2.25, 3, 12),
            ('Cookies (pack of 6)', 2.50, 8, 8),
            ('Fruit Snack Pack', 1.75, 5, 10),

            -- Personal Care
            ('Toothpaste', 3.50, 1, 9),
            ('Hand Sanitizer (small)', 2.00, 2, 13),
            ('Pain Relievers (pack)', 5.00, 1, 5),
            ('Bandages (box)', 3.00, 0, 10),
            ('Sunscreen (small)', 5.50, 6, 5),

            -- Household
            ('Batteries (AA, pack of 4)', 4.00, 1, 5),
            ('Light Bulbs (LED, 2-pack)', 6.00, 3, 3),
            ('Trash Bags (small, 10-pack)', 3.00, 5, 10),
            ('Paper Towels (single roll)', 2.50, 3, 8),
            ('Multi-Surface Cleaner', 4.50, 2, 5),

            -- Others
            ('Lottery Tickets', 2.00, 17, 20),
            ('Newspaper', 1.50, 22, 20)
        """
    )
    conn.commit()


def load_data(conn):
    """Loads the inventory data from the database."""
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM inventory")
        data = cursor.fetchall()
    except:
        return None

    df = pd.DataFrame(
        data,
        columns=[
            "event_id",
            "activity"
            "start_time",
            "duration",
            "activity_date"
        ],
    )

    return df


def update_data(conn, df, changes):
    """Updates the inventory data in the database."""
    cursor = conn.cursor()

    if changes["edited_rows"]:
        deltas = st.session_state.inventory_table["edited_rows"]
        rows = []

        for i, delta in deltas.items():
            row_dict = df.iloc[i].to_dict()
            row_dict.update(delta)
            rows.append(row_dict)

        cursor.executemany(
            """
            UPDATE inventory
            SET
                activity = :activity,
                start_time = :start_time,
                event_duration = :event_duration,
                activity_date = :activity_date,
            WHERE event_id = :event_id
            """,
            rows,
        )

    if changes["added_rows"]:
        cursor.executemany(
            """
            INSERT INTO inventory
                (event_id, activity, start_time, event_duration, activity_date)
            VALUES
                (:event_id, :activity, :start_time, :event_duration, :activity_date)
            """,
            (defaultdict(lambda: None, row) for row in changes["added_rows"]),
        )

    if changes["deleted_rows"]:
        cursor.executemany(
            "DELETE FROM inventory WHERE event_id = :event_id",
            ({"event_id": int(df.loc[i, "event_id"])} for i in changes["deleted_rows"]),
        )

    conn.commit()


# -----------------------------------------------------------------------------
# Draw the actual page, starting with the inventory table.

# Set the title that appears at the top of the page.
"""
# :shopping_bags: Test title

**Welcome to Rupert's activity tracker!**
This page reads and writes directly from/to our inventory database.
"""

st.info(
    """
    Use the table below to add, remove, and edit items.
    And don't forget to commit your changes when you're done.
    """
)

# Connect to database and create table if needed
conn, db_was_just_created = connect_db()

# Initialize data.
if db_was_just_created:
    initialize_data(conn)
    st.toast("Database initialized with some sample data.")

# Load data from database
df = load_data(conn)

# Display data with editable table
edited_df = st.data_editor(
    df,
    disabled=["event_id"],  # Don't allow editing the 'id' column.
    num_rows="dynamic",  # Allow appending/deleting rows.
    column_config={
        # Show dollar sign before price columns.
        "event_duration": st.column_config.NumberColumn(format="$%.2f"),
    },
    key="inventory_table",
)

has_uncommitted_changes = any(len(v) for v in st.session_state.inventory_table.values())

st.button(
    "Commit changes",
    type="primary",
    disabled=not has_uncommitted_changes,
    # Update data in database
    on_click=update_data,
    args=(conn, df, st.session_state.inventory_table),
)


# -----------------------------------------------------------------------------
# Now some cool charts

# Add some space
""
""
""

st.subheader("Units left", divider="red")

need_to_reorder = df[df["units_left"] < df["reorder_point"]].loc[:, "start_time"]

if len(need_to_reorder) > 0:
    items = "\n".join(f"* {name}" for name in need_to_reorder)

    st.error(f"We're running dangerously low on the items below:\n {items}")

""
""

st.altair_chart(
    # Layer 1: Bar chart.
    alt.Chart(df)
    .mark_bar(
        orient="horizontal",
    )
    .encode(
        x="units_left",
        y="start_time",
    )
    # Layer 2: Chart showing the reorder point.
    + alt.Chart(df)
    .mark_point(
        shape="diamond",
        filled=True,
        size=50,
        color="salmon",
        opacity=1,
    )
    .encode(
        x="reorder_point",
        y="start_time",
    ),
    use_container_width=True,
)

st.caption("NOTE: The :diamonds: location shows the reorder point.")

""
""
""

# -----------------------------------------------------------------------------

st.subheader("Best sellers", divider="orange")

""
""

st.altair_chart(
    alt.Chart(df)
    .mark_bar(orient="horizontal")
    .encode(
        x="activity",
        y=alt.Y("start_time").sort("-x"),
    ),
    use_container_width=True,
)
