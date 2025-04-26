import unittest
from ..data.common import get_roles


class TestRoles(unittest.TestCase):
    def test_get_roles(self):
        roles = get_roles(1284999735694065694)
        print(roles)
        self.assertIsNotNone(roles)

if __name__ == "__main__":
    unittest.main()