import requests
import json
import flet as ft
### Google Apps ScriptのURLを指定
url="https://script.google.com/macros/s/AKfycbx5OhI63X2zNDLAAuTgWRMiJ4t0qX71xJKXdgpfDRBlWr38ORBfz7URt-kIG0g5TG0wQQ/exec"

def fetch_data(value):
    global url
    url2=url+"?keyword=" + value
    # Google Apps ScriptのURLを指定
    response = requests.get(url2)
    print(response.status_code)
    if response.status_code == 200:
        print(response.text)
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

def main(page: ft.Page):
    def on_click(e):
        value = text_field.value
        data = fetch_data(value)
        if data:
            #カウントして１行ずつ表示
            result_text.value = ""
            for i in range(len(data)):
                result_text.value += str(i+1) + "行目" + data[i]['name'] + "さんのデータが取得できました。\n"
        else:
            result_text.value = "データの取得に失敗しました。"
        page.update()
    ##GUIコンポーネントの定義
    label =ft.Text("Flet 動作確認アプリ", size=24)
    text_field = ft.TextField(label="検索キー   を入力", value="001")
    result_text = ft.Text(value="ここに結果が表示されます。")
    fetch_button = ft.ElevatedButton(text="データを取得", on_click=on_click)
    ##GUIコンポーネントの配置
    page.add(label, text_field, fetch_button, result_text)

ft.app(target=main)