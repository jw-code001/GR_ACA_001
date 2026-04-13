# %%
import pandas as pd

df = pd.read_csv('../src/csv/노인요양시설.csv',  encoding='cp949')
# %%
print(df)

# %%
print(df.shape)
# %%
print(df.transpose())
# %%
print('확인')
print(df.head())
print(df.head(1))
# %%
print(df.columns)

# %%
print(type(df))
# %%
print(df.dtypes)

# %%
# df_t = df.transpose()
# print(df_t, df_t.shape, df_t.columns)
# %%
print('전치후 컬럼명 확인하기/ 숫자임')
df_t = df.T
print(df_t.head(), df_t.shape, df_t.columns)

# %%
print('컬럼명 수정하기')
df_t = df_t.reset_index()
df_t.columns = ["년월", "신고수", "신축수"]
print(df_t.head())

# %%
# df_t.columns = df_t.iloc[0]
print(df_t.columns)
print(df_t[2:3])

# df_t[0:3]: 0, 1, 2번 행 (총 3개)

# df_t[2:3]: 2번 행 딱 하나 (3번은 포함 안 됨)

# df_t[5:10]: 5, 6, 7, 8, 9번 행 (총 5개)

# %%
df_t = df_t[1:]
print(df_t.head())

# %%

import numpy as np
df_t[['신고수', '신축수']] = df_t[['신고수', '신축수']].replace(0, np.nan)
print(df_t)

# %%
print(df_t.isnull().sum())
# %%
# '신고수'와 '신축수' 컬럼의 빈값을 숫자 0으로 채우기
df_t[['신고수', '신축수']] = df_t[['신고수', '신축수']].fillna(0)
print('빈값은 \n',df_t.isnull().sum())

print('0의 값은 \n', (df_t == 0).sum())
# %%
# 1. 각 행의 모든 값이 0인지 검사 (True/False 결과 반환)
# axis=0 (기본값): 세로 방향 (위에서 아래로)

#axis=1: 가로 방향 (왼쪽에서 오른쪽으로)
# null은 실수라 다른 값으로 대체될때 소수점이 생김
print(df_t)
all_zero_rows = (df_t == 0).all(axis=1)

# 2. True(모든 값이 0인 행)의 개수 합산
print(all_zero_rows.sum())
# %%
df_t[['신고수', '신축수']] = df_t[['신고수', '신축수']].astype(int)
print(df_t.head(3))
all_zero_rows = (df_t == 0).all(axis=1)

# 2. True(모든 값이 0인 행)의 개수 합산
print('모든 행의 값이 0인 행의 수는 ', all_zero_rows.sum())
# %%
custom_zero_rows = (df_t[['신고수', '신축수']] == 0).all(axis=1)
count = custom_zero_rows.sum()
print(f"두 컬럼 모두 0인 행의 개수: {count}")
print('전체 행의 개수 ',df_t.shape[0])
# %%
# 1. 두 컬럼이 모두 0인 행을 찾음
condition = (df_t['신고수'] == 0) & (df_t['신축수'] == 0)

# 2. 물결표(~)를 붙여서 '조건에 해당하지 않는' 행들만 골라 새로운 변수에 저장
df_filtered = df_t[~condition].copy()

# 확인
print(f"원본 행 개수: {len(df_t)}")
print(f"삭제 후 행 개수: {len(df_filtered)}")

print(df_filtered)
# %%
import matplotlib.pyplot as plt

# 한글 대신 영어 컬럼명으로 잠시 변경해서 그리기

df_plot = df_filtered[['신고수', '신축수']].iloc[0]
df_plot.index = ['Report_Count', 'New_Construction'] # 한글 -> 영어
df_plot.plot(kind='bar')
plt.show()
# %%
# 2. 시각화 설정
# width=0.8 혹은 0.9 정도로 설정하면 막대가 두꺼워지며 서로 가까워집니다.
ax = df_plot.plot(kind='bar', 
                  color=['#3498db', '#e67e22'], # 각각 다른 색상
                  width=.8,                     # 막대 두께 (간격 조절)
                  figsize=(6, 5)) #표사이즈 비율로 확인

# 3. y축 세부 설정 (0부터 5까지, 1단위)
plt.ylim(0, 5) 
# plt.yticks(np.arange(0, 6, 1)) 
plt.yticks([0, 2, 5, 10])

# 4. 기타 스타일 정리
plt.title(f"{df_filtered['년월'].iloc[0]} report", fontsize=14, pad=15)
plt.xticks(rotation=0) # x축 글자 똑바로
plt.grid(axis='y', linestyle='--', alpha=0.3) # 보조선 추가

# 막대 위에 숫자 표시
for i, v in enumerate(df_plot):
    ax.text(i, v + 0.1, str(int(v)), ha='center', fontweight='bold')

plt.show()

# %%
