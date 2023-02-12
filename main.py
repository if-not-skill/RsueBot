import requests
from bs4 import BeautifulSoup


url = 'https://rsue.ru/raspisanie/'


def parse_select(select):
    items = select.find_all('option')
    container = []
    for item in items[1:]:
        container.append((item['value'], item.text))
    return container


def get_faculties():
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    soup = soup.find_all('select')[0]
    return parse_select(soup)


def parse_timetable(faculty_id, course_id, group_id):
    response = requests.post(url, data={
        "f": faculty_id,
        "k": course_id,
        "g": group_id
    })
    print(response.text)


faculties = get_faculties()
for faculty in faculties:
    print(faculty)

parse_timetable(3, 1, 6)


