import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import hashlib
import json
import sqlite3
from pathlib import Path

st.set_page_config(page_title = "Dashboard", page_icon = "⚙，", layout = "wide")

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

def main():
    st.header("GTE - 试题生成和查询")
    create_t_itemtable()

    tab1, tab2 = st.tabs(["当前试题", "增加新试题"])

    # Tab1 显示当前考题

    with tab1:
     user_result = view_all_t_item()
     clean_db = pd.DataFrame(
                        user_result, columns=["题型", "问题", "选项A","选项B","选项C","选项D","答案"]
                    )
     st.dataframe(clean_db,use_container_width=True)

    # Tab2 增加新考题

    with tab2:
     with st.form("my_form"):
      option = st.selectbox( '请选择题型?',('单选', '判断', '多选','问答'))
      question = st.text_input('请描述题干', '')
      col1, col2 = st.columns(2)
      with col1:
         choice_a = st.text_input('请描述选项A', '')
      with col2:
         choice_b = st.text_input('请描述选项B', '')
      col3, col4 = st.columns(2)
      with col3:
         choice_c = st.text_input('请描述选项C', '')
      with col4:
         choice_d = st.text_input('请描述选项D', '')
      if option == "单选":
        answer = st.radio( "请给出答案",('A', 'B', 'C','D'), horizontal=True )
      elif option == "判断":
        answer = st.radio( "请给出答案",('T-正确', 'F-错误'), horizontal=True )
      else:
        answer = st.text_input('Please describe the answer', 'name')

   # Every form must have a submit button.
      submitted = st.form_submit_button("试题提交")
      if submitted:  
       add_t_itemdata(option,question,choice_a,choice_b,choice_c,choice_d,answer)
       st.success("提交成功")
     
def getuser():
  with open("userinfo.log", "a") as f:  
    login_user = f.read()
    return login_user



if __name__ == "__main__":
    main()