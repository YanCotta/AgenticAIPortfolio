import pytest
from src.utils.helpers import pretty_print_result, get_api_key, load_env
from unittest.mock import patch, MagicMock
import logging

def test_pretty_print_result():
    long_text = "This is a very long line that should be broken into multiple lines because it exceeds the maximum length limit of 80 characters"
    result = pretty_print_result(long_text)
    assert all(len(line) <= 80 for line in result.split('\n'))

def test_pretty_print_result_empty_string():
    assert pretty_print_result("") == ""

def test_pretty_print_result_non_string_input():
    assert pretty_print_result(123) == 123

def test_pretty_print_result_single_word_per_line():
    text = "word " * 20
    result = pretty_print_result(text)
    assert all(len(line) <= 80 for line in result.split('\n'))

@patch('os.getenv')
def test_get_api_key(mock_getenv):
    mock_getenv.return_value = "test-api-key"
    key = get_api_key("TEST_KEY")
    assert key == "test-api-key"
    mock_getenv.assert_called_once_with("TEST_KEY")

@patch('src.utils.helpers.load_dotenv')
@patch('src.utils.helpers.find_dotenv')
def test_load_env_file_not_found(mock_find_dotenv, mock_load_dotenv):
    mock_find_dotenv.return_value = "fake_path"
    mock_load_dotenv.return_value = False
    
    with pytest.raises(EnvironmentError):
        load_env()

@patch('os.getenv')
def test_get_api_key_with_special_characters(mock_getenv):
    mock_getenv.return_value = "test!@#$%^&*()"
    key = get_api_key("TEST_KEY")
    assert key == "test!@#$%^&*()"

@patch('logging.Logger.warning')
@patch('os.getenv')
def test_get_api_key_logs_warning_when_missing(mock_getenv, mock_warning):
    mock_getenv.return_value = None
    key = get_api_key("MISSING_KEY")
    assert key is None
    mock_warning.assert_called_once()

def test_get_api_key_missing():
    key = get_api_key("NONEXISTENT_KEY")
    assert key is None
