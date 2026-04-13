# %% [1] 라이브러리 로드 및 샘플 데이터 생성
import pandas as pd
import numpy as np

# 아나콘다 환경에서 잘 작동하는지 확인하기 위해 샘플 데이터를 만듭니다.
data = {
    '날짜': pd.date_range(start='2024-01-01', periods=5),
    '매출': [150, 230, 180, 450, 320],
    '방문객': [50, 65, 55, 120, 90],
    '도시': ['서울', '부산', '서울', '인천', '부산']
}

df = pd.DataFrame(data)

# 실행 후 Interactive 창 상단의 'Variables' 버튼을 눌러 df를 데이터 뷰어로 확인하세요!
print("1. 데이터 프레임 생성 완료! 변수 목록에서 df를 클릭해 보세요.")

# %% [2] 간단한 시각화 UI 확인
import matplotlib.pyplot as plt

# 한글 깨짐 방지 설정 (아나콘다 윈도우 기본 폰트인 맑은 고딕 설정)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# df.plot() 실행
df.plot(kind='line', x='날짜', y=['매출', '방문객'], marker='o', figsize=(10, 5))

plt.title("주간 영업 실적 현황")
plt.grid(True)
plt.show()

print("2. 그래프 시각화 완료! 오른쪽 Interactive 창에 그래프가 표시됩니다.")
# %%
