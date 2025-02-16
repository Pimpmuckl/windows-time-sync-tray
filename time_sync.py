import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QWidget
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QIcon
import threading
import ctypes

class TimeSyncApp(QWidget):
    def __init__(self):
        super().__init__()
        # Request admin privileges
        if not ctypes.windll.shell32.IsUserAnAdmin():
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            sys.exit()

        self.timer = QTimer()
        self.timer.timeout.connect(self.sync_time)
        self.sync_active = False
        
        self.setup_tray()

    def setup_tray(self):
        # Create system tray icon
        self.tray = QSystemTrayIcon(self)
        self.tray.setToolTip('Windows Time Sync')
        
        # Create right-click menu
        menu = QMenu()
        
        self.sync_now_action = menu.addAction('Resync Now')
        self.sync_now_action.triggered.connect(self.sync_time)
        
        self.start_action = menu.addAction('Start')
        self.start_action.triggered.connect(self.start_sync)
        
        self.stop_action = menu.addAction('Stop')
        self.stop_action.triggered.connect(self.stop_sync)
        self.stop_action.setEnabled(False)
        
        menu.addSeparator()
        
        exit_action = menu.addAction('Exit')
        exit_action.triggered.connect(self.close_app)
        
        # Set the menu
        self.tray.setContextMenu(menu)
        
        # Set a default icon (you may want to replace this with your own icon)
        self.tray.setIcon(QIcon('clock.ico'))
        self.tray.show()

    def sync_time(self):
        try:
            subprocess.run(['w32tm', '/resync', '/force'], 
                         check=True, 
                         capture_output=True,
                         creationflags=subprocess.CREATE_NO_WINDOW)
            self.tray.showMessage('Time Sync', 'Time synchronized successfully', 
                                QSystemTrayIcon.Information, 2000)
        except subprocess.CalledProcessError as e:
            self.tray.showMessage('Time Sync Error', f'Failed to sync time: {e}', 
                                QSystemTrayIcon.Critical, 2000)

    def start_sync(self):
        self.sync_active = True
        self.timer.start(60000)  # 60000 ms = 1 minute
        self.start_action.setEnabled(False)
        self.stop_action.setEnabled(True)
        self.tray.showMessage('Time Sync', 'Automatic sync started', 
                            QSystemTrayIcon.Information, 2000)

    def stop_sync(self):
        self.sync_active = False
        self.timer.stop()
        self.start_action.setEnabled(True)
        self.stop_action.setEnabled(False)
        self.tray.showMessage('Time Sync', 'Automatic sync stopped', 
                            QSystemTrayIcon.Information, 2000)

    def close_app(self):
        self.timer.stop()
        QApplication.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    window = TimeSyncApp()
    sys.exit(app.exec_())