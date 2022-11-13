"""API tests"""
import unittest
import datetime
import requests

BASE_URL = 'https://reqres.in'
BASE_TIMEOUT = 5
USER_ID = 5
USER_ID_BAD = 23
user_json = {'name': 'Ivan', 'job': 'leader'}
user_json_login = {"email": "eve.holt@reqres.in", "password": "pistol"}
resp_json = {"id": 4, "token": "QpwL5tke4Pnpja7X4"}
login_not_valid = [{"email": "", "password": ""}, {"email": "eve.holt@reqres.in", "password": ""},
                   {"email": "1", "password": "1"}, {"email": "", "password": "1"}]


class TestsAPI(unittest.TestCase):
    """API test suit"""
    def test_get_users_list(self) -> None:
        """Test of GET:/api/users-LIST USERS"""
        response = requests.get(f'{BASE_URL}/api/users', timeout=BASE_TIMEOUT)

        self.assertEqual(200, response.status_code)
        self.assertEqual('application/json; charset=utf-8', response.headers['Content-Type'])
        self.assertEqual('{"success_fraction":0,"report_to":"cf-nel","max_age":604800}',
                         response.headers['NEL'])
        self.assertNotEqual(0, response.json()['total'])
        self.assertEqual(1, response.json()['data'][0]['id'])
        self.assertRegex(response.json()['data'][0]['email'],
                         r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')

    def test_get_user_record(self) -> None:
        """Test of GET:/api/users/2-SINGLE USER"""
        response = requests.get(f'{BASE_URL}/api/users/{USER_ID}', timeout=BASE_TIMEOUT)

        self.assertEqual(200, response.status_code)
        self.assertEqual('application/json; charset=utf-8',
                         response.headers['Content-Type'])
        self.assertEqual('{"success_fraction":0,"report_to":"cf-nel","max_age":604800}',
                         response.headers['NEL'])
        self.assertEqual(USER_ID, response.json()['data']['id'])
        self.assertRegex(response.json()['data']['email'],
                         r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        self.assertNotEqual('', response.json()['data']['avatar'])

    def test_get_user_not_found(self) -> None:
        """Test of GET:/api/users/23-SINGLE USER NOT FOUND"""
        response = requests.get(f'{BASE_URL}/api/users/{USER_ID_BAD}', timeout=BASE_TIMEOUT)

        self.assertEqual(404, response.status_code)
        self.assertEqual('2', response.headers['Content-Length'])
        self.assertEqual({}, response.json())

    def test_post_user_create(self) -> None:
        """Test of POST:/api/users-CREATE"""
        response = requests.post(f'{BASE_URL}/api/users', json=user_json, timeout=BASE_TIMEOUT)

        self.assertEqual(201, response.status_code)
        self.assertEqual('application/json; charset=utf-8',
                         response.headers['Content-Type'])
        self.assertEqual('{"success_fraction":0,"report_to":"cf-nel","max_age":604800}',
                         response.headers['NEL'])
        self.assertEqual(user_json['name'], response.json()['name'])
        self.assertEqual(user_json['job'], response.json()['job'])
        self.assertNotEqual('', response.json()['id'])
        self.assertEqual(str(datetime.date.today()), response.json()['createdAt'][0:10])

    def test_put_user_update(self) -> None:
        """Test of PUT:/api/users/2-UPDATE"""
        response = requests.put(f'{BASE_URL}/api/users/{USER_ID}', json=user_json,
                                timeout=BASE_TIMEOUT)

        self.assertEqual('application/json; charset=utf-8',
                         response.headers['Content-Type'])
        self.assertEqual('{"success_fraction":0,"report_to":"cf-nel","max_age":604800}',
                         response.headers['NEL'])
        self.assertEqual(200, response.status_code)
        self.assertEqual(user_json['name'], response.json()['name'])
        self.assertEqual(user_json['job'], response.json()['job'])
        self.assertEqual(str(datetime.date.today()), response.json()['updatedAt'][0:10])

    def test_delete_user(self) -> None:
        """Test of DELETE:/api/users/2-DELETE"""
        response = requests.delete(f'{BASE_URL}/api/users/{USER_ID}', timeout=BASE_TIMEOUT)

        self.assertEqual(204, response.status_code)
        self.assertEqual('{"success_fraction":0,"report_to":"cf-nel","max_age":604800}',
                         response.headers['NEL'])
        self.assertEqual('', response.text)

    def test_post_user_signin(self) -> None:
        """Test of POST:/api/register-REGISTER-SUCCESSFUL"""
        response = requests.post(f'{BASE_URL}/api/register/', json=user_json_login,
                                 timeout=BASE_TIMEOUT)

        self.assertEqual(200, response.status_code)
        self.assertEqual('{"success_fraction":0,"report_to":"cf-nel","max_age":604800}',
                         response.headers['NEL'])
        self.assertEqual(resp_json, response.json())

    def test_post_user_signin_negative(self) -> None:
        """Test of POST:/api/register-REGISTER-UNSUCCESSFUL"""
        for json_set in login_not_valid:
            if json_set['email'] == '':
                resp_json_in = {"error": "Missing email or username"}
            elif json_set['email'] != '' and json_set['password'] == '':
                resp_json_in = {"error": "Missing password"}
            elif json_set['email'] != 'eve.holt@reqres.in' and json_set['password'] != '':
                resp_json_in = {"error": "Note: Only defined users succeed registration"}
            else:
                resp_json_in = {}

            response = requests.post(f'{BASE_URL}/api/register/', json=json_set,
                                     timeout=BASE_TIMEOUT)

            self.assertEqual(400, response.status_code)
            self.assertEqual('{"success_fraction":0,"report_to":"cf-nel","max_age":604800}',
                             response.headers['NEL'])
            self.assertEqual(resp_json_in, response.json())

    def test_get_users_list_perfomance(self) -> None:
        """Test of GET:/api/users?delay=3-DELAYED RESPONSE(less than 3 seconds)"""
        response = requests.get(f'{BASE_URL}/api/users?delay=3', timeout=BASE_TIMEOUT)

        self.assertEqual(200, response.status_code)
        self.assertEqual('application/json; charset=utf-8', response.headers['Content-Type'])
        self.assertEqual('{"success_fraction":0,"report_to":"cf-nel","max_age":604800}',
                         response.headers['NEL'])
        self.assertGreater(3, response.elapsed.seconds, 'Response time is more than 3 sec.')


if __name__ == '__main__':
    unittest.main()
