EXPRESSIONS = {
    "Unreinforced slope dynamic": """
collect_geometries(
    with_variable(
        'target_geom',
        geometry(
            -- Плейсхолдеры будут заменены кодом плагина
            get_feature( @layer, map(__CAT_FIELD__, __BOTTOM_CAT_VALUE__, __ID_FIELD__, attribute(__ID_FIELD__)))
        ),
        if (
            @target_geom is not null,
            array_cat(
                array_foreach(
                    generate_series(0, length($geometry), (@map_scale * 2) / 1000),
                    make_line(
                        line_interpolate_point($geometry, @element),
                        closest_point(@target_geom, line_interpolate_point($geometry, @element))
                    )
                ),
                array_foreach(
                    generate_series(((@map_scale * 2) / 1000) / 2, length($geometry), (@map_scale * 2) / 1000),
                    with_variable('stroke_ratio', 0.2,
                    with_variable('start_pt', line_interpolate_point($geometry, @element),
                    with_variable('end_pt_full', closest_point(@target_geom, line_interpolate_point($geometry, @element)),
                    with_variable('full_line', make_line(@start_pt, @end_pt_full),
                        make_line(
                            @start_pt,
                            line_interpolate_point(
                                @full_line,
                                length(@full_line) * @stroke_ratio
                            )
                        )
                    ))))
                )
            ),
            make_line(make_point(0,0),make_point(0,0))
        )
    )
)
    """,
    "Reinforced slope dynamic": """
collect_geometries(
    with_variable(
        'target_geom',
        geometry(
            -- Плейсхолдеры будут заменены кодом плагина
            get_feature( @layer, map(__CAT_FIELD__, __BOTTOM_CAT_VALUE__, __ID_FIELD__, attribute(__ID_FIELD__)))
        ),
        if (
            @target_geom is not null,
            with_variable('step_in_map_units', (@map_scale * 2) / 1000,
            with_variable('intermediate_stroke_map_units', (@map_scale * 2.5) / 1000,
            with_variable('gap_map_units', (@map_scale * 1) / 1000,
            with_variable('second_stroke_map_units', (@map_scale * 1.5) / 1000,
                array_cat(
                    array_cat(
                        array_foreach(
                            generate_series(0, length($geometry), @step_in_map_units),
                            make_line(
                                line_interpolate_point($geometry, @element),
                                closest_point(@target_geom, line_interpolate_point($geometry, @element))
                            )
                        ),
                        array_foreach(
                            generate_series(@step_in_map_units / 2, length($geometry), @step_in_map_units),
                            with_variable('start_pt', line_interpolate_point($geometry, @element),
                            with_variable('end_pt_full', closest_point(@target_geom, line_interpolate_point($geometry, @element)),
                            with_variable('full_line', make_line(@start_pt, @end_pt_full),
                                make_line(
                                    @start_pt,
                                    line_interpolate_point(
                                        @full_line,
                                        min(@intermediate_stroke_map_units, length(@full_line))
                                    )
                                )
                            )))
                        )
                    ),
                    array_foreach(
                        generate_series(@step_in_map_units / 2, length($geometry), @step_in_map_units),
                        with_variable('start_pt', line_interpolate_point($geometry, @element),
                        with_variable('end_pt_full', closest_point(@target_geom, line_interpolate_point($geometry, @element)),
                        with_variable('full_line', make_line(@start_pt, @end_pt_full),
                        with_variable('first_stroke_end_pos', min(@intermediate_stroke_map_units, length(@full_line)),
                        with_variable('second_stroke_start_pos', @first_stroke_end_pos + @gap_map_units,
                            if (
                                @second_stroke_start_pos < length(@full_line),
                                make_line(
                                    line_interpolate_point(@full_line, @second_stroke_start_pos),
                                    line_interpolate_point(
                                        @full_line,
                                        min(length(@full_line), @second_stroke_start_pos + @second_stroke_map_units)
                                    )
                                ),
                                geom_from_wkt('LINESTRING EMPTY')
                            )
                        )))))
                    )
                )
            )))),
            make_line(make_point(0,0),make_point(0,0))
        )
    )
)
    """,
    "Cliff": """
collect_geometries(
    with_variable(
        'target_geom',
        geometry(
            -- Плейсхолдеры будут заменены кодом плагина
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