# RALC - Russia Award Local Cluster
## RUS
Приложение показывающее споты по незакрытым слотам национальной дипломной радиолюбительской программы 
"Россия и Россия на всех диапазонах" на Hamlog - [https://hamlog.online/srr/russia/](https://hamlog.online/srr/russia/)

Приложение в автоматическом режиме получает с сайта hamlog.online данные о закрытых и незакрытых слотах по дипломной 
радилюбительской программе "Россия и Россия на всех диапазонах" для заданного позывного. После чего с телнет кластера 
типа VE7CC показываются только споты по незакрытым слотам, причем с учетом выбранных дополнительных настроек по 
диапазонам и модуляциям.

Документация: /help/

## Сборка EXE
Сборка в один exe файл производится файлом build.cmd через pyinstaller с использование upx.

## ENG
Application for CC telnet clusters spots filtering based on ["National award RUSSIA"](https://hamlog.online/srr/russia/) 
completing statistic.

## Very quick start
* Get your ID, last 4 digits of URL from page with you personal statistic of ["National award RUSSIA"](https://hamlog.online/srr/russia/)
and set this ID and set this ID to **last field of 'Settings' -> 'Hamlog URL'**
* Set your callsign to **'Settings' -> 'Callsign'** 
* Push **Start** button on **'Spots'** page

## Build EXE
Start build.cmd to build one exe file