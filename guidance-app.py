
# Version 16 updated: 01.16.26
# Project objective
# Provided services
# Production-ready

# .\myenv\Scripts\activate (Windows/CLI)
# . ienv/bin/activate : run venv (macOS)
# pip install -r requirements.txt

import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import gspread
from google.oauth2.service_account import Credentials
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Image, Table, TableStyle, Spacer
from reportlab.lib import colors
from datetime import datetime
from reportlab.platypus import Image
from reportlab.lib.units import cm

# -------------------------------
# Default setting & DATA FILE
# -------------------------------
plt.rcParams['font.family'] = 'Tahoma'
plt.rcParams['axes.unicode_minus'] = False

st.set_page_config(page_title="Academic Guidance System", page_icon="images/icon2.png", layout="centered")

@st.cache_resource
def get_gsheet():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scope
    )

    client = gspread.authorize(creds)
    spreadsheet = client.open("Academic_Guidance_Dataset")

    return spreadsheet.sheet1

def register_thai_font():
    pdfmetrics.registerFont(
        TTFont("THSarabun", "fonts/THSarabunNew.ttf")
    )

def fmt(val):
    return f"{val:.2f}" if val is not None else ""

def truncate(value, decimals=2):
    if value is None:
        return ""
    factor = 10 ** decimals
    return int(value * factor) / factor

