import hashlib
import json
import sqlite3
from pathlib import Path
import datetime
import pandas as pd
import streamlit as st
import streamlit_authenticator as stauth
import extra_streamlit_components as stx
import yaml
from yaml.loader import SafeLoader


st.set_page_config(page_title = "GTE Certification System", page_icon = "random", layout = "wide")


# Convert Pass into hash format
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# Check password matches during login
def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False

# DB Management

conn = sqlite3.connect("userinfo_data.db")
c = conn.cursor()


# DB Functions for create table
def create_usertable():
    c.execute(
        "CREATE TABLE IF NOT EXISTS userstable(name TEXT,username TEXT UNIQUE,email TEX UNIQUE,password TEXT,usergroup TEXT)"
    )


# Insert the data into table
def add_userdata(name,username,email,password,usergroup):
    c.execute(
        "INSERT OR REPLACE INTO userstable(name,username,email,password,usergroup) VALUES (?,?,?,?,?)",
        (name,username,email,password,usergroup),
    )
    conn.commit()


# Password and email fetch
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



authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

name, authentication_status, username = authenticator.login('Login', 'main')

# 如下的先不用
def new_auth():
        if authentication_status:
            authenticator.logout('Logout', 'main', key='unique_key')
            st.write(f'Welcome *{name}*')
            st.title('Some content')
        elif authentication_status is False:
            st.error('Username/password is incorrect')
        elif authentication_status is None:
            st.warning('Please enter your username and password')


        if st.session_state["authentication_status"]:
            authenticator.logout('Logout', 'main', key='unique_key')
            st.write(f'Welcome *{st.session_state["name"]}*')
            st.title('Some content')
        elif st.session_state["authentication_status"] is False:
            st.error('Username/password is incorrect')
        elif st.session_state["authentication_status"] is None:
            st.warning('Please enter your username and password')

        if authentication_status:
            try:
                if authenticator.reset_password(username, 'Reset password'):
                    st.success('Password modified successfully')
            except Exception as e:
                st.error(e)

        #  Register 
        try:
            if authenticator.register_user('Register user', preauthorization=False):
                st.success('User registered successfully')
        except Exception as e:
            st.error(e)


        try:
            username_forgot_pw, email_forgot_password, random_password = authenticator.forgot_password('Forgot password')
            if username_forgot_pw:
                st.success('New password sent securely')
                # Random password to be transferred to user securely
            else:
                st.error('Username not found')
        except Exception as e:
            st.error(e)


        try:
            username_forgot_username, email_forgot_username = authenticator.forgot_username('Forgot username')
            if username_forgot_username:
                st.success('Username sent securely')
                # Username to be transferred to user securely
            else:
                st.error('Email not found')
        except Exception as e:
            st.error(e)

        if authentication_status:
            try:
                if authenticator.update_user_details(username, 'Update user details'):
                    st.success('Entries updated successfully')
            except Exception as e:
                st.error(e)



def main(): 
  if authentication_status:
    with st.container():
        cols1,cols2,cols3,cols4,cols5 = st.columns(5)
        cols1.write('Current login user is *%s*' % (name))

        with cols5.container():
            authenticator.logout('Logout', 'main')
    welcome()
 
    
  elif authentication_status == False:
    st.error('Username/password is incorrect')
  elif authentication_status == None:
    st.warning('Please enter your username and password')
    st.write("-----")
    st.subheader("Signup to create new account for first time user")
    new_usernick = st.text_input("Nickname", placeholder="Nickname")
    new_user = st.text_input("Username to login", placeholder="name")
    new_user_email = st.text_input("Email Id", placeholder="email")
    new_password = st.text_input("Password", type="password")

    if st.button("Signup"):
      if new_usernick == "":  # if user name empty then show the warnings
          st.warning("Inavlid user name")
      elif new_user == "":  # if user name empty then show the warnings
          st.warning("Inavlid user name")
      elif new_user_email == "":  # if email empty then show the warnings
          st.warning("Invalid email id")
      elif new_password == "":  # if password empty then show the warnings
          st.warning("Invalid password")
      else:
          usergroup = "default user"
          create_usertable()
          add_userdata(new_usernick,new_user, new_user_email, make_hashes(new_password),usergroup)
          st.success("You have successfully created a valid Account")
          st.info("Go up and Login to you account")
          st.subheader("User Profiles")
          user_result = view_all_users()
          clean_db = pd.DataFrame(user_result, columns=["Nickname","Username", "Email", "Password","Usergroup"])
          st.dataframe(clean_db,use_container_width=True)



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

