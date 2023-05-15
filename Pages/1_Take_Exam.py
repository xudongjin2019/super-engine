import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import hashlib
import json
import sqlite3
from pathlib import Path
import time
import datetime

st.set_page_config(page_title = "GTE Certification System", page_icon = ":writing_hand:", layout = "wide")

st.write()

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


# t_item  fetch  试题查询
def search_exam(grade,course_name, version):
    c.execute(
        "SELECT * FROM course_table WHERE grade =? AND course_name =? AND version =?", (grade,course_name,version)
    )
    exam_data = c.fetchall()
    return exam_data



def view_all_course():
    c.execute("SELECT * FROM course_table")
    data = c.fetchall()
    return data

def get_test_item():
    # 获取DB中的考题名称，选项，和答案
    c.execute("SELECT t_itemquestion, t_item_c1, t_item_c2, t_item_c3, t_item_c4, t_itemanswer FROM t_itemtable")
    test_item = c.fetchall()
    return test_item

def view_exam_course():
    c.execute("SELECT grade,course_name,version FROM course_table")
    data = c.fetchall()
    return data

def view_grade_course(grade):
    c.execute("SELECT course_name,version FROM course_table WHERE grade = ?",grade)
    data = c.fetchall()
    return data

def get_examlist():
        course_result = view_exam_course()
        course_db = pd.DataFrame( course_result, columns=["grade", "course_name", "version"])
        # st.dataframe(course_db, use_container_width=True)

        grade_list= sorted(set(course_db.iloc[:,0].to_list()),reverse=False)
        course_name_list= sorted(set(course_db.iloc[:,1].to_list()),reverse=True)
        course_version_list= sorted(set(course_db.iloc[:,2].to_list()),reverse=True)
        
        return grade_list,course_name_list,course_version_list

# DB Functions for create table
def create_score_table():
    c.execute(
        "CREATE TABLE IF NOT EXISTS score_table(grade TEXT, course_name TEXT, version TEXT,user_name TEXT,user_mail TEXT, user_dept TEXT, user_score TEXT, score_time TEXT )"
    )


# Insert or replace the data into table
def add_score(grade, course_name, version,user_name,user_mail, user_dept,user_score,score_time):
    c.execute(
        "INSERT OR REPLACE INTO score_table(grade, course_name, version,user_name,user_mail, user_dept,user_score,score_time) VALUES (?,?,?,?,?,?,?,?)",
        (grade, course_name, version,user_name,user_mail, user_dept,user_score,score_time),
    )
    conn.commit()

def view_all_score():
    c.execute("SELECT * FROM score_table")
    data = c.fetchall()
    return data


