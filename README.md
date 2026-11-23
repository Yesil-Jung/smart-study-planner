# smart-study-planner

## 자동 스케줄러 (B 파트)

### 주요 기능
- 과제 마감일을 기준으로 우선순위 정렬
- 예상 소요 시간에 따라 공부 시간 자동 배치
- 수업 시간표를 기준으로 공부 가능한 빈 시간 계산
- 여러 과제를 등록하고 공부 계획 생성
- Streamlit 웹페이지에서 생성된 공부 계획 확인

### 관련 파일
- `scheduler.py`: 과제 정렬 및 자동 배치
- `free_time.py`: 수업 시간을 제외한 빈 시간 계산
- `scheduler_page.py`: Streamlit 웹페이지

### 실행 방법

1. 필요한 패키지를 설치합니다.

    python -m pip install streamlit

2. 프로젝트 폴더에서 다음 명령어를 실행합니다.

    python -m streamlit run scheduler_page.py

3. 웹페이지에서 과목명, 과제명, 마감일, 예상 소요 시간을 입력합니다.

4. 과제를 추가한 후 '공부 계획 생성' 버튼을 클릭합니다.

### 개발 환경
- Python 3
- Streamlit

### 현재 구현 상태
- 여러 과제 자동 배치 기능 구현 완료
- 테스트용 시간표를 이용한 빈 시간 계산 구현 완료
- 팀원 시간표 데이터 연동 및 통합 테스트 예정

