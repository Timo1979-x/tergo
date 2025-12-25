#!/usr/bin/env python3

"""
Конвертер BMP изображений в C-массив для OLED дисплея SSD1306 128x64
"""

from PIL import Image
import argparse
import os
import sys

def convert_bmp_to_ssd1306_array(input_file, array_name="image_data"):
    """
    Конвертирует BMP файл в массив байтов для SSD1306
    """
    try:
        # Открываем изображение
        img = Image.open(input_file)
        
        # Проверяем размеры
        if img.size != (128, 64):
            print(f"Предупреждение: Размер изображения {img.size} не соответствует 128x64.")
            print("Изображение будет масштабировано до 128x64")
            img = img.resize((128, 64), Image.Resampling.LANCZOS)
        
        # Конвертируем в монохромный (1 бит на пиксель)
        img = img.convert('1')  # '1' означает 1-битный монохромный
        
        # Получаем данные пикселей
        pixels = img.load()
        
        # SSD1306 имеет ширину 128 пикселей (16 байт по 8 пикселей вертикально)
        # и высоту 64 пикселя (8 страниц по 8 строк)
        width, height = img.size
        pages = height // 8  # 64 / 8 = 8 страниц
        
        # Создаем массив байтов
        byte_array = bytearray()
        
        # Организация данных для SSD1306:
        # Данные записываются постранично, каждая страница - 8 строк по вертикали
        # В каждом байте бит 0 - верхний пиксель, бит 7 - нижний пиксель
        for page in range(pages):
            for x in range(width):
                byte_value = 0
                for bit in range(8):
                    y = page * 8 + bit
                    if y < height:
                        # Получаем значение пикселя (0 или 255)
                        pixel_value = pixels[x, y]
                        # Преобразуем в 0 или 1 (инвертировать, если нужно)
                        # Для SSD1306: 1 - пиксель включен, 0 - выключен
                        bit_value = 1 if pixel_value == 0 else 0  # Инвертируем, если белый на черном
                        # Устанавливаем соответствующий бит
                        byte_value |= (bit_value << bit)
                byte_array.append(byte_value)
        
        # Генерируем C-код
        c_code = f"""// Автоматически сгенерированный файл из {os.path.basename(input_file)}
// Размер изображения: {width}x{height} пикселей
// Размер данных: {len(byte_array)} байт

#include <stdint.h>

const uint8_t {array_name}[] = {{
"""
        
        # Добавляем байты в виде hex-значений
        bytes_per_line = 16
        for i in range(0, len(byte_array), bytes_per_line):
            line_bytes = byte_array[i:i + bytes_per_line]
            hex_values = ', '.join([f'0x{b:02X}' for b in line_bytes])
            c_code += f"    {hex_values}"
            if i + bytes_per_line < len(byte_array):
                c_code += ","
            c_code += "\n"
        
        c_code += "};\n\n"
        
        print(c_code)
        
        print(f"\nУспешно конвертировано!")
        print(f"Входной файл: {input_file}")
        print(f"Имя массива: {array_name}")
        print(f"Размер массива: {len(byte_array)} байт")
        
        # Показываем предпросмотр изображения
        print("\nПредпросмотр изображения:")
        print("-" * 33)
        for y in range(height):
            line = ""
            for x in range(width):  # Показываем первые 64 столбца
                pixel = pixels[x, y]
                line += "█" if pixel == 0 else " "
            print(line)
        print("-" * 33)
        
    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description='Конвертер BMP изображений в C-массив для SSD1306 128x64',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  %(prog)s image.bmp image.h
  %(prog)s --help
        """
    )
    
    parser.add_argument('input', help='Входной BMP файл')
    
    args = parser.parse_args()
    
    # Проверяем существование входного файла
    if not os.path.exists(args.input):
        print(f"Ошибка: Файл '{args.input}' не найден")
        sys.exit(1)
    
    # Проверяем расширение
    if not args.input.lower().endswith('.bmp'):
        print("Предупреждение: Рекомендуется использовать BMP файлы")
    
    # Конвертируем
    convert_bmp_to_ssd1306_array(args.input, "image_data")

if __name__ == '__main__':
    main()
