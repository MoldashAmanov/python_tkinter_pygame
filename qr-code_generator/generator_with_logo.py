from PIL import Image
import qrcode


data = "pillow==13.0.0, pygame-ce==2.5.8, qrcode==8.2"

qr = qrcode.QRCode(
    version=2,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=10,
    border=4
)
qr.add_data(data)
qr.make(fit=True)

# Генерируем изображение
img = qr.make_image(fill_color = '#FF1493', back_color = 'black').convert('RGB')

# Загружаем логотип
logo = Image.open('logoBlackR.png')

# Масштаб лого - 20% от ширины кода
qr_width, qr_height = img.size
logo_size = qr_width // 5
logo = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)

# Расчет позиции логотипа (по центру)
logo_pos = (
    (qr_width - logo_size) // 2,
    (qr_height - logo_size) // 2
)

# Вставляем логотип
img.paste(logo, logo_pos)

# Сохраняем результат
img.save('qr_with_logoR.png', quality=95)
img.show()

print("✅ QR-код с логотипом успешно создан!")
