@echo off

REM Move the cursor to where the batch file is
cd %~dp0%
cd nodes_registry_db

echo Please change the database's password in the file nodes_registry_db/docker-compose.yml if not already done.
pause

REM Build the database
docker-compose up

pause
