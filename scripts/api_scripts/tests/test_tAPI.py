import io
import pytest
import requests
import unittest.mock
import pymysql
import configparser
from tAPI import read_key, read_db_params, handle_api_response, main
from unittest.mock import patch, mock_open, Mock, MagicMock, call
from io import StringIO

#Test that "with open()" reads in the correct data #NOT POSSIBLE WITHOUT RETURN STATEMENT
def test_read_key():
    #Test1: Check what happens if api.env is filled and correct
    mock_api_env = '"key1" = "1a2b"\n\
                    "RedCircle" = "3c4d"\n\
                    "key3" = "5e6f"'
    with patch('builtins.open', new_callable=mock_open, read_data=mock_api_env):
        key1 = read_key()
        assert key1 == "3c4d", f"Test 1: returned {key1}, expected '3c4d'."
    
    #Test2: Check what happens when api.env is empty
    mock_api_env =''
    with patch('builtins.open', new_callable=mock_open, read_data=mock_api_env):
        key2 = read_key()
        assert key2 == "key", f"Test 2: returned {key2}, expected 'key'."
    
    #Test3: Check what happens if "RedCircle" is not in the file
    mock_api_env ='"key1" = "1a2b"\n\
                   "key2" = "3c4d"\n\
                   "key3" = "5e6f"'
    with patch('builtins.open', new_callable=mock_open, read_data=mock_api_env):
        key3 = read_key()
        assert key3 == "key", f"Test 3: returned {key3}, expected 'key'."
        
    #Test4: Check what happens if len(parts) != 2
    mock_api_env ='"key1" = "1a2b"\n\
                   "RedCircle"\n\
                   "key3" = "5e6f"'
    with patch('builtins.open', new_callable=mock_open, read_data=mock_api_env):
        key4 = read_key()
        assert key4 == "key", f"Test 4: returned {key4}, expected 'key'."

#Create config object
def create_config(section, options):
    config = configparser.ConfigParser()
    config[section] = options
    return config

def test_read_db_params():
    #Test1: Check that read_db_params can successfully create db_params when config is filled with all needed info
    with unittest.mock.patch('configparser.ConfigParser.read'):
        # Test when all options are set
        config_all_set = create_config('database', {
            'host': 'test_host',
            'user': 'test_user',
            'password': 'test_pw',
            'db': 'test_db'
        })

        # Manually set the sections and options in the ConfigParser instance
        config = configparser.ConfigParser()
        config.read_dict(config_all_set)

        expected = {
                'host': 'test_host',
                'user': 'test_user',
                'password': 'test_pw',
                'db': 'test_db',
                'charset': 'utf8mb4',
                'cursorclass': pymysql.cursors.DictCursor
            }
        
        with unittest.mock.patch('configparser.ConfigParser', return_value=config):
            result = read_db_params()
            assert  result == expected, f"Test1 failed, returned {result}, expected {expected}."

        #Test2: Check that a KeyError is raised when the key 'database' is missing.
        config.clear()
        config_key_miss = create_config('dtaabsae', {
            'host': 'test_host',
            'user': 'test_user',
            'password': 'test_pw',
            'db': 'test_db'
        })

        config = configparser.ConfigParser()
        config.read_dict(config_key_miss)

        with unittest.mock.patch('configparser.ConfigParser', return_value=config):
            with pytest.raises(KeyError, match="database"):
                read_db_params()
        
        
        #Test3: Check that a KeyError is raised when 'host' is missing
        config.clear()
        config_miss_host = create_config('database', {
            'user': 'test_user',
            'password': 'test_pw',
            'db': 'test_db'
        })

        
        config.read_dict(config_miss_host)
        with unittest.mock.patch('configparser.ConfigParser', return_value=config):
            with pytest.raises(KeyError, match="host"):
                read_db_params()

        #Test4: Check that a KeyError is raised when 'user' is missing
        config.clear()
        config_miss_user = create_config('database', {
            'host': 'test_host',
            'password': 'test_pw',
            'db': 'test_db'
        })

        config = configparser.ConfigParser()
        config.read_dict(config_miss_user)
        
        with unittest.mock.patch('configparser.ConfigParser', return_value=config):
            with pytest.raises(KeyError, match="user"):
                read_db_params()

        #Test5: Check that a KeyError is raised when 'password' is missing
        config.clear()
        config_miss_pw = create_config('database', {
            'host': 'test_host',
            'user': 'test_user',
            'db': 'test_db'
        })

        config = configparser.ConfigParser()
        config.read_dict(config_miss_pw)

        with unittest.mock.patch('configparser.ConfigParser', return_value=config):
            with pytest.raises(KeyError, match="password"):
                read_db_params()

        #Test6: Check that a KeyError is raised when 'db' is missing
        config.clear()
        config_miss_db = create_config('database', {
            'host': 'test_host',
            'user': 'test_user',
            'password': 'test_pw'
        })

        config = configparser.ConfigParser()
        config.read_dict(config_miss_db)

        with unittest.mock.patch('configparser.ConfigParser', return_value=config):
            with pytest.raises(KeyError, match='db'):
                read_db_params()

        #Test7: Check that a KeyError is raised when 'db' is missing in create_config
        config.clear()
        config_empty = create_config('database', {})  # Create an empty config

        config = configparser.ConfigParser()
        config.read_dict(config_empty)
        
        with unittest.mock.patch('configparser.ConfigParser', return_value=config_empty):
            with pytest.raises(KeyError):
                read_db_params()


