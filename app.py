import streamlit as st
import pandas as pd
import plotly.express as px

# Set the page to a wide layout for a better timeline view
st.set_page_config(layout="wide")

st.title("Interactive Course Timeline")
st.markdown("This timeline visualizes our course schedule. Use the sidebar to filter by track.")

# --- GOOGLE SHEETS CONNECTION ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1DLS_qkd22eoASDaQTDke2q5K4Jhp4ZTxllr_icbj_Hg/export?format=csv&gid=531384324#gid=531384324"

# --- COLOR MAPPING ---
TRACK_COLORS = {
    "Data Theory": "#ea4335",
    "Google Sheets": "#34a853",
    "Python": "#4285f4",
    "Shell": "#fbbc04",
    "Git/Github": "#9e9e9e",
    "SQL": "#ff6d00",
    "Docker": "#00acc1",
    "Certificates": "#8fbc8f"
}


@st.cache_data
def load_data(url):
    """Loads data from Google Sheet and preprocesses it."""
    df = pd.read_csv(url)
    # Sanitize column names to prevent issues with spaces or special characters
    df.columns = df.columns.str.strip().str.lower().str.replace('#', 'num', regex=False).str.replace(' ', '_',
                                                                                                     regex=False)
    # Convert date columns to datetime objects, crucial for Plotly
    df["start_time"] = pd.to_datetime(df["start_time"], dayfirst=True)
    df["end_time"] = pd.to_datetime(df["end_time"], dayfirst=True)
    return df


try:
    df = load_data(SHEET_URL)

    # --- Sidebar Filters ---
    st.sidebar.header("Filter Options")
    all_tracks = sorted(df["track"].unique().tolist())

    selected_tracks = st.sidebar.multiselect(
        "Select Tracks to Display:",
        options=all_tracks,
        default=all_tracks  # By default, show all tracks
    )

    if not selected_tracks:
        st.warning("Please select at least one track from the sidebar.")
    else:
        filtered_df = df[df["track"].isin(selected_tracks)].copy()

        # --- Gantt Chart Visualization ---
        st.header("Course Schedule Gantt Chart")

        # Create the Gantt chart
        fig = px.timeline(
            filtered_df,
            x_start="start_time",
            x_end="end_time",
            y="course",
            color="track",
            color_discrete_map=TRACK_COLORS,
            hover_name="course",
            title="Course Progress and Deadlines"
        )

        # Improve the chart's layout for better readability
        fig.update_yaxes(autorange="reversed")
        fig.update_layout(
            title_font_size=24,
            font_size=16,
            xaxis_title="Date",
            yaxis_title="Course",
            legend_title="Track"
        )

        st.plotly_chart(fig, use_container_width=True)

        # --- Display Data Table ---
        st.header("Course Data")
        st.dataframe(filtered_df)

except Exception as e:
    st.error(f"Failed to load or process data: {e}")
    st.info("Please ensure your Google Sheet URL is correct and public.")