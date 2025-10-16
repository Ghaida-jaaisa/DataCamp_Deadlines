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
def image_to_base64(path):
    """Converts a local image file to a Base64 string for embedding in HTML."""
    try:
        img = Image.open(path)
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        return f"data:image/png;base64,{base64.b64encode(buffered.getvalue()).decode()}"
    except FileNotFoundError:
        return None

# --- HEADER WITH EMBEDDED LOGOS ---
try:
    # Convert all logos to Base64
    bzu_logo_b64 = image_to_base64("bzu.png")
    gsg_logo_b64 = image_to_base64("gsg.png")
    gdg_logo_b64 = image_to_base64("gdg.png")
    dc_logo_b64 = image_to_base64("dc.png")

    # Define the HTML and CSS for the logo bar
    logo_html = f"""
    <style>
        .logo-container {{
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 1rem 0;
            gap: 2rem; 
            flex-wrap: wrap; 
        }}
        .logo-img {{
            max-height: 55px; 
            padding: 8px;
            background-color: #FFFFFF; 
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
    </style>
    <div class="logo-container">
        <img src="{bzu_logo_b64}" class="logo-img">
        <img src="{gsg_logo_b64}" class="logo-img">
        <img src="{gdg_logo_b64}" class="logo-img">
        <img src="{dc_logo_b64}" class="logo-img">
    </div>
    """
    st.markdown(logo_html, unsafe_allow_html=True)

except Exception as e:
    st.error(f"An error occurred while loading the logos: {e}")

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

        today = pd.Timestamp.now().tz_localize(None)
        fig.add_shape(
            type="line",
            x0=today, x1=today,
            y0=0, y1=1,
            yref="paper",
            line=dict(color="Red", width=2, dash="dash")
        )

        fig.add_annotation(
            x=today,
            y=1.08,
            yref="paper",
            text="Today",
            showarrow=False,
            font=dict(color="white", size=14)
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
                "course_link": st.column_config.LinkColumn("Course Link", display_text="🔗 Go to Course"),
                "num_days": None,
                "emoji": None,
                "hover_text": None
            },
            hide_index=True,
            use_container_width=True
        )

except Exception as e:
    st.error(f"⚠️ An error occurred: {e}")
    st.info("Please check with the moderators.")