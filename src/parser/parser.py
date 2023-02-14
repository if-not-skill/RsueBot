import requests
import json
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
                faculty_id = faculty[0]
                courses = self.__parse_courses(faculty_id)
                for course in courses:
                    log.debug(course)
                    course_id = course[0]
                    groups = self.__parse_groups(faculty_id, course_id)
                    for group in groups:
                        log.debug(group)

            # self.__parse_timetable(1, 1, 1)

        except Exception as ex:
            log.critical(f'[{self.__name}] parse exception: {ex}')

        log.info(f'[{self.__name}] Parsing ended')

    def __parse_faculties(self):
        r = requests.get(url=self.__url, headers=self.__headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        soup = soup.find_all('select')[0]
        return self.__parse_select(soup)

    def __parse_courses(self, faculty_id):
        r = requests.post(
            url=self.__url + "query.php",
            data={
                "query": "getKinds",
                "type_id": faculty_id
            },
            headers=self.__headers)
        courses = []
        for keys in json.loads(r.text):
            courses.append((keys['kind_id'], keys['kind']))
        return courses

    def __parse_groups(self, faculty_id, course_id):
        r = requests.post(
            url=self.__url + "query.php",
            data={
                "query": "getCategories",
                "type_id": faculty_id,
                "kind_id": course_id
            },
            headers=self.__headers)
        groups = []
        for keys in json.loads(r.text):
            groups.append((keys['category_id'], keys['category']))
        return groups

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
