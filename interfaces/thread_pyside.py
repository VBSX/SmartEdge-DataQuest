from PySide6.QtCore import QThread,Signal
from components.last_version_finder import LatestVersion
from components.automation_windows.create_post import BrowserController

class DownloadThread(QThread):
    download_finished = Signal()
    download_cancelled = Signal(bool)
    def __init__(
        self,
        is_build= None,
        thread_create_post = False,
        message = None,
        bitrix_username = None,
        bitrix_password = None,
        forum_username = None,
        forum_password = None,
        final_version = None,
        topic_name_of_final_version = None,
        **argumentos_nomeados
        ):
        super().__init__()
        self.is_build = is_build
        self.thread_create_post = thread_create_post
        self.message = message
        self.bitrix_username = bitrix_username
        self.bitrix_password = bitrix_password
        self.forum_username = forum_username
        self.forum_password = forum_password
        self.is_final_version = final_version
        self.topic_name_of_final_version = topic_name_of_final_version
        self.download = LatestVersion()
        self.canceled = False

    def run(self):
        if self.is_build:
            self.download.download_latest_build()
        elif self.thread_create_post:
            BrowserController(
                message_version=self.message,
                bitrix_username=self.bitrix_username,
                bitrix_passwd=self.bitrix_password,
                forum_username=self.forum_username,
                forum_passwd=self.forum_password,
                final_version=self.is_final_version,
                topic_name_of_final_version=self.topic_name_of_final_version
                )   
            print('thread finished')     
        else:
            self.download.download_latest_release()
        if not self.canceled:
            self.download_finished.emit()
    
    def cancel(self):
        self.canceled = True
        self.download.cancel_download()
        self.terminate()
        self.wait()
        print('thread canceled')
        self.download_cancelled.emit(True)