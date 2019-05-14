from os import mkdir
from os.path import expanduser, exists
from click import command, option, Path, echo
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from neaki import Neaki

download_folder = expanduser("~") + "/Downloads"

def init_driver():
    options = Options()
    options.add_argument('--headless')
    driver = Firefox(options=options)
    return driver

def path_exists(path):
    if not exists(path):
        mkdir(path)

@command()
@option('-p', '--path', 'path', default=download_folder, type=Path(exists=True))
def getmemes(path):
    driver = init_driver()
    neaki = Neaki(driver, path)

    if neaki.navigate():
        path_exists(path)
        downloaded_memes = [neaki.download_meme(url=url)
                            for url in neaki._get_meme_image()]
        echo(downloaded_memes)
    else:
        exit()


if __name__ == '__main__':
    getmemes()
