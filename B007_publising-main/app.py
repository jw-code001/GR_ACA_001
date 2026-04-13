# %%
import streamlit as st
import pandas as pd
import numpy as np

# 앱 제목 설정
st.title("수정된 타이틀")

# 간단한 설명
st.write("이 앱은 Streamlit을 사용하여 웹으로 배포된 대시보드 예시입니다.")

# 데이터 생성
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['A', 'B', 'C']
)

# 사이드바 제어 요소 추가
st.sidebar.header("설정")
show_data = st.sidebar.checkbox("원본 데이터 보기")

if show_data:
    st.subheader("Raw Data")
    st.write(chart_data)

# 라인 차트 시각화
st.subheader("데이터 트렌드 (Line Chart)")
st.line_chart(chart_data)