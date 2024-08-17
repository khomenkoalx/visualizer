# Визуализация образований ЖКТ

## Описание

Проект предназначен для визуализации образований желудочно-кишечного тракта (ЖКТ). Основные пользователи программы врачи-эндоскописты. Программа позволяет создавать готовые к печати файлы для наглядной демонстрации пациенту имеющихся у него образований ЖКТ.

## Возможности

- Внесение личных данных пациента.
- Добавление текстовых блоков с описанием локализации и типов образований.
- Визуализация связей между блоками и изображением органа.
- Экспорт результата в PDF.

## Установка

### 1. Клонирование репозитория

Сначала клонируйте репозиторий:

```bash
git clone https://github.com/khomenkoalx/visualizer.git
```


### 2. Установка зависимостей
Перейдите в папку проекта и установите зависимости:

```bash
cd visualizer
pip install -r requirements.txt
```

### 3. Запуск проекта
Для запуска проекта выполните:

```bash
python main.py
```

Вы также можете создать исполняемый файл (.exe) с использованием PyInstaller:

```bash
pyinstaller --onefile --windowed --add-data "resources/Arial.ttf;resources" --add-data "resources/Arial-Bold.ttf;resources" --add-data "resources/digest.png;resources" main.py
```

### 4. Структура проекта
main.py - Главный файл приложения.  
drawing.py - Контроллер для работы с изображениями.  
state.py - Управление состоянием приложения.  
ui.py - Пользовательский интерфейс приложения.  
constants.py - Константы и конфигурации.  
resources/ - Папка с ресурсами (шрифты, изображения).  
>-Arial.ttf - Обычный шрифт.  
>-Arial-Bold.ttf - Полужирный шрифт.  
>-digest.png - Изображение ЖКТ.  

### 5. Зависимости
Python 3.12  
Tkinter  
Pillow  
ReportLab  
PyInstaller

## 6. Как использовать
1. Запустите приложение.
2. Заполните информацию о пациенте.
3. Выберите нужный протокол обследования (ФЭГДС/ФКС).
4. Выберите необходимые локализации, отметьте соответствующие образования, введите комментарии.
5. Для получения готового к печати файла нажмите кнопку "Экспорт в PDF"

# Примечания
Все ресурсы, включая шрифты и изображения должны находиться в папке resources.
В файле constants.py можно изменить путь к необходимым Вам папкам.
Для создания исполняемого файла убедитесь, что все ресурсы включены в сборку.

# Контакты
Для вопросов и предложений: Telegram - @drkhomenko, email - a.khomenko42@gmail.com