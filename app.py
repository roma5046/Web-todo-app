from flask import Flask, render_template, request, redirect, url_for, session, flash # Импорт необходимых функций из Flask
from werkzeug.security import generate_password_hash, check_password_hash # Импорт хэширования паролей

app = Flask(__name__) #Создание экземпляра приложения
app.secret_key = "supersecretkey" # Ключ для работы сессий

users = {} # Словарь пользователей: username -> hashed_password
tasks = {} # Словарь: username -> список задач

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users:
            flash("Пользователь уже существует")
        else:
            users[username] = generate_password_hash(password)
            tasks[username] = []
            flash("Регистрация успешна, войдите в систему")
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users and check_password_hash(users[username], password):
            session['user'] = username
            return redirect(url_for('home'))
        else:
            flash("Неверный логин или пароль")
    return render_template('login.html')

@app.route('/') # Главная страница со списком задач
def home():
    if 'user' not in session: # Проверка авторизации
        return redirect(url_for('login'))   # Если не авторизован, редирект на логин
    user_tasks = tasks[session['user']]     # Получение задач текущего пользователя
    return render_template('index.html', tasks=user_tasks) # Отображение списка задач

@app.route('/add', methods=['POST'])# Маршрут добавления новой задачи, только POST-запросы
def add_task():
    if 'user' not in session: # Проверка авторизации
        return redirect(url_for('login')) # Редирект если не авторизован
    title = request.form.get('title') # Получение названия задачи из формы
    description = request.form.get('description') # Получение описания задачи из формы
    tasks[session['user']].append({'title': title, 'description': description, 'done': False}) # Добавление задачи в список, отметка выполнения
    return redirect(url_for('home')) # Перенаправление на главную страницу

@app.route('/delete/<int:index>')  # маршрут для удаления задачи по индексу
def delete_task(index):
    if 'user' not in session: # Проверка авторизации
        return redirect(url_for('login')) # Редирект если не авторизован
    user_tasks = tasks[session['user']]     # Получение списка задач пользователя
    if 0 <= index < len(user_tasks):  	    # Проверка индекса
        deleted_task = user_tasks.pop(index)    # Удаление задачи из списка
        flash(f"Задача '{deleted_task['title']}' удалена") # Вывод сообщения пользователю о удалении задачи
        return redirect(url_for('home'))  # Возврат на главную страницу

@app.route('/toggle/<int:index>')  # Маршрут для изменения статуса выполнения задачи
def toggle_task(index):
    if 'user' not in session: # Проверка авторизации
         return redirect(url_for('login')) # Редирект если не авторизован
    user_tasks = tasks[session['user']] # Получение списка задач пользователя
    if 0 <= index < len(user_tasks):  # Проверка индекса
        user_tasks[index]['done'] = not user_tasks[index]['done']  # Переключение статуса задачи
        flash(f"Задача '{user_tasks[index]['title']}' помечена как {'выполненная' if user_tasks[index]['done'] else 'невыполненная'}") # Вывод сообщения пользователю о текущем статусе задачи
    return redirect(url_for('home'))  # Возврат на главную страницу

@app.route('/logout') # Выход пользователя
def logout():
    session.pop('user', None) # Удаление пользователя из сессии
    return redirect(url_for('login')) # Перенаправление на логин

# Запуск сервера, если файл запущен
if __name__ == '__main__': # Запуск сервера, если файл запущен
    app.run(debug=True) # Запуск серверa в режиме отладки
