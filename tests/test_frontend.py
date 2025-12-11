import unittest
from unittest.mock import patch, MagicMock
import gui

class FrontendTests(unittest.TestCase):
    def setUp(self):
        # create a headless Tk root for widget creation
        import tkinter as tk
        self.root = tk.Tk()
        self.root.withdraw()
        self.app = gui.LibraryGUI(self.root)

    def tearDown(self):
        self.root.destroy()

    @patch("gui.requests.get")
    def test_load_all_populates(self, mock_get):
        mock_get.return_value = MagicMock(status_code=200, json=lambda: [{"name":"X","author":"A","publication_date":"2020","category":"Book"}])
        self.app.load_all()
        self.assertEqual(self.app.listbox.size(), 1)

    @patch("gui.requests.get")
    def test_search_not_found(self, mock_get):
        m = MagicMock()
        m.status_code = 404
        mock_get.return_value = m
        # set search var and call
        self.app.search_var.set("DoesNotExist")
        # should not raise
        self.app.search_name()

if __name__=="__main__":
    unittest.main()
