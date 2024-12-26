import os
from .installed_browsers import what_is_the_default_browser

from selenium import webdriver
from selenium.webdriver.edge.service import Service


__all__ = ['service_run']


def _find_driver(path):
    browser = what_is_the_default_browser()
    if browser == 'Microsoft Edge':
        return os.path.join(path, 'drivers', 'msedgedriver.exe')
    elif browser == 'Google Chrome':
        return os.path.join(path, 'drivers', 'chromedriver.exe')
    else:
        raise ValueError("There is no '%s' browser" % browser)
        
        
def service_run(path):
    path = _find_driver(path)
    service = Service(path)
    return webdriver.Edge(service=service)