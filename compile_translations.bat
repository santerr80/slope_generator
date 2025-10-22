@echo off
echo Compiling translation files...

REM Set path to lrelease
set LRELEASE="C:\Users\sante\anaconda3\Library\bin\lrelease.exe"

REM Check if lrelease is available
if not exist %LRELEASE% (
    echo Error: lrelease not found at %LRELEASE%
    echo Please check the path or install Qt SDK.
    pause
    exit /b 1
)

REM Compile each translation file
echo Compiling Russian translation...
%LRELEASE% i18n\ru.ts

echo Compiling English translation...
%LRELEASE% i18n\en.ts

echo Compiling French translation...
%LRELEASE% i18n\fr.ts

echo Compiling German translation...
%LRELEASE% i18n\de.ts

echo.
echo Translation compilation completed!
echo Compiled files:
dir i18n\*.qm

pause
