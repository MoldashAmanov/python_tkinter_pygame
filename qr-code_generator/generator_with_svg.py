import qrcode
import qrcode.image.svg

data = "pillow==13.0.0, pygame-ce==2.5.8, qrcode==8.2"

# Указываем, что хотим сохранить изображение в формате SVG
factory = qrcode.image.svg.SvgImage 

# Генерируем код с SVG-фабрикой
img = qrcode.make(data, image_factory=factory)

# Сохраняем
img.save('requirements_with_SVG.png')

print("✅ SVG-файл успешно сохранён!")

"""
Почему SVG важен:
* Масштабируемость без потери качества. Вектор можно увеличить
до любого размера
* Гибкость редактирования. SVG можно открыть в Illustrator, Inkscape 
или в любом кодовом редакторе и изменить стиль
* Меньше вес при большом разрешении. В отличие от PNG, векторный файл
не утяжеляется при большом размере
"""