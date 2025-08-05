#!/usr/bin/env python3
"""
Обновленный скрипт для запуска тестов Candy Crush Saga
"""

import subprocess
import sys
import os
import argparse
from datetime import datetime

def run_tests(test_suite="all", html_report=True, verbose=True):
    """Запуск тестов с настройками"""
    
    print("🎮 Candy Crush Saga - Автоматизированное тестирование")
    print("=" * 60)
    
    # Создаем папку для отчетов если её нет
    reports_dir = "reports"
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
    
    # Определяем какие тесты запускать
    test_files = {
        "all": ["tests/"],
        "stability": ["tests/test_app_stability.py"],
        "interactions": ["tests/test_screen_interactions.py"],
        "performance": ["tests/test_performance.py"],
        "visual": ["tests/test_visual_validation.py"],
        "full_suite": ["tests/test_app_stability.py", "tests/test_screen_interactions.py", "tests/test_performance.py", "tests/test_visual_validation.py"]
    }
    
    if test_suite not in test_files:
        print(f"❌ Неизвестный набор тестов: {test_suite}")
        print(f"Доступные наборы: {list(test_files.keys())}")
        return False
    
    files_to_test = test_files[test_suite]
    
    # Генерируем имя файла отчета
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Базовая команда pytest
    cmd = ["pytest"]
    
    # Добавляем файлы для тестирования
    cmd.extend(files_to_test)
    
    # Параметры вывода
    if verbose:
        cmd.extend(["-v", "-s"])  # verbose и показывать print'ы
    
    # HTML отчет
    if html_report:
        report_file = f"{reports_dir}/test_report_{test_suite}_{timestamp}.html"
        cmd.extend([f"--html={report_file}", "--self-contained-html"])
        print(f"📊 HTML отчет будет сохранен в: {report_file}")
    
    # Дополнительные параметры
    cmd.extend([
        "--tb=short",  # короткий traceback
        "-q",  # тихий режим для менее важных сообщений
        f"--maxfail=10"  # остановка после 10 ошибок
    ])
    
    print(f"🚀 Запускаем набор тестов: {test_suite}")
    print(f"📁 Файлы: {files_to_test}")
    print("-" * 60)
    
    try:
        # Запускаем тесты
        result = subprocess.run(cmd, capture_output=False)
        
        print("-" * 60)
        if result.returncode == 0:
            print("✅ Все тесты прошли успешно!")
        elif result.returncode == 1:
            print("⚠️ Некоторые тесты упали")
        else:
            print("❌ Ошибка выполнения тестов")
        
        if html_report:
            print(f"📊 Подробный отчет: {os.path.abspath(report_file)}")
        
        return result.returncode == 0
        
    except KeyboardInterrupt:
        print("\n⏹️ Тестирование прервано пользователем")
        return False
    except Exception as e:
        print(f"❌ Ошибка при запуске тестов: {e}")
        return False

def check_environment():
    """Проверка готовности окружения"""
    print("🔍 Проверка окружения...")
    
    # Проверяем Appium сервер (упрощенная версия)
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex(('localhost', 4723))
        sock.close()
        
        if result == 0:
            print("✅ Appium сервер доступен на порту 4723")
        else:
            print("❌ Appium сервер недоступен")
            print("💡 Запустите: appium --port 4723")
            return False
    except Exception as e:
        print(f"❌ Ошибка проверки Appium: {e}")
        return False
    
    # Проверяем устройство
    try:
        result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
        if "device" in result.stdout:
            print("✅ Android устройство подключено")
        else:
            print("❌ Android устройство не найдено")
            return False
    except:
        print("❌ ADB не найден")
        return False
    
    # Проверяем приложение
    try:
        result = subprocess.run(
            ["adb", "shell", "pm", "list", "packages", "com.king.candycrushsaga"], 
            capture_output=True, text=True
        )
        if "com.king.candycrushsaga" in result.stdout:
            print("✅ Candy Crush Saga установлен")
        else:
            print("❌ Candy Crush Saga не найден")
            return False
    except:
        print("❌ Не удается проверить приложение")
        return False
    
    print("✅ Окружение готово!")
    return True

def main():
    parser = argparse.ArgumentParser(description="Запуск тестов Candy Crush Saga")
    parser.add_argument(
        "--suite", 
        choices=["all", "stability", "interactions", "performance", "visual", "full_suite"],
        default="stability",
        help="Набор тестов для запуска"
    )
    parser.add_argument("--no-html", action="store_true", help="Не создавать HTML отчет")
    parser.add_argument("--quiet", action="store_true", help="Тихий режим")
    parser.add_argument("--check-env", action="store_true", help="Только проверить окружение")
    
    args = parser.parse_args()
    
    # Если нужна только проверка окружения
    if args.check_env:
        success = check_environment()
        sys.exit(0 if success else 1)
    
    # Проверяем окружение перед запуском тестов
    if not check_environment():
        print("\n❌ Окружение не готово. Исправьте ошибки и попробуйте снова.")
        sys.exit(1)
    
    # Запускаем тесты
    success = run_tests(
        test_suite=args.suite,
        html_report=not args.no_html,
        verbose=not args.quiet
    )
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
