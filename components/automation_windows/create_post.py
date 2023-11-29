from time import sleep
from pywinauto.application import Application
from pywinauto import Desktop


# tab_forum = 'Visual Software - Fórum - Histórico de Versão'
tab_forum = u'Visual Software - Fórum - Histórico de Versão'

def open_brave_browser():
    # Caminho para o executável do Brave Browser
    brave_path = r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe'
    url = 'https://forum.visualsoftware.inf.br/forumdisplay.php?fid=30'
    chrome = Application(backend='uia')
    chrome.start(brave_path + ' --force-renderer-accessibility --start-maximized ' + url)
    # show the elements of the page
    chrome[tab_forum].print_control_identifiers()
    # chrome[tab_forum].child_window(title_re='Reload.*', control_type='Button').wait('visible', timeout=10)
    
    return chrome

def main():
    app = open_brave_browser()
    if app:
        print("A aplicação do Brave Browser foi aberta com sucesso.")
    else:
        print("A aplicação do Brave Browser não foi aberta.")
        
if __name__ == "__main__":
    main()
