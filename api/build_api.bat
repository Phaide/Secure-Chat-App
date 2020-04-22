@echo off

REM Move the cursor to where the batch file is
cd %~dp0%

REM Build "Dockerfile" and name it "sca-api"
docker build -t sca-api .

REM Run the image in a new container
docker run -p 42202:42202 sca-api

pause
