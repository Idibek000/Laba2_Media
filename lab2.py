import os
import datetime
from PIL import Image, ImageFilter, ImageOps

# ==========================================
# НАСТРОЙКА ПУТЕЙ (твой путь с картинки)
# ==========================================
BASE_DIR = r"C:\Users\Abdus\OneDrive\Desktop\Laba2_Media"

INPUT_DIR = os.path.join(BASE_DIR, "data", "input")
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "output")
LOG_FILE = os.path.join(BASE_DIR, "logs", "history.txt")

def write_log(filename, status, filter_name):
    """Функция для записи в лог с кодировкой UTF-8"""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{now}] Файл: {filename} | Фильтр: {filter_name} | Статус: {status}\n"
    
    # Режим 'a' - добавление в конец файла
    with open(LOG_FILE, "a", encoding="UTF-8") as log:
        log.write(log_line)

def main():
    filter_name = "Повышение резкости (Unsharp Masking) + Автоконтраст"
    
    # 1. Потоковый ввод
    filename = input("Введите имя файла для обработки (например, image1.jpg): ").strip()
    
    if not filename:
        print("Вы ничего не ввели.")
        return

    filepath = os.path.join(INPUT_DIR, filename)

    try:
        # ХИТРОСТЬ ДЛЯ WINDOWS: Проверка атрибута "Только чтение"
        # В Windows этот атрибут не вызывает PermissionError сам по себе, 
        # поэтому проверяем его вручную, чтобы лаба отработала как надо!
        if os.path.exists(filepath):
            if not os.access(filepath, os.W_OK) or (os.stat(filepath).st_file_attributes & 1):
                raise PermissionError

        # 2. Открытие файла 
        img = Image.open(filepath)
        
        # 3. Обработка изображения (Задание №1 и №2)
        print("Файл открыт. Повышаем резкость (Unsharp Masking)...")
        # radius - радиус размытия, percent - сила эффекта, threshold - порог
        img_sharp = img.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
        
        print("Применяем Автоконтраст...")
        img_final = ImageOps.autocontrast(img_sharp)
        
        # 4. Сохранение результата
        result_path = os.path.join(OUTPUT_DIR, "result.jpg")
        # Конвертируем в RGB на случай, если PNG с альфа-каналом (прозрачностью)
        img_final.convert("RGB").save(result_path, "JPEG")
        
        print(f"✅ Успешно! Результат сохранен в: {result_path}")
        
        # 5. Логирование успеха
        write_log(filename, "Успешно", filter_name)

    except PermissionError:
        # 3. Обработка ошибки прав доступа
        error_msg = f"Ошибка: Нет прав на чтение файла {filename}. Обратитесь к администратору"
        print(error_msg)
        write_log(filename, "Ошибка доступа", filter_name)

    except FileNotFoundError:
        # 3. Обработка ошибки "файл не найден"
        print("Ошибка: Файл не найден")
        
    except Exception as e:
        # Ловим другие возможные ошибки (например, если файл битый)
        print(f"Произошла непредвиденная ошибка: {e}")

if __name__ == "__main__":
    main()
