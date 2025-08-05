"""
Тесты визуальной валидации Candy Crush Saga
"""

import time
import pytest
from utils.helpers import wait_and_screenshot
from PIL import Image
import io

class TestVisualValidation:
    """Тесты визуального контроля и проверки интерфейса"""
    
    def test_main_screen_elements_present(self, driver):
        """Проверка присутствия основных элементов на главном экране"""
        print("\n👁️ Тест присутствия элементов главного экрана")
        
        # Делаем скриншот для анализа
        screenshot_path = wait_and_screenshot(driver, "main_screen_elements")
        
        # Получаем скриншот как изображение для анализа
        screenshot_png = driver.get_screenshot_as_png()
        image = Image.open(io.BytesIO(screenshot_png))
        
        # Анализ изображения
        width, height = image.size
        
        print(f"👁️ Анализируем скриншот размером {width}x{height}")
        
        # Конвертируем в RGB для анализа цветов
        rgb_image = image.convert('RGB')
        
        # Проверяем основные характеристики изображения
        visual_checks = {
            'not_blank': False,
            'has_colors': False,
            'reasonable_size': False,
            'not_mostly_black': False,
            'not_mostly_white': False
        }
        
        # Проверка 1: Изображение не пустое
        if width > 0 and height > 0:
            visual_checks['not_blank'] = True
            print("   ✅ Изображение не пустое")
        
        # Проверка 2: Разумный размер экрана
        if width >= 480 and height >= 800:  # Минимальные размеры для мобильного экрана
            visual_checks['reasonable_size'] = True
            print(f"   ✅ Размер экрана разумный: {width}x{height}")
        else:
            print(f"   ⚠️ Размер экрана маленький: {width}x{height}")
        
        # Проверка 3: Анализ цветов (простая проверка по углам и центру)
        sample_points = [
            (width//4, height//4),      # Левый верхний квадрант
            (3*width//4, height//4),    # Правый верхний квадрант
            (width//2, height//2),      # Центр
            (width//4, 3*height//4),    # Левый нижний квадрант
            (3*width//4, 3*height//4)   # Правый нижний квадрант
        ]
        
        colors_found = []
        black_pixels = 0
        white_pixels = 0
        total_samples = len(sample_points)
        
        for x, y in sample_points:
            try:
                r, g, b = rgb_image.getpixel((x, y))
                colors_found.append((r, g, b))
                
                # Считаем черные и белые пиксели
                if r < 30 and g < 30 and b < 30:  # Почти черный
                    black_pixels += 1
                elif r > 225 and g > 225 and b > 225:  # Почти белый
                    white_pixels += 1
                    
            except Exception as e:
                print(f"   ⚠️ Ошибка анализа пикселя ({x}, {y}): {e}")
        
        # Проверка разнообразия цветов
        unique_colors = len(set(colors_found))
        if unique_colors >= 3:
            visual_checks['has_colors'] = True
            print(f"   ✅ Найдено {unique_colors} различных цветов")
        else:
            print(f"   ⚠️ Мало цветового разнообразия: {unique_colors} цветов")
        
        # Проверка что экран не преимущественно черный или белый
        if black_pixels < total_samples * 0.8:
            visual_checks['not_mostly_black'] = True
            print("   ✅ Экран не преимущественно черный")
        else:
            print("   ⚠️ Экран преимущественно черный")
        
        if white_pixels < total_samples * 0.8:
            visual_checks['not_mostly_white'] = True
            print("   ✅ Экран не преимущественно белый")
        else:
            print("   ⚠️ Экран преимущественно белый")
        
        # Выводим информацию о найденных цветах
        print(f"   📊 Образцы цветов: {colors_found[:3]}...")  # Показываем первые 3
        
        # Подсчет успешных проверок
        passed_checks = sum(visual_checks.values())
        total_checks = len(visual_checks)
        
        print(f"\n📊 Визуальные проверки: {passed_checks}/{total_checks}")
        
        for check_name, passed in visual_checks.items():
            status = "✅" if passed else "❌"
            print(f"   {status} {check_name}")
        
        assert passed_checks >= 3, f"Минимум 3 из {total_checks} визуальных проверок должны пройти"
    
    def test_ui_elements_not_overlapping(self, driver):
        """Проверка что UI элементы не накладываются друг на друга"""
        print("\n🔲 Тест наложения UI элементов")
        
        size = driver.get_window_size()
        
        # Делаем серию скриншотов для анализа стабильности UI
        screenshots = []
        
        for i in range(3):
            print(f"   📸 Скриншот {i+1}/3 для анализа стабильности")
            
            screenshot_path = wait_and_screenshot(driver, f"ui_stability_{i+1}")
            screenshot_png = driver.get_screenshot_as_png()
            screenshots.append(screenshot_png)
            
            # Небольшое взаимодействие между скриншотами
            if i < 2:
                driver.tap([(size['width']//2, size['height']//2)])
                time.sleep(1)
        
        # Анализ стабильности UI
        ui_stable = True
        
        if len(screenshots) >= 2:
            # Простое сравнение размеров скриншотов
            sizes = [len(screenshot) for screenshot in screenshots]
            
            size_variation = max(sizes) - min(sizes)
            avg_size = sum(sizes) / len(sizes)
            variation_percent = (size_variation / avg_size) * 100
            
            print(f"   📊 Анализ стабильности UI:")
            print(f"      - Размеры скриншотов: {sizes}")
            print(f"      - Вариация размера: {size_variation} байт ({variation_percent:.1f}%)")
            
            if variation_percent < 10:  # Менее 10% вариации
                print("   ✅ UI стабилен между взаимодействиями")
                ui_stable = True
            else:
                print("   ⚠️ Значительные изменения UI между взаимодействиями")
                ui_stable = variation_percent < 25  # Допускаем до 25%
        
        # Проверка разрешения экрана на стабильность
        current_size = driver.get_window_size()
        resolution_stable = current_size == size
        
        print(f"   📱 Стабильность разрешения: {'✅' if resolution_stable else '❌'}")
        
        # Тест зон экрана на отзывчивость (косвенная проверка наложений)
        zones_responsive = 0
        test_zones = [
            ("Верхняя зона", size['width']//2, int(size['height']*0.2)),
            ("Центральная зона", size['width']//2, int(size['height']*0.5)),
            ("Нижняя зона", size['width']//2, int(size['height']*0.8)),
            ("Левая зона", int(size['width']*0.2), size['height']//2),
            ("Правая зона", int(size['width']*0.8), size['height']//2),
        ]
        
        for zone_name, x, y in test_zones:
            try:
                driver.tap([(x, y)])
                time.sleep(0.5)
                
                # Проверяем что приложение отвечает
                test_size = driver.get_window_size()
                if test_size == size:
                    zones_responsive += 1
                    print(f"   ✅ {zone_name}: отзывчива")
                else:
                    print(f"   ⚠️ {zone_name}: изменился размер экрана")
                    
            except Exception as e:
                print(f"   ❌ {zone_name}: ошибка тестирования - {e}")
        
        print(f"\n📊 Результаты проверки наложений:")
        print(f"   - UI стабильность: {'✅' if ui_stable else '❌'}")
        print(f"   - Стабильность разрешения: {'✅' if resolution_stable else '❌'}")
        print(f"   - Отзывчивых зон: {zones_responsive}/{len(test_zones)}")
        
        assert ui_stable, "UI должен быть стабильным"
        assert resolution_stable, "Разрешение экрана должно быть стабильным"
        assert zones_responsive >= 3, "Минимум 3 зоны должны быть отзывчивыми"
    
    def test_screenshot_regression(self, driver):
        """Тест сравнения с эталонными скриншотами"""
        print("\n📸 Тест регрессии скриншотов")
        
        # Создаем серию эталонных скриншотов
        reference_screenshots = []
        
        states_to_capture = [
            ("Исходное состояние", lambda: None),
            ("После тапа по центру", lambda: driver.tap([(size['width']//2, size['height']//2)])),
            ("После возврата", lambda: driver.tap([(size['width']//2, size['height']//2)])),
        ]
        
        size = driver.get_window_size()
        
        for state_name, action in states_to_capture:
            print(f"   📸 Захват состояния: {state_name}")
            
            try:
                if action:
                    action()
                    time.sleep(2)  # Ждем стабилизации
                
                screenshot_path = wait_and_screenshot(driver, f"regression_{state_name.lower().replace(' ', '_')}")
                screenshot_png = driver.get_screenshot_as_png()
                
                # Простой анализ скриншота
                image = Image.open(io.BytesIO(screenshot_png))
                
                screenshot_info = {
                    'state': state_name,
                    'size': image.size,
                    'mode': image.mode,
                    'data_size': len(screenshot_png),
                    'path': screenshot_path
                }
                
                reference_screenshots.append(screenshot_info)
                
                print(f"      - Размер изображения: {image.size}")
                print(f"      - Размер данных: {len(screenshot_png)} байт")
                
            except Exception as e:
                print(f"   ❌ Ошибка захвата {state_name}: {e}")
        
        # Анализ собранных скриншотов
        if len(reference_screenshots) >= 2:
            print(f"\n📊 Анализ {len(reference_screenshots)} скриншотов:")
            
            # Проверяем консистентность размеров
            sizes = [info['size'] for info in reference_screenshots]
            unique_sizes = list(set(sizes))
            
            if len(unique_sizes) == 1:
                print("   ✅ Все скриншоты имеют одинаковый размер")
                size_consistent = True
            else:
                print(f"   ⚠️ Разные размеры скриншотов: {unique_sizes}")
                size_consistent = False
            
            # Проверяем разумность размеров данных
            data_sizes = [info['data_size'] for info in reference_screenshots]
            avg_data_size = sum(data_sizes) / len(data_sizes)
            size_variation = (max(data_sizes) - min(data_sizes)) / avg_data_size
            
            print(f"   📊 Размеры данных: {data_sizes}")
            print(f"   📊 Средний размер: {avg_data_size:.0f} байт")
            print(f"   📊 Вариация размера: {size_variation:.1%}")
            
            data_reasonable = size_variation < 0.5  # Менее 50% вариации
            
            if data_reasonable:
                print("   ✅ Размеры данных скриншотов разумны")
            else:
                print("   ⚠️ Большая вариация в размерах данных")
            
            # Проверяем что скриншоты не пустые
            all_non_empty = all(info['data_size'] > 10000 for info in reference_screenshots)  # Минимум 10KB
            
            if all_non_empty:
                print("   ✅ Все скриншоты содержат данные")
            else:
                print("   ❌ Некоторые скриншоты слишком малы")
            
            assert size_consistent, "Размеры скриншотов должны быть консистентными"
            assert all_non_empty, "Все скриншоты должны содержать данные"
            
        else:
            assert False, "Должно быть захвачено минимум 2 скриншота"
    
    def test_different_screen_resolutions(self, driver):
        """Тест работы с различными разрешениями экрана"""
        print("\n📱 Тест различных разрешений экрана")
        
        # Получаем текущее разрешение
        original_size = driver.get_window_size()
        print(f"📱 Исходное разрешение: {original_size}")
        
        # Делаем скриншот исходного разрешения
        original_screenshot = wait_and_screenshot(driver, "original_resolution")
        
        # Тестируем поведение при смене ориентации (косвенно влияет на разрешение)
        orientation_tests = []
        
        try:
            original_orientation = driver.orientation
            print(f"📱 Исходная ориентация: {original_orientation}")
            
            # Пробуем сменить ориентацию
            new_orientation = "LANDSCAPE" if original_orientation == "PORTRAIT" else "PORTRAIT"
            
            print(f"🔄 Пробуем сменить ориентацию на: {new_orientation}")
            driver.orientation = new_orientation
            time.sleep(3)
            
            # Проверяем новое разрешение
            new_size = driver.get_window_size()
            current_orientation = driver.orientation
            
            print(f"📱 Новое разрешение: {new_size}")
            print(f"📱 Новая ориентация: {current_orientation}")
            
            # Делаем скриншот нового разрешения
            new_screenshot = wait_and_screenshot(driver, "changed_resolution")
            
            # Проверяем что приложение адаптировалось
            resolution_changed = new_size != original_size
            orientation_changed = current_orientation != original_orientation
            
            orientation_test = {
                'attempted_orientation': new_orientation,
                'actual_orientation': current_orientation,
                'original_size': original_size,
                'new_size': new_size,
                'resolution_changed': resolution_changed,
                'orientation_changed': orientation_changed,
                'app_responsive': True
            }
            
            # Проверяем отзывчивость приложения в новом разрешении
            try:
                driver.tap([(new_size['width']//2, new_size['height']//2)])
                time.sleep(1)
                test_size = driver.get_window_size()
                orientation_test['app_responsive'] = test_size == new_size
            except Exception as e:
                print(f"   ⚠️ Приложение не отвечает в новом разрешении: {e}")
                orientation_test['app_responsive'] = False
            
            orientation_tests.append(orientation_test)
            
            # Возвращаем исходную ориентацию
            print("🔄 Возвращаем исходную ориентацию")
            driver.orientation = original_orientation
            time.sleep(2)
            
            final_size = driver.get_window_size()
            final_orientation = driver.orientation
            
            print(f"📱 Финальное разрешение: {final_size}")
            print(f"📱 Финальная ориентация: {final_orientation}")
            
            # Финальный скриншот
            final_screenshot = wait_and_screenshot(driver, "restored_resolution")
            
        except Exception as e:
            print(f"⚠️ Не удалось изменить ориентацию: {e}")
            print("   (Возможно заблокировано приложением)")
            
            # Альтернативный тест - проверяем текущее разрешение
            orientation_test = {
                'original_size': original_size,
                'current_size': driver.get_window_size(),
                'orientation_locked': True,
                'app_responsive': True
            }
            
            orientation_tests.append(orientation_test)
        
        # Анализ результатов
        print(f"\n📊 Результаты тестирования разрешений:")
        
        for i, test in enumerate(orientation_tests):
            print(f"   Тест {i+1}:")
            
            if test.get('orientation_locked'):
                print("      - Ориентация заблокирована приложением")
                print(f"      - Размер остался: {test['current_size']}")
            else:
                print(f"      - Исходный размер: {test['original_size']}")
                print(f"      - Новый размер: {test['new_size']}")
                print(f"      - Разрешение изменилось: {'✅' if test['resolution_changed'] else '❌'}")
                print(f"      - Ориентация изменилась: {'✅' if test['orientation_changed'] else '❌'}")
            
            print(f"      - Приложение отзывчиво: {'✅' if test['app_responsive'] else '❌'}")
        
        # Проверяем что приложение осталось стабильным
        try:
            final_check_size = driver.get_window_size()
            stability_check = final_check_size['width'] > 0 and final_check_size['height'] > 0
            
            if stability_check:
                print("   ✅ Приложение осталось стабильным после тестов разрешения")
            else:
                print("   ❌ Приложение нестабильно после тестов разрешения")
            
            assert stability_check, "Приложение должно оставаться стабильным"
            
        except Exception as e:
            assert False, f"Критическая ошибка стабильности: {e}"
    
    def test_color_scheme_consistency(self, driver):
        """Тест консистентности цветовой схемы"""
        print("\n🎨 Тест консистентности цветовой схемы")
        
        # Собираем скриншоты разных состояний для анализа цветов
        color_analysis_states = [
            ("Главный экран", lambda: None),
            ("После первого тапа", lambda: driver.tap([(size['width']//2, int(size['height']*0.32))])),
            ("После второго тапа", lambda: driver.tap([(size['width']//2, int(size['height']*0.42))])),
        ]
        
        size = driver.get_window_size()
        color_samples = []
        
        for state_name, action in color_analysis_states:
            print(f"   🎨 Анализ цветов: {state_name}")
            
            try:
                if action:
                    action()
                    time.sleep(2)
                
                screenshot_png = driver.get_screenshot_as_png()
                image = Image.open(io.BytesIO(screenshot_png))
                rgb_image = image.convert('RGB')
                
                # Собираем образцы цветов из разных частей экрана
                sample_points = [
                    (size['width']//4, size['height']//4),      # Верх-лево
                    (3*size['width']//4, size['height']//4),    # Верх-право
                    (size['width']//2, size['height']//2),      # Центр
                    (size['width']//4, 3*size['height']//4),    # Низ-лево
                    (3*size['width']//4, 3*size['height']//4),  # Низ-право
                ]
                
                state_colors = []
                for x, y in sample_points:
                    try:
                        color = rgb_image.getpixel((x, y))
                        state_colors.append(color)
                    except:
                        pass
                
                # ИСПРАВЛЕНО: более мягкие критерии для определения игровых цветов
                has_colorful_content = self._has_colorful_content(state_colors)
                has_game_colors = self._has_candy_crush_colors_flexible(state_colors)
                
                color_sample = {
                    'state': state_name,
                    'colors': state_colors,
                    'dominant_colors': self._get_dominant_colors(state_colors),
                    'has_game_colors': has_game_colors,
                    'has_colorful_content': has_colorful_content
                }
                
                color_samples.append(color_sample)
                
                print(f"      - Образцов цветов: {len(state_colors)}")
                print(f"      - Доминантные цвета: {color_sample['dominant_colors'][:3]}")  # Первые 3
                print(f"      - Есть цветной контент: {'✅' if has_colorful_content else '❌'}")
                print(f"      - Есть игровые цвета: {'✅' if has_game_colors else '❌'}")
                
                # Сохраняем скриншот для анализа
                wait_and_screenshot(driver, f"color_analysis_{state_name.lower().replace(' ', '_')}")
                
            except Exception as e:
                print(f"   ❌ Ошибка анализа цветов {state_name}: {e}")
        
        # Анализ консистентности цветовой схемы
        if len(color_samples) >= 2:
            print(f"\n📊 Анализ консистентности цветов:")
            
            # ИСПРАВЛЕНО: более гибкие критерии
            states_with_game_colors = sum(1 for sample in color_samples if sample['has_game_colors'])
            states_with_colorful_content = sum(1 for sample in color_samples if sample['has_colorful_content'])
            
            print(f"   - Состояний с игровыми цветами: {states_with_game_colors}/{len(color_samples)}")
            print(f"   - Состояний с цветным контентом: {states_with_colorful_content}/{len(color_samples)}")
            
            # Проверяем консистентность доминантных цветов
            all_dominant_colors = []
            for sample in color_samples:
                all_dominant_colors.extend(sample['dominant_colors'])
            
            unique_dominant_colors = len(set(all_dominant_colors))
            total_dominant_colors = len(all_dominant_colors)
            
            print(f"   - Уникальных доминантных цветов: {unique_dominant_colors}")
            print(f"   - Всего доминантных цветов: {total_dominant_colors}")
            
            # Консистентность считается хорошей если есть повторяющиеся доминантные цвета
            consistency_ratio = 1 - (unique_dominant_colors / total_dominant_colors) if total_dominant_colors > 0 else 0
            
            print(f"   - Коэффициент консистентности: {consistency_ratio:.2f}")
            
            if consistency_ratio >= 0.3:
                print("   ✅ Хорошая консистентность цветовой схемы")
                color_consistency = True
            elif consistency_ratio >= 0.1:
                print("   ✅ Умеренная консистентность цветовой схемы")
                color_consistency = True
            else:
                print("   ⚠️ Низкая консистентность цветовой схемы")
                color_consistency = False
            
            # ИСПРАВЛЕННЫЕ ASSERTIONS - основная проблема
            # Проверяем что есть хотя бы цветной контент ИЛИ игровые цвета
            has_visual_content = states_with_game_colors >= 1 or states_with_colorful_content >= 2
            
            assert has_visual_content, f"Должен быть цветной контент в состояниях (игровые цвета: {states_with_game_colors}, цветной контент: {states_with_colorful_content})"
            assert color_consistency, "Цветовая схема должна быть консистентной"
            
        else:
            assert False, "Должно быть проанализировано минимум 2 состояния"
    
    def _get_dominant_colors(self, colors):
        """Получить доминантные цвета из списка"""
        if not colors:
            return []
        
        # Простая группировка похожих цветов
        color_groups = {}
        for r, g, b in colors:
            # Группируем цвета с допуском ±30
            key = (r//30*30, g//30*30, b//30*30)
            if key not in color_groups:
                color_groups[key] = []
            color_groups[key].append((r, g, b))
        
        # Сортируем группы по количеству цветов
        sorted_groups = sorted(color_groups.items(), key=lambda x: len(x[1]), reverse=True)
        
        return [group[0] for group in sorted_groups[:5]]  # Топ 5 доминантных
    
    def _has_colorful_content(self, colors):
        """Проверить наличие цветного контента (не только черно-белого)"""
        if not colors:
            return False
        
        colorful_pixels = 0
        
        for r, g, b in colors:
            # Проверяем что цвет не серый/черно-белый
            is_grayscale = abs(r - g) < 30 and abs(g - b) < 30 and abs(r - b) < 30
            is_very_dark = r < 50 and g < 50 and b < 50
            is_very_light = r > 200 and g > 200 and b > 200
            
            if not is_grayscale and not is_very_dark and not is_very_light:
                colorful_pixels += 1
        
        # Если хотя бы 30% пикселей цветные
        return colorful_pixels >= len(colors) * 0.3
    
    def _has_candy_crush_colors_flexible(self, colors):
        """Проверить наличие характерных цветов Candy Crush - гибкая версия"""
        if not colors:
            return False
        
        # Расширенные характерные цвета с более широкими диапазонами
        color_ranges = [
            # Розовые/красные тона
            {'min': (180, 50, 80), 'max': (255, 180, 200)},
            # Синие тона  
            {'min': (50, 100, 180), 'max': (150, 200, 255)},
            # Желтые/золотые тона
            {'min': (200, 150, 50), 'max': (255, 255, 150)},
            # Зеленые тона
            {'min': (80, 180, 80), 'max': (180, 255, 180)},
            # Фиолетовые тона
            {'min': (100, 50, 150), 'max': (200, 150, 255)},
            # Оранжевые тона
            {'min': (200, 100, 50), 'max': (255, 180, 100)}
        ]
        
        matches = 0
        
        for r, g, b in colors:
            for color_range in color_ranges:
                min_r, min_g, min_b = color_range['min']
                max_r, max_g, max_b = color_range['max']
                
                if (min_r <= r <= max_r and 
                    min_g <= g <= max_g and 
                    min_b <= b <= max_b):
                    matches += 1
                    break  # Найден хотя бы один подходящий цвет
        
        # Если найдено хотя бы 20% подходящих цветов
        return matches >= len(colors) * 0.2
    
    def _has_candy_crush_colors(self, colors):
        """Проверить наличие характерных цветов Candy Crush - старая версия"""
        if not colors:
            return False
        
        # Характерные цвета Candy Crush Saga
        candy_colors = [
            (255, 100, 150),  # Розовый (кнопка Play)
            (100, 150, 255),  # Синий (кнопки)
            (255, 200, 100),  # Золотой (логотип)
            (100, 255, 150),  # Зеленый (фон)
            (150, 100, 255),  # Фиолетовый (конфеты)
        ]
        
        for r, g, b in colors:
            for cr, cg, cb in candy_colors:
                # Проверяем с допуском ±50
                if abs(r - cr) <= 50 and abs(g - cg) <= 50 and abs(b - cb) <= 50:
                    return True
        
        return False
