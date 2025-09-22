function test(){
  var result = getSheetData("001");
  Logger.log(result);
}

function doGet(e) {
  const keyword = (e.parameter.keyword || "").trim();
  if (!keyword) {
    return ContentService.createTextOutput(
      JSON.stringify({ error: "No keyword provided" })
    ).setMimeType(ContentService.MimeType.JSON);
  }

  result = getSheetData(keyword);

  const output = result ? JSON.stringify(result) : JSON.stringify({});
  return ContentService
    .createTextOutput(output)
    .setMimeType(ContentService.MimeType.JSON);
}

function getSheetData(keyword){
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("シート1"); // 1は半角
  const data = sheet.getDataRange().getValues(); // 2次元配列
  const headers = data[0];

  let result = null;

  for (let i = 1; i < data.length; i++) {
    const id = data[i][0]; // 1列目: ID
    const name = data[i][1]; // 2列目: 名前
    const hp = data[i][2]; // 3列目: HP
    if (id === keyword) {
      result = { [headers[0]]: id, [headers[1]]: name, [headers[2]]: hp };
      break;
    }
  }
  return result;
}

function getSheetMultiData(keyword){
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("シート1");
  const data = sheet.getDataRange().getValues(); // [[用語, 定義], ...]
  const results = [];
  const headers = data[0];

  for (let i = 1; i < data.length; i++) {
    const id = data[i][0]; // 1列目: ID
    const name = data[i][1]; // 2列目: 名前
    const hp = data[i][2]; // 3列目: HP
      if (id === keyword) {
      results.push({ [headers[0]]: id, [headers[1]]: name, [headers[2]]: hp });
    }
  }
  return results;
}

