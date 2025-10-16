import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from PIL import Image
import base64
from io import BytesIO

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Course Timeline",
    page_icon="🗓️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --- HELPER FUNCTION TO MANAGE IMAGES ---
def image_to_base64(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


# --- HEADER WITH LOGOS ---
st.markdown("""
<style>
.logo-container {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 1rem;
    gap: 2rem; 
}
.logo-img {
    max-height: 60px; 
    padding: 8px; 
    background-color: #FFFFFF; 
    border-radius: 10px; 
    box-shadow: 0 4px 8px rgba(0,0,0,0.1); 
}
</style>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.image("bzu.png", use_column_width=True)
with col2:
    st.image("gsg.png", use_column_width=True)
with col3:
    st.image("gdg.png", use_column_width=True)
with col4:
    st.image("dc.png", use_column_width=True)

st.title("🗓️ Datcamp Course Timeline")
st.markdown("### A visual guide to our program schedule and deadlines.")

# --- DATA LOADING AND PREPARATION ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1DLS_qkd22eoASDaQTDke2q5K4Jhp4ZTxllr_icbj_Hg/export?format=csv&gid=531384324#gid=531384324"

@st.cache_data
def load_data(url):
    """Load and preprocess data from Google Sheets."""
    df = pd.read_csv(url)
    # Sanitize column names
    df.columns = df.columns.str.strip().str.lower().str.replace('#', 'num', regex=False).str.replace(' ', '_',regex=False)
    # Convert dates
    df["start_time"] = pd.to_datetime(df["start_time"], dayfirst=True)
    df["end_time"] = pd.to_datetime(df["end_time"], dayfirst=True)
    return df


# --- EMOJI AND COLOR MAPPING ---
TRACK_EMOJIS = {
    "Data Theory": "🧠",
    "Google Sheets": "📊",
    "Python": "🐍",
    "Shell": "💻",
    "Git/Github": "🐙",
    "SQL": "🔍",
    "Docker": "🐳",
    "Certificates": "🏆"
}

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

try:
    df = load_data(SHEET_URL)
    df['emoji'] = df['track'].map(TRACK_EMOJIS).fillna("🔹")
    df['hover_text'] = df['emoji'] + " " + df['track']

    # --- DEBUGGING OUTPUT AS YOU SUGGESTED ---
    st.subheader("🕵️ Debugging Information")
    program_start_date = df['start_time'].min()
    program_end_date = df['end_time'].max()
    # Create a timezone-NAIVE timestamp for today for a fair comparison
    today_naive = pd.Timestamp.now().tz_localize(None)
    tsvalue = pd.Timestamp.now().value

    st.write(f"**Program Start Date:** `{program_start_date}`")
    st.write(f"**Program End Date:** `{program_end_date}`")
    st.write(f"**'Today' (Timezone-Naive):** `{today_naive}`")
    st.write(f"**'Today' Timestamp Value:** `{tsvalue}`")
    is_within_range = program_start_date <= today_naive <= program_end_date
    st.write(f"**Is 'Today' within the program's date range?** `{is_within_range}`")
    st.write("---")


    # --- SIDEBAR FILTERS ---
    st.sidebar.header("Filter Options")
    all_tracks = sorted(df["track"].unique().tolist())
    selected_tracks = st.sidebar.multiselect(
        "Select Tracks to Display:",
        options=all_tracks,
        default=all_tracks
    )

    if not selected_tracks:
        st.warning("Please select at least one track from the sidebar to display the timeline.")
    else:
        filtered_df = df[df["track"].isin(selected_tracks)].copy()

        # --- GANTT CHART VISUALIZATION ---
        st.header("Course Schedule Gantt Chart")

        fig = px.timeline(
            filtered_df,
            x_start="start_time",
            x_end="end_time",
            y="course",
            color="track",
            color_discrete_map=TRACK_COLORS,
            hover_name="course",
            hover_data={
                'track': False,
                'hover_text': True,
                'start_time': '|%B %d, %Y',
                'end_time': '|%B %d, %Y'
            },
            labels={"hover_text": "Track"}
        )

        # We draw a line shape from the bottom to the top of the chart at today's date
        fig.add_shape(
            type="line",
            x0=today_naive, x1=today_naive,  # The x-coordinates are today's date
            y0=0, y1=1,  # The y-coordinates span the entire plot height
            yref="paper",  # Use 'paper' coordinates for y-axis
            line=dict(color="Red", width=2, dash="dash")
        )
        # We add a separate annotation for the label
        fig.add_annotation(
            x=today_naive,
            y=1.05,  # Position it slightly above the top
            yref="paper",
            text="Today",
            showarrow=False,
            font=dict(color="Red", size=14)
        )

        fig.update_yaxes(autorange="reversed")
        fig.update_layout(
            title_font_size=24,
            font_size=16,
            xaxis_title=None,
            yaxis_title=None,
            legend_title="Course Tracks"
        )
        st.plotly_chart(fig, use_container_width=True)

        # --- DATA TABLE DISPLAY ---
        st.header("Course Details & Links")
        st.dataframe(
            filtered_df,
            column_config={
                "course": st.column_config.TextColumn("Course Title", width="large"),
                "track": "Track",
                "num_hours": "Hours",
                "start_time": st.column_config.DateColumn("Start Date", format="YYYY-MM-DD"),
                "end_time": st.column_config.DateColumn("End Date", format="YYYY-MM-DD"),
                "link_to_course": st.column_config.LinkColumn("Course Link", display_text="🔗 Go to Course"),
                "num_days": None,
            },
            hide_index=True,
            use_container_width=True
        )

except Exception as e:
    st.error(f"⚠️ An error occurred: {e}")
    st.info("Please check with the moderators.")