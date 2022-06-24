##NumbersTest.
https://docs.google.com/spreadsheets/d/1x3q1Tkj4I_gViKM0SNQpMZwqN66QwoNDXDFuzU8oJR8/edit#gid=0
###Instruction how-to quickly setup:

1. ```git clone https://github.com/Zarbul/numbers_test.git```
2. Install requierements:
   * ```pip install -r req.txt```
3. Добавил файл образец .env
4. Make migrations
```
./manage.py makemigrations
./manage.py migrate
```
5. ####Install RabbitMQ
   #### Install from docker:
* ```sudo docker volume create rabbitmq_data```
* ```sudo docker run -d --hostname rabbitmq --log-driver=journald --name rabbitmq -p 5672:5672 -p 15672:15672 -p 15674:15674 -p 25672:25672 -p 61613:61613 -v rabbitmq_data:/var/lib/rabbitmq rabbitmq:3.9-management```
* ```sudo docker exec -it rabbitmq /bin/bash```
* #### Create user and password:
* ```rabbitmqctl add_user numbers numbers2022```
* #### Create virtualhost:
* ```rabbitmqctl add_vhost numbershost```
* #### Setting Permissions:
* ```rabbitmqctl set_permissions -p "numbershost" "numbers" ".*" ".*" ".*"```
* ####проверяем список оставшихся юзеров
* ```rabbitmqctl list_users```
* ####Удаляем всех ненужных (особенно базовый - guest)
* ```rabbitmqctl delete_user 'guest'```
6. Установить PostgreSQL.
* создать базу с параметрами из файла ```.env```

7. Запустить Селери в другом терминале:
```
celery -A config worker -l info
```

7.1 Запустить Celery Beat (он же CRON) в другом
```
celery -A config beat -l INFO
``` 