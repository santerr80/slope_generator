.. SlopeGenerator documentation master file, created by
   sphinx-quickstart on Sun Feb 12 17:11:03 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to SlopeGenerator's documentation!
=========================================

Overview
--------

SlopeGenerator creates slope hachures using QGIS Geometry Generator expressions. It links crest and toe lines from a single line layer via an ID field and styles the crest category non-destructively.

Key capabilities:

- Automatic main and intermediate strokes for multiple slope types.
- Percent-based intermediate strokes option: the first short stroke length can be set as a percentage of the full base stroke (distance to the opposite side). For Forced slope, the second short stroke begins after the first (plus gap), inheriting the same basis for the first stroke.
- Scale-aware parameters using ``@map_scale``.

Parameters
----------

- Step: spacing of main strokes.
- Intermediate: first short stroke length; can be in units or percent when the checkbox “% of total length inter. stroke” is enabled in the dialog.
- Gap: gap between the first and second short strokes (Forced).
- Second: length of the second short stroke (Forced).
- Trim: trims the end of the line symbol (data-defined).

Usage
-----

1. Select the line layer containing both crest and toe.
2. Choose the pair ID field (e.g., ``SLOPE_ID``) and a categorization field.
3. Pick crest and toe category values.
4. Choose slope type and set parameters. Enable the percent checkbox if you want ``Intermediate`` as a percentage of the full base stroke.
5. Apply — the style is appended to the crest category.

Contents:

.. toctree::
   :maxdepth: 2

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

