# sarenkov-SkillFactory-B6
Homework

Для проверки работы необходимо:
  1. Скачать скрипт
  2. Запустить скрипт
  3. Установить пакет httpie
  4. Открыть командную строку
  5. Выполнить в командной строке: http -f POST localhost:8080/albums year="2015" artist="Madonna" genre="Female" album="empty" 
     Параметры можно менять на произвольные
  6. Для проверки GET запроса можно выполнить в командной строке http -f GET localhost:8080/albums/Madonna 
     Параметр можно менять произвольно. 
     Но красивше будет открыть страницу http://localhost:8080/albums/Madonna в браузере при запущенном скрипте.
