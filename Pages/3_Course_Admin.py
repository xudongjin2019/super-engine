import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
from io import StringIO
import numpy as np
import datetime
import hashlib
import json
import sqlite3
from pathlib import Path
import pandas.io.sql as pd_sql
import sqlalchemy


def exam_welcome():
   st.write("# Welcome to Courses Manage Session 👋")
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
   
def Course_review():
    # list current course
    st.markdown(""" **👈 List current course**  """ )
   
def upload():
    uploaded_file = st.file_uploader("Choose a CSV or EXCEL file")
    if uploaded_file is not None:
        # Can be used wherever a "file-like" object is accepted:
      bytes_data = uploaded_file.read()
      st.write("filename:", uploaded_file.name)
      st.info('Showing course in current EXCEL file')
      courselist = pd.read_excel(uploaded_file)
      if courselist is not None:
        st.dataframe(courselist, use_container_width=True)
    
      st.write('Use current date and hour as version',datetime.datetime.now().strftime("%Y%m%d%H"))
      

      # datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# 保存上传内容，存到DB中
      cols1,cols2 = st.columns(2)
      with cols1:
        if st.button('Save current file to Database'):
         version = datetime.datetime.now().strftime("%Y%m%d%H") # 获取当前时间为Version

         with cols2:
            courselist.iloc[:,2]= version  # Version写入第二列
            # courselist.iloc[:,3]= version + 

            # 写入本地数据库
            for index,row in courselist.iterrows():
              row[3]= version + str(index+1)
              add_course(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9])
                
            
            st.success('Save to Database Success!', icon="✅")
        
        else: 
         with cols2:
            st.warning('If this is OK, please save the content.')

def showdb(): # 显示SQL数据库中存储的试题
    st.info('Showing course with updated version in local database ')
    if st.button('Show Database',key=st.info):
        course_result = view_all_course()
        course_db = pd.DataFrame( course_result, columns=["grade", "course_name", "version","NO","question","c1","c2","c3","c4","Answer"])
        st.dataframe(course_db, use_container_width=True)

    else: 
        def convert_df(df):  # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_csv().encode('utf-8')
  
        course_result = view_all_course()
        course_db = pd.DataFrame( course_result, columns=["grade", "course_name", "version","NO","question","c1","c2","c3","c4","Answer"])
        csv = convert_df(course_db)
        st.download_button(
            label="Download data as Excel",
            data=csv,
            file_name='large_df.xls',
            mime='text/xls',
        )


# DB Management

conn = sqlite3.connect("gte_course.db")
c = conn.cursor()


# DB Functions for create table
def create_course_table():
    c.execute(
        "CREATE TABLE IF NOT EXISTS course_table(grade TEXT, course_name TEXT, version TEXT,NO TEXT UNIQUE,question TEXT, c1 TEXT,c2 TEXT,c3 TEXT,c4 TEXT, answer TEXT)"
    )


# Insert or replace the data into table
def add_course(grade, course_name, version,NO,question, c1,c2,c3 ,c4 , answer):
    c.execute(
        "INSERT OR REPLACE INTO course_table(grade, course_name, version,NO,question, c1,c2,c3 ,c4 , answer) VALUES (?,?,?,?,?,?,?,?,?,?)",
        (grade, course_name, version,NO,question, c1,c2,c3 ,c4 , answer),
    )
    conn.commit()


# t_item  fetch
def login_user(email, password):
    c.execute(
        "SELECT * FROM userstable WHERE email =? AND password = ?", (email, password)
    )
    data = c.fetchall()
    return data



def view_all_course():
    c.execute("SELECT * FROM course_table")
    data = c.fetchall()
    return data

def get_test_item():
    # 获取DB中的考题名称，选项，和答案
    c.execute("SELECT t_itemquestion, t_item_c1, t_item_c2, t_item_c3, t_item_c4, t_itemanswer FROM t_itemtable")
    test_item = c.fetchall()
    return test_item


def main(): 
    exam_welcome()
    create_course_table()
    upload()
    st.divider()
    showdb()
 

if __name__ == "__main__":
    main()