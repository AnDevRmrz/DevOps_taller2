import importlib
import sys
import types
import unittest


class ApplicationTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Stub the 'funtions' module before importing 'application' so that
        # application.data is populated with predictable test data.
        fake = types.ModuleType("funtions")

        def fake_load_file(file_name: str):
            return {
                "1": {
                    "name": "Batman",
                    "gender": "Male",
                    "eye_color": "blue",
                    "race": "Human",
                    "hair_color": "black",
                    "height": "188",
                    "publisher": "DC Comics",
                    "skin_color": "",
                    "alignment": "good",
                    "weight": "95",
                },
                "2": {
                    "name": "Wonder Woman",
                    "gender": "Female",
                    "eye_color": "blue",
                    "race": "Amazon",
                    "hair_color": "black",
                    "height": "183",
                    "publisher": "DC Comics",
                    "skin_color": "",
                    "alignment": "good",
                    "weight": "75",
                },
            }

        fake.load_file = fake_load_file
        sys.modules["funtions"] = fake

        # Import after stubbing to ensure the application uses our fake data
        cls.app_module = importlib.import_module("application")
        cls.client = cls.app_module.application.test_client()
        cls.data = cls.app_module.data

    def test_index_returns_all_data(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.is_json)
        self.assertEqual(resp.get_json(), self.data)

    def test_heroe_valid_id(self):
        resp = self.client.get("/1")
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.is_json)
        self.assertEqual(resp.get_json(), self.data["1"])

    def test_heroe_invalid_id_returns_404(self):
        resp = self.client.get("/999")
        self.assertEqual(resp.status_code, 404)
        self.assertTrue(resp.is_json)
        self.assertEqual(resp.get_json(), {"error": "not found", "id": "999"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
