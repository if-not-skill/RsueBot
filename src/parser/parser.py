import requests
import json
from logging import getLogger
from bs4 import BeautifulSoup
from enum import Enum

log = getLogger('parser')


class Weekday(Enum):
    MONDAY = 0, "Понедельник"
    TUESDAY = 1, "Вторник"
    WEDNESDAY = 2, "Среда"
    THURSDAY = 3, "Четверг"
    FRIDAY = 4, "Пятница"
    SATURDAY = 5, "Суббота"
    SUNDAY = 6, "Воскресенье"

    @staticmethod
    def from_str(string: str):
        weekday: Weekday = Weekday.MONDAY

        if string == Weekday.TUESDAY.value[1]:
            weekday = Weekday.TUESDAY
        elif string == Weekday.WEDNESDAY.value[1]:
            weekday = Weekday.WEDNESDAY
        elif string == Weekday.THURSDAY.value[1]:
            weekday = Weekday.THURSDAY
        elif string == Weekday.FRIDAY.value[1]:
            weekday = Weekday.FRIDAY
        elif string == Weekday.SATURDAY.value[1]:
            weekday = Weekday.SATURDAY
        elif string == Weekday.SUNDAY.value[1]:
            weekday = Weekday.SUNDAY

        return weekday


class Week:
    def __init__(self, is_even):
        self.is_even: bool = is_even
        self.days = []

    def __str__(self):
        string = ''
        string += 'Четная неделя' if self.is_even else 'Нечетная неделя'
        string += '\n'
        for day in self.days:
            string += str(day) + '\n'
        return string


class Day:
    def __init__(self, weekday):
        self.weekday: Weekday = weekday
        self.lessons = []

    def __str__(self):
        string = ''
        string += self.weekday.value[1] + '\n'
        for lesson in self.lessons:
            string += str(lesson) + '\n'
        return string


class Lesson:
    def __init__(self):
        self.time = ''
        self.name = ''
        self.teacher = ''
        self.aud = ''
        self.l_type = ''

    def __str__(self):
        string = ''
        string += self.time + '\n'
        string += self.name + '\n'
        string += self.teacher + '\n'
        string += self.aud + '\n'
        string += self.l_type + '\n'
        return string


class Parser:
    def __init__(self, url, headers):
        self.__name = "Parser"
        self.__url = url
        self.__headers = headers

    async def start_parsing(self):
        log.info(f'[{self.__name}] Parsing {self.__url} started')
        
        try:
            # faculties = self.__parse_faculties()
            # for faculty in faculties:
            #     log.debug(faculty)
            #     faculty_id = faculty[0]
            #     courses = self.__parse_courses(faculty_id)
            #     for course in courses:
            #         log.debug(course)
            #         course_id = course[0]
            #         groups = self.__parse_groups(faculty_id, course_id)
            #         for group in groups:
            #             log.debug(group)

            self.__parse_timetable(1, 1, 1)

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
        soup = BeautifulSoup(response.text, 'html.parser')

        even = soup.find("h1", class_="ned").text == 'Четная неделя'
        weeks = [Week(even), Week(not even)]

        days = soup.find_all("div", class_="col-lg-2 col-md-2 col-sm-2")
        last_weekday = None
        week_index = 0
        for day in days:
            school_day = self.__parse_day(day)
            if school_day is None:
                continue

            if last_weekday is not None and school_day.weekday.value[0] <= last_weekday.value[0]:
                week_index += 1
            weeks[week_index].days.append(school_day)
            last_weekday = school_day.weekday

        for week in weeks:
            log.debug('\n' + str(week))

    @staticmethod
    def __parse_day(self, day):
        weekday = day.find("div", id="nedelya")
        if weekday is None:
            weekday = day.find("div", id="nedelya-select")

        if weekday is None:
            return None

        weekday = Weekday.from_str(weekday.text)
        result_day = Day(weekday)

        times = day.find_all("span", class_="time")
        lessons = day.find_all("span", class_="lesson")
        teachers = day.find_all("span", class_="prepod")
        types = day.find_all("span", class_="type n-type")
        auditoriums = day.find_all("span", class_="aud")[1::2]

        lesson_count = len(day.find_all("span", class_="time"))
        for i in range(lesson_count):
            lesson = Lesson()
            lesson.time = times[i].text
            lesson.name = lessons[i].text
            lesson.teacher = teachers[i].text
            lesson.aud = auditoriums[i].text
            lesson.l_type = types[i].text
            result_day.lessons.append(lesson)
        return result_day

    @staticmethod
    def __parse_select(select):
        items = select.find_all('option')
        container = []
        for item in items[1:]:
            container.append((item['value'], item.text))
        return container
