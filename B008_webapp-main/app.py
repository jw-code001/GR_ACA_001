import streamlit as st
import numpy as np
import pandas as pd

# 앱 제목
st.title("간단한 데이터 분석 대시보드")

# 사용자 입력 (사이드바)
st.sidebar.header("설정 메뉴")
number = st.sidebar.slider("데이터 포인트 개수 선택", 10, 100, 50)

# 데이터 생성
data = pd.DataFrame(
    np.random.randn(number, 2),
    columns=['값 1', '값 2']
)

# 시각화 출력
st.subheader("랜덤 데이터 분포 차트")
st.line_chart(data)

# 데이터프레임 확인 여부
if st.checkbox("데이터 테이블 보기"):
    st.write(data)