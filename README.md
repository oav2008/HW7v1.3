# HWin7v1.3
Зависимости:
	pip install pyinstaller			>> if need
	pip install impacket
	\mysmb.py
	\files	с файлами етблю, даблпульс...
	\dlls	с длл
	\logs	с любым файлом
	pyinstaller -F --add-data ../files;files/ --add-data ..dlls;dlls --add-data ..logs;logs HWin7v1.3.py
папка logs не должна быть пустой
	Запуск через cmd окно. Принимает 1 ip или ip/24 /16 ...etc.
Создаёт администратора local_service:flvbyrf в русской win7 32/64 (если поправить, может XP)
Создаёт файл check_log.txt в папке C:\Windows\Temp 

Антивирус может ловить извлечённые файлы в C:\Users\юзер\AppData\Local\Temp
