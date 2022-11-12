import unittest
import requests


class TestsAPI(unittest.TestCase):
    BASE_URL = 'https://reqres.in'

    def test_get_users_list(self) -> None:
        """Test of GET:/api/users-LIST USERS"""
        pass

    def test_get_user_record(self) -> None:
        """Test of GET:/api/users/2-SINGLE USER"""
        pass

    def test_get_user_not_found(self) -> None:
        """Test of GET:/api/users/23-SINGLE USER NOT FOUND"""
        pass

    def test_post_user_create(self) -> None:
        """Test of POST:/api/users-CREATE"""
        pass

    def test_put_user_update(self) -> None:
        """Test of PUT:/api/users/2-UPDATE"""
        pass

    def test_delete_user(self) -> None:
        """Test of DELETE:/api/users/2-DELETE"""
        pass

    def test_post_user_signin(self) -> None:
        """Test of POST:/api/register-REGISTER-SUCCESSFUL"""
        pass

    def test_post_user_signin_negative(self) -> None:
        """Test of POST:/api/register-REGISTER-UNSUCCESSFUL"""
        pass

    def test_get_users_list_perfomance(self) -> None:
        """Test of GET:/api/users?delay=3-DELAYED RESPONSE(less than 3 seconds)"""
        pass


if __name__ == '__main__':
    unittest.main()
