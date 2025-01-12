import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from Windows.gesture_control_win import (
        volume_up, volume_down, swipe_left, swipe_right,
        execute_action, toggle_developer_mode, on_press, on_release,
        developer_mode
    )
except ImportError:
    print("Error: Could not import Windows gesture control module")
    raise

class TestWindowsGestureControl(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test"""
        print("Setting up Windows test...")
    
    @patch('pycaw.pycaw.AudioUtilities.GetSpeakers')
    def test_volume_up(self, mock_speakers):
        """Test Windows volume up function"""
        mock_interface = MagicMock()
        mock_volume = MagicMock()
        mock_speakers.return_value.Activate.return_value = mock_interface
        volume_up()
        # Verify that the volume control was accessed
        mock_speakers.assert_called_once()
    
    @patch('pycaw.pycaw.AudioUtilities.GetSpeakers')
    def test_volume_down(self, mock_speakers):
        """Test Windows volume down function"""
        mock_interface = MagicMock()
        mock_volume = MagicMock()
        mock_speakers.return_value.Activate.return_value = mock_interface
        volume_down()
        # Verify that the volume control was accessed
        mock_speakers.assert_called_once()
    
    @patch('builtins.print')
    def test_swipe_left(self, mock_print):
        """Test Windows swipe left function"""
        swipe_left()
        mock_print.assert_called_with("Swipe Left - Windows Desktop Switch")
    
    @patch('builtins.print')
    def test_swipe_right(self, mock_print):
        """Test Windows swipe right function"""
        swipe_right()
        mock_print.assert_called_with("Swipe Right - Windows Desktop Switch")

if __name__ == '__main__':
    unittest.main(verbosity=2) 