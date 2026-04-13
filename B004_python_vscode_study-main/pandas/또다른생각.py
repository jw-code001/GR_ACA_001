# %%
import pandas as pd

df = pd.read_csv('../src/csv/노인요양시설.csv',  encoding='cp949')

print(df)



# %%

df_t = df.T
df_t = df_t.reset_index()
df_t.columns = ["년월", "신고수", "신축수"]
df_t = df_t[1:]
print(df_t)
# %%
# 1. 두 컬럼이 모두 0인 행을 찾음
condition = (df_t['신고수'] == 0) & (df_t['신축수'] == 0)

# 2. 물결표(~)를 붙여서 '조건에 해당하지 않는' 행들만 골라 새로운 변수에 저장
df_filtered = df_t[~condition].copy()

# 1. 필터링된 결과가 딱 1개인지 확인
if len(df_filtered) == 1:
    # 해당 행의 '이름'을 가져와서 원본(df_t)에서의 '숫자 위치'를 찾음
    target_row_name = df_filtered.index[0]
    target_idx = df_t.index.get_loc(target_row_name)
    
    # 앞뒤 2개씩 범위를 잡음 (0보다 작아지거나 전체 길이를 넘지 않게 조절)
    start = max(0, target_idx - 2)
    end = min(len(df_t), target_idx + 3) # 슬라이싱 끝은 미포함이라 +3
    
    # 최종적으로 5개(혹은 그 근처)의 행을 가진 데이터프레임 생성
    df_context = df_t.iloc[start:end]
    
    print(f"타겟 행 위치: {target_idx}, 추출된 범위: {start} ~ {end-1}")
else:
    # 0개이거나 2개 이상일 때는 다른 처리를 함
    df_context = df_filtered

print(df_context, len(df_context))
# %%
import matplotlib.pyplot as plt
import numpy as np
import platform

# 1. 한글 폰트 설정 (환경에 맞게)
if platform.system() == 'Windows':
    plt.rc('font', family='Malgun Gothic')
elif platform.system() == 'Darwin':
    plt.rc('font', family='AppleGothic')
else:
    # 깃코드스페이스용 나눔폰트 설정 (설치되어 있다고 가정)
    plt.rc('font', family='NanumGothic')
plt.rcParams['axes.unicode_minus'] = False

# 2. 데이터 처리 (len이 1일 때 앞뒤 2개씩 가져오기)
if len(df_filtered) == 1:
    target_row_name = df_filtered.index[0]
    target_idx = df_t.index.get_loc(target_row_name)
    
    # 앞뒤 2개씩 범위 계산 (슬라이싱용)
    start = max(0, target_idx - 2)
    end = min(len(df_t), target_idx + 3)
    df_context = df_t.iloc[start:end].copy()
else:
    df_context = df_filtered.copy()

# 3. 시각화 시작
# '신고수'와 '신축수' 두 컬럼을 나란히 그립니다.
ax = df_context[['신고수', '신축수']].plot(kind='bar', 
                                         figsize=(10, 6), 
                                         width=0.8,
                                         color=['#3498db', '#e67e22']) # 신고수: 파랑, 신축수: 주황

# 4. y축 설정 (0~5까지 1단계씩)
plt.ylim(0, 5)
plt.yticks(np.arange(0, 6, 1))

# 5. 막대 위에 숫자 넣기
for p in ax.patches:
    # 하이값이 0보다 클 때만 표시 (깨끗하게 보이기 위해)
    if p.get_height() > 0:
        ax.annotate(f"{int(p.get_height())}", 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='center', 
                    xytext=(0, 7), 
                    textcoords='offset points',
                    fontsize=10, fontweight='bold')

# 6. 제목 및 레이블 (알맹이 값만 추출)
title_date = df_filtered['년월'].iloc[0] if len(df_filtered) > 0 else "No Data"
plt.title(f"{title_date} 전후 리포트 비교", fontsize=15, pad=20)
plt.xticks(rotation=0) # 날짜(x축) 똑바로 세우기
plt.grid(axis='y', linestyle='--', alpha=0.3)
plt.legend(loc='upper right')

plt.tight_layout()
plt.show()
# %%
