Копирование приложений из QS на QS2

Аутентификация через virtual proxy "header-authentification"

Таски находятся в папке tasks

Для добавления новой таски:
    -скопировать любой существующий .bat, переименовать (имя будет отображаться в логах)
    -внутри файла поменять app_id на id нужного приложения
    -создать новый external program task в QMC QS, с ссылкой на новый .bat

пример .bat
@echo off
cd C:\QS_to_QS2\
set "app_id=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx "
set "script_name=%~n0"
call venv\Scripts\activate
set "app_id=%app_id%"
start cmd /k "python -u main.py & timeout /t 5 & exit"


обрабатываются только опубликованные приложения!!!
на QS2 должен юыть предварительно создан поток с соответствующим названием, как на QS!!

ДЛЯ ДОБАВЛЕНИЯ НОВОГО ПРИЛОЖЕНИЯ ВАЖНО КОРРЕКТНО УКАЗАТЬ ID
БЕЗ ЛИШНИХ СИМВОЛОВ И КАВЫЧЕК В ВИДЕ 94738bc7-90be-4397-97a2-b09900db97a6

Процесс состоит из трех этапов


1. Экспорт приложения из QS.
1.1 export шаг 1 - post
1.2 export шаг 2 - get (сохраняет файл приложения в папку exported_qvf_apps в корне проекта)

2. Копирование экспортированного приложения на QS2 (копирует приложение из exported_qvf_apps в importfolder на QS2)

3. Импорт приложения (файл приложения должен находиться в папке importfolder (см.документацию API))

Если приложение ранее не импортировалось, то:
3.1 import - post
3.2 publish - put

Если приложение уже импортировано и опубликовано:

3.1 replace - post


Если на QS2 найдется два или более опубликованных приложений с названием, равным названию переносимого приложения,
то обработано будет приложение с наиболее поздней датой публицации

все шаги выполняются в указанной выше последовательности для каждого приложения - по одному приложению за раз,
асинхронная обработка шагов для разных приложений будет блокировать сессии

логи QS_to_QS2.log

замер времени в results.csv (перезаписывается после каждого запуска)