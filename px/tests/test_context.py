#!/usr/bin/env python3
# BoBoBo
import unittest
from unittest.mock import MagicMock
from unittest.mock import patch

from px.context import PxContext
from px.context import setup_default_process_module
from px.context import setup_request_process_module
from px.context import setup_wsgi_process_module


class TestSetupFunctions(unittest.TestCase):
    def test_setup_default_process_module(self):
        setup_default_process_module()
        self.assertIsNotNone(PxContext.request_process_module)

    def test_setup_request_process_module_with_valid_module(self):
        with patch("importlib.import_module") as mock_import_module:
            mock_module = MagicMock()
            mock_import_module.return_value = mock_module

            setup_request_process_module("my_module.some_module")
            self.assertIsNotNone(PxContext.request_process_module)
            self.assertIsInstance(PxContext.request_process_module, MagicMock)
            self.assertTrue(callable(PxContext.request_process_module.process_request))

    def test_setup_request_process_module_with_invalid_module(self):
        with self.assertRaises(ValueError):
            setup_request_process_module("invalid_module_name")

    def test_setup_wsgi_process_module_with_valid_module(self):
        with patch("importlib.import_module") as mock_import_module:
            mock_app_module = MagicMock()
            mock_app_module.wsgi_app = MagicMock(
                return_value=lambda env, start_response: None
            )
            mock_import_module.return_value = mock_app_module

            setup_wsgi_process_module("my_module.some_module")

            self.assertIsNotNone(PxContext.wsgi_app)
            self.assertTrue(callable(PxContext.wsgi_app))

            self.assertIsNotNone(PxContext.request_process_module)
            self.assertEqual(
                PxContext.request_process_module.__name__, "px.wsgi_process_module"
            )

            mock_app_module.wsgi_app.assert_called_once()

    def test_setup_wsgi_process_module_with_invalid_module(self):
        with self.assertRaises(ValueError):
            setup_wsgi_process_module("invalid_module_name")


if __name__ == "__main__":
    unittest.main()
