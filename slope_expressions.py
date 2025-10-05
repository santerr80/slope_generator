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
      'step', (@map_scale * 2) / 1000, -- The step of the main strokes
      'intermediate', (@map_scale * 2.5) / 1000 -- The length of the additional stroke
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
            make_line(
              @pt,
              line_interpolate_point(
                @line,
                min(map_get(@vars,'intermediate'), length(@line))
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
      'step', (@map_scale * 2) / 1000, -- The step of the main strokes
      'intermediate', (@map_scale * 2.5) / 1000, -- The length of the additional stroke
      'gap', (@map_scale * 0.3) / 1000, -- The length of the gap
      'second', (@map_scale * 0.6) / 1000 -- The length of the second short stroke
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
                  make_line(
                    @start,
                    line_interpolate_point(@line, min(map_get(@vars,'intermediate'), length(@line)))
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
                with_variable('pos1', min(map_get(@vars,'intermediate'), length(@line)),
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
            -- Placeholders will be replaced by plugin code
            get_feature( @layer, map(__CAT_FIELD__, __BOTTOM_CAT_VALUE__, __ID_FIELD__, attribute(__ID_FIELD__)))
        ),
        if(
            @target_geom is not null,
            with_variable(
                'step', (@map_scale * 2) / 1000,
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
    """
}