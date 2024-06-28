# Приложение My Cloud

### Deploy приложения на сервере.

1. На сервисе [reg.ru](https://www.reg.ru/vps/) необходимо арендовать виртуальный сервер VPS с ОС Ubuntu.
2. Настраиваем SSH ключ для безопасного подключения к серверу и для подтверждения своей идентичности.
Для macOS вводим в терминале:
```angular2html
ssh-keygen
```
для копирования ssh ключа:
```angular2html
cat ~/.ssh/id_rsa.pub
```
3. В личном кабинете сервиса REG.RU выбираем настройку SSL, где применяем ранее скопированный SSH ключ.
4. Используя терминал  и логин / пароль, которые пришли на почту после аренды сервера,
заходим на сервер через терминал:
```
ssh root@ip_adress_server  
```
Где логин это root.
5. Создаем нового пользователя:
```
adduser admin 
 ```
где admin это имя нового пользователя и подтверждаем паролем.
6. Предоставляем права новосму пользователю: 
```
usermod admin -aG sudo
```
7. Переключаем на пользователя:
```
su admin
```
8. Переходим в его директорию:
```angular2html
cd ~
```
9. Обновляем пакетный менеджер командой:
```
sudo apt update
```
10. Устанавливаем postgres для нашего приложения:
```
sudo apt install python3-pip postgresql
 ```
11. Устанавливаем виртуальное окружение: 
```
sudo apt install python3-venv
```
12. Заходим под пользователем Postgres  в систему sql :
```
sudo su postgres
psql
```
13. Cоздаем пользователя БД:
```
CREATE USER admin;
```
14. Создаем для него пароль: 
```
ALTER USER admin WITH PASSWORD 'password';
```
15. Присваиваем права суперпользователя:
```
    ALTER USER admin WITH SUPERUSER; 
```
16. Cоздаем БД с таким же именем как пользователь:
```
CREATE DATABASE admin;
```
17. Выходим из системы:
```
\q
Exit
```
18. Заходим под своим именем:
```
admin@cv3888091:~$ psql
```
19. Создаем БД:
```
CREATE DATABASE cloud_project;
\q
```
20. Клонируем проект с github:
```
git clone https://github.com/Mariza0/fpy-diplom-backend.git
```
21. Переходим в папку проекта:
```
cd fpy-diplom-backend
```
22. Создаем виртуальные окружение:
```
python3 -m venv env
```
23. Активируем виртуальные окружение:
```
source env/bin/activate
```
24. Устанавливаем все зависимости из проекта:
```
pip install -r requirements.txt
```
25. Создаем файл .env:
```
nano .env
```
26. Записываем в файле данные для работы приложения:
```
SECRET_KEY=8@!rm9a8r+7z=oqyqkz-0inj@3dskfhslf9&2ee^ez&69q9mr1dfku%s+t
DEBUG=False
ALLOWED_HOSTS=ip_address_вашего_VPS_сервера
DB_ENGINE=django.db.backends.postgresql
DB_NAME=cloud_project
DB_USER=admin
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
```
где SECRET_KEY произвольный набор символов. Можно сгенерировать на [сервисе](https://djecrety.ir/).
27. В активированном виртуальном окружении применяем миграции из проекта: 
```
python manage.py migrate
```
28. Создаем суперпользователя:
```angular2html
python manage.py createsuperuser
```
30. Собираем статику: 
```
python manage.py collectstatic
```
31. Выходим из виртуального окружения и устанавливаем nginx и запускаем:
```
sudo apt install nginx
sudo systemctl start nginx
```
32. Настраиваем конфигурационные файлы для управления nginx:
```angular2html
sudo nano /etc/nginx/sites-available/project
```
где вместо project может быть любое имя.
содержимое файла:
```angular2html
server {
    listen 80;
    server_name 89.111.175.58;

    location / {
        root /home/admin/fpy-diplom-backend/static/react/dist/;
        try_files $uri $uri/ /index.html;
    }

    # Обслуживание статических файлов
    location /static/ {
        alias /home/admin/fpy-diplom-backend/static/;
        try_files $uri $uri/ =404;
    }
    # Проксирование запросов к /admin/ на Django-сервер
    location /admin/ {
        proxy_pass http://unix:/home/admin/fpy-diplom-backend/app/project.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
# Проксирование запросов к /api/ на Django-сервер
    location /api/ {
        proxy_pass http://unix:/home/admin/fpy-diplom-backend/app/project.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    # Проксирование запросов к /storage/ на Django-сервер
    location /storage/ {
        proxy_pass http://unix:/home/admin/fpy-diplom-backend/app/project.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
        # Проксирование запросов к /users/ на Django-сервер
    location /users/ {
        proxy_pass http://unix:/home/admin/fpy-diplom-backend/app/project.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

```
33. Открываем редактор ```sudo nano /etc/nginx/nginx.conf``` и добавляем:
```
http {
...
    upstream backend {
        server unix:/home/admin/fpy-diplom-backend/app/project.sock;
    }   
    
    client_max_body_size 10000M;  # увеличиваем ограничение на размер файлов, допустимого для пользователей.

...
```
34. Создаем ссылку:
```
sudo ln -s /etc/nginx/sites-available/project /etc/nginx/sites-enabled/
```
35. Устанавливаем wsgi сервер для взаимодействия веб-сервера и python приложением. Будем устанавливать блиотеку gunicorn.
Активируем виртуальное окружение и устанавливаем 
```
pip install gunicorn
```
36. Указываем как подключать gunicorn: 
```
gunicorn app.wsgi --bind 0.0.0.0:8000
 ```
где app - это основное python приложение, а порт это то, к чему привязываем gunicorn.

37. Настраиваем, чтобы gunicorn был всегда запущен. Выходим из виртуального окружения и открываем конфигурационный файл:
```
sudo nano /etc/systemd/system/gunicorn.service
```
Содержимое файла:
```
[Unit]
Description=service for wsgi
After=network.target

[Service]
User=admin
Group=www-data
WorkingDirectory=/home/admin/fpy-diplom-backend
ExecStart=/home/admin/fpy-diplom-backend/env/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/admin/fpy-diplom-backend/app/project.sock app.wsgi:application

[Install]
WantedBy=multi-user.target
```
38. Активируем gunicorn:
```angular2html
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```
39. Перезапускаем nginx:
```angular2html
sudo systemctl restart nginx
```
Если при запуске сервера будет ошибка 500 и в логах ```sudo tail -n 50 /var/log/nginx/error.log```
сообщение Permission denied необходимо предоставить 
доступ nginx к Permission 
```/home/admin/fpy-diplom-backend/static/react/dist/:```
```angular2html
sudo chmod 755 /home/admin
sudo chown -R admin:www-data /home/admin/fpy-diplom-backend
sudo systemctl restart nginx
sudo systemctl restart gunicorn
```

-------------------------------------------
деплой react приложения
------------------------------------------
 - Перейдите в редактор вашего React-проекта и выполните команду сборки:
```
npm run build
```
в результате сборки будем создана папка dist в корне проекта react.
- На сервере в директории fpy-diplom-backend/static создаем директорию react и перемещаем туда созданную ранее папку dist.

