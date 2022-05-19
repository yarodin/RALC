# RALC - Russia Award Local Cluster
## RUS
Приложение показывающее споты по незакрытым слотам национальной дипломной радиолюбительской программы 
"Россия и Россия на всех диапазонах" на Hamlog - [https://hamlog.online/srr/russia/](https://hamlog.online/srr/russia/)

Приложение в автоматическом режиме получает с сайта hamlog.online данные о закрытых и незакрытых слотах по дипломной 
радилюбительской программе "Россия и Россия на всех диапазонах" для заданного позывного. После чего с телнет кластера 
типа VE7CC показываются только споты по незакрытым слотам, причем с учетом выбранных дополнительных настроек по 
диапазонам и модуляциям.

Документация: /help/

## Очень быстрый старт 
* Внесите последние 4 цифры адреса страницы с вашей персональной статистикой [дипломной программы "Россия и Россия на всех диапазонах"](https://hamlog.online/srr/russia/)
в последнее поле опции **'Hamlog URL'** на странице **'Settings'**
* Укажите ваш позывной в поле **'Callsign'**  на странице **'Settings'** 
* Нажмите кнопку **'Save'** на странице **'Settings'**
* Нажмите кнопку **'Start'** на странице **'Spots'**

## Сборка EXE
Сборка в один exe файл производится запуском build.cmd. Для сборки используются pyinstaller с upx.
venv должен находится в директории с build.cmd

## ENG
Application for CC telnet clusters spots filtering based on ["National award RUSSIA"](https://hamlog.online/srr/russia/) 
completing statistic.

## Very quick start
* Get your ID, last 4 digits of URL from page with you personal statistic of ["National award RUSSIA"](https://hamlog.online/srr/russia/)
and set this ID and set this ID to **last field of 'Settings' -> 'Hamlog URL'**
* Set your callsign to **'Settings' -> 'Callsign'** 
* Press **'Save'** button on **'Settings'** page
* Press **'Start'** button on **'Spots'** page

## Build EXE
Start build.cmd to build one exe file.
venv should be at the same directory with build.cmd