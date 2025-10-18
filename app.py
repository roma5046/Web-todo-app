from flask import Flask, render_template, request, redirect, url_for # Импорт необходимых функций из Flask

app = Flask(__name__) #Создание экземпляра приложения

tasks = [] # Список задач (в памяти)

@app.route('/') # Маршрут для главной страницы
def home():
    return render_template('index.html', tasks=tasks) # указание HTML-шаблона и передача списока задач

@app.route('/add', methods=['POST'])# Маршрут добавления новой задачи, только POST-запросы
def add_task():
    title = request.form.get('title') # Получение названия задачи из формы
    description = request.form.get('description') # Получение описания задачи из формы
    tasks.append({'title':title, 'description': description}) # Добавление задачи в список
    return redirect(url_for('home')) # Перенаправление на главную страницу

# Запуск сервера, если файл запущен
if __name__ == '__main__': # Запуск сервера, если файл запущен
    app.run(debug=True) # Запуск серверa в режиме отладки
