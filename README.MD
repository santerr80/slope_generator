# QGIS Slope Generator Plugin

A QGIS plugin that automatically generates slope symbols (hachures) based on line layers containing the top (crest) and bottom (toe) of the slopes. The styling is applied non-destructively using a geometry generator.

![Plugin in action](./assets/demo.mp4)
*(Note: Replace this link with an actual GIF demonstrating your plugin)*

## Key Features

*   **Automatic Styling:** Creates complex slope symbols in just a few clicks.
*   **Non-Destructive Editing:** Uses QGIS's **Geometry Generator**, leaving your original data untouched.
*   **Flexible Configuration:** Allows the user to select the layer, as well as the fields for slope identification and categorization.
*   **Multiple Slope Types:** Includes several preset styles (e.g., unreinforced, reinforced, cliff) that can be easily extended.
*   **Dynamic Display:** The symbols adapt to the current map scale.
*   **Quick Categorization:** Automatically applies a unique style to the layer based on the values in a chosen attribute field.

## Data Requirements

For the plugin to work correctly, your data must be structured in a specific way.

1.  **Single Line Layer:** All lines (both the top/crest and bottom/toe of the slopes) must be in a **single** vector layer.
2.  **Categorization Field:** The layer must have an attribute field that clearly distinguishes lines as either "top of slope" (crest) or "bottom of slope" (toe). For example, a `TYPE` field with values `top` and `bottom`, or a `CODE` field with values like `512210000` and `512220000`.
3.  **Unique Slope ID Field:** The layer must have a field containing a unique identifier for **each pair** of top and bottom lines. This allows the plugin to correctly link each top line to its corresponding bottom line.

#### Example Attribute Table

| id | geometry   | TYPE   | SLOPE_ID |
| -- | ---------- | ------ | -------- |
| 1  | LineString | `top`  | `101`    |
| 2  | LineString | `bottom` | `101`    |
| 3  | LineString | `top`  | `102`    |
| 4  | LineString | `bottom` | `102`    |

## Workflow

1.  **Prepare your data** according to the requirements above.
2.  **Open the plugin** by clicking its icon in the QGIS toolbar.
3.  **Select the line layer** that contains your slopes.
4.  **Select the Slope ID field** (e.g., `SLOPE_ID` from the example).
5.  **Select the field for styling/categorization** (e.g., `TYPE`). The plugin will automatically color the layer based on the unique values in this field.
6.  In the **"Top of Slope Category"** and **"Bottom of Slope Category"** dropdowns, choose the appropriate values that were populated after categorization.
7.  **Choose the desired slope style** (e.g., "Unreinforced slope dynamic").
8.  Click the **"Apply"** button. The style will be added to the selected "Top of Slope" category.

## Installation

1.  Open QGIS.
2.  Go to `Plugins` -> `Manage and Install Plugins...`.
3.  In the search bar, find `Slope Generator`.
4.  Click the `Install Plugin` button.
5.  After installation, the plugin icon will appear in your toolbar.

*(If the plugin is not yet published in the official QGIS repository, describe the installation process from a ZIP archive here).*

## Feedback and Contribution

*   If you find a bug, please create an [Issue](https://github.com/santerr80/SlopeGenerator/issues) in this repository.
*   Suggestions for improvements and new features are welcome.
*   Pull requests to enhance the code are also welcome.

## License

This plugin is distributed under the terms of the **GNU General Public License v2.0** or any later version.

## Author

*   **santerr80**
*   Email: [santerr80@gmail.com](mailto:santerr80@gmail.com)