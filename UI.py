# StepPet for M5Stack Core2 (MicroPython / UIFlow2)
# 修正版：インデント統一、UIFlow互換ラッパ導入

import json, os, math, time

try:
    from m5stack import lcd
except Exception:
    import lcd

try:
    from m5stack import imu as _imu
    imu = _imu.IMU()
except Exception:
    try:
        from imu import IMU
        imu = IMU()
    except Exception:
        imu = None

try:
    from m5stack import touch as _touch
    HAS_TOUCH = True
except Exception:
    HAS_TOUCH = False

# ---- 定数 ----
SCR_LOGIN, SCR_MENU, SCR_SETTINGS, SCR_ZUKAN, SCR_CHAR_PROFILE, SCR_STEPS, SCR_RESULT_UP, SCR_RESULT_DOWN = range(8)
STATE = SCR_LOGIN
DATA_FILE = '/flash/steppet.json'

# ---- 初期データ ----
def _empty_data():
    return {
        'user': {'name': '', 'age': 0, 'bMonth': 1, 'bDay': 1, 'password': ''},
        'week': {'daily': [0]*7, 'goalPerDay': 3000, 'level': 1, 'eggType': 0, 'inited': False, 'lastWday': None}
    }

def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return _empty_data()

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

data = load_data()

# ---- 互換ラッパ ----
def fill_roundrect(x,y,w,h,r,color):
    try:
        lcd.roundrect(x,y,w,h,r,color,color)
    except Exception:
        lcd.rect(x,y,w,h,color,color)

def fill_triangle(x0,y0,x1,y1,x2,y2,color):
    try:
        lcd.fillTriangle(x0,y0,x1,y1,x2,y2,color)
    except Exception:
        try:
            lcd.triangle(x0,y0,x1,y1,x2,y2,color)
        except Exception:
            pass

def get_touch():
    if not HAS_TOUCH:
        return None
    try:
        p = _touch.read()
        if p:
            return p[0], p[1]
    except Exception:
        try:
            arr = _touch.get_touches()
            if arr and len(arr)>0:
                return arr[0][0], arr[0][1]
        except Exception:
            pass
    return None

# ---- 画面ヘルパ ----
DAYS = '月火水木金土日'
W, H = 320, 240
lcd.clear(lcd.BLACK)
lcd.font(lcd.FONT_DejaVu18)

def header(t):
    lcd.rect(0,0,W,24,lcd.WHITE,lcd.BLACK)
    lcd.print(t,8,4,lcd.WHITE)

def draw_btn(x,y,w,h,label):
    lcd.roundrect(x,y,w,h,8,lcd.WHITE)
    tw = lcd.textWidth(label)
    lcd.print(label,x+(w-tw)//2,y+(h-20)//2,lcd.WHITE)

def in_rect(x,y,rx,ry,rw,rh):
    return rx<=x<rx+rw and ry<=y<ry+rh

# ---- 画面描画関数 ----
def draw_login():
    lcd.clear(lcd.BLACK)
    header('一番最初の設定')
    lcd.roundrect(12,36,296,160,12,lcd.WHITE)
    lcd.print('なまえ / パスワード を入力',20,70,lcd.WHITE)
    draw_btn(20,60,120,40,'なまえ:A')
    draw_btn(20,110,120,40,'ﾊﾟｽ:1111')
    draw_btn(180,180,120,40,'OK')

def draw_menu():
    lcd.clear(lcd.BLACK)
    header('選択画面')
    lcd.fillCircle(65,105,40,lcd.BLUE)
    lcd.print('ほすう',45,95,lcd.WHITE)
    fill_triangle(160,30,210,120,110,120,lcd.GREEN)
    lcd.print('ずかん',140,95,lcd.WHITE)
    fill_roundrect(210,60,90,90,12,lcd.MAGENTA)
    lcd.print('せってい',225,95,lcd.WHITE)

def draw_settings():
    lcd.clear(lcd.BLACK)
    header('設定')
    u=data['user']
    lcd.print('ねんれい:%dさい'%u['age'],20,40,lcd.WHITE)
    lcd.print('たんじょうび:%d月%d日'%(u['bMonth'],u['bDay']),20,60,lcd.WHITE)
    for (x,y,lbl) in [(30,70,'年齢+'),(100,70,'年齢-'),(30,120,'月+'),(100,120,'月-'),(170,120,'日+'),(240,120,'日-')]:
        draw_btn(x,y,60,40,lbl)
    draw_btn(10,190,100,40,'< 戻る')

def draw_steps():
    lcd.clear(lcd.BLACK)
    header('歩数')
    wk=data['week']
    lcd.print('今日:%d歩'%wk['daily'][time.localtime()[6]],16,70,lcd.WHITE)
    lcd.print('目標:%d歩'%wk['goalPerDay'],16,95,lcd.WHITE)
    draw_btn(10,190,90,40,'+10歩')
    draw_btn(110,190,90,40,'目標+')
    draw_btn(210,190,90,40,'目標-')
    draw_btn(10,140,100,40,'< 戻る')

# ---- メインループ ----
STATE = SCR_LOGIN if not data['user']['name'] else SCR_MENU
if STATE==SCR_LOGIN:
    draw_login()
else:
    draw_menu()

while True:
    p=get_touch()
    if not p:
        time.sleep(0.1)
        continue
    x,y=p
    if STATE==SCR_LOGIN and in_rect(x,y,180,180,120,40):
        data['user']['name']='たろう'
        STATE=SCR_MENU
        draw_menu()
    elif STATE==SCR_MENU and x<110:
        STATE=SCR_STEPS
        draw_steps()
    elif STATE==SCR_STEPS and in_rect(x,y,10,140,100,40):
        STATE=SCR_MENU
        draw_menu()
    time.sleep(0.1)