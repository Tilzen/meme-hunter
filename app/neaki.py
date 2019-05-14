from datetime import datetime
from requests import get
from shutil import copyfileobj


class Neaki:
    def __init__(self, driver, path):
        self.driver = driver
        self.path = path
        self.message = ''
        self.url = 'http://naoentreaki.com.br'
        self.meme_url = '/html/body/div[2]/div[3]/div[1]/div[1]/article[1]/p/span/a/img'
        self.btn_arribas = '/html/body/div[2]/div[3]/div[1]/div[1]/article[1]/div[3]/a[1]'
        self.btn_muertes = '/html/body/div[2]/div[3]/div[1]/div[1]/article[1]/div[3]/a[2]'

    def navigate(self) -> bool:
        """
        Performs the navigation to the site informed by the url.
        """
        try:
            self.driver.get(self.url)
            return True
        except Exception as ex:
            self.message = ex
            return False

    @staticmethod
    def _save_binary(name: str, url: str, path: str, *, type_: str='jpeg') -> str:
        """
        Save image binaries from your urls.
        param: name
            - receives a name for the file.
        param: url
            - receives the url where the image is located to request it.
        param: path
            - receives the location where the binary will be allocated on
              the computer.
        param: type_
            - receives the extension of the binary to be downloaded.
        return:
            - returns the location where the file was saved.
        """
        response = get(url, stream=True)
        file_name = f'{path}/{name}.{type_}'
        #import ipdb; ipdb.set_trace()

        with open(file_name, 'wb') as file:
            copyfileobj(response.raw, file)
        return file_name

    @staticmethod
    def _format_votes(votes: str) -> int:
        """
        Performs the formatting of user evaluations.
        """
        votes = [vote.text for vote in votes]
        votes = [vote.replace('.', '') for vote in votes]
        votes = list(map(int, votes))
        return votes

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

    def _get_arribas_muertes(self) -> int:
        """
        Return the amount of arribes and muertes from the memes.
        """
        arribas = self.driver.find_elements_by_xpath(self.btn_arribas)
        muertes = self.driver.find_elements_by_xpath(self.btn_muertes)
        arribas = self._format_votes(arribas)
        muertes = self._format_votes(muertes)
        return arribas, muertes

    def _get_meme_image(self):
        """
        Return the url from meme image.
        """
        images_urls = self.driver.find_elements_by_xpath(self.meme_url)
        return [image_url.get_attribute('src') for image_url in images_urls]

    def download_meme(self, url: str) -> bool:
        """
        Downloads the meme after checking that it is rated as good.
        param: url
            - receives the url where the image is located to request it.
        return:
            - returns a boolean value informing if the meme was
              downloaded or not.
        """
        name = 'neaki-' + str(datetime.date(datetime.now()))
        self.driver.implicitly_wait(5)
        arribas, muertes = self._get_arribas_muertes()

        for arriba, muerte in zip(arribas, muertes):
            if self._is_good_meme(arriba, muerte):
                print(self._save_binary(name, url, self.path))
                return True
            return False
