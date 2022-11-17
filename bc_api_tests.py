"""API tests"""
import unittest
import datetime
import json
import requests

BASE_URL = 'https://reqres.in'
BASE_TIMEOUT = 5
USER_ID = 5
USER_ID_BAD = 23
NEL_DIC = {"success_fraction": 0, "report_to": "cf-nel", "max_age": 604800}
USER_JSON = {'name': 'Ivan', 'job': 'leader'}
USER_JSON_MOD = {'name': 'Peter', 'job': 'NOTleader'}
USER_NEW_JSON = {"email": "eve.holt@reqres.in", "password": "pistol"}
USER_NEW_RESP_JSON = {"id": 4, "token": "QpwL5tke4Pnpja7X4"}
INVALID_REGISTRATION = [
    {
        'body': {"email": "", "password": ""},
        'error': 'Missing email or username'
    },
    {
        'body': {"email": "eve.holt@reqres.in", "password": ""},
        'error': 'Missing password'
    },
    {
        'body': {"email": "1", "password": "1"},
        'error': 'Note: Only defined users succeed registration'
    },
    {
        'body': {"email": "", "password": "pistol"},
        'error': 'Missing email or username'
    }
]


class TestsAPI(unittest.TestCase):
    """API test suit"""

    def test_get_users_list(self) -> None:
        """Test of GET:/api/users-LIST USERS"""
        response = requests.get(f'{BASE_URL}/api/users', timeout=BASE_TIMEOUT)
        lists_value = response.json()['total'] / response.json()['per_page']
        print(len(response.json()['data']))
        self.assertEqual(200, response.status_code)
        self.assertEqual('application/json; charset=utf-8', response.headers['Content-Type'])
        self.assertDictEqual(NEL_DIC, json.loads(response.headers['NEL']))
        self.assertGreater(response.json()['total'], 0)
        self.assertEqual(lists_value, response.json()['total_pages'])
        self.assertEqual(response.json()['per_page'], len(response.json()['data']))
        self.assertGreater(response.json()['data'][0]['id'], 0)
        self.assertRegex(response.json()['data'][0]['email'],
                         r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

    def test_get_user_record(self) -> None:
        """Test of GET:/api/users/2-SINGLE USER"""
        response = requests.get(f'{BASE_URL}/api/users/{USER_ID}', timeout=BASE_TIMEOUT)

        self.assertEqual(200, response.status_code)
        self.assertEqual('application/json; charset=utf-8', response.headers['Content-Type'])
        self.assertDictEqual(NEL_DIC, json.loads(response.headers['NEL']))
        self.assertEqual(USER_ID, response.json()['data']['id'])
        self.assertRegex(response.json()['data']['email'],
                         r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        self.assertNotEqual('', response.json()['data']['avatar'])

    def test_get_user_not_found(self) -> None:
        """Test of GET:/api/users/23-SINGLE USER NOT FOUND"""
        user_id_404 = 0
        while True:
            resp = requests.get(f'{BASE_URL}/api/users/{USER_ID_BAD}', timeout=BASE_TIMEOUT)
            if resp.status_code == 404:
                break
            user_id_404 += USER_ID_BAD + 100

        response = requests.get(f'{BASE_URL}/api/users/{user_id_404}', timeout=BASE_TIMEOUT)

        self.assertEqual(404, response.status_code)
        self.assertEqual('2', response.headers['Content-Length'])
        self.assertEqual({}, response.json())

    def test_post_user_create(self) -> None:
        """Test of POST:/api/users-CREATE"""
        response = requests.post(f'{BASE_URL}/api/users', json=USER_JSON, timeout=BASE_TIMEOUT)

        self.assertEqual(201, response.status_code)
        self.assertEqual('application/json; charset=utf-8', response.headers['Content-Type'])
        self.assertDictEqual(NEL_DIC, json.loads(response.headers['NEL']))
        self.assertEqual(USER_JSON['name'], response.json()['name'])
        self.assertEqual(USER_JSON['job'], response.json()['job'])
        self.assertNotEqual('', response.json()['id'])
        self.assertEqual(str(datetime.date.today()), response.json()['createdAt'][0:10])

    def test_put_user_update(self) -> None:
        """Test of PUT:/api/users/2-UPDATE"""
        user_id_new = self.create_new_user()
        response_org = requests.get(f'{BASE_URL}/api/users/{user_id_new}',
                                    timeout=BASE_TIMEOUT)

        response_mod = requests.put(f'{BASE_URL}/api/users/{user_id_new}', json=USER_JSON_MOD,
                                    timeout=BASE_TIMEOUT)

        self.assertEqual('application/json; charset=utf-8', response_mod.headers['Content-Type'])
        self.assertDictEqual(NEL_DIC, json.loads(response_mod.headers['NEL']))
        self.assertEqual(200, response_mod.status_code)
        self.assertEqual(USER_JSON_MOD['name'], response_mod.json()['name'])
        self.assertEqual(USER_JSON_MOD['job'], response_mod.json()['job'])
        self.assertEqual(str(datetime.date.today()), response_mod.json()['updatedAt'][0:10])
        self.assertNotEqual(response_org.json()['name'], response_mod.json()['name'])
        self.assertNotEqual(response_org.json()['job'], response_mod.json()['job'])

    def test_delete_user(self) -> None:
        """Test of DELETE:/api/users/2-DELETE"""
        user_id_new = self.create_new_user()
        response = requests.delete(f'{BASE_URL}/api/users/{user_id_new}', timeout=BASE_TIMEOUT)
        response_post_del = requests.get(f'{BASE_URL}/api/users/{user_id_new}',
                                         timeout=BASE_TIMEOUT)

        self.assertEqual(204, response.status_code)
        self.assertDictEqual(NEL_DIC, json.loads(response.headers['NEL']))
        self.assertEqual('', response.text)
        self.assertEqual(404, response_post_del.status_code)

    def test_post_user_signup(self) -> None:
        """Test of POST:/api/register-REGISTER-SUCCESSFUL"""
        response = requests.post(f'{BASE_URL}/api/register/', json=USER_NEW_JSON,
                                 timeout=BASE_TIMEOUT)

        self.assertEqual(200, response.status_code)
        self.assertDictEqual(NEL_DIC, json.loads(response.headers['NEL']))
        self.assertDictEqual(USER_NEW_RESP_JSON, response.json())

    def test_post_user_signup_negative(self) -> None:
        """Test of POST:/api/register-REGISTER-UNSUCCESSFUL"""
        for registration in INVALID_REGISTRATION:
            response = requests.post(f'{BASE_URL}/api/register/', json=registration['body'],
                                     timeout=BASE_TIMEOUT)

            self.assertEqual(400, response.status_code)
            self.assertDictEqual(NEL_DIC, json.loads(response.headers['NEL']))
            self.assertEqual(registration['error'], response.json()['error'])

    def test_get_users_list_performance(self) -> None:
        """Test of GET:/api/users?delay=3-DELAYED RESPONSE(less than 3 seconds)"""
        response = requests.get(f'{BASE_URL}/api/users?delay=3', timeout=BASE_TIMEOUT)

        self.assertEqual(200, response.status_code)
        self.assertEqual('application/json; charset=utf-8', response.headers['Content-Type'])
        self.assertDictEqual(NEL_DIC, json.loads(response.headers['NEL']))
        self.assertGreater(3, response.elapsed.seconds, 'Response time is more than 3 sec.')

    @staticmethod
    def create_new_user() -> int:
        """New user creation method,  return user ID """
        resp_user_crt = requests.post(f'{BASE_URL}/api/users', json=USER_JSON,
                                      timeout=BASE_TIMEOUT)
        return resp_user_crt.json()['id']


if __name__ == '__main__':
    unittest.main()
