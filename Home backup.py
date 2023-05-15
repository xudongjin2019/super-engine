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
        "CREATE TABLE IF NOT EXISTS userstable(name TEXT,username TEXT,email TEX, password TEXT)"
    )


# Insert the data into table
def add_userdata(name,username, email, password):
    c.execute(
        "INSERT INTO userstable(name,username,email,password) VALUES (?,?,?,?)",
        (name,username, email, password),
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


if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False


# Main function
# def main():   # 先不用这部分
    # """Login page"""
    st.title("欢迎! ")
    menu = ["Login", "SignUp"]
    choice = st.selectbox(
        "从下拉菜单中选择注册或登陆Select Login or SignUp from dropdown box ▾",
        menu,
    )
    st.markdown(
        "<h10 style='text-align: left; color: #ffffff;'> If you do not have an account, create an accouunt by select SignUp option from above dropdown box.</h10>",
        unsafe_allow_html=True,
    )
    if choice == "":
        st.subheader("Login")
    elif choice == "Login":
        st.write("-------")
        st.subheader("Log in to the App")

        email = st.text_input("User Name", placeholder="email")

        password = st.text_input("Password", type="password")

        if st.button("Login"):
            # if password == '12345':
            # Hash password creation and store in a table
            create_usertable()
            hashed_pswd = make_hashes(password)

            result = login_user(email, check_hashes(password, hashed_pswd))
            if result:
                st.session_state["logged_in"] = True
                st.success("Logged In as {}".format(email))

                with open("loginfo.log", "a") as f:  
                    f.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + email + " logged in\n")
                    f.close()
                with open("userinfo.log", "w") as f:  
                    f.write(email)
                    f.close()

                

                if st.success:
                    st.subheader("User Profiles")
                    user_result = view_all_users()
                    clean_db = pd.DataFrame(
                        user_result, columns=["Username", "Email", "Password"]
                    )
                    st.dataframe(clean_db)
            else:
                st.warning("Incorrect Username/Password")
                
    elif choice == "SignUp":
        st.write("-----")
        st.subheader("Create New Account for first time user")
        new_user = st.text_input("Username", placeholder="name")
        new_user_email = st.text_input("Email id", placeholder="email")
        new_password = st.text_input("Password", type="password")

        if st.button("Signup"):
            if new_user == "":  # if user name empty then show the warnings
                st.warning("Inavlid user name")
            elif new_user_email == "":  # if email empty then show the warnings
                st.warning("Invalid email id")
            elif new_password == "":  # if password empty then show the warnings
                st.warning("Invalid password")
            else:
                create_usertable()
                add_userdata(new_user, new_user_email, make_hashes(new_password))
                st.success("You have successfully created a valid Account")
                st.info("Go up and Login to you account")



# 如下代码数据，可以来自数据库
names = ['Jeremy', 'GTE管理员']
usernames = ['jeremy', 'gteadmin']
passwords = ['1210', 'ad123']

hashed_passwords = stauth.Hasher(passwords).generate()

authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
    'some_cookie_name', 'some_signature_key', cookie_expiry_days=30)

name, authentication_status, username = authenticator.login('Login', 'main')

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
          create_usertable()
          add_userdata(new_usernick,new_user, new_user_email, make_hashes(new_password))
          st.success("You have successfully created a valid Account")
          st.info("Go up and Login to you account")

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