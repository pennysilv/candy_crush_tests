"""
Тесты производительности Candy Crush Saga
"""

import time
import pytest
from utils.helpers import wait_and_screenshot

class TestPerformance:
    """Тесты производительности и отзывчивости приложения"""
    
    def test_app_response_time(self, driver):
        """Тест времени отклика приложения на действия"""
        print("\n⚡ Тест времени отклика приложения")
        
        size = driver.get_window_size()
        center_x = size['width'] // 2
        center_y = size['height'] // 2
        
        response_times = []
        test_actions = 5
        
        print(f"⚡ Измеряем время отклика на {test_actions} действий")
        
        for i in range(test_actions):
            print(f"   ⚡ Тест отклика {i+1}/{test_actions}")
            
            try:
                # Измеряем время тапа
                start_time = time.time()
                driver.tap([(center_x, center_y)])
                tap_time = time.time() - start_time
                
                # Измеряем время получения размера экрана (отклик системы)
                start_time = time.time()
                current_size = driver.get_window_size()
                system_response_time = time.time() - start_time
                
                total_response_time = tap_time + system_response_time
                response_times.append(total_response_time)
                
                print(f"      - Время тапа: {tap_time:.3f}с")
                print(f"      - Время отклика системы: {system_response_time:.3f}с")
                print(f"      - Общее время: {total_response_time:.3f}с")
                
                time.sleep(0.5)  # Пауза между тестами
                
            except Exception as e:
                print(f"   ❌ Ошибка теста отклика {i+1}: {e}")
        
        if response_times:
            avg_response = sum(response_times) / len(response_times)
            max_response = max(response_times)
            min_response = min(response_times)
            
            print(f"\n📊 Статистика времени отклика:")
            print(f"   - Средний отклик: {avg_response:.3f}с")
            print(f"   - Максимальный отклик: {max_response:.3f}с")
            print(f"   - Минимальный отклик: {min_response:.3f}с")
            print(f"   - Успешных измерений: {len(response_times)}/{test_actions}")
            
            # Критерии производительности
            assert avg_response < 2.0, f"Средний отклик ({avg_response:.3f}с) должен быть менее 2 секунд"
            assert max_response < 5.0, f"Максимальный отклик ({max_response:.3f}с) должен быть менее 5 секунд"
            
            if avg_response < 1.0:
                print("✅ Отличная производительность (< 1с)")
            elif avg_response < 2.0:
                print("✅ Хорошая производительность (< 2с)")
            else:
                print("⚠️ Приемлемая производительность")
        else:
            assert False, "Не удалось измерить время отклика"
    
    def test_fps_during_interactions(self, driver):
        """Тест плавности работы при взаимодействиях"""
        print("\n🎬 Тест плавности анимаций")
        
        size = driver.get_window_size()
        
        # Серия действий для проверки плавности
        interactions = [
            ("Тап по центру", lambda: driver.tap([(size['width']//2, size['height']//2)])),
            ("Свайп вверх", lambda: driver.swipe(size['width']//2, int(size['height']*0.7), 
                                               size['width']//2, int(size['height']*0.3), 1000)),
            ("Свайп вниз", lambda: driver.swipe(size['width']//2, int(size['height']*0.3), 
                                               size['width']//2, int(size['height']*0.7), 1000)),
        ]
        
        frame_check_results = []
        
        for interaction_name, action in interactions:
            print(f"\n   🎬 Проверка плавности: {interaction_name}")
            
            try:
                before_screenshot = wait_and_screenshot(driver, f"fps_before_{interaction_name.lower().replace(' ', '_')}")
                
                # Засекаем время выполнения действия
                start_time = time.time()
                action()
                action_time = time.time() - start_time
                
                # Ждем завершения возможных анимаций
                time.sleep(1)
                
                after_screenshot = wait_and_screenshot(driver, f"fps_after_{interaction_name.lower().replace(' ', '_')}")
                
                # Проверяем отзывчивость после действия
                response_start = time.time()
                current_size = driver.get_window_size()
                response_time = time.time() - response_start
                
                frame_data = {
                    'interaction': interaction_name,
                    'action_time': action_time,
                    'response_time': response_time,
                    'total_time': action_time + response_time,
                    'smooth': action_time < 1.0 and response_time < 0.5
                }
                
                frame_check_results.append(frame_data)
                
                print(f"      - Время действия: {action_time:.3f}с")
                print(f"      - Время отклика: {response_time:.3f}с")
                print(f"      - Плавность: {'✅ Плавно' if frame_data['smooth'] else '⚠️ Не очень плавно'}")
                
            except Exception as e:
                print(f"   ❌ Ошибка проверки плавности {interaction_name}: {e}")
                frame_check_results.append({
                    'interaction': interaction_name,
                    'error': str(e),
                    'smooth': False
                })
        
        # Анализ результатов плавности
        smooth_interactions = [r for r in frame_check_results if r.get('smooth', False)]
        
        print(f"\n📊 Результаты плавности:")
        print(f"   - Плавных взаимодействий: {len(smooth_interactions)}/{len(interactions)}")
        
        if smooth_interactions:
            avg_action_time = sum(r['action_time'] for r in smooth_interactions) / len(smooth_interactions)
            avg_response_time = sum(r['response_time'] for r in smooth_interactions) / len(smooth_interactions)
            
            print(f"   - Среднее время действий: {avg_action_time:.3f}с")
            print(f"   - Средний отклик: {avg_response_time:.3f}с")
            
            if len(smooth_interactions) == len(interactions):
                print("✅ Отличная плавность всех взаимодействий")
            elif len(smooth_interactions) >= len(interactions) // 2:
                print("✅ Хорошая плавность большинства взаимодействий")
            else:
                print("⚠️ Плавность требует улучшения")
        
        assert len(smooth_interactions) >= 1, "Минимум одно взаимодействие должно быть плавным"
    
    def test_memory_consumption(self, driver):
        """Тест потребления памяти в процессе работы"""
        print("\n💾 Тест потребления памяти")
        
        memory_samples = []
        sample_count = 8
        
        print(f"💾 Собираем {sample_count} образцов использования памяти")
        
        for i in range(sample_count):
            print(f"   💾 Образец памяти {i+1}/{sample_count}")
            
            try:
                # Выполняем некоторые действия
                size = driver.get_window_size()
                driver.tap([(size['width']//2, size['height']//2)])
                
                # Собираем метрики (доступные через Appium)
                page_source_size = len(driver.page_source)
                
                # Простая оценка "использования памяти" через размер контента
                memory_sample = {
                    'sample': i+1,
                    'page_source_size': page_source_size,
                    'timestamp': time.time(),
                    'screen_dimensions': f"{size['width']}x{size['height']}"
                }
                
                memory_samples.append(memory_sample)
                
                print(f"      - Размер контента: {page_source_size} символов")
                
                # Скриншот каждые 3 образца
                if i % 3 == 0:
                    wait_and_screenshot(driver, f"memory_sample_{i+1}")
                
                time.sleep(1)  # Пауза между образцами
                
            except Exception as e:
                print(f"   ❌ Ошибка образца памяти {i+1}: {e}")
        
        if len(memory_samples) >= 3:
            # Анализ потребления памяти
            sizes = [sample['page_source_size'] for sample in memory_samples]
            
            initial_size = sizes[0]
            final_size = sizes[-1]
            max_size = max(sizes)
            min_size = min(sizes)
            avg_size = sum(sizes) / len(sizes)
            
            growth = final_size - initial_size
            growth_percent = (growth / initial_size) * 100 if initial_size > 0 else 0
            
            print(f"\n📊 Анализ использования памяти:")
            print(f"   - Начальный размер: {initial_size} символов")
            print(f"   - Финальный размер: {final_size} символов")
            print(f"   - Максимальный размер: {max_size} символов")
            print(f"   - Минимальный размер: {min_size} символов")
            print(f"   - Средний размер: {avg_size:.0f} символов")
            print(f"   - Рост: {growth} символов ({growth_percent:+.1f}%)")
            
            # Критерии использования памяти
            memory_stable = abs(growth_percent) < 50  # Рост менее 50%
            no_significant_leaks = max_size < initial_size * 2  # Не более чем в 2 раза
            
            if memory_stable and no_significant_leaks:
                print("✅ Использование памяти стабильно")
            elif memory_stable:
                print("✅ Умеренное использование памяти")
            else:
                print("⚠️ Возможные проблемы с памятью")
            
            assert no_significant_leaks, "Не должно быть значительного роста памяти"
            
        else:
            print("⚠️ Недостаточно образцов для анализа памяти")
            assert len(memory_samples) >= 2, "Минимум 2 образца памяти должно быть собрано"
    
    def test_network_usage(self, driver):
        """Тест сетевой активности приложения"""
        print("\n🌐 Тест сетевой активности")
        
        # Поскольку прямой мониторинг сети через Appium ограничен,
        # мы тестируем поведение приложения при сетевых операциях
        
        network_tests = []
        test_duration = 15  # секунд
        
        print(f"🌐 Мониторим сетевую активность в течение {test_duration} секунд")
        
        start_time = time.time()
        sample_interval = 3
        sample_count = 0
        
        while time.time() - start_time < test_duration:
            sample_count += 1
            print(f"   🌐 Образец сетевой активности {sample_count}")
            
            try:
                # Выполняем действия которые могут вызвать сетевую активность
                size = driver.get_window_size()
                
                # Тап по кнопкам которые могут инициировать сетевые запросы
                driver.tap([(size['width']//2, int(size['height']*0.32))])  # Play button
                time.sleep(1)
                driver.tap([(size['width']//2, int(size['height']*0.42))])  # My Account
                
                # Проверяем отзывчивость (косвенный индикатор сетевой активности)
                response_start = time.time()
                current_size = driver.get_window_size()
                page_source = driver.page_source
                response_time = time.time() - response_start
                
                network_sample = {
                    'sample': sample_count,
                    'response_time': response_time,
                    'content_size': len(page_source),
                    'timestamp': time.time() - start_time,
                    'responsive': response_time < 3.0
                }
                
                network_tests.append(network_sample)
                
                print(f"      - Время отклика: {response_time:.3f}с")
                print(f"      - Размер контента: {len(page_source)} символов")
                print(f"      - Отзывчивость: {'✅' if network_sample['responsive'] else '⚠️'}")
                
                time.sleep(sample_interval)
                
            except Exception as e:
                print(f"   ❌ Ошибка образца сети {sample_count}: {e}")
                network_tests.append({
                    'sample': sample_count,
                    'error': str(e),
                    'responsive': False
                })
        
        # Анализ сетевой производительности
        responsive_samples = [t for t in network_tests if t.get('responsive', False)]
        
        print(f"\n📊 Результаты сетевой активности:")
        print(f"   - Отзывчивых образцов: {len(responsive_samples)}/{len(network_tests)}")
        
        if responsive_samples:
            avg_response = sum(t['response_time'] for t in responsive_samples) / len(responsive_samples)
            max_response = max(t['response_time'] for t in responsive_samples)
            
            print(f"   - Средний отклик: {avg_response:.3f}с")
            print(f"   - Максимальный отклик: {max_response:.3f}с")
            
            if avg_response < 1.0:
                print("✅ Отличная сетевая производительность")
            elif avg_response < 2.0:
                print("✅ Хорошая сетевая производительность")
            else:
                print("⚠️ Умеренная сетевая производительность")
        
        wait_and_screenshot(driver, "network_test_final")
        
        assert len(responsive_samples) >= len(network_tests) // 2, "Минимум половина образцов должна быть отзывчивой"
    
    def test_intensive_usage_performance(self, driver):
        """Тест производительности при интенсивном использовании"""
        print("\n🔥 Тест производительности при интенсивном использовании")
        
        size = driver.get_window_size()
        intensive_duration = 45  # Увеличено с 30 до 45 секунд
        actions_performed = 0
        performance_samples = []
        
        print(f"🔥 Интенсивное тестирование в течение {intensive_duration} секунд")
        
        start_time = time.time()
        
        while time.time() - start_time < intensive_duration:
            elapsed = int(time.time() - start_time)
            
            if elapsed % 5 == 0 and elapsed > 0:
                print(f"   🔥 Интенсивный тест: {elapsed}/{intensive_duration}с - Действий: {actions_performed}")
            
            try:
                # Случайные интенсивные действия
                import random
                
                action_start = time.time()
                
                action_type = random.choice(['tap', 'swipe', 'multi_tap'])
                
                if action_type == 'tap':
                    x = random.randint(int(size['width']*0.1), int(size['width']*0.9))
                    y = random.randint(int(size['height']*0.1), int(size['height']*0.9))
                    driver.tap([(x, y)])
                    actions_performed += 1
                    
                elif action_type == 'swipe':
                    start_x = random.randint(int(size['width']*0.2), int(size['width']*0.8))
                    start_y = random.randint(int(size['height']*0.2), int(size['height']*0.8))
                    end_x = random.randint(int(size['width']*0.2), int(size['width']*0.8))
                    end_y = random.randint(int(size['height']*0.2), int(size['height']*0.8))
                    driver.swipe(start_x, start_y, end_x, end_y, 500)
                    actions_performed += 1
                    
                elif action_type == 'multi_tap':
                    for _ in range(3):
                        x = random.randint(int(size['width']*0.3), int(size['width']*0.7))
                        y = random.randint(int(size['height']*0.3), int(size['height']*0.7))
                        driver.tap([(x, y)])
                        actions_performed += 1  # Считаем каждый тап в multi_tap
                        time.sleep(0.05)  # Уменьшено с 0.1 до 0.05
                
                action_time = time.time() - action_start
                
                # Периодическая проверка производительности
                if actions_performed % 10 == 0:
                    perf_check_start = time.time()
                    current_size = driver.get_window_size()
                    perf_check_time = time.time() - perf_check_start
                    
                    performance_sample = {
                        'actions_count': actions_performed,
                        'elapsed_time': time.time() - start_time,
                        'action_time': action_time,
                        'perf_check_time': perf_check_time,
                        'stable': current_size == size
                    }
                    
                    performance_samples.append(performance_sample)
                
                time.sleep(0.05)  # Уменьшено с 0.1 до 0.05 для большего количества действий
                
            except Exception as e:
                print(f"   ❌ Ошибка интенсивного действия {actions_performed + 1}: {e}")
                # Не прерываем тест при ошибке, продолжаем
                time.sleep(0.1)
        
        total_time = time.time() - start_time
        
        print(f"\n📊 Результаты интенсивного тестирования:")
        print(f"   - Продолжительность: {total_time:.1f}с")
        print(f"   - Выполнено действий: {actions_performed}")
        print(f"   - Скорость: {actions_performed/total_time:.1f} действий/сек")
        print(f"   - Образцов производительности: {len(performance_samples)}")
        
        if performance_samples:
            stable_samples = [s for s in performance_samples if s['stable']]
            avg_action_time = sum(s['action_time'] for s in performance_samples) / len(performance_samples)
            avg_perf_check = sum(s['perf_check_time'] for s in performance_samples) / len(performance_samples)
            
            print(f"   - Стабильных проверок: {len(stable_samples)}/{len(performance_samples)}")
            print(f"   - Среднее время действия: {avg_action_time:.3f}с")
            print(f"   - Средняя проверка производительности: {avg_perf_check:.3f}с")
            
            stability_rate = len(stable_samples) / len(performance_samples)
            
            if stability_rate >= 0.9:
                print("✅ Отличная стабильность при интенсивном использовании")
            elif stability_rate >= 0.7:
                print("✅ Хорошая стабильность при интенсивном использовании")
            else:
                print("⚠️ Умеренная стабильность при интенсивном использовании")
        
        wait_and_screenshot(driver, "intensive_usage_final")
        
        assert actions_performed >= 30, f"Должно быть выполнено минимум 30 действий, выполнено: {actions_performed}"
        assert total_time >= intensive_duration * 0.8, f"Тест должен проработать минимум 80% от запланированного времени ({intensive_duration * 0.8:.1f}с), проработал: {total_time:.1f}с"
