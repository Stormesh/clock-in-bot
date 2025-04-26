import unittest


class PermissionsTest(unittest.TestCase):
    def test_permissions(self):
        owner_id = 15432
        id = owner_id
        channels_permission = True
        if not (channels_permission or id == owner_id):
            return self.assertTrue(False)
        return self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
