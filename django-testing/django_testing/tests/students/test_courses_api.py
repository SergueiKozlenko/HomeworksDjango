import pytest
from django.urls import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
import random


@pytest.mark.django_db
def test_course(api_client, course_factory, student_factory):
    """Тест получения 1го курса (retrieve-логика)."""

    student = student_factory(_quantity=2)
    course = course_factory(students=student)
    url = reverse('courses-detail', args=[course.id])

    resp = api_client.get(url)

    assert resp.status_code == HTTP_200_OK
    assert resp.json()['id'] == course.id


@pytest.mark.django_db
def test_courses_list(api_client, course_factory, student_factory):
    """Тест получения списка курсов (list-логика)."""

    students = student_factory(_quantity=3)
    courses = course_factory(students=students, _quantity=5)
    expected_ids_set = [course.id for course in courses]
    url = reverse('courses-list')

    resp = api_client.get(url)

    results_ids_set = [result['id'] for result in resp.json()]

    assert resp.status_code == HTTP_200_OK
    assert len(resp.json()) == 5
    assert results_ids_set == expected_ids_set


@pytest.mark.django_db
def test_courses_filter_by_id(api_client, course_factory, student_factory):
    """Тест фильтрации списка курсов по id."""

    students = student_factory(_quantity=3)
    courses = course_factory(students=students, _quantity=5)
    random_id = random.choice(courses).id
    url = reverse('courses-list')

    resp = api_client.get(url, {'id': random_id})

    assert resp.status_code == HTTP_200_OK
    assert resp.json()[0]
    assert resp.json()[0]['id'] == random_id


@pytest.mark.django_db
def test_courses_filter_by_name(api_client, course_factory, student_factory):
    """Тест фильтрации списка курсов по name."""

    students = student_factory(_quantity=3)
    courses = course_factory(students=students, _quantity=5)
    random_name = random.choice(courses).name
    url = reverse('courses-list')

    resp = api_client.get(url, {'name': random_name})

    assert resp.status_code == HTTP_200_OK
    assert resp.json()[0]
    assert resp.json()[0]['name'] == random_name


@pytest.mark.django_db
def test_course_create(api_client):
    """Тест успешного создания курса."""

    course_payload = {'name': 'test_course_created'}
    url = reverse('courses-list')

    resp = api_client.post(url, course_payload, format='json')
    resp_get = api_client.get(url, {'name': course_payload['name']})

    assert resp.status_code == HTTP_201_CREATED
    assert resp_get.json()[0]
    assert resp_get.json()[0]['name'] == course_payload['name']


@pytest.mark.django_db
def test_course_update(api_client, course_factory, student_factory):
    """Тест успешного обновления курса."""

    students = student_factory(_quantity=2)
    course_old = course_factory(students=students)
    course_new = course_factory(students=students)
    url = reverse('courses-detail', args=[course_old.id])

    resp = api_client.patch(url, {'name': course_new.name}, format='json')
    resp_get = api_client.get(url, {'id': course_old.id})

    assert resp.status_code == HTTP_200_OK
    assert resp.json()['id'] == course_old.id and resp.json()['name'] == course_new.name
    assert resp_get.json()['id'] == course_old.id and resp_get.json()['name'] == course_new.name


@pytest.mark.django_db
def test_course_delete(api_client, course_factory, student_factory):
    """Тест успешного удаления курса."""

    students = student_factory(_quantity=3)
    courses = course_factory(students=students, _quantity=5)
    random_id = random.choice(courses).id
    url = reverse('courses-detail', args=[random_id])
    url_get = reverse('courses-list')

    resp = api_client.delete(url)
    resp_get = api_client.get(url_get)

    existed_ids = [course['id'] for course in resp_get.json()]

    assert resp.status_code == HTTP_204_NO_CONTENT
    assert random_id not in existed_ids
