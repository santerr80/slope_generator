# Slope Generator Plugin Translation Guide

## Supported Languages

The plugin supports the following languages:
- Russian (ru)
- English (en) 
- French (fr)
- German (de)

## Translation Files Structure

```
i18n/
├── ru.ts          # Russian translation
├── en.ts          # English translation
├── fr.ts          # French translation
├── de.ts          # German translation
└── *.qm           # Compiled translation files
```

## Compiling Translations

### Linux/macOS
```bash
# Update translation files
make transup

# Compile translations
make transcompile
```

### Windows (PowerShell)
```powershell
# Update translation files
.\scripts\update-strings.ps1 ru en fr de

# Compile translations
.\scripts\compile-strings.ps1 lrelease ru en fr de
```

### Windows (Batch)
```cmd
# Update translation files
scripts\update-strings.bat ru en fr de

# Compile translations
scripts\compile-strings.bat lrelease ru en fr de
```

### Quick Compilation (Windows)
```cmd
# Use the convenient compilation script
compile_translations.bat
```

## Testing Translations

To test translations, open the plugin dialog in QGIS. The interface should automatically display in the language corresponding to your QGIS interface settings.

## Adding a New Language

1. Create a new file `i18n/XX.ts` where XX is the language code
2. Add the language code to `LOCALES` in the Makefile
3. Fill in the translations in the .ts file
4. Compile the translations

## Translation File Structure

Translation files use Qt TS (Translation Source) format:

```xml
<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE TS><TS version="2.0" language="XX" sourcelanguage="en">
<context>
    <name>SlopeGenerator</name>
    <message>
        <source>English text</source>
        <translation>Translated text</translation>
    </message>
</context>
</TS>
```

## Automatic Language Detection

The plugin automatically detects the QGIS interface language and loads the corresponding translation. If a translation for the current language is not available, English is used as the default language.

## Requirements

For compiling translations, you need:
- `pylupdate4` - for updating translation files
- `lrelease` - for compiling .ts files to .qm files

These tools are usually included in the Qt SDK.

## Troubleshooting

### Translations Not Working

1. **Check file names**: Ensure .qm files are named correctly (e.g., `ru.qm`, `en.qm`)
2. **Restart QGIS**: After making changes, restart QGIS completely
3. **Check locale**: Verify your QGIS locale settings
4. **File permissions**: Ensure the plugin has read access to translation files

### Common Issues

- **Missing translations**: Some strings may not be translated if they're missing from the .ts file
- **Wrong context**: Make sure the context name is `SlopeGenerator` in all translation files
- **Encoding issues**: Ensure all .ts files are saved in UTF-8 encoding

## Development Notes

- Translation files are automatically loaded when the plugin initializes
- The plugin uses Qt's translation system for internationalization
- All UI strings are set programmatically in Python code for better control
- Translation context is set to `SlopeGenerator` for consistency
