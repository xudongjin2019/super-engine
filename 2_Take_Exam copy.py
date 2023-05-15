import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import hashlib
import json
import sqlite3
from pathlib import Path

st.set_page_config(page_title = "GTE Certification System", page_icon = "random", layout = "wide")

st.write()

st.header('GTE - 能力测评')

# DB Management

conn = sqlite3.connect("test.db")
c = conn.cursor()


# DB Functions for create table
def create_t_itemtable():
    c.execute(
        "CREATE TABLE IF NOT EXISTS t_itemtable(t_itemcat TEXT,t_itemquestion TEXT, t_item_c1 TEXT,t_item_c2 TEXT,t_item_c3 TEXT,t_item_c4 TEXT, t_itemanswer TEXT)"
    )


# Insert the data into table
def add_t_itemdata(t_itemcat, t_itemquestion, t_item_c1,t_item_c2,t_item_c3,t_item_c4,t_itemanswer):
    c.execute(
        "INSERT INTO t_itemtable(t_itemcat, t_itemquestion, t_item_c1, t_item_c2, t_item_c3, t_item_c4, t_itemanswer) VALUES (?,?,?,?,?,?,?)",
        (t_itemcat, t_itemquestion, t_item_c1,t_item_c2,t_item_c3,t_item_c4,t_itemanswer),
    )
    conn.commit()


# t_item  fetch
def login_user(email, password):
    c.execute(
        "SELECT * FROM userstable WHERE email =? AND password = ?", (email, password)
    )
    data = c.fetchall()
    return data



def view_all_t_item():
    c.execute("SELECT * FROM t_itemtable")
    data = c.fetchall()
    return data

def get_test_item():
    # 获取DB中的考题名称，选项，和答案
    c.execute("SELECT t_itemquestion, t_item_c1, t_item_c2, t_item_c3, t_item_c4, t_itemanswer FROM t_itemtable")
    test_item = c.fetchall()
    return test_item


def main():
    # placeholder = st.empty()
    # with placeholder.container():
        user_result = view_all_t_item()
        df = pd.DataFrame(user_result, columns=["题型", "问题", "选项A","选项B","选项C","选项D","答案"])
        # st.dataframe(df,use_container_width=True)
        # st.write(df)
        with st.form("test_form"):
         for index, row in df.iterrows():
            testitemindex = index +1
            st.write("第",testitemindex,"题   ",row["题型"],row["问题"]) # 输出考试题

            col1, col2 = st.columns(2)
            with col1:
                choice_a = st.write(row["选项A"]) 
            with col2:
                choice_b = st.write(row["选项B"]) 
            col3, col4 = st.columns(2)
            with col3:
                choice_c = st.write(row["选项C"]) # 输出考试题
            with col4:
                choice_d = st.write(row["选项D"]) # 输出考试题
            answer = st.radio( "请给出答案",('A', 'B', 'C','D'), key=index,horizontal=True )

         submitted = st.form_submit_button("试题提交")
         if submitted:  
            # add_t_itemdata(option,question,choice_a,choice_b,choice_c,choice_d,answer)
           st.success("提交成功")
    # placeholder.empty()


if __name__ == "__main__":
    main()