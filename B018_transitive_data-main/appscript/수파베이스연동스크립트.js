function syncSheetToSupabase() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName('Survey_Setup');
  var data = sheet.getDataRange().getValues();
  
  // 슈파베이스 설정 (본인의 정보로 교체)
  var SUPABASE_URL = 'https://XXXXX.supabase.co';
  var SUPABASE_KEY = '키복사'; // 보안을 위해 service_role 키 사용 권장
  
  var payload = [];
  
  for (var i = 1; i < data.length; i++) {
    payload.push({
      "question_no": data[i][0],      // PK
      "content": data[i][1],
      "question_type": data[i][2],    // r, c, t
      "options_summary": data[i][3],
      "is_active": data[i][4]
    });
  }

  var options = {
    "method": "post",
    "contentType": "application/json",
    "headers": {
      "apikey": SUPABASE_KEY,
      "Authorization": "Bearer " + SUPABASE_KEY,
      "Prefer": "resolution=merge-duplicates" // ★ 중복 시 업데이트(Upsert) 옵션
    },
    "payload": JSON.stringify(payload)
  };

  try {
    var response = UrlFetchApp.fetch(SUPABASE_URL + "/rest/v1/survey_questions", options);
    SpreadsheetApp.getUi().alert("✅ 슈파베이스 동기화 성공!");
  } catch (e) {
    Logger.log(e.toString());
    SpreadsheetApp.getUi().alert("❌ 에러 발생: " + e.message);
  }
}
