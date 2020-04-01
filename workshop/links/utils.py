"""
    Utils module for link application
"""
import difflib
from django.conf import settings
from selenium import webdriver

from .constant import SIMILAR_RATIO


def is_similar(source, target):
    """
        Return if source string is similar to target string
    """
    seq = difflib.SequenceMatcher(a=source, b=target)
    ratio = seq.ratio()
    return ratio >= SIMILAR_RATIO


def get_display(width, height):
    try:
        from pyvirtualdisplay import Display
        display = Display(visible=0, size=(width, height))
        display.start()
        return display
    except:
        pass
    return None


def get_screenshot(url, filename):
    if settings.USE_DISPLAY:
        display = get_display(settings.DISPLAY_WIDTH, settings.DISPLAY_HEIGHT)
    if settings.BROWSER_TO_SCREENSHOTS == 'firefox':
        driver = webdriver.Firefox(executable_path='/usr/bin/geckodriver')
    else:
        driver = webdriver.Chrome()
    driver.get(url)
    screenshot = driver.save_screenshot(filename)
    driver.quit()
    if settings.USE_DISPLAY:
        display.stop()
    return screenshot
