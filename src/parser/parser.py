import requests
from logging import getLogger
from bs4 import BeautifulSoup

log = getLogger('parser')


class Parser:
    def __init__(self, url, headers):
        self.__name = "Parser"
        self.__url = url
        self.__headers = headers

    async def start_parsing(self):
        log.info(f'[{self.__name}] Parsing {self.__url} started')

        try:
            faculties = self.__parse_faculties()
            for faculty in faculties:
                log.debug(faculty)
        except Exception as ex:
            log.critical(f'[{self.__name}] parse exception: {ex}')

        log.info(f'[{self.__name}] Parsing ended')

    def __parse_faculties(self):
        r = requests.get(url=self.__url, headers=self.__headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        soup = soup.find_all('select')[0]
        return self.__parse_select(soup)

    def __parse_timetable(self, faculty_id, course_id, group_id):
        response = requests.post(
            url=self.__url,
            data={
                "f": faculty_id,
                "k": course_id,
                "g": group_id
            },
            headers=self.__headers)
        print(response.text)

    @staticmethod
    def __parse_select(select):
        items = select.find_all('option')
        container = []
        for item in items[1:]:
            container.append((item['value'], item.text))
        return container