#mock connect
@pytest.fixture
def mock_pymysql_connect():
    with patch('tAPI.pymysql.connect') as mock_connect:
        yield mock_connect

def test_handle_api_response(mock_pymysql_connect):
    #Test1: Check the function works correctly when all key-value pairs are present
    response_mock = Mock()
    response_mock.json.return_value = {
        'Store': {
            'Products': [
                {
                    'UPC': '123456789',
                    'Name': 'Product 1',
                    'Category_ID': 1,
                    'Sub_category_ID': 2,
                    'Description': 'Product description',
                    'Keywords': 'Keyword1, Keyword2',
                    'Img_URL': 'https://example.com/image.jpg',
                    'Update_Count': 42
                }
            ]
        }
    }

    with patch.object(mock_pymysql_connect.return_value, 'commit') as mock_commit:
        handle_api_response(mock_pymysql_connect.return_value, 'search_term', response_mock)

        # Assert that the execute method was called with the expected parameters
        mock_cursor = mock_pymysql_connect.return_value.cursor.return_value.__enter__.return_value
        mock_cursor.execute.assert_called_once_with(
            """
            INSERT INTO Product (UPC, Name, Category_ID, Sub_category_ID, Description, Keywords, Img_URL, Update_Count)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            ('123456789', 'Product 1', 1, 2, 'Product description', 'Keyword1, Keyword2', 'https://example.com/image.jpg', 42)
        )

        # Assert that commit was called
        mock_commit.assert_called_once()

        mock_pymysql_connect.return_value.cursor.return_value.__enter__.return_value.execute.reset_mock()

    #Test2: Check that the function works properly when there is more than one product
    response_mock.json.return_value = {
        'Store': {
            'Products': [
                {
                    'UPC': '123',
                    'Name': 'Product 1',
                    'Category_ID': 1,
                    'Sub_category_ID': 2,
                    'Description': 'Product description',
                    'Keywords': 'Keyword1, Keyword2',
                    'Img_URL': 'https://example.com/image1.jpg',
                    'Update_Count': 42
                },
                {
                    'UPC': '456',
                    'Name': 'Product 2',
                    'Category_ID': 3,
                    'Sub_category_ID': 4,
                    'Description': 'Another product description',
                    'Keywords': 'Keyword3, Keyword4',
                    'Img_URL': 'https://example.com/image2.jpg',
                    'Update_Count': 10
                }
            ]
        }
    }

    with patch.object(mock_pymysql_connect.return_value, 'commit') as mock_execute_commit:
        handle_api_response(mock_pymysql_connect.return_value, 'search_term', response_mock)

        # Assert that execute was called twice (for each product)
        assert mock_pymysql_connect.return_value.cursor.return_value.__enter__.return_value.execute.call_count == 2

        # Assert that commit was called
        mock_execute_commit.assert_called_once()

        mock_pymysql_connect.return_value.cursor.return_value.__enter__.return_value.execute.reset_mock()
    
    #Test3: Check that the function works correctly when there are no products
    response_mock.json.return_value = {'Store': {'Products': []}}

    # Ensure that the function does not raise an error and does not attempt to insert anything
    with patch.object(mock_pymysql_connect.return_value, 'commit') as mock_execute_commit:
        handle_api_response(mock_pymysql_connect.return_value, 'search_term', response_mock)

        # Assert that execute was not called
        mock_pymysql_connect.return_value.cursor.return_value.__enter__.return_value.execute.assert_not_called()

        # Assert that commit was called
        mock_execute_commit.assert_called_once()

    
    #Test4: Check that the function fills in missing key-value pairs correctly when they are missing
    response_mock.json.return_value = {
        'Store': {
            'Products': [
                {
                    'UPC': '123',
                    'Name': 'Product 1',
                    'Category_ID': 1,
                    'Update_Count': 42
                }
            ]
        }
    }

    with patch.object(mock_pymysql_connect.return_value, 'commit') as mock_execute_commit:
        handle_api_response(mock_pymysql_connect.return_value, 'search_term', response_mock)

        # Assert that execute was called with default or empty values for missing fields
        mock_cursor = mock_pymysql_connect.return_value.cursor.return_value.__enter__.return_value
        mock_cursor.execute.assert_called_once_with(
            """
            INSERT INTO Product (UPC, Name, Category_ID, Sub_category_ID, Description, Keywords, Img_URL, Update_Count)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            ('123', 'Product 1', 1, '', '', '', '', 42)
        )

        # Assert that commit was called
        mock_execute_commit.assert_called_once()

