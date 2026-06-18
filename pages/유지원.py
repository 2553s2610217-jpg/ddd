import streamlit as st
import pandas as pd
import os
from datetime import datetime

FILE = "reservations.csv"

# 파일 없으면 생성
if not os.path.exists(FILE):
    df = pd.DataFrame(
        columns=[
            "학년",
            "반",
            "생년월일",
            "이름",
            "증상",
            "예약시간"
        ]
    )
    df.to_csv(FILE, index=False, encoding="utf-8-sig")


def load_data():
    return pd.read_csv(FILE, encoding="utf-8-sig")


def save_data(data):
    data.to_csv(FILE, index=False, encoding="utf-8-sig")


st.set_page_config(
    page_title="학교 보건실 예약",
    page_icon="🏥"
)

st.title("🏥 학교 보건실 예약 시스템")


st.subheader("예약하기")

grade = st.selectbox(
    "학년",
    [1, 2, 3]
)

class_num = st.number_input(
    "반",
    min_value=1,
    max_value=20,
    step=1
)

birth = st.date_input(
    "생년월일"
)

name = st.text_input(
    "이름"
)

symptom = st.text_area(
    "증상"
)


if st.button("예약하기"):

    if not name or not symptom:
        st.warning("이름과 증상을 입력해주세요.")

    else:
        data = load_data()

        duplicate = data[
            (data["학년"] == grade) &
            (data["반"] == class_num) &
            (data["생년월일"] == str(birth)) &
            (data["이름"] == name)
        ]

        if len(duplicate) > 0:
            st.error(
                "이미 같은 정보로 예약되어 있습니다."
            )

        else:
            new = pd.DataFrame(
                [{
                    "학년": grade,
                    "반": class_num,
                    "생년월일": str(birth),
                    "이름": name,
                    "증상": symptom,
                    "예약시간":
                        datetime.now().strftime(
                            "%Y-%m-%d %H:%M"
                        )
                }]
            )

            data = pd.concat(
                [data, new],
                ignore_index=True
            )

            save_data(data)

            st.success(
                "예약이 완료되었습니다!"
            )


st.divider()

st.subheader("📋 현재 예약 목록")

data = load_data()

if len(data) == 0:
    st.info("예약자가 없습니다.")

else:
    st.dataframe(
        data,
        use_container_width=True
    )
