@echo off
setlocal enabledelayedexpansion

REM Get all locales from command line arguments
set LOCALES=%*

REM Get newest .py files so we don't update strings unnecessarily
set CHANGED_FILES=0
for /r %%f in (*.py *.ui) do (
    for %%t in ("%%f") do set CHANGED=%%~tf
    if !CHANGED! gtr !CHANGED_FILES! (
        set CHANGED_FILES=!CHANGED!
    )
)

REM Qt translation stuff
REM for .ts file
set UPDATE=false
for %%L in (%LOCALES%) do (
    set TRANSLATION_FILE=i18n\%%L.ts
    if not exist !TRANSLATION_FILE! (
        REM Force translation string collection as we have a new language file
        type nul > !TRANSLATION_FILE!
        set UPDATE=true
        goto :break
    )
    
    for %%t in ("!TRANSLATION_FILE!") do set MODIFICATION_TIME=%%~tf
    if !CHANGED_FILES! gtr !MODIFICATION_TIME! (
        REM Force translation string collection as a .py file has been updated
        set UPDATE=true
        goto :break
    )
)

:break
if "%UPDATE%"=="true" (
    echo Please provide translations by editing the translation files below:
    for %%L in (%LOCALES%) do (
        echo i18n\%%L.ts
        REM Note we don't use pylupdate with qt .pro file approach as it is flakey
        REM about what is made available.
        pylupdate4 -noobsolete *.py *.ui -ts i18n\%%L.ts
    )
) else (
    echo No need to edit any translation files (.ts) because no python files
    echo has been updated since the last update translation.
)
