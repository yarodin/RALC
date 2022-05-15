# RALC - Russia Award Local Cluster
## Russian
Приложение показывающее споты по незакрытым слотам национальной дипломной радиолюбительской программы 
"Россия и Россия на всех диапазонах" на Hamlog - [https://hamlog.online/srr/russia/](https://hamlog.online/srr/russia/)

Приложение в автоматическом режиме получает с сайта hamlog.online данные о закрытых и незакрытых слотах по дипломной 
радилюбительской программе "Россия и Россия на всех диапазонах" для заданного позывного. После чего с телнет кластера 
типа VE7CC показываются только споты по незакрытым слотам, причем с учетом выбранных дополнительных настроек по 
диапазонам и модуляциям.

Документация: /help/

## EXE build
Сборка в один exe файл производится файлом build.cmd через pyinstaller с использование upx.

## English

Application for CC telnet clusters spots filtering based on ["National award RUSSIA"](https://hamlog.online/srr/russia/) completing statistic.