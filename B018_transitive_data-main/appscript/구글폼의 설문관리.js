/**
 * 새로운 구글 시트 탭을 생성하고 13개 문항 데이터를 초기화하는 함수
 */
function setupNewSurveySheet() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheetName = 'Survey_Setup'; // 새로 만들 탭 이름
  var sheet = ss.getSheetByName(sheetName);
  
  // 1. 이미 탭이 있다면 삭제하거나 새로 만듦
  if (sheet) {
    var ui = SpreadsheetApp.getUi();
    var response = ui.alert('알림', "'" + sheetName + "' 탭이 이미 존재합니다. 삭제하고 새로 만들까요?", ui.ButtonSet.YES_NO);
    if (response == ui.Button.YES) {
      ss.deleteSheet(sheet);
      sheet = ss.insertSheet(sheetName);
    } else {
      return; // 아니오 클릭 시 중단
    }
  } else {
    sheet = ss.insertSheet(sheetName);
  }

  // 2. 헤더 설정 (슈파베이스 컬럼명과 일치)
  var headers = [
    ['question_no', 'content', 'question_type', 'options_summary', 'is_active']
  ];
  sheet.getRange(1, 1, 1, 5).setValues(headers)
       .setBackground('#eeeeee')
       .setFontWeight('bold')
       .setHorizontalAlignment('center');

  // 3. 13개 문항 데이터 (r, c, t 기호 적용)
  var surveyData = [
    [1, '귀하의 연령대는 어떻게 되십니까?', 'r', '10대, 20대, 30대, 40대, 50대, 60대 이상', true],
    [2, '귀하의 성별은 무엇입니까?', 'r', '여성, 남성, 선택하지 않음', true],
    [3, '현재 가장 신경 쓰이는 피부 고민은 무엇입니까? (다중 선택)', 'c', '여드름 및 트러블, 모공 및 피지, 건조함 및 속당김, 주름 및 탄력 저하, 색소 침착 (기미/잡티), 홍조 및 민감성', true],
    [4, '평소 피부과나 에스테틱(피부관리실)을 얼마나 자주 방문하시나요?', 'r', '전혀 방문하지 않음 (홈케어만 진행), 1년에 1~2회, 2~3개월에 1회, 한 달에 1회 이상', true],
    [5, '에스테틱 방문 대신 홈케어를 선호하거나 병행하시는 주된 이유는 무엇인가요?', 'r', '비용 부담이 적어서, 샵에 방문할 시간을 내기 어려워서, 홈케어 기기/제품만으로도 충분해서, 프라이빗한 관리를 원해서', true],
    [6, '홈케어를 위해 주로 사용하시거나 알고 계신 스킨케어/뷰티 디바이스 브랜드가 있다면 적어주세요.', 't', '', true],
    [7, '에스테틱 관리를 받는다면, 가장 집중적으로 관리받고 싶은 부위는 어디인가요?', 'c', '얼굴 전체 (윤곽, 탄력 등), 국소 부위 (눈가, 팔자주름 등), 목 (목주름, 탄력 등), 바디 라인', true],
    [8, '효과가 확실하다면, 한 달에 몇 회 정도 에스테틱을 방문하는 것이 가장 이상적이라고 생각하시나요?', 'r', '한 달에 1회, 한 달에 2회 (격주), 한 달에 4회 (매주), 기타', true],
    [9, '피부 관리를 위해 "한 달에" 지출할 수 있는 최대 비용은 얼마인가요?', 'r', '5만 원 미만, 5만 원 ~ 10만 원 미만, 10만 원 ~ 20만 원 미만, 20만 원 ~ 30만 원 미만, 30만 원 이상', true],
    [10, '1회 관리(약 60분~90분 소요)를 기준으로, 적절하다고 생각하는 1회당 비용은 얼마인가요?', 'r', '3만 원 미만, 3만 원 ~ 5만 원 미만, 5만 원 ~ 8만 원 미만, 8만 원 ~ 12만 원 미만, 12만 원 이상', true],
    [11, '피부 관리실(에스테틱)을 선택할 때 가장 중요하게 생각하는 요소는 무엇입니까?', 'r', '합리적인 가격 및 프로모션, 집이나 직장과의 거리 (접근성), 실제 고객의 후기 및 지인 추천, 원장님의 경력 및 상담 전문성', true],
    [12, '그 외 에스테틱 서비스에 바라는 점이나, 평소 피부 관리에 있어 어려운 점이 있다면 자유롭게 적어주세요.', 't', '', true],
    [13, '다른 의견이 있으시면 적어 주세요.', 't', '', true]
  ];

  // 4. 데이터 삽입
  sheet.getRange(2, 1, surveyData.length, 5).setValues(surveyData);

  // 5. E열(is_active)을 체크박스로 변환
  sheet.getRange(2, 5, surveyData.length, 1).insertCheckboxes();
  
  // 6. 보기 좋게 열 너비 자동 조절
  sheet.autoResizeColumns(1, 5);
  sheet.setColumnWidth(2, 400); // 질문 내용은 길어서 별도 지정
  sheet.setColumnWidth(4, 300); // 선택지도 길어서 별도 지정

  SpreadsheetApp.getUi().alert('🎉 ' + sheetName + ' 탭에 데이터가 성공적으로 세팅되었습니다!');
}
