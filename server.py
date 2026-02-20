from flask import Flask, jsonify, request
from flask_cors import CORS
import win32gui
import win32con
import win32api
import time

app = Flask(__name__)
CORS(app)

MONITOR_CENTER_X = 960
MONITOR_CENTER_Y = 540

def find_window_by_keyword(keyword):
    result = []
    def callback(hwnd, _):
        title = win32gui.GetWindowText(hwnd)
        if keyword.lower() in title.lower():
            result.append(hwnd)
    win32gui.EnumWindows(callback, None)
    return result[0] if result else None

def focus_window(hwnd):
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    time.sleep(0.2)
    win32api.keybd_event(win32con.VK_MENU, 0, 0, 0)
    win32gui.SetForegroundWindow(hwnd)
    win32api.keybd_event(win32con.VK_MENU, 0, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(0.5)

def mouse_move_and_click(x, y):
    """마우스 이동 후 좌클릭"""
    win32api.SetCursorPos((x, y))
    time.sleep(0.2)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

@app.route('/ping')
def ping():
    return 'pong'

@app.route('/click')
def click():
    """
    기본: 화면 중앙으로 이동 후 클릭
    옵션: /click?x=960&y=540 으로 좌표 지정 가능
    """
    hwnd = find_window_by_keyword('Lineage Classic')
    if not hwnd:
        return jsonify({'status': 'error', 'message': 'Lineage Classic not found'}), 400

    focus_window(hwnd)

    x = int(request.args.get('x', MONITOR_CENTER_X))
    y = int(request.args.get('y', MONITOR_CENTER_Y))

    mouse_move_and_click(x, y)

    return jsonify({'status': 'ok', 'message': f'Clicked at ({x}, {y})'})

if __name__ == '__main__':
    print("Server started! http://localhost:5000")
    app.run(port=5000)
