import pytest
from rest_framework.reverse import reverse
from students.models import Course


@pytest.mark.django_db
def test_one_course(client, course_factory, student_factory):
    students = student_factory(_quantity=10)
    course = course_factory(students=students)
    url = reverse(f'courses-detail', kwargs={'pk': course.id})
    response = client.get(url)

    assert response.status_code == 200

    data = response.json()

    assert data['name'] == course.name

    for i, j in enumerate(data['students']):
        assert j == course.students.all()[i].id


@pytest.mark.django_db
def test_all_course(client, course_factory, student_factory):
    students = student_factory(_quantity=10)
    courses = course_factory(_quantity=5, students=students)
    url = reverse(f'courses-list')
    response = client.get(url)

    assert response.status_code == 200

    data = response.json()

    assert len(data) == len(courses)

    for i, j in enumerate(data):
        assert j['name'] == courses[i].name
        for a, b in enumerate(j['students']):
            assert b == courses[i].students.all()[a].id


@pytest.mark.django_db
def test_filter_course_id(client, course_factory, student_factory):
    students = student_factory(_quantity=10)
    courses = course_factory(_quantity=5, students=students)
    url = reverse(f'courses-list') + f'?id={courses[1].id}'
    response = client.get(url)

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1

    assert data[0]['name'] == courses[1].name


@pytest.mark.django_db
def test_filter_course_name(client, course_factory, student_factory):
    students = student_factory(_quantity=10)
    courses = course_factory(_quantity=5, students=students)
    url = reverse(f'courses-list') + f'?name={courses[2].name}'
    response = client.get(url)

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1

    assert data[0]['name'] == courses[2].name


@pytest.mark.django_db
def test_create_course(client):
    url = '/api/v1/courses/'
    count = Course.objects.count()
    response = client.post(url, data={'name': 'course_1'})

    assert response.status_code == 201

    assert Course.objects.count() == count + 1

    assert response.json()['name'] == 'course_1'


@pytest.mark.django_db
def test_update_course(client, course_factory, student_factory):
    students = student_factory(_quantity=10)
    course = course_factory(students=students)
    url = '/api/v1/courses/' + f'{course.id}/'

    response = client.patch(url, data={'name': 'course_2'})

    assert response.status_code == 200

    assert response.json()['name'] == 'course_2'


@pytest.mark.django_db
def test_delete_course(client, course_factory, student_factory):
    students = student_factory(_quantity=10)
    course = course_factory(students=students)
    url = '/api/v1/courses/' + f'{course.id}/'

    response = client.delete(url)

    assert response.status_code == 204

    assert Course.objects.filter(id=course.id).count() == 0
