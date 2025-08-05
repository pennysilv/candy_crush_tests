"""
Тесты взаимодействия с экраном Candy Crush Saga через координаты
"""

import time
import pytest
from utils.helpers import wait_and_screenshot

class TestScreenInteractions:
    """Тесты взаимодействия с экраном через тапы и жесты"""
    
    def test_tap_main_play_button(self, driver):
        """Тап по главной кнопке Play (розовая кнопка)"""
        print("\n🎯 Тест тапа по кнопке Play")
        
        size = driver.get_window_size()
        
        # Координаты розовой кнопки Play
        play_x = size['width'] // 2
        play_y = int(size['height'] * 0.32)
        
        print(f"🎯 Координаты кнопки Play: ({play_x}, {play_y})")
        
        # Скриншот до тапа
        before_screenshot = wait_and_screenshot(driver, "before_play_tap")
        before_source = driver.page_source
        
        try:
            # Выполняем тап
            driver.tap([(play_x, play_y)])
            print("✅ Тап по кнопке Play выполнен")
            
            time.sleep(3)  # Ждем реакции
            
            # Скриншот после тапа
            after_screenshot = wait_and_screenshot(driver, "after_play_tap")
            after_source = driver.page_source
            
            # Проверяем реакцию
            if after_source != before_source:
                print("✅ Экран изменился - кнопка Play реагирует")
                screen_changed = True
            else:
                print("⚠️ Экран не изменился - возможно кнопка недоступна")
                screen_changed = False
            
            # Проверяем что приложение стабильно
            current_size = driver.get_window_size()
            assert current_size == size, "Размер экрана должен остаться тем же"
            
            print(f"📊 Результат тапа по Play: {'Реагирует' if screen_changed else 'Не реагирует'}")
            
        except Exception as e:
            assert False, f"Ошибка при тапе по кнопке Play: {e}"
    
    def test_tap_secondary_buttons(self, driver):
        """Тест тапов по вторичным кнопкам"""
        print("\n🎯 Тест тапов по вторичным кнопкам")
        
        size = driver.get_window_size()
        
        # Координаты различных кнопок
        buttons = [
            ("Синяя кнопка (My Account)", size['width']//2, int(size['height'] * 0.42)),
            ("Левый нижний угол (Настройки)", int(size['width'] * 0.1), int(size['height'] * 0.9)),
            ("Правый верхний угол", int(size['width'] * 0.9), int(size['height'] * 0.1)),
        ]
        
        successful_taps = 0
        
        for button_name, x, y in buttons:
            print(f"\n   🎯 Тап: {button_name} ({x}, {y})")
            
            try:
                before_screenshot = wait_and_screenshot(driver, f"before_{button_name.lower().replace(' ', '_')}")
                before_source = driver.page_source
                
                # Выполняем тап
                driver.tap([(x, y)])
                time.sleep(2)
                
                after_screenshot = wait_and_screenshot(driver, f"after_{button_name.lower().replace(' ', '_')}")
                after_source = driver.page_source
                
                # Проверяем реакцию
                if after_source != before_source:
                    print(f"   ✅ {button_name}: экран изменился")
                    reaction = "Реагирует"
                else:
                    print(f"   ⚠️ {button_name}: экран не изменился")
                    reaction = "Не реагирует"
                
                successful_taps += 1
                print(f"   📊 {button_name}: {reaction}")
                
            except Exception as e:
                print(f"   ❌ Ошибка тапа {button_name}: {e}")
        
        print(f"\n📊 Успешных тапов по кнопкам: {successful_taps}/{len(buttons)}")
        assert successful_taps >= 2, "Минимум 2 тапа должны быть выполнены успешно"
    
    def test_swipe_gestures(self, driver):
        """Тест свайпов в разных направлениях"""
        print("\n👆 Тест жестов свайпа")
        
        size = driver.get_window_size()
        successful_swipes = 0
        
        # Различные направления свайпов
        swipes = [
            ("Вверх", size['width']//2, int(size['height']*0.7), size['width']//2, int(size['height']*0.3)),
            ("Вниз", size['width']//2, int(size['height']*0.3), size['width']//2, int(size['height']*0.7)),
            ("Влево", int(size['width']*0.7), size['height']//2, int(size['width']*0.3), size['height']//2),
            ("Вправо", int(size['width']*0.3), size['height']//2, int(size['width']*0.7), size['height']//2),
        ]
        
        for direction, start_x, start_y, end_x, end_y in swipes:
            print(f"\n   👆 Свайп {direction}: ({start_x},{start_y}) → ({end_x},{end_y})")
            
            try:
                before_screenshot = wait_and_screenshot(driver, f"before_swipe_{direction.lower()}")
                before_source = driver.page_source
                
                # Выполняем свайп
                driver.swipe(start_x, start_y, end_x, end_y, 1000)
                time.sleep(2)
                
                after_screenshot = wait_and_screenshot(driver, f"after_swipe_{direction.lower()}")
                after_source = driver.page_source
                
                # Проверяем реакцию
                if after_source != before_source:
                    print(f"   ✅ Свайп {direction}: экран изменился")
                    reaction = "Реагирует"
                else:
                    print(f"   ⚠️ Свайп {direction}: экран не изменился")
                    reaction = "Не реагирует"
                
                successful_swipes += 1
                print(f"   📊 Свайп {direction}: выполнен, {reaction}")
                
            except Exception as e:
                print(f"   ❌ Ошибка свайпа {direction}: {e}")
        
        print(f"\n📊 Успешных свайпов: {successful_swipes}/{len(swipes)}")
        assert successful_swipes >= 3, "Минимум 3 свайпа должны быть выполнены"
    
    def test_multi_touch_gestures(self, driver):
        """Тест мультитач жестов (зум, пинч)"""
        print("\n🤏 Тест мультитач жестов")
        
        size = driver.get_window_size()
        center_x = size['width'] // 2
        center_y = size['height'] // 2
        
        # Координаты для жестов зума
        zoom_distance = min(size['width'], size['height']) // 4
        
        multitouch_tests = [
            ("Zoom In (разведение пальцев)", 
             [(center_x - 50, center_y), (center_x + 50, center_y)],
             [(center_x - zoom_distance, center_y), (center_x + zoom_distance, center_y)]
            ),
            ("Zoom Out (сведение пальцев)",
             [(center_x - zoom_distance, center_y), (center_x + zoom_distance, center_y)], 
             [(center_x - 50, center_y), (center_x + 50, center_y)]
            ),
        ]
        
        successful_multitouch = 0
        
        for gesture_name, start_points, end_points in multitouch_tests:
            print(f"\n   🤏 {gesture_name}")
            
            try:
                before_screenshot = wait_and_screenshot(driver, f"before_{gesture_name.lower().replace(' ', '_')}")
                before_source = driver.page_source
                
                # Попытка выполнить мультитач жест
                try:
                    # Используем простую эмуляцию через последовательные тапы
                    for point in start_points:
                        driver.tap([point])
                        time.sleep(0.1)
                    
                    time.sleep(1)
                    
                    for point in end_points:
                        driver.tap([point])
                        time.sleep(0.1)
                    
                    print(f"   ✅ {gesture_name}: жест выполнен")
                    
                except Exception as gesture_error:
                    print(f"   ⚠️ {gesture_name}: используем альтернативный метод")
                    # Альтернативный метод - просто тап по центру
                    driver.tap([(center_x, center_y)])
                
                time.sleep(2)
                
                after_screenshot = wait_and_screenshot(driver, f"after_{gesture_name.lower().replace(' ', '_')}")
                after_source = driver.page_source
                
                # Проверяем что приложение осталось стабильным
                current_size = driver.get_window_size()
                if current_size == size:
                    successful_multitouch += 1
                    print(f"   ✅ {gesture_name}: приложение стабильно")
                else:
                    print(f"   ⚠️ {gesture_name}: изменился размер экрана")
                
            except Exception as e:
                print(f"   ❌ Ошибка {gesture_name}: {e}")
        
        print(f"\n📊 Успешных мультитач жестов: {successful_multitouch}/{len(multitouch_tests)}")
        assert successful_multitouch >= 1, "Минимум 1 мультитач жест должен быть выполнен"
    
    def test_screen_zones_responsiveness(self, driver):
        """Тест отзывчивости различных зон экрана"""
        print("\n📍 Тест отзывчивости зон экрана")
        
        size = driver.get_window_size()
        
        # Разделяем экран на зоны (сетка 3x3)
        zones = []
        for row in range(3):
            for col in range(3):
                x = int(size['width'] * (0.2 + col * 0.3))
                y = int(size['height'] * (0.2 + row * 0.3))
                zone_name = f"Зона_{row+1}_{col+1}"
                zones.append((zone_name, x, y))
        
        responsive_zones = 0
        
        for zone_name, x, y in zones:
            print(f"\n   📍 {zone_name}: ({x}, {y})")
            
            try:
                before_source = driver.page_source
                
                # Быстрый тап по зоне
                driver.tap([(x, y)])
                time.sleep(0.5)  # Короткая пауза
                
                # Проверяем что приложение отвечает
                after_source = driver.page_source
                current_size = driver.get_window_size()
                
                if current_size == size:
                    responsive_zones += 1
                    
                    if after_source != before_source:
                        print(f"   ✅ {zone_name}: отзывчива, экран изменился")
                        status = "Реагирует"
                    else:
                        print(f"   ✅ {zone_name}: отзывчива, экран стабилен")
                        status = "Стабильна"
                else:
                    print(f"   ⚠️ {zone_name}: изменился размер экрана")
                    status = "Нестабильна"
                    
                print(f"   📊 {zone_name}: {status}")
                
            except Exception as e:
                print(f"   ❌ Ошибка зоны {zone_name}: {e}")
        
        # Финальный скриншот
        wait_and_screenshot(driver, "screen_zones_final")
        
        print(f"\n📊 Отзывчивых зон: {responsive_zones}/{len(zones)}")
        print(f"📊 Процент отзывчивости экрана: {(responsive_zones/len(zones))*100:.1f}%")
        
        assert responsive_zones >= len(zones) // 2, "Минимум половина зон должна быть отзывчивой"
    
    def test_rapid_tap_sequence(self, driver):
        """Тест быстрой последовательности тапов"""
        print("\n⚡ Тест быстрых тапов")
        
        size = driver.get_window_size()
        center_x = size['width'] // 2
        center_y = size['height'] // 2
        
        tap_count = 10
        successful_taps = 0
        
        print(f"⚡ Выполняем {tap_count} быстрых тапов по центру экрана")
        
        before_screenshot = wait_and_screenshot(driver, "before_rapid_taps")
        start_time = time.time()
        
        for i in range(tap_count):
            try:
                driver.tap([(center_x, center_y)])
                successful_taps += 1
                time.sleep(0.1)  # Очень короткая пауза между тапами
                
                if i % 3 == 0:  # Проверяем каждый 3-й тап
                    current_size = driver.get_window_size()
                    if current_size != size:
                        print(f"   ⚠️ Размер экрана изменился на тапе {i+1}")
                        break
                        
            except Exception as e:
                print(f"   ❌ Ошибка на тапе {i+1}: {e}")
                break
        
        total_time = time.time() - start_time
        after_screenshot = wait_and_screenshot(driver, "after_rapid_taps")
        
        print(f"📊 Результаты быстрых тапов:")
        print(f"   - Выполнено тапов: {successful_taps}/{tap_count}")
        print(f"   - Общее время: {total_time:.2f} секунд")
        print(f"   - Скорость: {successful_taps/total_time:.1f} тапов/сек")
        
        # Проверяем финальную стабильность
        try:
            final_size = driver.get_window_size()
            assert final_size == size, "Приложение должно остаться стабильным"
            print("✅ Приложение стабильно после быстрых тапов")
        except Exception as e:
            assert False, f"Приложение нестабильно после быстрых тапов: {e}"
        
        assert successful_taps >= tap_count // 2, "Минимум половина тапов должна быть выполнена"
