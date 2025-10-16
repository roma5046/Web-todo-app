from flask import Flask # Импорт Flask

app = Flask(__name__) #Создание экземпляра приложения
# Определение маршрута (адрес) для главной страницы
@app.route('/')
def home():
    return "hello word! Этот проект будет использовать фреймворк Flask."
# Запуск сервера, если файл запущен
if __name__ == '__main__':
    app.run(debug=True)