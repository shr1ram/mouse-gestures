import os
from setuptools import setup

# Get absolute path to icon file
ICON_FILE = os.path.abspath('icon.icns')

APP = ['macOS/gesture_control_macOS.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': False,
    'packages': ['pynput', 'appdirs'],
    'includes': [
        'subprocess', 
        'platform', 
        'time', 
        'pkg_resources'],
    'excludes': [
        'pkg_resources._vendor.appdirs',
        'win32com',
        'StringIO',
        'pep517',
        'test',
        '_manylinux'
    ],
    'iconfile': ICON_FILE,  # Use absolute path
    'plist': {
        'LSUIElement': True,
        'NSAppleEventsUsageDescription': 'This app needs to control system events for gesture controls.',
        'NSRequiresAquaSystemAppearance': 'No',
        'CFBundleName': 'Middle Click',
        'CFBundleDisplayName': 'Middle Click',
        'CFBundleIdentifier': 'com.yourname.middleclick',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'NSRequiredUpgradedSystemVersion': '10.0.0',
        'NSHumanReadableCopyright': 'Copyright © 2024',
        'NSInputMonitoringUsageDescription': 'This app needs to monitor input to detect gestures.',
        'NSAppleEventsUsageDescription': 'This app needs to control system events.',
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    name="Middle Click",
    install_requires=[
        'pynput>=1.7.0',
        'appdirs',
    ],
) 