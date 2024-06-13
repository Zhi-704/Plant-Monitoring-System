'''File used for testing the archive file for the storing long term data'''
import pytest
from unittest.mock import patch, MagicMock
from archive import get_connection


class TestGetConnection:
    '''Contains tests for get connection function'''

    def test_missing_key(self) -> None:
        '''Tests if the scenario where the env variable is missing'''
        pass
