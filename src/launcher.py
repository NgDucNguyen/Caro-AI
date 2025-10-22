import webview   # pip install pywebview
import sys, os, subprocess, traceback

HERE = os.path.abspath(os.path.dirname(__file__))

def resource_path(rel):
    """Return absolute path for a resource relative to this file."""
    return os.path.join(HERE, rel)

class LauncherApi:
    def start_game(self, mode, size, winlen):
        """
        Called from JS. Spawn new process to run ui.py with CLI args.
        """
        try:
            ui_py = resource_path('ui.py')
            if not os.path.exists(ui_py):
                return {'error': f"ui.py not found in {HERE}"}

            cmd = [sys.executable, ui_py, '--mode', mode, '--size', str(size), '--winlen', str(winlen)]

            # Spawn detached so child keeps running when launcher closes
            if os.name == 'nt':
                # Windows: detach using creationflags
                CREATE_NEW_PROCESS_GROUP = 0x00000200
                DETACHED_PROCESS = 0x00000008
                creationflags = CREATE_NEW_PROCESS_GROUP | DETACHED_PROCESS
                subprocess.Popen(cmd, cwd=HERE, creationflags=creationflags)
            else:
                # POSIX: start new session
                subprocess.Popen(cmd, cwd=HERE, start_new_session=True)

            return {'ok': True}
        except Exception as e:
            return {'error': str(e) + '\n' + traceback.format_exc()}

if __name__ == '__main__':
    # load external HTML
    html_path = resource_path(os.path.join('uiLauncher.html'))
    if not os.path.exists(html_path):
        html = "<html><body><h3>uiLauncher.html not found</h3><p>Put your launcher HTML at uiLauncher.html</p></body></html>"
    else:
        with open(html_path, 'r', encoding='utf-8') as f:
            html = f.read()

    api = LauncherApi()
    webview.create_window('Caro Launcher', html=html, js_api=api, width=420, height=360)
    # debug=True helps show logs in terminal if something goes wrong
    webview.start(debug=True)
