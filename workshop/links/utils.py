"""
    Utils module for link application
"""
import difflib
from selenium import webdriver

from .constant import SIMILAR_RATIO


def is_similar(source, target):
    """
        Return if source string is similar to target string
    """
    seq = difflib.SequenceMatcher(a=source, b=target)
    ratio = seq.ratio()
    return ratio >= SIMILAR_RATIO


def get_screenshot(url, filename):
    driver = webdriver.Firefox(executable_path='/usr/bin/geckodriver')
    driver.get(url)
    screenshot = driver.save_screenshot(filename)
    driver.quit()
    return screenshot
