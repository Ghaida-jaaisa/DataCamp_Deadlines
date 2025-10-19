# 🚀 Interactive Course Schedule & Deadline Tracker 

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://aaupdatacampdeadlines.streamlit.app/)

A dynamic, real-time timeline built to keep students organized and on track. Powered by Google Sheets and visualized with Streamlit & Plotly.

![Dashboard Screenshot](Screenshot.png)

## ✨ Why this is awesome

Forget static PDFs. This dashboard offers a live view of the entire program schedule.

*   **📊 Interactive Gantt Chart**: Zoom, pan, and hover for details with custom track emojis.
*   **🔄 Real-Time Sync**: Update the Google Sheet, and the app updates instantly. No redeploying needed.
*   **📍 Smart "Today" Marker**: A vertical line automatically highlights the current date so students know exactly where they should be.
*   **🔗 One-Click Access**: The data table includes direct, clickable links to course materials.
*   **🎨 Professional UI**: Features institutional logos and dynamic track coloring.

## 🏃‍♂️ Quick Start (Run Locally)

Get it running on your machine in under a minute.

1.  **Clone & Enter:**
    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Launch:**
    ```bash
    streamlit run app.py
    ```

## 🔌 Connect Your Own Data

Want to use this for your own program? It's easy.

1.  **Create a Google Sheet** with these exact columns:
    `Course` | `Track` | `# hours` | `Course Link` | `Start time` | `End time`
2.  Make the sheet **Public (Viewer)** via the Share settings.
3.  Construct your CSV export URL (replace `SHEET_ID` and `GID`):
    `https://docs.google.com/spreadsheets/d/SHEET_ID/export?format=csv&gid=GID#gid=GID`
4.  Paste this URL into the `SHEET_URL` variable inside `app.py`.

## 🛠️ Tech Stack

Built with ❤️ using:
*   [Streamlit](https://streamlit.io/)
*   [Plotly Express](https://plotly.com/python/plotly-express/)
*   [Pandas](https://pandas.pydata.org/)
