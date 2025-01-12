import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from macOS.gesture_control_macOS import (
        volume_up, volume_down, swipe_left, swipe_right,
        execute_action, toggle_developer_mode, on_press, on_release,
        developer_mode
    )
except ImportError:
    print("Error: Could not import macOS gesture control module")
    raise

class TestMacGestureControl(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test"""
        print("Setting up macOS test...")
        
    @patch('subprocess.run')
    def test_volume_up(self, mock_run):
        """Test macOS volume up function"""
        volume_up()
        mock_run.assert_called_with(
            ['osascript', '-e', 'set volume output volume (output volume of (get volume settings) + 10)'],
            capture_output=True
        )
    
    @patch('subprocess.run')
    def test_volume_down(self, mock_run):
        """Test macOS volume down function"""
        volume_down()
        mock_run.assert_called_with(
            ['osascript', '-e', 'set volume output volume (output volume of (get volume settings) - 10)'],
            capture_output=True
        )
    
    @patch('subprocess.run')
    def test_swipe_left(self, mock_run):
        """Test macOS swipe left function"""
        swipe_left()
        mock_run.assert_called_with(
            ['osascript', '-e', 'tell application "System Events" to key code 123 using {control down}'],
            capture_output=True
        )
    
    @patch('subprocess.run')
    def test_swipe_right(self, mock_run):
        """Test macOS swipe right function"""
        swipe_right()
        mock_run.assert_called_with(
            ['osascript', '-e', 'tell application "System Events" to key code 124 using {control down}'],
            capture_output=True
        )

if __name__ == '__main__':
    unittest.main(verbosity=2) 