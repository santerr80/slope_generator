param(
    [string[]]$Locales
)

# Get all .py and .ui files
$PythonFiles = Get-ChildItem -Recurse -Include "*.py", "*.ui"

# Find the newest file
$ChangedFiles = 0
foreach ($file in $PythonFiles) {
    $changed = $file.LastWriteTime.Ticks
    if ($changed -gt $ChangedFiles) {
        $ChangedFiles = $changed
    }
}

# Check if we need to update
$Update = $false
foreach ($locale in $Locales) {
    $TranslationFile = "i18n\$locale.ts"
    if (-not (Test-Path $TranslationFile)) {
        # Force translation string collection as we have a new language file
        New-Item -Path $TranslationFile -ItemType File -Force | Out-Null
        $Update = $true
        break
    }
    
    $ModificationTime = (Get-Item $TranslationFile).LastWriteTime.Ticks
    if ($ChangedFiles -gt $ModificationTime) {
        # Force translation string collection as a .py file has been updated
        $Update = $true
        break
    }
}

if ($Update) {
    Write-Host "Please provide translations by editing the translation files below:"
    foreach ($locale in $Locales) {
        Write-Host "i18n\$locale.ts"
        # Note we don't use pylupdate with qt .pro file approach as it is flakey
        # about what is made available.
        & pylupdate4 -noobsolete *.py *.ui -ts "i18n\$locale.ts"
    }
} else {
    Write-Host "No need to edit any translation files (.ts) because no python files"
    Write-Host "has been updated since the last update translation."
}
