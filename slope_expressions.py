"""
QGIS geometry generator expression templates for slope symbology.

The plugin replaces placeholders in these templates at runtime to produce
valid QGIS expressions:
- __CAT_FIELD__: name of the categorization field (string literal)
- __BOTTOM_CAT_VALUE__: category value representing the bottom slope side (string literal)
- __ID_FIELD__: name of the feature id field to match bottom feature (string literal)
- __STEP__: main stroke spacing, scaled by map scale
- __INTERMEDIATE__: intermediate short-stroke value
- __INTERMEDIATE_IS_PERCENT__: 1 treats __INTERMEDIATE__ as percent of full length, 0 as units
- __GAP__: gap between first and second short strokes (forced slope)
- __SECOND__: length of the second short stroke (forced slope)

All numeric placeholders are injected as numbers (no quotes). String
placeholders are injected as quoted strings to be valid in QGIS `map()` calls.
"""

EXPRESSIONS = {
    "Unreinforced slope": """
    collect_geometries(
  with_variable(
    'vars',
    map(
      -- Steamline geometry
      'target_geom', geometry(
        get_feature(
          @layer,
          map(__CAT_FIELD__, __BOTTOM_CAT_VALUE__, __ID_FIELD__, attribute(__ID_FIELD__))
        )
      ),
      -- Translated into unit maps
      'step', (@map_scale * __STEP__) / 1000, -- The step of the main strokes
      'intermediate', (@map_scale * __INTERMEDIATE__) / 1000 -- Units-based intermediate length (unused if percent mode)
    ),

    if(
      map_get(@vars,'target_geom') is null,
      make_line(make_point(0,0),make_point(0,0)),

      array_cat(

        -- Block 1: Basic strokes
        array_foreach(
          generate_series(0, length($geometry), map_get(@vars,'step')),
          with_variable('pt', line_interpolate_point($geometry,@element),
            make_line(
              @pt,
              closest_point(map_get(@vars,'target_geom'), @pt)
            )
          )
        ),

        -- Block 2: Intermediate strokes
        array_foreach(
          generate_series(map_get(@vars,'step')/2, length($geometry), map_get(@vars,'step')),
          with_variable('pt', line_interpolate_point($geometry,@element),
          with_variable('end', closest_point(map_get(@vars,'target_geom'), @pt),
          with_variable('line', make_line(@pt,@end),
            with_variable(
              'inter_len',
              if(
                __INTERMEDIATE_IS_PERCENT__ = 1,
                length(@line) * (__INTERMEDIATE__) / 100,
                map_get(@vars,'intermediate')
              ),
              make_line(
                @pt,
                line_interpolate_point(
                  @line,
                  min(@inter_len, length(@line))
                )
              )
            )
          )))
        )
      )
    )
  )
)
    """,
    "Forced slope": """
collect_geometries(
  with_variable(
    'vars',
    map(
      'target_geom', geometry(
        get_feature( @layer, map(__CAT_FIELD__, __BOTTOM_CAT_VALUE__, __ID_FIELD__, attribute(__ID_FIELD__)))
      ),
      'step', (@map_scale * __STEP__) / 1000, -- The step of the main strokes
      'intermediate', (@map_scale * __INTERMEDIATE__) / 1000, -- Units-based intermediate length (unused if percent mode)
      'gap', (@map_scale * __GAP__) / 1000, -- The length of the gap
      'second', (@map_scale * __SECOND__) / 1000 -- The length of the second short stroke
    ),
    if(
      map_get(@vars,'target_geom') is null,
      make_line(make_point(0,0), make_point(0,0)),

      -- We combine three arrays through nested array_cat
      array_cat(
        array_cat(
          -- Block 1: Basic strokes
          array_foreach(
            generate_series(0, length($geometry), map_get(@vars,'step')),
            make_line(
              line_interpolate_point($geometry, @element),
              closest_point(map_get(@vars,'target_geom'), line_interpolate_point($geometry, @element))
            )
          ),

          -- Block 2: First intermediate strokes
          array_foreach(
            generate_series(map_get(@vars,'step')/2, length($geometry), map_get(@vars,'step')),
            with_variable('start', line_interpolate_point($geometry, @element),
              with_variable('end', closest_point(map_get(@vars,'target_geom'), @start),
                with_variable('line', make_line(@start, @end),
                  with_variable(
                    'inter_len',
                    if(
                      __INTERMEDIATE_IS_PERCENT__ = 1,
                      length(@line) * (__INTERMEDIATE__) / 100,
                      map_get(@vars,'intermediate')
                    ),
                    make_line(
                      @start,
                      line_interpolate_point(@line, min(@inter_len, length(@line)))
                    )
                  )
                )
              )
            )
          )
        ),

        -- Block 3: Second (additional) intermediate strokes
        array_foreach(
          generate_series(map_get(@vars,'step')/2, length($geometry), map_get(@vars,'step')),
          with_variable('start', line_interpolate_point($geometry, @element),
            with_variable('end', closest_point(map_get(@vars,'target_geom'), @start),
              with_variable('line', make_line(@start, @end),
                with_variable(
                  'pos1',
                  min(
                    if(
                      __INTERMEDIATE_IS_PERCENT__ = 1,
                      length(@line) * (__INTERMEDIATE__) / 100,
                      map_get(@vars,'intermediate')
                    ),
                    length(@line)
                  ),
                  with_variable('pos2', @pos1 + map_get(@vars,'gap'),
                    if(
                      @pos2 < length(@line),
                      make_line(
                        line_interpolate_point(@line, @pos2),
                        line_interpolate_point(@line, min(length(@line), @pos2 + map_get(@vars,'second')))
                      ),
                      geom_from_wkt('LINESTRING EMPTY')
                    )
                  )
                )
              )
            )
          )
        )
      )
    )
  )
)

    """,
    "Cliff": """
collect_geometries(
    with_variable(
        'target_geom',
        geometry(
            -- Placeholders will be replaced by plugin code at runtime
            get_feature( @layer, map(__CAT_FIELD__, __BOTTOM_CAT_VALUE__, __ID_FIELD__, attribute(__ID_FIELD__)))
        ),
        if(
            @target_geom is not null,
            with_variable(
                'step', (@map_scale * __STEP__) / 1000,
                array_foreach(
                    generate_series(0, length($geometry), @step),
                    make_line(
                        line_interpolate_point($geometry, @element),
                        closest_point(@target_geom, line_interpolate_point($geometry, @element))
                    )
                )
            ),
            make_line(make_point(0,0), make_point(0,0))
        )
    )
)
    """,
}
