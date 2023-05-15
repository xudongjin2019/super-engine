import hashlib
import json
import sqlite3
from pathlib import Path
import datetime
import pandas as pd
import streamlit as st
import streamlit_authenticator as stauth
import extra_streamlit_components as stx

st.set_page_config(page_title = "GTE Certification System", page_icon = "random", layout = "wide")

# DB Management

conn = sqlite3.connect("gte_course.db")
c = conn.cursor()

def create_usertable():  
    c.execute(
        "CREATE TABLE IF NOT EXISTS userstable(name TEXT,username TEXT UNIQUE,email TEX UNIQUE,password TEXT,usergroup TEXT)"
    )

def add_userdata(name,username,email,password,usergroup):
    c.execute(
        "INSERT OR REPLACE INTO userstable(name,username,email,password,usergroup) VALUES (?,?,?,?,?)",
        (name,username,email,password,usergroup),
    )
    conn.commit()

def login_user(email, password):
    c.execute(
        "SELECT * FROM userstable WHERE email =? AND password = ?", (email, password)
    )
    data = c.fetchall()
    return data

def view_all_users():
    c.execute("SELECT * FROM userstable")
    data = c.fetchall()
    return data



def main(): 

    welcome()

  
def welcome():
   st.write("# Welcome to GTE Certification System! 👋")
   st.markdown(
        """
        GTE Certification System is a web app built with Streamlit specifically for Course Exam and Certification. 
        GTE Solution team reserve all the rights.
        - **👈 Select the page from the sidebar to go directly for course manage,take exam or get certification!**
        - **👈 Course admin is only for authorized user to upload and update courses.**
        - **👈 Suggest to take exam after trainning session hold by GTE team**
        - **👈 You can get certification paper in case you pass the exam!**
        - **👈 If you have any question or trouble,please contact with GTE solution team.**

    """
    )
   


if __name__ == "__main__":
    main()