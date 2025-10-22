param(
    [string]$LRelease,
    [string[]]$Locales
)

foreach ($locale in $Locales) {
    Write-Host "Processing: $locale.ts"
    # Note we don't use pylupdate with qt .pro file approach as it is flakey
    # about what is made available.
    & $LRelease "i18n\$locale.ts"
}