def test_main():
    with patch('tAPI.read_db_params') as mock_read_db_params,\
         patch('tAPI.pymysql.connect') as mock_pymysql_connect,\
         patch('tAPI.read_key') as mock_read_key,\
         patch('requests.get') as mock_requests_get,\
         patch('tAPI.handle_api_response') as mock_handle_api_response,\
         patch('builtins.print') as mock_print,\
         patch('tAPI.pymysql.connect.close') as mock_close:

        # Mock the return values or side effects as needed
        mock_read_db_params.return_value = {'host': 'test_host', 'user': 'test_user', 'password': 'test_password', 'database': 'test_db'}
        mock_pymysql_connect.return_value = Mock()  # You may need to mock more methods or attributes here
        mock_read_key.return_value = 'test_key'
        mock_requests_get.return_value.raise_for_status.side_effect = None
        mock_handle_api_response.side_effect = lambda conn, term, resp: None  # Mock the handle_api_response function to do nothing

        main([])
        mock_read_db_params.assert_called_once()
        mock_pymysql_connect.assert_called_once_with(host='test_host', user='test_user', password='test_password', database='test_db')
        mock_read_key.assert_not_called()
        mock_requests_get.assert_not_called()
        mock_handle_api_response.assert_not_called()
        mock_print.assert_not_called()

        mock_read_db_params.call_count = 0
        mock_pymysql_connect.call_count = 0
             
        # Call the main function
        main(['term'])

        # Add assertions based on your expectations
        mock_read_db_params.assert_called_once()
        mock_pymysql_connect.assert_called_once_with(host='test_host', user='test_user', password='test_password', database='test_db')
        mock_read_key.assert_called_once()
        mock_requests_get.assert_called_once_with('https://api.redcircleapi.com/request', params={'api_key': 'test_key', 'search_term': 'term', 'type': 'search'})
        mock_requests_get.return_value.raise_for_status.assert_called_once()
        mock_handle_api_response.assert_called_once()
        mock_print.assert_not_called()  # Check that the print function was not called in case of exceptions


        mock_requests_get.return_value.raise_for_status.side_effect = requests.HTTPError('Test HTTPError')
        main(['term'])
        mock_print.assert_called_once()

        mock_print.call_count = 0
        mock_requests_get.return_value.raise_for_status.side_effect = requests.ConnectionError('Test ConnectionError')
        main(['term'])
        mock_print.assert_called_once()

        mock_print.call_count = 0
        mock_requests_get.return_value.raise_for_status.side_effect = requests.Timeout('Test Timeout')
        main(['term'])
        mock_print.assert_called_once()

        mock_print.call_count = 0
        mock_requests_get.return_value.raise_for_status.side_effect = requests.TooManyRedirects('Test TooManyRedirects')
        main(['term'])
        mock_print.assert_called_once()

        mock_print.call_count = 0
        mock_requests_get.return_value.raise_for_status.side_effect = requests.RequestException('Test RequestException')
        main(['term'])
        mock_print.assert_called_once()