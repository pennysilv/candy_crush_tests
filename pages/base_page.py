"""
Базовый класс для всех страниц приложения
"""

import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class BasePage:
    """Базовый класс для всех Page Object классов"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        
    def find_element(self, by, value, timeout=10):
        """Найти элемент с ожиданием"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            return wait.until(EC.presence_of_element_located((by, value)))
        except TimeoutException:
            print(f"❌ Элемент не найден: {by}={value}")
            return None
    
    def find_elements(self, by, value, timeout=10):
        """Найти все элементы с ожиданием"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.presence_of_element_located((by, value)))
            return self.driver.find_elements(by, value)
        except TimeoutException:
            print(f"❌ Элементы не найдены: {by}={value}")
            return []
    
    def click_element(self, by, value, timeout=10):
        """Кликнуть на элемент с ожиданием"""
        element = self.find_element(by, value, timeout)
        if element:
            try:
                element.click()
                print(f"✅ Кликнули на элемент: {by}={value}")
                return True
            except Exception as e:
                print(f"❌ Не удалось кликнуть: {e}")
                return False
        return False
    
    def wait_for_element(self, by, value, timeout=10):
        """Ждать появления элемента"""
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.presence_of_element_located((by, value)))
            print(f"✅ Элемент появился: {by}={value}")
            return True
        except TimeoutException:
            print(f"❌ Элемент не появился за {timeout}с: {by}={value}")
            return False
    
    def is_element_present(self, by, value):
        """Проверить присутствие элемента без ожидания"""
        try:
            self.driver.find_element(by, value)
            return True
        except NoSuchElementException:
            return False
    
    def get_all_clickable_elements(self):
        """Получить все кликабельные элементы на экране"""
        return self.driver.find_elements(AppiumBy.XPATH, "//*[@clickable='true']")
    
    def take_screenshot(self, name="screenshot"):
        """Сделать скриншот экрана"""
        filename = f"reports/{name}_{int(time.time())}.png"
        self.driver.save_screenshot(filename)
        print(f"📸 Скриншот сохранен: {filename}")
        return filename
    
    def get_page_source(self):
        """Получить исходный код страницы для отладки"""
        return self.driver.page_source
    
    def scroll_down(self):
        """Прокрутить экран вниз"""
        size = self.driver.get_window_size()
        start_x = size['width'] // 2
        start_y = size['height'] * 0.8
        end_y = size['height'] * 0.2
        
        self.driver.swipe(start_x, start_y, start_x, end_y, 1000)
    
    def scroll_up(self):
        """Прокрутить экран вверх"""
        size = self.driver.get_window_size()
        start_x = size['width'] // 2
        start_y = size['height'] * 0.2
        end_y = size['height'] * 0.8
        
        self.driver.swipe(start_x, start_y, start_x, end_y, 1000)
