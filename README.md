# tap_game

### Для успешного разворачивания при локальной разработке:
1. На основе .env.example создать и заполнить значениями .env файл в корневой директории репозитория
2. Собрать и запустить docker-контейнер командой в терминале
   </br>
    ```docker compose up -d --build```
3. Накатить миграции
   </br>
   ```docker compose exec -it app alembic upgrade head```
4. Сделать посев (создать 100 тестовых пользователей)
   </br>
   ```docker compose exec -it app python seed.py```

### Бот для админа: [здесь]((https://t.me/cr_user_admin_bot))

### Production bot: [здесь](https://t.me/cr_prod_bot)

## Примеры запросов к API   
1. Получение списка всех пользователей</br>

```bash
curl -X GET "http://localhost:8000/user?api-key=sokfe30230fe9wdjhsuhcnaop!29eu-fjAFK229JDNFD"
```
#### Postman

![](requests_api_exmaples/get_all.png)
2. Получение конкретного пользователя по username
```bash
curl -X GET "http://localhost:8000/user/{username}?api-key=sokfe30230fe9wdjhsuhcnaop!29eu-fjAFK229JDNFD"
```
#### Postman
![](requests_api_exmaples/get_user.png)
3. Создание нового пользователя
```bash
curl -X POST "http://localhost:8000/user?api-key=sokfe30230fe9wdjhsuhcnaop!29eu-fjAFK229JDNFD" \
-H "Content-Type: application/json" \
-d '{
    "username": "new_user",
    "telegram_uid": 24424
}'
```
#### Postman
![](requests_api_exmaples/create_user.png)
4. Редактирование существующего пользователя по telegram_uid
```bash
curl -X PUT "http://localhost:8000/user/{uid}?api-key=sokfe30230fe9wdjhsuhcnaop!29eu-fjAFK229JDNFD" \
-H "Content-Type: application/json" \
-d '{
    "username": "new_user",
    "coins": 22144,
    "rating": 21242
}'
```
#### Postman
![](requests_api_exmaples/edit_user.png)