def main(): 
    st.write("# Welcome to GTE Certification System! 👋")
    st.divider()
    # 获取课程列表
    course_grade,course_name,course_version = get_examlist()
    # grade 和 course 要联动


    if 'search_result' not in st.session_state:
        st.session_state.search_result = False

    if 'exam_finish' not in st.session_state:
        st.session_state.exam_finish = False

    if 'exam_start' not in st.session_state:
        st.session_state.exam_start = False


    
  
    with st.form("user_form"):
        st.markdown("**:red[Please input user information and select course to start test]**")
        col1, col2, col3 = st.columns(3)
        with col1:
            user_name = st.text_input('Name', '')
            exam_grade = st.selectbox('Select grade?',course_grade)

        with col2:
            user_mail = st.text_input('E-mail', 'xxx@lenovo.com')
            exam_name = st.selectbox('Select course name?',course_name)

        with col3:
            user_dept = st.selectbox('Select dept?',('GE-GTE', 'LSSC-NB-ENG', 'LSSC-DT-ENG','LSSC-SVR-ENG','TJSC-NB-ENG'))
            exam_version = st.selectbox('Select course version?',course_version)
        


    # Every form must have a submit button.
        submitted = st.form_submit_button("Couse search")
        if submitted:
            if user_name == "":  # if user name empty then show the warnings
                st.warning("Inavlid user name")
            elif user_mail == "":  # if user name empty then show the warnings
                st.warning("Inavlid user mail")
            elif exam_name == "":  # if email empty then show the warnings
                st.warning("Invalid couse")
            else:
                st.success("course search success ")
                st.session_state.search_result = True
                st.session_state.exam_start = False
                st.session_state.exam_finish = False

    placeholder = st.empty()
    with placeholder.container():

        if st.session_state.search_result == True and st.session_state.exam_finish == False :
            with st.form('user_exam_form'):
                st.markdown("**:red[Please confirm the information to start test]**")
                st.write('Hello, ',user_name,'from',user_dept, 'with e-mail',user_mail,' ',':sunglasses:')
                st.write('You choose','Grade  ',exam_grade, 'Name ',exam_name, 'verison',exam_version,'for exam! :ledger:')
                st.write('Press following button to proceed. Good Luck to get 	:100: ')


            #  st.markdown("**:blue[Show exam table]**")
            #  exam_list = search_exam(exam_grade,exam_name,exam_version)
            #  show_exam_list = pd.DataFrame( exam_list, columns=["grade", "course_name", "version",'NO','question','c1','c2','c3','C4','Answer'])
            #  st.dataframe(show_exam_list,use_container_width=True)
        
            #st.session_state.user_agreement = st.checkbox('Confirm above information')
                st.divider()
                st.session_state.exam_start = True
                st.markdown("**:blue[Start Test ]**")
                exam_list=search_exam(exam_grade,exam_name,exam_version)
                exam_pd = pd.DataFrame( exam_list, columns=["grade", "course_name", "version",'NO','question','c1','c2','c3','C4','Answer'])
                exam_answer_list =exam_pd['Answer']
                user_answer_list =[]
                question_list = exam_pd['question']
                for row_index,row in exam_pd.iterrows(): 
                    exam_question = st.write('NO',str(row_index+1),',',row[4],':question:') 
                    col1, col2 = st.columns([3,1])
                    with col1:
                        st.write('A,',row[5])
                        st.write('B,',row[6])
                        st.write('C,',row[7])
                        st.write('D,',row[8])
                    with col2:
                        exam_answer = st.radio('Please choose',('A','B','C','D'),label_visibility='visible',key=row_index,horizontal= True)
                        rate = str(format((row_index+1)/len(exam_pd),'.0%'))
                        st.write('Total',str(len(exam_pd)),',     :blue[Finish rate] =',rate )
                    user_answer_list.append(exam_answer)
                    st.divider()
                



                exam_finish = st.checkbox('Ready to submit')
                submitted_exam = st.form_submit_button("Submit the answer")
                if submitted_exam and exam_finish :
                    st.success("**:blue[Finished]**, Close exam in 3 seconds") 
                    st.session_state.exam_finish = True 
                   # Get score
                    st.write(user_answer_list)
                    st.write(exam_answer_list)

                    total, correct = 0, 0
                    for i in range(len(user_answer_list)):
                        if exam_answer_list[i] == user_answer_list[i]:
                            st.write('NO',str(i),'......',question_list[i], ':o:','......Answer is',user_answer_list[i])
                            correct += 1
                        else:
                            st.write('NO',str(i),'......',question_list[i],':x:', '......Coccrect answer is',exam_answer_list[i], '......You choose',user_answer_list[i])
                        total += 1

                    score = int(correct / total * 100)
                    st.write('Your Score is ',str(score))

                    # 写入score数据库
                    create_score_table()
                    grade=exam_grade
                    course_name=exam_name
                    version = exam_version
                    user_score = str(score)
                    score_time = datetime.datetime.now().strftime("%Y%m%d%H%M")
                    add_score(grade, course_name, version,user_name,user_mail,user_dept,user_score,score_time)

                    # 显示score DB
                    score_result = view_all_score()
                    score_db = pd.DataFrame( score_result, columns=["grade", "course_name", "version","user_name","user_mail","user_dept","user_score","score_time"])
                    st.dataframe(score_db, use_container_width=True)





                    time.sleep(10)
                    placeholder.empty()

        

    


if __name__ == "__main__":
    main()