# python_project
# 오늘 파이썬 첫수업

# 깃허브 컨트롤 vscode

1 git init   현재 폴더를 Git 저장소로 초기화 (최초 1회만)

2 git config --global user.name    "이름"사용자 이름 설정 (최초 1회만)
--> git config user.name jw-code001

3 git config --global user.email   "메일"사용자 이메일 설정 (최초 1회만)
--> git config user.email jwgame0804@gmail.com

4 git add .(중요)    현재 폴더의 모든 변경 사항을 스테이징(장바구니)에 담기

5 git commit -m "메시지"   장바구니에 담긴 파일을 확정(스냅샷 찍기)

6 git remote add origin [URL]   (중요) 내 컴퓨터와 온라인 깃허브 저장소를 연결

7 git branch -M main   기본 브랜치 이름을 main으로 변경 (최신 깃허브 권장)

8 git push -u origin main --force   깃허브로 파일 전송 (처음 이후엔 git push만)