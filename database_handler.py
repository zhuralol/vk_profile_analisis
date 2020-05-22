import sqlite3


def vk_request():
    # answer = {}
    # answer = {'id': 4129223, 'first_name': 'Алексей', 'last_name': 'Николаев', 'is_closed': False, 'can_access_closed': True, 'city': {'id': 1, 'title': 'Москва'}, 'photo_100': 'https://sun9-18.userapi.com/c854024/v854024461/ecd73/ffYDQaQKjcw.jpg?ava=1', 'online': 0, 'origin': 4532077}
    answer = {'id': 12437923, 'first_name': 'Владимир', 'last_name': 'Журавлёв', 'country':'Russia', 'is_closed': False, 'can_access_closed': True, 'sex': 2, 'bdate': '4.10', 'city': {'id': 1, 'title': 'Москва'}, 'photo_400': 'https://sun9-26.userapi.com/c848524/v848524775/82499/6THfWbMBfSE.jpg?ava=1', 'mobile_phone': '12345 mobile', 'home_phone': '12345 additional', 'last_seen': {'time': 1589126887, 'platform': 7}, 'career': [], 'military': [], 'university': 0, 'university_name': '', 'faculty': 0, 'faculty_name': '', 'graduation': 0, 'relation': 0, 'personal': {'political': 2, 'langs': ['Русский', 'English', 'Español'], 'religion': 'Дискордианство', 'people_main': 0, 'life_main': 0, 'smoking': 0, 'alcohol': 0}, 'interests': 'Человеческое общество', 'activities': 'Освобождение венгров', 'universities': [], 'schools': [{'id': '1231', 'country': 1, 'city': 1, 'name': 'Школа № 220'}, {'id': '3709', 'country': 1, 'city': 1, 'name': 'Школа № 155'}, {'id': '5083', 'country': 1, 'city': 1, 'name': 'Лицей № 1550', 'type': 2, 'type_str': 'Лицей'}], 'about': '', 'relatives': []}
    return answer


conn = sqlite3.connect(':memory:')

c = conn.cursor()

fields = ['id', 'first_name', 'last_name', 'is_closed', 'bdate', 'photo_400', 'about', 'activities', 'career',
                  'city', 'connections', 'contacts', 'education', 'exports', 'interests', 'last_seen', 'military',
                  'personal', 'relatives', 'relation', 'schools', 'sex', 'universities']
# id, first_name, last_name, is_closed, bdate, photo_400, about, activities, career,
#                   city, connections, contacts, education, exports, interests, last_seen, military,
#                   personal, relatives, relation, schools, sex, universities

c.execute("""
        CREATE TABLE Users (
        id INTEGER PRIMARY KEY ON CONFLICT IGNORE,
        first_name TEXT,
        last_name TEXT,
        city INTEGER,
        country INTEGER,
        sex INTEGER,
        bdate INTEGER,
        photo_400 TEXT,
        relation INTEGER,
        religion INTEGER,
        political INTEGER,
        peopleMain INTEGER,
        lifeMain INTEGER,
        smoking INTEGER,
        alcohol INTEGER,
        favorite BOOLEAN DEFAULT 0,
        inaccurateAge BOOLEAN DEFAULT 0,
        groupId INTEGER,
        openMessages INTEGER,
        countryId INTEGER
        )
        """)

class User:
    """A sample Employee class"""
    args = ['id', 'first_name', 'last_name', 'is_closed', 'bdate', 'photo_400', 'about', 'activities', 'career',
                  'city', 'connections', 'contacts', 'education', 'exports', 'interests', 'last_seen', 'military',
                  'personal', 'relatives', 'relation', 'schools', 'sex', 'universities']
    def __init__(self, *args):
        for arg in args:
            self.arg = arg


def insert_emp(emp):
    with conn:
        c.execute("INSERT INTO employees VALUES (:first, :last, :pay)", {'first': emp.first, 'last': emp.last, 'pay': emp.pay})


def get_emps_by_name(lastname):
    c.execute("SELECT * FROM employees WHERE last=:last", {'last': lastname})
    return c.fetchall()


def update_pay(emp, pay):
    with conn:
        c.execute("""UPDATE employees SET pay = :pay
                    WHERE first = :first AND last = :last""",
                  {'first': emp.first, 'last': emp.last, 'pay': pay})


def remove_emp(emp):
    with conn:
        c.execute("DELETE from employees WHERE first = :first AND last = :last",
                  {'first': emp.first, 'last': emp.last})

# emp_1 = Employee('John', 'Doe', 80000)
# emp_2 = Employee('Jane', 'Doe', 90000)

insert_emp(emp_1)
insert_emp(emp_2)

emps = get_emps_by_name('Doe')
print(emps)

update_pay(emp_2, 95000)
remove_emp(emp_1)

emps = get_emps_by_name('Doe')
print(emps)

conn.close()