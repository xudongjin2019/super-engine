import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import hashlib
import json
import sqlite3
from pathlib import Path

st.set_page_config(page_title = "GTE Certification System", page_icon = "⚙，", layout = "wide")

# DB Management

conn = sqlite3.connect("user_data.db")
c = conn.cursor()


def view_all_users():
    c.execute("SELECT * FROM userstable")
    data = c.fetchall()
    return data

def main():
    st.subheader("User Profiles")
    user_result = view_all_users()
    clean_db = pd.DataFrame(
                        user_result, columns=["Username", "Email", "Password"]
                    )
    st.dataframe(clean_db)

    alluser_db = pd.DataFrame(user_result)
    st.dataframe(alluser_db)


if __name__ == "__main__":
    main()