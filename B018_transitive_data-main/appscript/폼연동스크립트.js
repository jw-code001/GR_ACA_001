function updateGoogleFormFromNewSheet() {
  var ui = SpreadsheetApp.getUi();
  var FORM_ID = '폼아이디'; 
  
  var form = FormApp.openById(FORM_ID);
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Survey_Setup');
  var data = sheet.getDataRange().getValues();
  
  // 🔥 [중복 방지 핵심] 기존 폼에 있던 모든 문항을 먼저 싹 지웁니다.
  var existingItems = form.getItems();
  for (var i = 0; i < existingItems.length; i++) {
    form.deleteItem(existingItems[i]);
  }
  
  // 데이터 삽입 루프
  for (var i = 1; i < data.length; i++) {
    var qNo      = data[i][0]; // A열: PK (질문번호)
    var content  = data[i][1]; // B열: 질문내용
    var qType    = data[i][2]; // C열: r, c, t
    var options  = data[i][3]; // D열: 선택지
    var isActive = data[i][4]; // E열: 활성여부
    
    // 활성화된 것만 생성 (슈파베이스 is_active 정책과 동일)
    if (isActive !== true || !content) continue;

    // 제목에 PK(질문번호)를 명시하여 상징성 유지
    var title = "Q" + qNo + ". " + content;
    
    // 선택지 중복 제거 로직 (Set 활용)
    var choiceArray = [];
    if (options) {
      var rawOptions = options.toString().split(',');
      var uniqueSet = new Set();
      rawOptions.forEach(opt => {
        var trimmed = opt.trim();
        if (trimmed) uniqueSet.add(trimmed);
      });
      choiceArray = Array.from(uniqueSet);
    }

    // 타입별 생성
    switch (qType) {
      case 'r':
        if (choiceArray.length < 2) choiceArray.push('선택지 부족');
        form.addMultipleChoiceItem().setTitle(title).setChoiceValues(choiceArray);
        break;
      case 'c':
        if (choiceArray.length < 2) choiceArray.push('선택지 부족');
        form.addCheckboxItem().setTitle(title).setChoiceValues(choiceArray);
        break;
      case 't':
        form.addParagraphTextItem().setTitle(title);
        break;
    }
  }
  ui.alert('✅ 동기화 완료! 중복 없이 ' + (data.length - 1) + '개 문항이 정리되었습니다.');
}
