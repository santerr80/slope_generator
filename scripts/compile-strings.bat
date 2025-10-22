@echo off
setlocal

set LRELEASE=%1
set LOCALES=%2

for %%L in (%LOCALES%) do (
    echo Processing: %%L.ts
    REM Note we don't use pylupdate with qt .pro file approach as it is flakey
    REM about what is made available.
    "%LRELEASE%" i18n\%%L.ts
)
