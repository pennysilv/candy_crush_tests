"""
Page Object для главного меню Candy Crush Saga
"""

from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage

class MainMenuPage(BasePage):
    """Класс для работы с главным экраном игры"""
    
    # Локаторы (разные варианты для поиска элементов)
    PLAY_BUTTON_LOCATORS = [
        (AppiumBy.XPATH, "//*[contains(@text, 'Play') or contains(@text, 'PLAY')]"),
        (AppiumBy.XPATH, "//*[contains(@content-desc, 'Play') or contains(@content-desc, 'play')]"),
        (AppiumBy.XPATH, "//*[contains(@resource-id, 'play')]"),
        (AppiumBy.XPATH, "//*[contains(@class, 'Button') and contains(@text, 'Play')]"),
    ]
    
    SETTINGS_BUTTON_LOCATORS = [
        (AppiumBy.XPATH, "//*[contains(@content-desc, 'Settings') or contains(@content-desc, 'settings')]"),
        (AppiumBy.XPATH, "//*[contains(@text, 'Settings')]"),
        (AppiumBy.XPATH, "//*[contains(@resource-id, 'settings')]"),
    ]
    
    SHOP_BUTTON_LOCATORS = [
        (AppiumBy.XPATH, "//*[contains(@content-desc, 'Shop') or contains(@content-desc, 'shop')]"),
        (AppiumBy.XPATH, "//*[contains(@text, 'Shop')]"),
        (AppiumBy.XPATH, "//*[contains(@resource-id, 'shop')]"),
    ]
    
    def __init__(self, driver):
        super().__init__(driver)
        
    def is_displayed(self):
        """Проверить что главное меню отображается"""
        print("🔍 Проверяем отображение главного меню...")
        
        # Проверяем наличие любого из основных элементов
        play_button = self.find_play_button()
        clickable_elements = self.get_all_clickable_elements()
        
        is_displayed = play_button is not None or len(clickable_elements) > 0
        
        if is_displayed:
            print("✅ Главное меню отображается")
        else:
            print("❌ Главное меню не найдено")
            
        return is_displayed
    
    def find_play_button(self):
        """Найти кнопку Play разными способами"""
        print("🔍 Ищем кнопку Play...")
        
        for i, (by, value) in enumerate(self.PLAY_BUTTON_LOCATORS):
            element = self.find_element(by, value, timeout=3)
            if element:
                print(f"✅ Кнопка Play найдена способом {i+1}: {by}={value}")
                return element
                
        print("❌ Кнопка Play не найдена ни одним способом")
        return None
    
    def click_play(self):
        """Кликнуть на кнопку Play"""
        print("👆 Пытаемся кликнуть на кнопку Play...")
        
        play_button = self.find_play_button()
        if play_button:
            try:
                play_button.click()
                print("✅ Кликнули на кнопку Play")
                return True
            except Exception as e:
                print(f"❌ Не удалось кликнуть на Play: {e}")
                return False
        else:
            print("❌ Кнопка Play не найдена для клика")
            return False
    
    def find_settings_button(self):
        """Найти кнопку Settings"""
        print("🔍 Ищем кнопку Settings...")
        
        for i, (by, value) in enumerate(self.SETTINGS_BUTTON_LOCATORS):
            element = self.find_element(by, value, timeout=3)
            if element:
                print(f"✅ Кнопка Settings найдена способом {i+1}")
                return element
                
        print("❌ Кнопка Settings не найдена")
        return None
    
    def click_settings(self):
        """Кликнуть на кнопку Settings"""
        settings_button = self.find_settings_button()
        if settings_button:
            try:
                settings_button.click()
                print("✅ Кликнули на Settings")
                return True
            except Exception as e:
                print(f"❌ Ошибка клика на Settings: {e}")
                return False
        return False
    
    def get_screen_info(self):
        """Получить информацию об экране для отладки"""
        info = {
            'clickable_elements_count': len(self.get_all_clickable_elements()),
            'has_play_button': self.find_play_button() is not None,
            'has_settings_button': self.find_settings_button() is not None,
            'screen_size': self.driver.get_window_size()
        }
        
        print(f"📊 Информация об экране:")
        print(f"   - Кликабельных элементов: {info['clickable_elements_count']}")
        print(f"   - Есть кнопка Play: {info['has_play_button']}")
        print(f"   - Есть кнопка Settings: {info['has_settings_button']}")
        print(f"   - Размер экрана: {info['screen_size']}")
        
        return info
    
    def debug_all_elements(self):
        """Вывести все элементы на экране для отладки"""
        print("🔧 Отладка: все элементы на экране")
        
        clickable_elements = self.get_all_clickable_elements()
        
        for i, element in enumerate(clickable_elements):
            try:
                text = element.get_attribute('text') or ''
                content_desc = element.get_attribute('content-desc') or ''
                resource_id = element.get_attribute('resource-id') or ''
                class_name = element.get_attribute('class') or ''
                
                print(f"Элемент {i+1}:")
                print(f"  text: '{text}'")
                print(f"  content-desc: '{content_desc}'")
                print(f"  resource-id: '{resource_id}'")
                print(f"  class: '{class_name}'")
                print("---")
                
            except Exception as e:
                print(f"Ошибка получения атрибутов элемента {i+1}: {e}")
                
        return clickable_elements
