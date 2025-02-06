from PySide6.QtCore import QThread,Signal
from components.last_version_finder import LatestVersion
from components.automation_windows.create_post import BrowserController

class DownloadThread(QThread):
    download_finished = Signal()
    download_cancelled = Signal(bool)
    error = Signal(bool)
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
        name_of_program = None,
        specific_version = None,
        **argumentos_nomeados
        ):
        super().__init__()
        self.is_build = is_build
        self.thread_create_post = thread_create_post
        self.message = message
        self.bitrix_username = bitrix_username
        self.bitrix_password = bitrix_password
        self.name_of_program = name_of_program
        self.forum_username = forum_username
        self.forum_password = forum_password
        self.is_final_version = final_version
        self.topic_name_of_final_version = topic_name_of_final_version
        self.download = LatestVersion()
        self.canceled = False
        self.msg_error = None
        self.specific_version = specific_version

    def run(self):
        if self.is_build == None:
            self.specific_version_finished = self.download.download_by_version(str(self.specific_version))
        elif self.is_build:
            self.download.download_latest_build()
        elif self.thread_create_post:
            browser_return = BrowserController(
                message_version=self.message,
                forum_username=self.forum_username,
                forum_passwd=self.forum_password,
                bitrix_username=self.bitrix_username,
                bitrix_passwd=self.bitrix_password,
                # test_mode=True,
                # test_forum=True,
                final_version=self.is_final_version,
                topic_name_of_final_version=self.topic_name_of_final_version,
                name_of_program=self.name_of_program,   
            )
            
            # if browser_return[0] == 'Error':
            #     self.msg_error = browser_return[1]
        else:
            self.download.download_latest_release()
        print('thread finished')
        if not self.canceled:
            if not self.msg_error:
                self.download_finished.emit()
            else:
                self.error.emit(True)
    
    def cancel(self):
        self.canceled = True
        self.download.cancel_download()
        self.terminate()
        self.wait()
        print('thread canceled')
        self.download_cancelled.emit(True)
    
    