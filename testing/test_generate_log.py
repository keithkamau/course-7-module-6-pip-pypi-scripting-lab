"""
Unit tests for the generate_log module.
"""

import os
import pytest
from datetime import datetime
from lib.generate_log import generate_log


class TestGenerateLog:
    """Test suite for generate_log function"""
    
    def test_create_log_file_with_valid_data(self, tmp_path):
        original_dir = os.getcwd()
        os.chdir(tmp_path)
        
        try:
            log_data = ["User logged in", "User updated profile", "Report exported"]
            filename = generate_log(log_data)
            
            expected_pattern = f"log_{datetime.now().strftime('%Y%m%d')}.txt"
            assert filename == expected_pattern
            assert os.path.exists(filename)
            
            with open(filename, 'r') as file:
                content = file.read().strip().split('\n')
            
            assert len(content) == 3
            assert content[0] == "User logged in"
            assert content[1] == "User updated profile"
            assert content[2] == "Report exported"
            
        finally:
            os.chdir(original_dir)
    
    def test_filename_pattern(self, tmp_path):
        original_dir = os.getcwd()
        os.chdir(tmp_path)
        
        try:
            log_data = ["Test entry"]
            filename = generate_log(log_data)
            
            date_part = datetime.now().strftime('%Y%m%d')
            expected = f"log_{date_part}.txt"
            assert filename == expected
            assert filename.startswith("log_")
            assert filename.endswith(".txt")
            
        finally:
            os.chdir(original_dir)
    
    def test_file_contents_match_input(self, tmp_path):
        original_dir = os.getcwd()
        os.chdir(tmp_path)
        
        try:
            log_data = ["Line 1", "Line 2", "Line 3", "Final line"]
            filename = generate_log(log_data)
            
            with open(filename, 'r') as file:
                content = file.read().strip().split('\n')
            
            assert content == log_data
            
        finally:
            os.chdir(original_dir)
    
    def test_raises_value_error_for_non_list(self):
        invalid_inputs = [
            "not a list",
            123,
            {"key": "value"},
            None
        ]
        
        for invalid_input in invalid_inputs:
            with pytest.raises(ValueError, match="log_data must be a list"):
                generate_log(invalid_input)
    
    def test_empty_list_creates_empty_file(self, tmp_path):
        original_dir = os.getcwd()
        os.chdir(tmp_path)
        
        try:
            log_data = []
            filename = generate_log(log_data)
            
            assert os.path.exists(filename)
            
            with open(filename, 'r') as file:
                content = file.read()
            
            assert content == ""
            
        finally:
            os.chdir(original_dir)
    
    def test_confirmation_message(self, tmp_path, capsys):
        original_dir = os.getcwd()
        os.chdir(tmp_path)
        
        try:
            log_data = ["Test entry"]
            filename = generate_log(log_data)
            
            captured = capsys.readouterr()
            expected_message = f"Log written to {filename}"
            assert expected_message in captured.out
            
        finally:
            os.chdir(original_dir)
    
    def test_file_created_and_removed(self, tmp_path):
        original_dir = os.getcwd()
        os.chdir(tmp_path)
        
        try:
            log_data = ["Test entry for cleanup"]
            filename = generate_log(log_data)
            
            assert os.path.exists(filename)
            
            os.remove(filename)
            
            assert not os.path.exists(filename)
            
        finally:
            os.chdir(original_dir)
    
    def test_raises_error_for_non_string_elements(self, tmp_path):
        original_dir = os.getcwd()
        os.chdir(tmp_path)
        
        try:
            log_data = ["Valid string", 123, "Another string"]
            with pytest.raises(ValueError, match="All elements in log_data must be strings"):
                generate_log(log_data)
        finally:
            os.chdir(original_dir)
