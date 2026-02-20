from flask import Flask, jsonify, request
from flask_cors import CORS
import win32gui
import win32con
import win32api
import ctypes
import time

app = Flask(__name__)
CORS(app)

MONITOR_CENTER_X = 960
MONITOR_CENTER_Y = 540

def find_window_by_keyword(keyword):
    result = []
    def callback(hwnd, _):
        try:
            title = win32gui.GetWindowText(hwnd)
            if keyword.lower() in title.lower():
                result.append(hwnd)
        except:
            pass
    win32gui.EnumWindows(callback, None)
    return result[0] if result else None

def focus_window(hwnd):
    try:
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        time.sleep(0.2)
        win32api.keybd_event(win32con.VK_MENU, 0, 0, 0)
        win32gui.SetForegroundWindow(hwnd)
        win32api.keybd_event(win32con.VK_MENU, 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(0.5)
        print("[DEBUG] focus_window OK")
    except Exception as e:
        print(f"[DEBUG] focus_window error (ignored): {e}")

def move_mouse(x, y):
    """ctypes로 마우스 이동만 (클릭 없음)"""
    screen_w = ctypes.windll.user32.GetSystemMetrics(0)
    screen_h = ctypes.windll.user32.GetSystemMetrics(1)
    nx = int(x * 65535 / screen_w)
    ny = int(y * 65535 / screen_h)
    ctypes.windll.user32.mouse_event(0x0001 | 0x8000, nx, ny, 0, 0)

@app.route('/ping')
def ping():
    return 'pong'

@app.route('/move')
def move():
    try:
        x = int(request.args.get('x', MONITOR_CENTER_X))
        y = int(request.args.get('y', MONITOR_CENTER_Y))
        print(f"[DEBUG] /move called x={x}, y={y}")

        hwnd = find_window_by_keyword('Lineage Classic')
        if not hwnd:
            print("[DEBUG] Lineage window NOT found")
            return jsonify({'status': 'error', 'message': 'Lineage Classic not found'}), 400

        focus_window(hwnd)

        print(f"[DEBUG] Moving mouse to ({x}, {y})")
        move_mouse(x, y)

        print("[DEBUG] Done!")
        return jsonify({'status': 'ok', 'message': f'Moved to ({x}, {y})'})

    except Exception as e:
        print(f"[DEBUG] Exception: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    print("Server started! http://localhost:5000")
    app.run(port=5000)
