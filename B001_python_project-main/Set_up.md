# 아나콘다. 파이썬 설치

# 아나콘다 설치 (1.1G)

3.13등 최신버전 디폴트는 체크하지 말것

[앱 실행 별칭]에서 앱설치 관리자 두개 끔

사용자 path 설정 (시스템환경변수 에서)

C:\Users\사용자이름\anaconda3

C:\Users\사용자이름\anaconda3\Scripts

C:\Users\사용자이름\anaconda3\Library\bin

conda --version 되는지 확인

# 가상환경 설정
1 ) python 설치 : conda create -n p310 python=3.10

2 ) python --version

3 ) pip install pandas gspread oauth2client plotly matplotlib

    numpy

    pandas : 표 데이터 분석등 작업

    plotly : 움직이는 그래프

    matplotlib

    gspread : 구글 스프레드시트 조종

    oauth2client : 구글 시트 접근시의 보안도구

# 설치검증 데이터 구조 예시

df = pd.DataFrame({'품목': ['셔츠', '바지'], '상태': ['세탁중', '완료']})

print("\n[현재 세탁소 현황]")

print(df)

print("축하합니다! 파이썬 엔진과 라이브러리가 완벽하게 연결되었습니다.")

# 아나콘다 환경 활성화 (p310 환경 기준)
conda activate p310

# 판다스가 있는지 확인
pip list | grep pandas​