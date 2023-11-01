import os
class LatestVersion():
    def __init__(self):
        self.path = r'\\10.1.1.110\\arquivos\\atualizacoes\\MyCommerce'

        
    def latest_release_version(self):
        all_archives = os.listdir(self.path)
        # find by .exe files
        archives = [archive for archive in all_archives if archive.endswith('0.exe') if not archive.endswith('MyCommerce_Full.exe')]
        return archives[0]
    
    def latest_release_version_text(self):
        return self.text_strip(self.latest_release_version())
    
    def latest_build_version(self):
        all_archives = os.listdir(self.path)
        # find by .exe files
        archives = [archive for archive in all_archives if archive.endswith('.exe') if not archive.endswith('MyCommerce_Full.exe') if not archive.endswith('0.exe')]
        return archives[-1]
    
    def latest_build_version_text(self):
        return self.text_strip(self.latest_build_version())
    
    def text_strip(self, text):
        text = text.replace('.exe', '').replace('MyCommerce_Atu', '').replace(' ', '')
        return text
    
    def download_file(self, file_name):
        # copy file to downloads folder
        d = os.path.join(os.path.expanduser('~'), 'Downloads')
        download_folder = f""" "{d}" """
        print(download_folder)
        path = f""" "{self.path}\\{file_name}" """
        print(path)
        command = f'copy {path} {download_folder}'
        print(command)
        os.system(command)

        return 'sucess'
    
    def download_latest_build(self):
        return self.download_file(self.latest_build_version())
    
    def download_latest_release(self):
        return self.download_file(self.latest_release_version())
    
if __name__ == '__main__':
    print(LatestVersion().latest_release_version_text())