"""
Page Object для игрового поля Candy Crush Saga
"""

from appium.webdriver.common.appiumby import AppiumBy
from .base_page import BasePage

class GameBoardPage(BasePage):
    """Класс для работы с игровым полем"""
    
    # Локаторы игровых элементов
    GAME_BOARD_LOCATORS = [
        (AppiumBy.XPATH, "//*[contains(@resource-id, 'game') or contains(@resource-id, 'board')]"),
        (AppiumBy.XPATH, "//*[contains(@class, 'game') or contains(@class, 'board')]"),
        (AppiumBy.XPATH, "//*[contains(@content-desc, 'game') or contains(@content-desc, 'board')]"),
    ]
    
    MOVES_COUNTER_LOCATORS = [
        (AppiumBy.XPATH, "//*[contains(@text, 'Moves') or contains(@text, 'moves')]"),
        (AppiumBy.XPATH, "//*[contains(@resource-id, 'moves')]"),
        (AppiumBy.XPATH, "//*[contains(@content-desc, 'moves')]"),
    ]
    
    SCORE_LOCATORS = [
        (AppiumBy.XPATH, "//*[contains(@text, 'Score') or contains(@text, 'score')]"),
        (AppiumBy.XPATH, "//*[contains(@resource-id, 'score')]"),
        (AppiumBy.XPATH, "//*[contains(@content-desc, 'score')]"),
    ]
    
    PAUSE_BUTTON_LOCATORS = [
        (AppiumBy.XPATH, "//*[contains(@content-desc, 'pause') or contains(@content-desc, 'Pause')]"),
        (AppiumBy.XPATH, "//*[contains(@text, 'Pause')]"),
        (AppiumBy.XPATH, "//*[contains(@resource-id, 'pause')]"),
    ]
    
    def __init__(self, driver):
        super().__init__(driver)
        
    def is_displayed(self):
        """Проверить что игровое поле отображается"""
        print("🔍 Проверяем отображение игрового поля...")
        
        # Ищем признаки игрового поля
        game_board = self.find_game_board()
        moves_counter = self.find_moves_counter()
        score = self.find_score()
        
        # Если нашли хотя бы один элемент игры
        is_displayed = any([game_board, moves_counter, score])
        
        if is_displayed:
            print("✅ Игровое поле отображается")
        else:
            print("❌ Игровое поле не найдено")
            
        return is_displayed
    
    def find_game_board(self):
        """Найти игровое поле"""
        print("🔍 Ищем игровое поле...")
        
        for i, (by, value) in enumerate(self.GAME_BOARD_LOCATORS):
            element = self.find_element(by, value, timeout=3)
            if element:
                print(f"✅ Игровое поле найдено способом {i+1}")
                return element
                
        print("❌ Игровое поле не найдено")
        return None
    
    def find_moves_counter(self):
        """Найти счетчик ходов"""
        print("🔍 Ищем счетчик ходов...")
        
        for i, (by, value) in enumerate(self.MOVES_COUNTER_LOCATORS):
            element = self.find_element(by, value, timeout=3)
            if element:
                print(f"✅ Счетчик ходов найден способом {i+1}")
                return element
                
        print("❌ Счетчик ходов не найден")
        return None
    
    def find_score(self):
        """Найти счет"""
        print("🔍 Ищем счет...")
        
        for i, (by, value) in enumerate(self.SCORE_LOCATORS):
            element = self.find_element(by, value, timeout=3)
            if element:
                print(f"✅ Счет найден способом {i+1}")
                return element
                
        print("❌ Счет не найден")
        return None
    
    def get_moves_count(self):
        """Получить количество оставшихся ходов"""
        moves_element = self.find_moves_counter()
        if moves_element:
            try:
                moves_text = moves_element.get_attribute('text') or ''
                # Извлекаем число из текста
                import re
                numbers = re.findall(r'\d+', moves_text)
                if numbers:
                    moves = int(numbers[0])
                    print(f"📊 Количество ходов: {moves}")
                    return moves
            except Exception as e:
                print(f"❌ Ошибка получения ходов: {e}")
        
        print("❌ Не удалось получить количество ходов")
        return None
    
    def get_score(self):
        """Получить текущий счет"""
        score_element = self.find_score()
        if score_element:
            try:
                score_text = score_element.get_attribute('text') or ''
                # Извлекаем число из текста
                import re
                numbers = re.findall(r'[\d,]+', score_text)
                if numbers:
                    # Убираем запятые и конвертируем в число
                    score = int(numbers[0].replace(',', ''))
                    print(f"📊 Текущий счет: {score}")
                    return score
            except Exception as e:
                print(f"❌ Ошибка получения счета: {e}")
        
        print("❌ Не удалось получить счет")
        return None
    
    def make_random_move(self):
        """Сделать случайный ход на игровом поле"""
        print("🎮 Пытаемся сделать случайный ход...")
        
        # Получаем размер экрана
        size = self.driver.get_window_size()
        
        # Предполагаем что игровое поле занимает центральную часть экрана
        center_x = size['width'] // 2
        center_y = size['height'] // 2
        
        # Делаем свайп в центре экрана (имитация хода)
        start_x = center_x - 50
        start_y = center_y
        end_x = center_x + 50
        end_y = center_y
        
        try:
            self.driver.swipe(start_x, start_y, end_x, end_y, 500)
            print("✅ Сделали свайп на игровом поле")
            return True
        except Exception as e:
            print(f"❌ Ошибка при свайпе: {e}")
            return False
    
    def click_pause(self):
        """Кликнуть на кнопку паузы"""
        print("⏸️ Пытаемся поставить на паузу...")
        
        for i, (by, value) in enumerate(self.PAUSE_BUTTON_LOCATORS):
            if self.click_element(by, value, timeout=3):
                print(f"✅ Кликнули на паузу способом {i+1}")
                return True
                
        print("❌ Кнопка паузы не найдена")
        return False
    
    def get_game_state_info(self):
        """Получить информацию о состоянии игры"""
        info = {
            'has_game_board': self.find_game_board() is not None,
            'has_moves_counter': self.find_moves_counter() is not None,
            'has_score': self.find_score() is not None,
            'moves_count': self.get_moves_count(),
            'current_score': self.get_score(),
            'clickable_elements_count': len(self.get_all_clickable_elements())
        }
        
        print(f"📊 Состояние игры:")
        print(f"   - Есть игровое поле: {info['has_game_board']}")
        print(f"   - Есть счетчик ходов: {info['has_moves_counter']}")
        print(f"   - Есть счет: {info['has_score']}")
        print(f"   - Количество ходов: {info['moves_count']}")
        print(f"   - Текущий счет: {info['current_score']}")
        print(f"   - Кликабельных элементов: {info['clickable_elements_count']}")
        
        return info
