from flask import Flask, jsonify
from flask_cors import CORS
import pyautogui
import pygetwindow as gw
import time

app = Flask(__name__)
CORS(app)

def focus_notepad():
    """열려있는 메모장 창을 찾아 포커스"""
    # 메모장 창 찾기 (한글/영문 모두 대응)
    windows = gw.getWindowsWithTitle('메모장') or gw.getWindowsWithTitle('Notepad')
    
    if not windows:
        return False, '메모장을 찾을 수 없습니다. 먼저 메모장을 열어주세요.'
    
    win = windows[0]
    
    # 최소화 되어있으면 복원
    if win.isMinimized:
        win.restore()
        time.sleep(0.3)
    
    # 창 앞으로 가져오기 + 포커스
    win.activate()
    time.sleep(0.4)  # 포커스 전환 대기
    
    return True, win.title

@app.route('/ping')
def ping():
    return 'pong'

@app.route('/type/abc')
def type_abc():
    success, msg = focus_notepad()
    
    if not success:
        return jsonify({'status': 'error', 'message': msg}), 400
    
    pyautogui.typewrite('abc', interval=0.1)
    return jsonify({'status': 'ok', 'message': f'"{msg}" 에 abc 입력 완료'})

if __name__ == '__main__':
    print("✅ 서버 시작! http://localhost:5000")
    print("메모장을 열어두고 웹페이지에서 버튼을 눌러보세요.")
    app.run(port=5000)
