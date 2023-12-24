## Запуск vk-tg-sync в Docker

Вы можете запустить этот проект в Docker. Вы можете собрать `image` самостоятельно с помощью `Dockerfile` или взять `image` из Docker Hub: [delitel/vk-tg-sync](https://hub.docker.com/repository/docker/delitel/vk-tg-sync/general)

В корне проекта находится `docker-compose.yml`, вы можете использовать его для запуска сразу mysql и vk-tg-sync.

Для контейнера `vk-tg-sync` и `db` вам необходимо указать переменные окружения:
```yml
vk-tg-sync:
    image: delitel/vk-tg-sync:latest
    container_name: vk-tg-sync
    environment:
        - DB_PASS=
        - DB_IP=db
        - DB_NAME=vk_tg_sync
        - TG_BOT_TOKEN=
        - VK_BOT_TOKEN=
    depends_on:
        - db
```

```yml
db:
    image: mysql:8.0
    restart: always
    environment:
      MYSQL_DATABASE: vk_tg_sync
      MYSQL_ROOT_PASSWORD: 
    volumes:
      - "./db_data:/var/lib/mysql"
```

> Переменные `DB_PASS` и `DB_NAME` должны быть одинаковы у обоих контейнеров!

После успешного запуска контейнеров перейдите в bash окружение контейнера `vk-tg-sync` командой:
```shell
docker ps # Узнаём id контейнера
docker exec -it <ТУТ_ID_Контейнера> bash
```

И применяем миграции для БД командой:
```shell
alembic upgade head
```