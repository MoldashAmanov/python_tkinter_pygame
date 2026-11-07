import qrcode

data = "pillow==13.0.0, pygame-ce==2.5.8, qrcode==8.2"

qr = qrcode.QRCode(
    version=1,                                          # Определяем размер кода, от 1 до 40 (версия 1 = 21х21 ячеек)
    error_correction=qrcode.constants.ERROR_CORRECT_L,  # Определяем уровень коррекции ошибок (L - до 7% повреждений, M - до 15%, Q - до 25%, H - до 30%)
    box_size=10,                                        # Определяем размер одной ячейки кода в пикселях
    border=4,                                           # Устанавливаем толщину рамки вокруг кода
)

qr.add_data(data)       # Загружаем данные
qr.make(fit=True)       # Автоматически подбираем минимальный размер кода, fit=True увеличит размер, если данные велики

# Генерируем визуальное изображение
img = qr.make_image(
    fill_color = '#FF1493',
    back_color = 'black'
)

img.show()
img.save('requirementsQRcode.png')

print('✅ QR-код успешно создан!')