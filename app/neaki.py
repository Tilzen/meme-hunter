from requests import get
from selenium.webdriver import Firefox
from shutil import copyfileobj


class Neaki:
    def __init__(self, driver, path):
        self.driver = driver
        self.path = path
        self.url = 'http://naoentreaki.com.br'
        self.btn_arribas = ('/html/body/div[2]/div[3]/'
                            'div[1]/div[1]/article[1]/div[3]/a[1]')
        self.btn_muertes = ('/html/body/div[2]/div[3]/'
                           'div[1]/div[1]/article[1]/div[3]/a[2]')

    def navigate(self) -> bool:
        """
        Performs the navigation to the site informed by the url.
        """
        try:
            self.driver.get(self.url)
            return True
        except Exception as ex:
            return False

    def get_arribas_muertes(self) -> int:
        """
        Return the amount of arribes and muertes from the memes.
        """
        arribas = self.driver.find_elements_by_xpath(self.btn_arribas).text
        muertes = self.driver.find_elements_by_xpath(self.btn_muertes).text
        arribas = format_votes(arribas)
        muertes = format_votes(muertes)
        return arribas, muertes

    def _is_good_meme(self, arribas: int, muertes: int) -> bool:
        """
        Checks if a meme is good based on user ratings.
        param: arribas
            - receives an integer number of positive reviews from the meme.
        param: muertes
            - receives an integer number of negative evaluations from the meme.
        return:
            - returns a boolean value indicating if it is a good meme.
        """
        return arribas > 300 and arribas > muertes

    def download_meme(self, name: str, url: str) -> bool:
        """
        Downloads the meme after checking that it is rated as good.
        param: name
            - receives a name for the file.
        param: url
            - receives the url where the image is located to request it.
        return:
            Returns a boolean value informing if the meme was downloaded or not.
        """

        arribas, muertes = self.get_arribas_muertes()
        if self._is_good_meme(arribas, muertes):
            save_binary(name, url)
            return True
        return False

    @staticmethod
    def _save_binary(name: str, url: str, *, path: str=self.path, type_: str='png') -> str:
        """
        Save image binaries from your urls.
        param: name
            - receives a name for the file.
        param: url
            - receives the url where the image is located to request it.
        param: path
            - receives the location where the binary will be allocated on the computer.
        param: type_
            - receives the extension of the binary to be downloaded.
        return:
            - returns the location where the file was saved.
        """
        response = get(url, stream=True)
        file_name = f'{path}/{name}.{type_}'

        with open(file_name) as file:
            copyfileobj(response.raw, file)
        return file_name

    @staticmethod
    def _format_votes(vote: str) -> int:
        """
        Performs the formatting of user evaluations.
        """
        vote = vote.replace('.', '')
        vote = int(vote)
        return vote
