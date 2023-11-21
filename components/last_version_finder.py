import os
import sys
path = os.path.abspath('./')
sys.path.append(path)
from components.os_handle import OsHandler

class LatestVersion():
    def __init__(self):
        self.path_mycommerce_att = r'\\10.1.1.110\\arquivos\\atualizacoes\\MyCommerce'
        
    def latest_release_version(self):
        all_archives = os.listdir(self.path_mycommerce_att)
        # find by .exe files
        archives = [archive for archive in all_archives if archive.endswith('0.exe') if not archive.endswith('MyCommerce_Full.exe')]
        if len(archives) >1:
            return archives[-1]
        elif len(archives) == 1:
            return archives[0]
    
    def latest_release_version_text(self):
        return self.text_strip(self.latest_release_version())
    
    def latest_build_version(self):
        all_archives = os.listdir(self.path_mycommerce_att)
        # find by .exe files
        archives = [archive for archive in all_archives if archive.endswith('.exe') if not archive.endswith('MyCommerce_Full.exe') if not archive.endswith('0.exe')]
        if archives:
            return archives[-1]
        else:
            return 'SemBuild'
    
    def latest_build_version_text(self):
        if self.latest_build_version() == 'SemBuild':
            return 'SemBuild'
        else:
            return self.text_strip(self.latest_build_version())
    
    def text_strip(self, text):
        text = text.replace('.exe', '').replace('MyCommerce_Atu', '').replace(' ', '')
        return text
    
    def download_file(self, file_name):
        OsHandler().download_version(self.path_mycommerce_att, file_name)
        return 'sucess'
    
    def download_latest_build(self):
        build = self.latest_build_version() 
        if build == 'SemBuild':
            return 'SemBuild'
        else:
            return self.download_file(build)
    
    def download_latest_release(self):
        return self.download_file(self.latest_release_version())

    
if __name__ == '__main__':
    print(LatestVersion().latest_release_version())
    

