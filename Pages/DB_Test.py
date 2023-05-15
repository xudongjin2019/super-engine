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
def get_course(grade, course_name,version):
    c.execute(
        "SELECT * FROM course_table WHERE grade =? AND course_name =? AND version =?", (grade, course_name,version)
    )
    data = c.fetchall()
    return data

def view_exam_course():
    c.execute("SELECT grade,course_name,version FROM course_table")
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



def match():
    with st.form("course_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            course_grade = st.selectbox('Select grade?',('B4', 'B5', 'B6','B7'))

        with col2:
            course_name = st.selectbox('Select dept?',('流程开发', '计算机基础', 'How to debug','编程'))

        with col3:
            course_version = st.text_input('version','')


        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            result = get_course(course_grade,course_name,course_version)
            result_list = pd.DataFrame( result, columns=["grade", "course_name", "version"])
            st.write(result_list)

def get_examlist():
        course_result = view_exam_course()
        course_db = pd.DataFrame( course_result, columns=["grade", "course_name", "version"])
        st.dataframe(course_db, use_container_width=True)

        grade_list= sorted(set(course_db.iloc[:,0].to_list()),reverse=True)
        course_name_list= sorted(set(course_db.iloc[:,1].to_list()),reverse=True)
        course_version_list= sorted(set(course_db.iloc[:,2].to_list()),reverse=True)
        
        return grade_list,course_name_list,course_version_list




if __name__ == "__main__":
    main()