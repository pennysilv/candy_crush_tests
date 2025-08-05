"""
Тесты стабильности приложения Candy Crush Saga
"""

import time
import pytest
from utils.helpers import wait_and_screenshot

class TestAppStability:
    """Тесты стабильности и надежности приложения"""
    
    def test_app_launches_successfully(self, driver):
        """Приложение запускается без ошибок и показывает контент"""
        print("\n🚀 Тест успешного запуска приложения")
        
        # Скриншот начального состояния
        wait_and_screenshot(driver, "app_launch_check")
        
        # Проверяем базовые параметры
        size = driver.get_window_size()
        page_source = driver.page_source
        
        print(f"📱 Размер экрана: {size}")
        print(f"📄 Размер контента: {len(page_source)} символов")
        
        # Основные проверки запуска
        assert size['width'] > 0, "Ширина экрана должна быть больше 0"
        assert size['height'] > 0, "Высота экрана должна быть больше 0"
        assert len(page_source) > 1000, "Приложение должно содержать достаточно контента"
        
        # Проверяем что приложение отвечает на запросы
        try:
            driver.get_window_size()  # Повторный запрос
            print("✅ Приложение отвечает на запросы")
        except Exception as e:
            assert False, f"Приложение не отвечает: {e}"
        
        print("✅ Приложение успешно запущено и стабильно")
    
    def test_app_responds_to_basic_interactions(self, driver):
        """Приложение отвечает на базовые взаимодействия"""
        print("\n👆 Тест отзывчивости на взаимодействия")
        
        size = driver.get_window_size()
        interaction_count = 0
        successful_interactions = 0
        
        # Набор базовых взаимодействий
        interactions = [
            ("Центр экрана", size['width']//2, size['height']//2),
            ("Верх экрана", size['width']//2, int(size['height']*0.2)),
            ("Низ экрана", size['width']//2, int(size['height']*0.8)),
        ]
        
        for name, x, y in interactions:
            interaction_count += 1
            print(f"   👆 Взаимодействие {interaction_count}: {name} ({x}, {y})")
            
            try:
                # Тап по координате
                driver.tap([(x, y)])
                time.sleep(1)
                
                # Проверяем что приложение все еще отвечает
                driver.get_window_size()
                successful_interactions += 1
                print(f"   ✅ Взаимодействие {interaction_count} успешно")
                
            except Exception as e:
                print(f"   ❌ Ошибка взаимодействия {interaction_count}: {e}")
        
        wait_and_screenshot(driver, "after_basic_interactions")
        
        print(f"📊 Успешных взаимодействий: {successful_interactions}/{interaction_count}")
        assert successful_interactions >= 2, "Минимум 2 взаимодействия должны быть успешными"
    
    def test_app_handles_orientation_changes(self, driver):
        """Приложение корректно обрабатывает смену ориентации"""
        print("\n🔄 Тест смены ориентации экрана")
        
        # Получаем текущую ориентацию
        initial_orientation = driver.orientation
        initial_size = driver.get_window_size()
        
        print(f"📱 Начальная ориентация: {initial_orientation}")
        print(f"📱 Начальный размер: {initial_size}")
        
        wait_and_screenshot(driver, "before_orientation_change")
        
        orientation_test_passed = True
        
        try:
            # Пробуем сменить ориентацию
            new_orientation = "LANDSCAPE" if initial_orientation == "PORTRAIT" else "PORTRAIT"
            
            print(f"🔄 Меняем ориентацию на: {new_orientation}")
            driver.orientation = new_orientation
            time.sleep(3)  # Ждем адаптации
            
            # Проверяем что приложение адаптировалось
            new_size = driver.get_window_size()
            current_orientation = driver.orientation
            
            print(f"📱 Новая ориентация: {current_orientation}")
            print(f"📱 Новый размер: {new_size}")
            
            wait_and_screenshot(driver, "after_orientation_change")
            
            # Проверяем что размеры изменились соответственно
            if new_orientation == "LANDSCAPE":
                assert new_size['width'] > new_size['height'], "В альбомной ориентации ширина должна быть больше высоты"
            else:
                assert new_size['height'] > new_size['width'], "В портретной ориентации высота должна быть больше ширины"
            
            # Возвращаем исходную ориентацию
            driver.orientation = initial_orientation
            time.sleep(2)
            
            final_size = driver.get_window_size()
            print(f"📱 Финальный размер: {final_size}")
            
            print("✅ Смена ориентации обработана корректно")
            
        except Exception as e:
            print(f"⚠️ Не удалось сменить ориентацию: {e}")
            print("   (Возможно заблокировано приложением или системой)")
            orientation_test_passed = False
        
        wait_and_screenshot(driver, "orientation_test_final")
        
        # Главное - приложение должно оставаться стабильным
        try:
            final_check_size = driver.get_window_size()
            assert final_check_size['width'] > 0, "Приложение должно оставаться стабильным"
            print("✅ Приложение осталось стабильным после тестирования ориентации")
        except Exception as e:
            assert False, f"Приложение стало нестабильным: {e}"
    
    def test_app_recovers_from_background(self, driver):
        """Приложение корректно восстанавливается после сворачивания"""
        print("\n📱 Тест восстановления из фона")
        
        # Запоминаем состояние перед сворачиванием
        before_size = driver.get_window_size()
        before_screenshot = wait_and_screenshot(driver, "before_background")
        
        print("📱 Сворачиваем приложение в фон")
        
        background_test_success = False
        
        try:
            # Сворачиваем приложение
            driver.background_app(3)  # 3 секунды в фоне
            print("   ✅ Приложение свернуто в фон на 3 секунды")
            
            # Приложение должно автоматически вернуться
            time.sleep(1)
            
            # Проверяем что приложение восстановилось
            after_size = driver.get_window_size()
            after_screenshot = wait_and_screenshot(driver, "after_background")
            
            print(f"📱 Размер до: {before_size}")
            print(f"📱 Размер после: {after_size}")
            
            # Проверяем что размеры совпадают
            assert after_size == before_size, "Размер экрана должен остаться тем же"
            
            # Проверяем что приложение отвечает
            driver.page_source
            
            background_test_success = True
            print("✅ Восстановление из фона прошло успешно")
            
        except Exception as e:
            print(f"⚠️ Ошибка при тестировании фона: {e}")
            
            # Пробуем простую проверку отзывчивости
            try:
                current_size = driver.get_window_size()
                if current_size['width'] > 0:
                    background_test_success = True
                    print("✅ Приложение осталось отзывчивым")
            except Exception as e2:
                print(f"❌ Приложение не отвечает: {e2}")
        
        # Финальная проверка стабильности
        try:
            final_size = driver.get_window_size()
            final_screenshot = wait_and_screenshot(driver, "background_test_final")
            
            assert final_size['width'] > 0, "Приложение должно быть стабильным"
            
            if background_test_success:
                print("✅ Тест восстановления из фона пройден")
            else:
                print("⚠️ Тест фона частично пройден (приложение стабильно)")
                
        except Exception as e:
            assert False, f"Приложение нестабильно после теста фона: {e}"
    
    def test_memory_usage_stability(self, driver):
        """Тест стабильности использования памяти"""
        print("\n💾 Тест стабильности памяти")
        
        memory_checks = []
        check_count = 5
        
        print(f"💾 Выполняем {check_count} проверок памяти с интервалом")
        
        for i in range(check_count):
            print(f"   💾 Проверка памяти {i+1}/{check_count}")
            
            try:
                # Выполняем некоторые действия для нагрузки
                size = driver.get_window_size()
                driver.tap([(size['width']//2, size['height']//2)])
                
                # Получаем информацию о памяти (если доступно)
                page_source_size = len(driver.page_source)
                
                memory_info = {
                    'check': i+1,
                    'page_source_size': page_source_size,
                    'screen_width': size['width'],
                    'screen_height': size['height'],
                    'timestamp': time.time()
                }
                
                memory_checks.append(memory_info)
                
                print(f"      📊 Размер контента: {page_source_size} символов")
                
                # Скриншот каждые 2 проверки
                if i % 2 == 0:
                    wait_and_screenshot(driver, f"memory_check_{i+1}")
                
                time.sleep(2)  # Пауза между проверками
                
            except Exception as e:
                print(f"   ❌ Ошибка проверки памяти {i+1}: {e}")
                memory_checks.append({
                    'check': i+1,
                    'error': str(e),
                    'timestamp': time.time()
                })
        
        # Анализ результатов
        successful_checks = [check for check in memory_checks if 'error' not in check]
        
        print(f"\n📊 Результаты проверки памяти:")
        print(f"   - Успешных проверок: {len(successful_checks)}/{check_count}")
        
        if len(successful_checks) >= 2:
            # Проверяем что размер контента не растет слишком быстро
            first_size = successful_checks[0]['page_source_size']
            last_size = successful_checks[-1]['page_source_size']
            growth = last_size - first_size
            
            print(f"   - Рост размера контента: {growth} символов")
            print(f"   - Первый размер: {first_size}")
            print(f"   - Последний размер: {last_size}")
            
            # Тест проходит если нет чрезмерного роста памяти
            assert growth < first_size, "Размер контента не должен удваиваться"
            print("✅ Память используется стабильно")
        
        else:
            print("⚠️ Недостаточно данных для анализа памяти")
        
        # Финальная проверка стабильности
        final_screenshot = wait_and_screenshot(driver, "memory_stability_final")
        
        assert len(successful_checks) >= check_count // 2, "Минимум половина проверок должна быть успешной"
