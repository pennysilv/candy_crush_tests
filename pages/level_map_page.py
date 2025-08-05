"""
Page Object для карты уровней Candy Crush Saga
"""

from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage

class LevelMapPage(BasePage):
    """Класс для работы с картой уровней"""
    
    # Локаторы элементов карты уровней
    LEVEL_BUTTON_LOCATORS = [
        (AppiumBy.XPATH, "//*[contains(@content-desc, 'Level') or contains(@content-desc, 'level')]"),
        (AppiumBy.XPATH, "//*[contains(@text, 'Level') or contains(@text, 'level')]"),
        (AppiumBy.XPATH, "//*[contains(@resource-id, 'level')]"),
        (AppiumBy.XPATH, "//*[contains(@class, 'Button') and @clickable='true']"),
    ]
    
    BACK_BUTTON_LOCATORS = [
        (AppiumBy.XPATH, "//*[contains(@content-desc, 'Back') or contains(@content-desc, 'back')]"),
        (AppiumBy.XPATH, "//*[contains(@text, 'Back')]"),
        (AppiumBy.XPATH, "//*[contains(@resource-id, 'back')]"),
    ]
    
    def __init__(self, driver):
        super().__init__(driver)
        
    def is_displayed(self):
        """Проверить что карта уровней отображается"""
        print("🔍 Проверяем отображение карты уровней...")
        
        # Ищем кнопки уровней
        level_buttons = self.find_level_buttons()
        back_button = self.find_back_button()
        
        is_displayed = len(level_buttons) > 0 or back_button is not None
        
        if is_displayed:
            print("✅ Карта уровней отображается")
        else:
            print("❌ Карта уровней не найдена")
            
        return is_displayed
    
    def find_level_buttons(self):
        """Найти кнопки уровней"""
        print("🔍 Ищем кнопки уровней...")
        
        all_buttons = []
        for i, (by, value) in enumerate(self.LEVEL_BUTTON_LOCATORS):
            elements = self.find_elements(by, value, timeout=3)
            if elements:
                print(f"✅ Найдено {len(elements)} кнопок уровней способом {i+1}")
                all_buttons.extend(elements)
                break
                
        if not all_buttons:
            print("❌ Кнопки уровней не найдены")
            
        return all_buttons
    
    def find_back_button(self):
        """Найти кнопку Назад"""
        print("🔍 Ищем кнопку Назад...")
        
        for i, (by, value) in enumerate(self.BACK_BUTTON_LOCATORS):
            element = self.find_element(by, value, timeout=3)
            if element:
                print(f"✅ Кнопка Назад найдена способом {i+1}")
                return element
                
        print("❌ Кнопка Назад не найдена")
        return None
    
    def click_first_level(self):
        """Кликнуть на первый доступный уровень"""
        print("👆 Пытаемся кликнуть на первый уровень...")
        
        level_buttons = self.find_level_buttons()
        if level_buttons:
            try:
                level_buttons[0].click()
                print("✅ Кликнули на первый уровень")
                return True
            except Exception as e:
                print(f"❌ Ошибка клика на уровень: {e}")
                return False
        else:
            print("❌ Нет доступных уровней для клика")
            return False
    
    def click_back(self):
        """Кликнуть на кнопку Назад"""
        back_button = self.find_back_button()
        if back_button:
            try:
                back_button.click()
                print("✅ Кликнули на кнопку Назад")
                return True
            except Exception as e:
                print(f"❌ Ошибка клика на Назад: {e}")
                return False
        return False
    
    def get_levels_count(self):
        """Получить количество доступных уровней"""
        level_buttons = self.find_level_buttons()
        count = len(level_buttons)
        print(f"📊 Найдено уровней: {count}")
        return count
    
    def get_map_info(self):
        """Получить информацию о карте уровней"""
        info = {
            'levels_count': self.get_levels_count(),
            'has_back_button': self.find_back_button() is not None,
            'clickable_elements_count': len(self.get_all_clickable_elements())
        }
        
        print(f"📊 Информация о карте уровней:")
        print(f"   - Количество уровней: {info['levels_count']}")
        print(f"   - Есть кнопка Назад: {info['has_back_button']}")
        print(f"   - Кликабельных элементов: {info['clickable_elements_count']}")
        
        return info