def setup_ui():
    st.markdown("""
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
    .stApp {
        padding-top: 50px;
        background: linear-gradient(to bottom right, #0033cc, #66ccff, #ffffff);
        background-attachment: fixed;
        background-repeat: no-repeat;
        color: black;
    }
    .title-box {
        background: linear-gradient(to left, #006cff, #1055C9, #006cff);
        color: white;
        padding: 10px;
        border-radius: 10px 10px 0 0;
        text-align: center;
        margin-top: 5px;
        font-size: 20px;
        font-weight: bold;
    }
    .sub-box {
        background-color: #3D90D7; 
        color: white;
        padding: 4px 12px; /* ลดความสูง */
        border-radius: 0 0 10px 10px; /* มุมล่างโค้ง */
        margin-top: 0px; /* ชิดกล่องบน */
        font-size: 14px;
        font-weight: 400;
        text-align: center;
        box-shadow: 0 6px 6px rgba(0,0,0,0.15);
    }
    .block-container {              
        padding: 2rem 1.5rem;
        margin-top: 30px; 
        background-color: rgba(255, 255, 255, 0.85);            
        border-radius: 15px;
        border-left:5px solid #739EC9; 
        border-right:5px solid #739EC9; 
        box-shadow: 0px 0px 10px rgba(0,0,0,0.15);
        text-align: left;
        color: black;
    }
    .section-box {           
        background-color: #ffffff;
        padding: 10px 15px;
        border-left:5px solid #F39C12;            
        font-weight:bold;
        font-size:18px;
        color:#0D3B66;
        margin-top: 5px;
        margin-bottom: 20px;
    }
    .small-gap {margin-top: 12px; margin-bottom: 12px; }

    .details-box summary {
        font-size: 16px;
        font-weight: bold;
        color: #0d6efd;
        cursor: pointer;
    }
    .details-box {
        background: linear-gradient(to bottom, #e3f2fd, #cfe2f3);
        border-left: 5px solid #0dcaf0;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 25px;
        font-weight: bold;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.15);
    }
    </style>
    """, unsafe_allow_html=True)



        # --- Title Box ---
    st.markdown("""
    <div class="title-box">
        <h2>📝 Academic Guidance Systems</h2>
        <p>ระบบแนะแนวการศึกษาตามความสนใจของผู้เรียน</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="sub-box">
        โรงเรียนเซนต์ฟรังซีสเซเวียร์
    </div><br>
    """, unsafe_allow_html=True)

        # --- Collapsible Details Box ---
    st.markdown("""
    <div class="details-box">
    <details>
    <summary>คำชี้แจง: การใช้งานระบบแนะแนวการศึกษาตามความสนใจของผู้เรียน</summary>
    <div style="margin-top:10px;">
        <p><strong>
        - วัตถุประสงค์ </strong> 
                <p>1. ระบบนี้ถูกพัฒนาขึ้นเพื่อช่วยผู้เรียนค้นพบแนวทางการศึกษาที่เหมาะสมกับตนเอง โดยอิงจากข้อมูลพื้นฐาน เช่น ชื่อ เพศ แผนการเรียน คะแนนเฉลี่ย (GPA) คะแนนเฉลี่ยสะสม (GPAX) และความสนใจส่วนบุคคล</p>
                <p>2. ระบบใช้หลักการ <strong>Rule-based</strong> เพื่อแนะนำแนวทางที่เกี่ยวข้องกับความสนใจ เช่น  
        วิทยาศาสตร์ คณิตศาสตร์ ภาษา ศิลปะ คอมพิวเตอร์ ธุรกิจ และสังคมศึกษา</p>
        <h5>ขั้นตอนการใช้งาน(How to Use)</h5>
        <ol>
        <li>กรอกชื่อ-นามสกุล และระดับชั้นของผู้เรียน</li>        
        <li>ระบุเกรดรายวิชาของแต่ละภาคเรียนตามที่ผู้เรียนต้องการ</li>
        <li>เลือกความสนใจอย่างน้อย 1 ด้าน</li>
        <li>กดปุ่ม "🔍 วิเคราะห์แนวทางการศึกษา"</li>
        <li>ดูผลลัพธ์การแนะนำแนวทางในการเลือกแผนการเรียนและกราฟแสดงผล GPA, GPAX ของผู้เรียนและ GPA สูงสุดในแต่ละกลุ่มสายวิชา พร้อมทำการบันทึก</li>
        </ol>
        <p class="text-muted">
        <strong>ข้อจำกัดความรับผิดชอบ:</strong>  
         ผลลัพธ์ที่ได้จากการวิเคราะห์เป็นเพียงคำแนะนำเบื้องต้น เพื่อช่วยให้ผู้เรียนเห็นแนวทางที่สอดคล้องกับตนเอง  
        ควรใช้ร่วมกับคำปรึกษาจากครูแนะแนวหรือผู้เชี่ยวชาญทางการศึกษา
        </p>
    </div>
    </details>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------
# Datasets subjects : M1-M3
# -------------------------------

# Subjects-s1-m1
def get_subjects_s1_m1():
    subjects_s1_m1 = {
        "ท 21101": {"name": "ภาษาไทยเบื้องต้น 1", "credit": 1.5},
        "ค 21101": {"name": "คณิตศาสตร์เบื้องต้น 1", "credit": 1.5},
        "ว 21101": {"name": "วิทยาศาสตร์เบื้องต้น 1", "credit": 1.0},
        "ว 21102": {"name": "การออกแบบเทคโนโลยี 1", "credit": 0.5},
        "ส 21101": {"name": "สังคมศึกษาฯ เบื้องต้น 1", "credit": 1.5},
        "ส 21102": {"name": "ประวัติศาสตร์เบื้องต้น 1", "credit": 0.5},
        "พ 21101": {"name": "สุขศึกษาเบื้องต้น 1", "credit": 0.5},
        "พ 21102": {"name": "พลศึกษาเบื้องต้น 1", "credit": 0.5},
        "ศ 21101": {"name": "ทัศนศิลป์เบื้องต้น 1", "credit": 0.5},
        "ศ 21102": {"name": "ดนตรีและนาฏศิลป์ 1", "credit": 0.5},
        "ง 21101": {"name": "การงานอาชีพเบื้องต้น 1", "credit": 1.0},
        "อ 21101": {"name": "ภาษาอังกฤษเบื้องต้น 1", "credit": 1.5},
    }
    extra_subjects_s1_m1 = [
        ("ว 20207", {"name": "AI Foundations 1", "credit": 0.5}),
        ("ว 21201", {"name": "โครงงานวิทยาศาสตร์ 1", "credit": 0.5}),
        ("จ 21201", {"name": "ภาษาจีนเบื้องต้น 1", "credit": 0.5}),
        ("อ 21201", {"name": "เสริมทักษะภาษา 1", "credit": 1.0}),
    ]
    return subjects_s1_m1, extra_subjects_s1_m1

# Subjects-s2-m1
def get_subjects_s2_m1():
    subjects_s2_m1 = {
        "ท 21102": {"name": "ภาษาไทยเบื้องต้น 2", "credit": 1.5},
        "ค 21102": {"name": "คณิตศาสตร์เบื้องต้น 2", "credit": 1.5},
        "ว 21103": {"name": "วิทยาศาสตร์เบื้องต้น 2", "credit": 1.0},
        "ว 21104": {"name": "วิทยาการคำนวณ 1", "credit": 0.5},
        "ส 21103": {"name": "สังคมศึกษาฯ เบื้องต้น 2", "credit": 1.5},
        "ส 21104": {"name": "ประวัติศาสตร์เบื้องต้น 2", "credit": 0.5},
        "พ 21103": {"name": "สุขศึกษาเบื้องต้น 2", "credit": 0.5},
        "พ 21104": {"name": "พลศึกษาเบื้องต้น 2", "credit": 0.5},
        "ศ 21103": {"name": "ทัศนศิลป์เบื้องต้น 2", "credit": 0.5},
        "ศ 21104": {"name": "ดนตรีและนาฏศิลป์ 2", "credit": 0.5},
        "ง 21102": {"name": "การงานอาชีพเบื้องต้น 2", "credit": 1.0},
        "อ 21102": {"name": "ภาษาอังกฤษเบื้องต้น 2", "credit": 1.5},
    }
    extra_subjects_s2_m1 = [
        ("ว 20208", {"name": "AI Foundations 2", "credit": 0.5}),
        ("ว 21202", {"name": "โครงงานวิทยาศาสตร์ 2", "credit": 0.5}),
        ("จ 21202", {"name": "ภาษาจีนเบื้องต้น 2", "credit": 0.5}),
        ("อ 21202", {"name": "เสริมทักษะภาษา 2", "credit": 1.0}),
    ]
    return subjects_s2_m1, extra_subjects_s2_m1


# Subjects-s1-m2
def get_subjects_s1_m2():
    subjects_s1_m2 = {
        "ท 22101": {"name": "ภาษาไทยเบื้องต้น 3", "credit": 1.5},
        "ค 22101": {"name": "คณิตศาสตร์เบื้องต้น 3", "credit": 1.5},
        "ว 22101": {"name": "วิทยาศาสตร์เบื้องต้น 3", "credit": 1.0},
        "ว 22102": {"name": "การออกแบบเทคโนโลยี 2", "credit": 0.5},
        "ส 22101": {"name": "สังคมศึกษาฯ เบื้องต้น 3", "credit": 1.5},
        "ส 22102": {"name": "ประวัติศาสตร์เบื้องต้น 3", "credit": 0.5},
        "พ 22101": {"name": "สุขศึกษาเบื้องต้น 3", "credit": 0.5},
        "พ 22102": {"name": "พลศึกษาเบื้องต้น 3", "credit": 0.5},
        "ศ 22101": {"name": "ทัศนศิลป์เบื้องต้น 3", "credit": 0.5},
        "ศ 22102": {"name": "ดนตรีและนาฏศิลป์ 3", "credit": 0.5},
        "ง 22101": {"name": "การงานอาชีพเบื้องต้น 3", "credit": 1.0},
        "อ 22101": {"name": "ภาษาอังกฤษเบื้องต้น 3", "credit": 1.5},
    }
    extra_subjects_s1_m2 = [
        ("ว 20207", {"name": "AI Foundations 1", "credit": 0.5}),
        ("ว 22201", {"name": "โครงงานวิทยาศาสตร์ 3", "credit": 0.5}),
        ("จ 22201", {"name": "ภาษาจีนเบื้องต้น 3", "credit": 0.5}),
        ("อ 22201", {"name": "เสริมทักษะภาษา 3", "credit": 1.0}),
    ]
    return subjects_s1_m2, extra_subjects_s1_m2


# Subjects-s2-m2
def get_subjects_s2_m2():
    subjects_s2_m2 = {
        "ท 22102": {"name": "ภาษาไทยเบื้องต้น 4", "credit": 1.5},
        "ค 22102": {"name": "คณิตศาสตร์เบื้องต้น 4", "credit": 1.5},
        "ว 22103": {"name": "วิทยาศาสตร์เบื้องต้น 4", "credit": 1.0},
        "ว 22104": {"name": "วิทยาการคำนวณ 2", "credit": 0.5},
        "ส 22103": {"name": "สังคมศึกษาฯ เบื้องต้น 4", "credit": 1.5},
        "ส 22104": {"name": "ประวัติศาสตร์เบื้องต้น 4", "credit": 0.5},
        "พ 22103": {"name": "สุขศึกษาเบื้องต้น 4", "credit": 0.5},
        "พ 22104": {"name": "พลศึกษาเบื้องต้น 4", "credit": 0.5},
        "ศ 22103": {"name": "ทัศนศิลป์เบื้องต้น 4", "credit": 0.5},
        "ศ 22104": {"name": "ดนตรีและนาฏศิลป์ 4", "credit": 0.5},
        "ง 22102": {"name": "การงานอาชีพเบื้องต้น 4", "credit": 1.0},
        "อ 22102": {"name": "ภาษาอังกฤษเบื้องต้น 4", "credit": 1.5},
    }
    extra_subjects_s2_m2 = [
        ("ว 20208", {"name": "AI Foundations 2", "credit": 0.5}),
        ("ว 22202", {"name": "โครงงานวิทยาศาสตร์ 4", "credit": 0.5}),
        ("จ 22202", {"name": "ภาษาจีนเบื้องต้น 4", "credit": 0.5}),
        ("อ 22202", {"name": "เสริมทักษะภาษา 4", "credit": 1.0}),
    ]
    return subjects_s2_m2, extra_subjects_s2_m2

# Subjects-s1-m3
def get_subjects_s1_m3():
    subjects_s1_m3 = {
        "ท 23101": {"name": "ภาษาไทยเบื้องต้น 5", "credit": 1.5},
        "ค 23101": {"name": "คณิตศาสตร์เบื้องต้น 5", "credit": 1.5},
        "ว 23101": {"name": "วิทยาศาสตร์เบื้องต้น 5", "credit": 1.0},
        "ว 23102": {"name": "การออกแบบเทคโนโลยี 3", "credit": 0.5},
        "ส 23101": {"name": "สังคมศึกษาฯ เบื้องต้น 5", "credit": 1.5},
        "ส 23102": {"name": "ประวัติศาสตร์เบื้องต้น 5", "credit": 0.5},
        "พ 23101": {"name": "สุขศึกษาเบื้องต้น 5", "credit": 0.5},
        "พ 23102": {"name": "พลศึกษาเบื้องต้น 5", "credit": 0.5},
        "ศ 23101": {"name": "ทัศนศิลป์เบื้องต้น 5", "credit": 0.5},
        "ศ 23102": {"name": "ดนตรีและนาฏศิลป์ 5", "credit": 0.5},
        "ง 23101": {"name": "การงานอาชีพเบื้องต้น 5", "credit": 1.0},
        "อ 23101": {"name": "ภาษาอังกฤษเบื้องต้น 5", "credit": 1.5},
    }
    extra_subjects_s1_m3 = [
        ("ว 20207", {"name": "AI Foundations 1", "credit": 0.5}),
        ("ว 23201", {"name": "โครงงานวิทยาศาสตร์ 5", "credit": 0.5}),
        ("จ 23201", {"name": "ภาษาจีนเบื้องต้น 5", "credit": 0.5}),
        ("อ 23201", {"name": "เสริมทักษะภาษา 5", "credit": 1.0}),
    ]
    return subjects_s1_m3, extra_subjects_s1_m3

# Subjects-s2-m3
def get_subjects_s2_m3():
    subjects_s2_m3 = {
        "ท 23102": {"name": "ภาษาไทยเบื้องต้น 6", "credit": 1.5},
        "ค 23102": {"name": "คณิตศาสตร์เบื้องต้น 6", "credit": 1.5},
        "ว 23103": {"name": "วิทยาศาสตร์เบื้องต้น 6", "credit": 1.0},
        "ว 23104": {"name": "วิทยาการคำนวณเบื้องต้น 3", "credit": 0.5},
        "ส 23103": {"name": "สังคมศึกษาฯ เบื้องต้น 6", "credit": 1.5},
        "ส 23104": {"name": "ประวัติศาสตร์เบื้องต้น 6", "credit": 0.5},
        "พ 23103": {"name": "สุขศึกษาเบื้องต้น 6", "credit": 0.5},
        "พ 23104": {"name": "พลศึกษาเบื้องต้น 6", "credit": 0.5},
        "ศ 23103": {"name": "ทัศนศิลป์เบื้องต้น 6", "credit": 0.5},
        "ศ 23104": {"name": "ดนตรีและนาฏศิลป์ 6", "credit": 0.5},
        "ง 23102": {"name": "การงานอาชีพเบื้องต้น 6", "credit": 1.0},
        "อ 23102": {"name": "ภาษาอังกฤษเบื้องต้น 6", "credit": 1.5},
    }
    extra_subjects_s2_m3 = [
        ("ว 20208", {"name": "AI Foundations 2", "credit": 0.5}),
        ("ว 23202", {"name": "โครงงานวิทยาศาสตร์ 6", "credit": 0.5}),
        ("จ 23202", {"name": "ภาษาจีนเบื้องต้น 6", "credit": 0.5}),
        ("อ 23202", {"name": "เสริมทักษะภาษา 6", "credit": 1.0}),
    ]
    return subjects_s2_m3, extra_subjects_s2_m3

# -------------------------------
# grade points 
# -------------------------------
grade_points = {4:4.0, 3.5:3.5, 3:3.0, 2.5:2.5, 2:2.0, 1.5:1.5, 1:1.0, 0:0.0}

# -------------------------------
# Display courses and calc GPA 
# Return: (gpa_or_None, all_grades_dict, all_subjects_dict, all_filled_bool)
# -------------------------------

def check_all_semesters_filled(filled_list):
    """
    filled_list: [filled_s1_m1, filled_s2_m1, filled_s1_m2, ...]
    return: True ถ้ากรอกครบทุกเทอม
    """
    return all(filled_list)

def calculate_gpa(grades, credits):
    """
    grades: list ของคะแนนเกรดเป็นตัวเลข เช่น [4.0, 3.0, 2.0]
    credits: list ของหน่วยกิตของวิชา เช่น [3, 2, 1]
    return: GPA
    """
    total_credits = sum(credits)
    if total_credits == 0:
        return 0
    return sum([g*c for g,c in zip(grades, credits)]) / total_credits

def calculate_gpax_dynamic(semester_data):
    """
    semester_data = [
        (gpa, subjects_all, filled),
        (gpa, subjects_all, filled),
        ...
    ]
    """
    total_grade_points = 0
    total_credits = 0

    for gpa, subs, filled in semester_data:
        if filled and gpa is not None and subs:
            # ✅ ดึงเฉพาะค่าหน่วยกิต (credit) จาก dict แต่ละวิชา
            credits = [sub["credit"] for sub in subs.values()]
            total_credits += sum(credits)
            total_grade_points += gpa * sum(credits)

    if total_credits == 0:
        return None
    return total_grade_points / total_credits

def calculate_gpax_per_semester(semester_data):
    gpax_each_semester = []
    total_sum = 0
    total_count = 0

    for g in semester_data:
        if isinstance(g, (int, float)):
            total_sum += g
            total_count += 1
            gpax_each_semester.append(total_sum / total_count)
        else:
            gpax_each_semester.append(None)
    return gpax_each_semester
            
def render_semester_block(subjects_dict, extra_list, semester_label):
    """
    subjects_dict: dict ของรายวิชาพื้นฐาน
    extra_list: list ของ (code, info) สำหรับรายวิชาเพิ่มเติม
    semester_label: string ใช้เป็น prefix key ใน selectbox
    """
    st.markdown(f'<div class="section-box">{semester_label} - รายวิชาพื้นฐาน</div>', unsafe_allow_html=True)
 
    columns_per_row = 4
    grades_sub = {}
    grades_ex = {}

    # ---------- Display subject courses ----------
    subject_items = list(subjects_dict.items())
    for i in range(0, len(subject_items), columns_per_row):
        row = subject_items[i:i+columns_per_row]
        cols = st.columns(len(row))
        for j, (code, info) in enumerate(row):
            with cols[j]:
                st.markdown(f"<div style='text-align:center; font-weight:bold'>{code}</div>"
                            f"<div style='text-align:center; font-size:14px'>{info['name']}</div>", unsafe_allow_html=True)
                options = [""] + list(grade_points.keys())
                grade_value = st.selectbox("", options=options, key=f"{semester_label}_grade_{code}")
                grades_sub[code] = grade_points[grade_value] if grade_value != "" else None

    # ---------- Display extra courses ----------
    st.markdown(f'<div class="section-box">{semester_label} - รายวิชาเพิ่มเติม</div>', unsafe_allow_html=True)
    for i in range(0, len(extra_list), columns_per_row):
        row = extra_list[i:i+columns_per_row]
        cols = st.columns(len(row))
        for j, (code, info) in enumerate(row):
            with cols[j]:
                st.markdown(f"<div style='text-align:center; font-weight:bold'>{code}</div>"
                            f"<div style='text-align:center; font-size:15px'>{info['name']}</div>", unsafe_allow_html=True)
                options = [""] + list(grade_points.keys())
                grade_value = st.selectbox("", options=options, key=f"{semester_label}_grade_extra_{code}_{i}_{j}")
                grades_ex[code] = grade_points[grade_value] if grade_value != "" else None

    # ---------- รวมรายวิชาและคำนวณ GPA ----------
    extra_dict = {code: info for code, info in extra_list}
    all_subjects = {**subjects_dict, **extra_dict}
    all_grades = {**grades_sub, **grades_ex}
    all_filled = all(all_grades.get(code) is not None for code in all_subjects)

    gpa = None
    gpax_value = None
    if all_filled:
        total_credits = sum(all_subjects[c]["credit"] for c in all_subjects)
        gpa = sum(all_grades[c] * all_subjects[c]["credit"] for c in all_subjects) / total_credits

        # เก็บ GPA ปัจจุบันใน session_state
        st.session_state[f"gpa_{semester_label.replace(' ','_')}"] = gpa

        # ---------- คำนวณ GPAX สะสม ----------
        past_gpas = [v for k, v in st.session_state.items() if k.startswith("gpa_")]
        gpax_value = sum(past_gpas) / len(past_gpas) if past_gpas else gpa

        # ---------- แสดง GPA ----------
        st.markdown(f"""
        <div style="
            background-color: #05339C;      
            color: white;                    
            font-weight: bold;
            font-size: 20px;
            text-align: center;
            padding: 12px;
            border-radius: 10px;
            box-shadow: 2px 4px 8px rgba(0,0,0,0.6);
            text-shadow: 1px 1px 2px rgba(0,0,0,0.7);
            margin-bottom: 15px;
        ">
        🎯 เกรดเฉลี่ย {semester_label}: {truncate(gpa):.2f}
        </div>
        """, unsafe_allow_html=True)

        # ---------- แสดง GPAX ----------
        st.markdown(f"""
        <div style="
            background-color: #1B3C53;      
            color: white;                    
            font-weight: bold;
            font-size: 20px;
            text-align: center;
            padding: 12px;
            border-radius: 10px;
            box-shadow: 2px 4px 8px rgba(0,0,0,0.6);
            text-shadow: 1px 1px 2px rgba(0,0,0,0.7);
            margin-bottom: 15px;
        ">
            📘 GPAX สะสมถึงเทอมนี้: {truncate(gpax_value):.2f}
        </div>
        """, unsafe_allow_html=True)

        # ---------- Feedback GPAX ----------
        threshold = 2.75
        diff = gpax_value - threshold
        if diff < 0:
            color = "#FF4C4C"
            msg = f"⚠️ GPAX ของคุณมีค่าเฉลี่ยต่ำกว่าเกณฑ์ {threshold:.2f} อยู่ที่ {abs(diff):.2f}"
        else:
            color = "#4CAF50"
            msg = f"✅ GPAX ของคุณมีค่าเฉลี่ยสูงกว่าเกณฑ์ {threshold:.2f} อยู่ที่ {diff:.2f}"

        st.markdown(f"""
        <div style="
            background-color: {color};      
            color: white;                    
            font-weight: bold;
            font-size: 20px;
            text-align: center;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 15px;
        ">
            {msg}
        </div>
        """, unsafe_allow_html=True)

    return gpa, all_grades, all_subjects, all_filled, gpax_value

# -------------------------------
# Calculate GPAX (5 semester)
# -------------------------------
def calculate_gpax(gpa_list, subjects_list):
    """
    gpa_list: [gpa_s1_m1, gpa_s2_m1, gpa_s1_m2, gpa_s2_m2, gpa_s1_m3, gpa_s2_m3]
    subjects_list: [subs_s1_m1_all, subs_s2_m1_all, subs_s1_m2_all, subs_s2_m2_all, subs_s1_m3_all, subs_s2_m3_all]
    """
    total_points = 0
    total_credits = 0
    for gpa, subjects in zip(gpa_list, subjects_list):
        if gpa is not None and subjects:
            credits = sum(sub["credit"] for sub in subjects.values())
            total_points += gpa * credits
            total_credits += credits
    if total_credits == 0:
        return None
    return total_points / total_credits

def plot_gpax_histogram(gpax_list, labels):

    # กรองเฉพาะ GPAX ที่ไม่เป็น None
    filtered_indices = [i for i, g in enumerate(gpax_list) if g is not None]
    if not filtered_indices:
        st.warning("ยังไม่มีข้อมูล GPAX ที่กรอก")
        return

    gpax_plot = [gpax_list[i] for i in filtered_indices]
    labels_plot = [labels[i] for i in filtered_indices]

    # Gradient สีฟ้า → ขาวอ่อน ไล่ตามแท่ง
    start_color = np.array([5/255, 51/255, 156/255])   # สีน้ำเงินเข้ม
    end_color   = np.array([30/255, 144/255, 255/255]) # ฟ้าอ่อน
    colors = []
    for i in range(len(gpax_plot)):
        ratio = (i+1)/len(gpax_plot)  # ไล่ gradient ตาม index
        color = start_color*(1-ratio) + end_color*ratio
        colors.append(color)

    # ตำแหน่งแท่งและความกว้าง
    x = np.array(filtered_indices)
    width = 0.5  # ลดความกว้างให้ไม่เต็มพื้นที่

    plt.figure(figsize=(10,5))
    plt.bar(x, gpax_plot, width=width, color=colors, edgecolor='black')
    plt.ylim(0, 4.0)
    plt.ylabel("GPAX")
    plt.title("GPAX ของแต่ละเทอม")
    plt.xticks(np.arange(len(labels)), labels, rotation=45)

    # เว้นขอบซ้าย-ขวา
    plt.subplots_adjust(left=0.15, right=0.95)

    # แสดงค่า GPAX บนแท่ง
    for i, val in zip(x, gpax_plot):
        plt.text(i, val + 0.05, f"{val:.2f}", ha='center', va='bottom', fontweight='bold')

    st.pyplot(plt)
    plt.close()

def calculate_gpax_from_grades(all_grades_list, all_subjects_list):
    total_points = 0
    total_credits = 0

    for grades, subjects in zip(all_grades_list, all_subjects_list):
        for code, grade in grades.items():
            if grade is not None:
                credit = subjects[code]["credit"]
                total_points += grade * credit
                total_credits += credit

    return total_points / total_credits if total_credits > 0 else None

def plot_gpa_gpax_bar(gpa_list, gpax_list, labels):
   

    n_terms = len(labels)
    x = np.arange(n_terms)
    width = 0.45

    # เตรียมค่าที่ไม่เป็น None
    gpa_vals = [g if g is not None else np.nan for g in gpa_list]
    gpax_vals = [g if g is not None else np.nan for g in gpax_list]

    # หา indices ของแท่งจริง
    idx_valid = [i for i, (g, gx) in enumerate(zip(gpa_vals, gpax_vals)) if not np.isnan(g) or not np.isnan(gx)]
    n_valid = len(idx_valid)

    # สี gradient GPA (ฟ้าเข้ม → ฟ้าอ่อน)
    start_gpa = np.array([5/255, 51/255, 156/255])
    end_gpa   = np.array([100/255, 149/255, 237/255])

    # สี gradient GPAX (ฟ้าอ่อน → ฟ้าเข้ม)
    start_gpax = np.array([173/255, 216/255, 230/255])
    end_gpax   = np.array([0/255, 0/255, 205/255])

    colors_gpa = [start_gpa*(1-(i+1)/n_valid) + end_gpa*((i+1)/n_valid) for i in range(n_valid)]
    colors_gpax = [start_gpax*(1-(i+1)/n_valid) + end_gpax*((i+1)/n_valid) for i in range(n_valid)]

    plt.figure(figsize=(10,5))

    for color_idx, i in enumerate(idx_valid):
        if not np.isnan(gpa_vals[i]):
            plt.bar(x[i]-width/2, gpa_vals[i], width=width, color=colors_gpa[color_idx], edgecolor='black', label="GPA" if color_idx==0 else "")
            plt.text(x[i]-width/2, gpa_vals[i]+0.05, f"{truncate(gpa_vals[i]):.2f}", ha='center', va='bottom', fontweight='bold')
        if not np.isnan(gpax_vals[i]):
            plt.bar(x[i]+width/2, gpax_vals[i], width=width, color=colors_gpax[color_idx], edgecolor='black', label="GPAX" if color_idx==0 else "")
            plt.text(x[i]+width/2, gpax_vals[i]+0.05, f"{truncate(gpax_vals[i]):.2f}", ha='center', va='bottom', fontweight='bold')

    plt.ylim(0,4.0)
    plt.ylabel("GPA and GPAX")
    plt.title("GPA and cumulative GPAX for each term")
    plt.xticks(x, labels, rotation=45)
    plt.subplots_adjust(left=0.15, right=0.95)
    plt.legend()
    st.pyplot(plt)
    plt.close()



def rule_based_advice(interests):
    if "คอมพิวเตอร์" in interests or "คณิตศาสตร์" in interests:
        return "แนะนำ: วิศวกรรมคอมพิวเตอร์ / วิทยาการข้อมูล / เทคโนโลยีสารสนเทศ"
    elif "วิทยาศาสตร์" in interests:
        return "แนะนำ: วิทยาศาสตร์ทั่วไป / เทคโนโลยีชีวภาพ / แพทย์"
    elif "ภาษา" in interests:
        return "แนะนำ: อักษรศาสตร์ / มนุษยศาสตร์ / การท่องเที่ยว"
    elif "ศิลปะ" in interests:
        return "แนะนำ: สถาปัตย์ / นิเทศศิลป์ / ออกแบบ"
    elif "ธุรกิจ" in interests or "สังคมศึกษา" in interests:
        return "แนะนำ: บัญชี / บริหารธุรกิจ / รัฐศาสตร์"
    else:
        return "ยังไม่สามารถระบุแนวทางได้!"
    
def generate_pdf_report(
    filename,
    student_id,
    name,
    gender,
    level,
    gpa_list,        # list ของ GPA 6 เทอม
    gpax_list,       # list ของ GPAX 6 เทอม
    interests,
    advice,
    evaluator="ครูอัศวิน สุรวัชโยธิน"
):
    register_thai_font()
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Thai", fontName="THSarabun", fontSize=14, leading=18))
    styles.add(ParagraphStyle(name="ThaiTitle", fontName="THSarabun", fontSize=20, leading=24, alignment=1))

    elements = []

    # Logo (ถ้ามี)
    logo_path = os.path.join("assets", "logo.png")
    if os.path.exists(logo_path):
        logo = Image(logo_path, width=2.5*cm, height=2.5*cm)
        logo.hAlign = "CENTER"
        elements.append(logo)
        elements.append(Spacer(1, 12))

    # Title
    elements.append(Paragraph("<b>Academic Guidance Report</b>", styles["ThaiTitle"]))
    elements.append(Spacer(1, 12))

    # วันที่และผู้ประเมิน
    today = datetime.now().strftime("%d/%m/%Y")
    elements.append(Paragraph(f"วันที่ประเมิน: {today}", styles["Thai"]))
    elements.append(Paragraph(f"ผู้ประเมิน: {evaluator}", styles["Thai"]))
    elements.append(Spacer(1, 12))

    # ข้อมูลนักเรียน
    elements.append(Paragraph(f"รหัสนักเรียน: {student_id}", styles["Thai"]))
    elements.append(Paragraph(f"ชื่อ-สกุล: {name}", styles["Thai"]))
    elements.append(Paragraph(f"เพศ: {gender}", styles["Thai"]))
    elements.append(Paragraph(f"ระดับชั้น: {level}", styles["Thai"]))
    elements.append(Spacer(1, 12))

    # ===============================
    # GPA & GPAX Wide Table
    # ===============================
    labels = ["ม.1/1", "ม.1/2", "ม.2/1", "ม.2/2", "ม.3/1", "ม.3/2"]
    table_data = [["ภาคเรียน", "GPA", "GPAX"]]

    for i, lbl in enumerate(labels):
        gpa_val = gpa_list[i] if i < len(gpa_list) else None
        gpax_val = gpax_list[i] if i < len(gpax_list) else None

        gpa_str = f"{truncate(gpa_val):.2f}" if isinstance(gpa_val, (float, int)) else "-"
        gpax_str = f"{truncate(gpax_val):.2f}" if isinstance(gpax_val, (float, int)) else "-"
        table_data.append([lbl, gpa_str, gpax_str])

    table = Table(table_data, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "THSarabun"),
        ("FONTSIZE", (0, 0), (-1, -1), 14),
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 12))

    # ความสนใจและผลแนะแนว
    elements.append(Paragraph(f"ความสนใจ: {', '.join(interests) if interests else '-'}", styles["Thai"]))
    elements.append(Paragraph(f"ผลแนะแนว: {advice if advice else '-'}", styles["Thai"]))

    doc.build(elements)


def main():
    setup_ui()
    sheet = get_gsheet()
    interests = []
    advice = ""

    # Subjects data
    subjects_s1_m1, extra_subjects_s1_m1 = get_subjects_s1_m1()
    subjects_s2_m1, extra_subjects_s2_m1 = get_subjects_s2_m1()
    subjects_s1_m2, extra_subjects_s1_m2 = get_subjects_s1_m2()
    subjects_s2_m2, extra_subjects_s2_m2 = get_subjects_s2_m2()
    subjects_s1_m3, extra_subjects_s1_m3 = get_subjects_s1_m3()
    subjects_s2_m3, extra_subjects_s2_m3 = get_subjects_s2_m3()

    # Part 1: User profile
    # 1.Header 
    st.markdown('<br><span style="color:#0869ed; font-weight:bold; font-size:20px;">ส่วนที่ 1: ข้อมูลประจำตัว</span>', unsafe_allow_html=True)
   
    st.markdown("""
    <hr style="border: 2px solid #C9CDCF; border-radius: 5px; margin-top:0; margin-bottom:5px;">
    """, unsafe_allow_html=True)

    # 2.studentID
    st.markdown("""
    <div style="display: inline-block; color:0D3B66; font-weight:normal; font-size:18px; margin-right:10px;">รหัสนักเรียน</div>
    """, unsafe_allow_html=True)
    student_id = st.text_input("",key="student_id_input")


    st.markdown("""
    <div style="display: inline-block; color:0D3B66; font-weight:normal; font-size:18px; margin-right:10px;">ชื่อ-นามสกุล</div>
    """, unsafe_allow_html=True)
    name = st.text_input("",key="student_name_input")

    st.markdown("""
    <div style="display: inline-block; color:0D3B66; font-weight:normal; font-size:18px; margin-right:10px;">เพศ</div>
    """, unsafe_allow_html=True)
    gender = st.selectbox("", ["", "ชาย", "หญิง", "อื่น ๆ"], key="gender_select", index=0)

    
    st.markdown("""
    <div style="display: inline-block; color:0D3B66; font-weight:normal; font-size:18px; margin-right:10px;">ระดับชั้น</div>
    """, unsafe_allow_html=True)
    level = st.selectbox("", [""] + ["ม.1/1", "ม.1/2", "ม.1/3", "ม.1/4", "ม.2/1", "ม.2/2", "ม.2/3", "ม.2/4", "ม.3/1", "ม.3/2", "ม.3/3", "ม.3/4"], key="level_select", index=0)

    st.markdown('<br><span style="color:#0869ed; font-weight:bold; font-size:20px">ส่วนที่ 2: คะแนนของคุณ</span>', unsafe_allow_html=True)
    st.markdown("""
    <hr style="border: 2px solid #C9CDCF; border-radius: 5px; margin-top:0; margin-bottom:5px;">
    """, unsafe_allow_html=True)
   

    # Display subjects: M1-M3 (6 semester)

    # Semester 1 block (แสดง section base แล้ว extra ต่อจาก อ 21101)
    
    gpa_s1_m1, grades_s1_m1_all, subs_s1_m1_all, filled_s1_m1, gpax_s1_m1 = render_semester_block(
        subjects_s1_m1, extra_subjects_s1_m1, "ม.1 ภาคเรียนที่ 1", # semester_label
        
    )

    # Semester 2 block (แสดง section base แล้ว extra ต่อจาก อ 21102)
    gpa_s2_m1, grades_s2_m1_all, subs_s2_m1_all, filled_s2_m1, gpax_s2_m1 = render_semester_block(
        subjects_s2_m1, extra_subjects_s2_m1, "ม.1 ภาคเรียนที่ 2" # semester_label
    )

    # Semester 1 block (แสดง section base แล้ว extra ต่อจาก อ 22101)
    gpa_s1_m2, grades_s1_m2_all, subs_s1_m2_all, filled_s1_m2, gpax_s1_m2 = render_semester_block(
        subjects_s1_m2, extra_subjects_s1_m2, "ม.2 ภาคเรียนที่ 1" # semester_label
    )

    # Semester 1 block (แสดง section base แล้ว extra ต่อจาก อ 22102)
    gpa_s2_m2, grades_s2_m2_all, subs_s2_m2_all, filled_s2_m2, gpax_s2_m2 = render_semester_block(
        subjects_s2_m2, extra_subjects_s2_m2, "ม.2 ภาคเรียนที่ 2" # semester_label
    )

    # Semester 1 block (แสดง section base แล้ว extra ต่อจาก อ 23101)
    gpa_s1_m3, grades_s1_m3_all, subs_s1_m3_all, filled_s1_m3, gpax_s1_m3 = render_semester_block(
        subjects_s1_m3, extra_subjects_s1_m3, "ม.3 ภาคเรียนที่ 1"  # semester_label
    )

    # Semester 1 block (แสดง section base แล้ว extra ต่อจาก อ 23102)
    gpa_s2_m3, grades_s2_m3_all, subs_s2_m3_all, filled_s2_m3, gpax_s2_m3 = render_semester_block(
        subjects_s2_m3, extra_subjects_s2_m3, "ม.3 ภาคเรียนที่ 2"  # semester_label
    )

    # ===== หลัง render ครบทุกเทอม =====
    gpa_list = [
        gpa_s1_m1,
        gpa_s2_m1,
        gpa_s1_m2,
        gpa_s2_m2,
        gpa_s1_m3,
        gpa_s2_m3
    ]

    all_grades_list = [
        grades_s1_m1_all,
        grades_s2_m1_all,
        grades_s1_m2_all,
        grades_s2_m2_all,
        grades_s1_m3_all,  
        grades_s2_m3_all
    ]

    all_subjects_list = [
        subs_s1_m1_all,
        subs_s2_m1_all,
        subs_s1_m2_all,
        subs_s2_m2_all,
        subs_s1_m3_all,    
        subs_s2_m3_all
    ]

    gpax_list = []
    for i in range(len(all_grades_list)):
        gpax_val = calculate_gpax_from_grades(
            all_grades_list[:i+1],
            all_subjects_list[:i+1]
        )
        gpax_list.append(gpax_val)
    # st.write("DEBUG GPA LIST:", gpa_list)
    # st.write("DEBUG GPAX:", gpax_list)

    # -------------------------------
    # Plot graph GPAX
    # -------------------------------
    # semester_labels_list = ["ม.1 เทอม1", "ม.1 เทอม2", "ม.2 เทอม1", "ม.2 เทอม2", "ม.3 เทอม1", "ม.3 เทอม2"]
    semester_labels_list = ["M1 TERM 1", "M1 TERM  2", "M2 TERM 1", "M2 TERM 2", "M3 TERM 1", "M3 TERM 2"]
    summary_text = ""

    for i, gpa in enumerate(gpa_list):
        label = semester_labels_list[i]

        if gpa is not None:
            gpax_val = gpax_list[i]
            gpa_str = f"{truncate(gpa):.2f}"
            gpax_str = f"{truncate(gpax_val):.2f}"

            summary_text += f"""
            
    <div style="
        border-left: 6px solid #2E6FF2;
        background: linear-gradient(90deg, #F0F6FF, #FFFFFF);
        padding: 10px 15px;
        margin-bottom: 10px;
        border-radius: 8px;
        font-size: 14px;
    ">
        <b><span style="font-size: 20px;">{label}</span></b><br>
        <span style="color:#1A4FCC; font-weight:800; font-size:16px; letter-spacing: 0.5px;">GPA:</span> <span style="font-size: 16px;">{gpa_str}</span> &nbsp; | &nbsp;
        <span style="color:#1A4FCC; font-weight:800; font-size:16px; letter-spacing: 0.5px;">GPAX:</span> <span style="font-size: 16px;">{gpax_str}
    </div>
    """
        else:
            summary_text += f"""
    <div style="
        border-left: 6px solid #313647;
        background: #F7F7F7;
        padding: 10px 15px;
        margin-bottom: 10px;
        border-radius: 8px;
    ">
        <b>{label}</b><br>
        <span style="color:#777;">GPA:</span> - &nbsp; | &nbsp;
        <span style="color:#777;">GPAX สะสม:</span> -
    </div>
    """

    st.markdown(summary_text, unsafe_allow_html=True)

    plot_gpa_gpax_bar(gpa_list, gpax_list, semester_labels_list)

    has_any_gpa = any(g is not None for g in [
            gpa_s1_m1, gpa_s2_m1,
            gpa_s1_m2, gpa_s2_m2,
            gpa_s1_m3, gpa_s2_m3
        ])

    # Calculate GPAX (5 semester)
    gpax_5 = None
    if all(g is not None for g in [gpa_s1_m1, gpa_s2_m1, gpa_s1_m2, gpa_s2_m2, gpa_s1_m3]):
        gpax_5 = calculate_gpax(
            [gpa_s1_m1, gpa_s2_m1, gpa_s1_m2, gpa_s2_m2, gpa_s1_m3],
            [subs_s1_m1_all, subs_s2_m1_all, subs_s1_m2_all, subs_s2_m2_all, subs_s1_m3_all]
        )
    
    # Calculate GPAX (6 semester)
    gpax_6 = None
    if all(g is not None for g in [gpa_s1_m1, gpa_s2_m1, gpa_s1_m2, gpa_s2_m2, gpa_s1_m3, gpa_s2_m3]):
        gpax_6 = calculate_gpax(
            [gpa_s1_m1, gpa_s2_m1, gpa_s1_m2, gpa_s2_m2, gpa_s1_m3, gpa_s2_m3],
            [subs_s1_m1_all, subs_s2_m1_all, subs_s1_m2_all, subs_s2_m2_all, subs_s1_m3_all, subs_s2_m3_all]
        )
   
        # -------------------------------
        # Academic plan recommendation
        # -------------------------------
        all_semesters = [
            grades_s1_m1_all,
            grades_s2_m1_all,
            grades_s1_m2_all,
            grades_s2_m2_all,
            grades_s1_m3_all,
            grades_s2_m3_all
        ]

        # ---------- คำนวณค่าเฉลี่ย 8 กลุ่มสาระแบบถ่วงน้ำหนักด้วยหน่วยกิต ----------
        prefix_points = {}
        prefix_credits = {}

        for grades, subjects in zip(all_grades_list, all_subjects_list):
            for code, grade in grades.items():
                if grade is not None:
                    prefix = code.split()[0]
                    credit = subjects[code]["credit"]

                    # รวมจีนเข้าอังกฤษ
                    if prefix == "จ":
                        prefix = "อ"

                    prefix_points[prefix] = prefix_points.get(prefix, 0) + grade * credit
                    prefix_credits[prefix] = prefix_credits.get(prefix, 0) + credit

        prefix_avg = {
            pfx: prefix_points[pfx] / prefix_credits[pfx]
            for pfx in prefix_points
        }
        
        # ตรวจสอบเงื่อนไขแต่ละแผน
        rec_plans = []
        if prefix_avg.get("ค", 0) >= 2.50 and prefix_avg.get("อ", 0) >= 2.50:
            rec_plans.append("🔹 แผนการเรียนคณิต–อังกฤษ")
        if prefix_avg.get("ว", 0) >= 2.75 and prefix_avg.get("ค", 0) >= 2.75:
            rec_plans.append("🔹 แผนการเรียนวิทย์–คณิต")
        if prefix_avg.get("อ", 0) >= 2.50:
            rec_plans.append("🔹 แผนการเรียนภาษาอังกฤษ–จีน / อังกฤษ–ฝรั่งเศส")

        # -------------------------------
        # Display academic plan + interest advice in Card
        # -------------------------------
        # st.markdown('<br><span style="color:#0D3B66; font-weight:bold; font-size:18px">ส่วนที่ 3: แนะนำแผนและคำแนะนำตามความสนใจ</span>', unsafe_allow_html=True)
        st.markdown('<br><span style="color:#0869ed; font-weight:bold; font-size:20px">ส่วนที่ 3: แนะนำแผนการเรียนและแนวทางการศึกษาต่อในอนาคต</span>', unsafe_allow_html=True)
        st.markdown("""
        <hr style="border: 2px solid #C9CDCF; border-radius: 5px; margin-top:0; margin-bottom:5px;">
        """, unsafe_allow_html=True)
        
        with st.container():
            st.markdown("### 📝 สรุปคำแนะนำ")
            
            # Card สำหรับแผนการเรียน
            if rec_plans:
                st.markdown("#### ✅ แผนการเรียนที่เหมาะสม")
                for plan in rec_plans:
                    st.info(plan)
            else:
                # st.warning("⚠️ ยังไม่ผ่านเกณฑ์ของทุกแผนการเรียน โปรดปรับปรุงผลการเรียนในบางวิชา")
                st.markdown("""
                <div style="
                    background-color:#FF4646;
                    color:#FFFFFF;
                    padding:10px;
                    border-radius:8px;
                    font-weight:bold;
                ">
                ⚠️ ยังไม่ผ่านเกณฑ์ของทุกแผนการเรียน โปรดปรับปรุงผลการเรียนในบางรายวิชา
                </div><br>
                """, unsafe_allow_html=True)

            # Card สำหรับความสนใจ

            st.markdown("""
            <div style="
                background: linear-gradient(135deg, #0033cc, #66ccff); /* ฟ้าเข้ม → ฟ้าอ่อน */
                color: white; /* ตัวอักษรสีขาว */
                font-weight: bold; /* ตัวหนา */
                font-size: 18px;
                padding: 12px;
                border-radius: 10px;
                text-shadow: 1px 1px 3px rgba(0,0,0,0.5); /* เงาตัวอักษร */
            ">
            เลือกความสนใจของคุณ (สามารถเลือกหลายข้อได้)
            </div>
            """, unsafe_allow_html=True)

            interests = st.multiselect(
                "",
                ["คอมพิวเตอร์", "คณิตศาสตร์", "วิทยาศาสตร์", "ภาษา", "ศิลปะ", "ธุรกิจ", "สังคมศึกษา"]
            )

            if interests:
                advice = rule_based_advice(interests)
                st.markdown("#### 💡 คำแนะนำตามความสนใจ")
                st.info(advice)
            else:
                st.info("⚠️ กรุณาเลือกความสนใจเพื่อรับคำแนะนำ")

        # -------------------------------
        # Display prefix average
        # -------------------------------
        # st.markdown("**📊 ค่าเฉลี่ยรายหมวดวิชา:**")
        st.markdown("**📊 ผลการเรียนเฉลี่ยสะสม (GPAX) แยกตามกลุ่มสาระการเรียนรู้ (6 ภาคเรียน)**")
        prefix_name_map = {
            "ท": "ภาษาไทย",
            "ค": "คณิตศาสตร์",
            "ว": "วิทยาศาสตร์",
            "ส": "สังคมศึกษา",
            "พ": "สุขศึกษาและพลศึกษา",
            "ศ": "ศิลปะ ดนตรีและนาฏศิลป์",
            "ง": "การงานอาชีพ",
            "อ": "ภาษาต่างประเทศ",
        }
        for pfx, val in prefix_avg.items():
            subject_name = prefix_name_map.get(pfx, pfx)
            # st.write(f"• กลุ่มรายวิชา {subject_name}:   ได้ค่าเฉลี่ย {val:.2f}")
            st.write(f"• กลุ่มสาระวิชา {subject_name}:   ได้ค่าเฉลี่ย {truncate(val):.2f}")

    save_enabled = bool(
        name and gender and level and has_any_gpa
    )

    # CSS button
    st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #0d6efd;  /* สีพื้นหลัง */
        color: white;                /* สีตัวอักษร */
        font-weight: bold;
        border-radius: 8px;          /* ขอบโค้ง */
        padding: 0.4rem 1rem;        /* ระยะภายในปุ่ม */
        border: none;
        transition: 0.3s;
    }
    div.stButton > button:first-child:hover {
        background-color: #0b5ed7;  /* สีเมื่อ hover */
        cursor: pointer;
    }
    div.stButton > button:first-child:disabled {
        background-color: #0BA6DF;  /* สีเมื่อปุ่ม disabled */
        cursor: not-allowed;
    }
    </style>
    """, unsafe_allow_html=True)

    if st.button("💾 Saved info", disabled=not save_enabled):    
        gpax5_str = f"{truncate(gpax_5):.2f}" if gpax_5 is not None else ""
        gpax6_str = f"{truncate(gpax_6):.2f}" if gpax_6 is not None else ""
    
        row = [
            student_id,
            name,
            gender,
            level,
            fmt(gpa_s1_m1),
            fmt(gpa_s2_m1),
            fmt(gpa_s1_m2),
            fmt(gpa_s2_m2),
            fmt(gpa_s1_m3),
            fmt(gpa_s2_m3),
            gpax5_str,
            gpax6_str,
            ", ".join(interests),
            advice if interests else ""
        ]
        sheet.append_row(row)
        st.success("✅ บันทึกข้อมูลเรียบร้อยแล้ว")
    else:
        if not save_enabled:            
            st.info("ℹ️ กรุณากรอกข้อมูลครบทุกช่องก่อนบันทึก")
    
    can_export = bool(
        name
        and has_any_gpa
        # and advice
    )
    gpa_list = [gpa_s1_m1, gpa_s2_m1, gpa_s1_m2, gpa_s2_m2, gpa_s1_m3, gpa_s2_m3]

    if st.button("📄 Export PDF Report", disabled=not can_export):
        pdf_path = "academic_report.pdf"

        generate_pdf_report(
            filename=pdf_path,
            student_id=student_id,
            name=name,
            gender=gender,
            level=level,
            gpa_list=gpa_list,
            gpax_list=gpax_list,
            interests=interests,
            advice=advice
        )

        with open(pdf_path, "rb") as f:
            st.download_button(
                "⬇️ Download PDF",
                f,
                file_name="Academic_Guidance_Report.pdf",
                mime="application/pdf"
            )

    if not can_export:
        st.info("ℹ️ กรุณากรอกข้อมูลและประเมินผลให้ครบก่อน Export รายงาน")

    # Footer copyright
    st.markdown("""
    <div style="
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: linear-gradient(to right, #e3f2fd, #cfe2f3);
        text-align: center;
        padding: 8px 0;
        font-size: 12px;
        color: #0D3B66;
        font-weight: 500;
        box-shadow: 0 -2px 5px rgba(0,0,0,0.5);
        border-bottom: 5px solid #739EC9;
        z-index: 1000;
    ">
        <p style='margin: 0;'>ผู้พัฒนาและปรับปรุงระบบแนะแนวการศึกษาตามความสนใจของผู้เรียน: <strong>ครูอัศวิน สุรวัชโยธิน</strong></p>
        <p style='margin: 0;'>Academic Guidance Systems 1.2.0 | Last updated : 01.20.26 | เพื่อเพิ่มประสิทธิภาพและความถูกต้องของข้อมูลแนะนำ</p>               
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
