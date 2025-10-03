EXPRESSIONS = {
    "Unreinforced slope": """
-- Собираем все созданные штрихи (основные и промежуточные) в одну геометрию
collect_geometries(
    -- Используем переменную, чтобы один раз найти геометрию парной линии
    with_variable(
        'target_geom',
        -- 1. Находим геометрию объекта в ЭТОМ ЖЕ слое
        geometry(
            get_feature( @layer, map(__CAT_FIELD__, __BOTTOM_CAT_VALUE__, __ID_FIELD__, attribute(__ID_FIELD__)))
        ),
        -- 2. Если парная геометрия найдена...
        if (
            @target_geom is not null,
            -- --- БЛОК НАСТРОЙКИ МАСШТАБА И РАЗМЕРОВ ---
            with_variable(
                'target_screen_mm', 2, -- Желаемое расстояние между основными штрихами НА ЭКРАНЕ (в мм)
                with_variable(
                    'intermediate_stroke_mm', 2.5, -- <<-- НОВАЯ НАСТРОЙКА: Желаемая длина промежуточного штриха НА ЭКРАНЕ (в мм)
                    with_variable(
                        'step_in_map_units', (@map_scale * @target_screen_mm) / 1000, -- Шаг основных штрихов в единицах карты
                        with_variable(
                            'intermediate_stroke_map_units', (@map_scale * @intermediate_stroke_mm) / 1000, -- Длина промежуточного штриха в единицах карты

                            -- 3. Объединяем два массива геометрий
                            array_cat(
                                -- --- БЛОК 1: ОСНОВНЫЕ ШТРИХИ (с динамическим шагом) ---
                                array_foreach(
                                    -- Генерируем серию от 0 до конца линии с рассчитанным шагом
                                    generate_series(0, length($geometry), @step_in_map_units),
                                    make_line(
                                        line_interpolate_point($geometry, @element),
                                        closest_point(@target_geom, line_interpolate_point($geometry, @element))
                                    )
                                ),

                                -- --- БЛОК 2: ПРОМЕЖУТОЧНЫЕ ШТРИХИ (с фиксированной длиной с учетом масштаба) ---
                                array_foreach(
                                    -- Начинаем с половины шага, чтобы штрих был между основными
                                    generate_series(@step_in_map_units / 2, length($geometry), @step_in_map_units),
                                    with_variable('start_pt', line_interpolate_point($geometry, @element),
                                    with_variable('end_pt_full', closest_point(@target_geom, line_interpolate_point($geometry, @element)),
                                    with_variable('full_line', make_line(@start_pt, @end_pt_full),
                                        make_line(
                                            @start_pt,
                                            line_interpolate_point(
                                                @full_line,
                                                -- Используем меньшее из двух значений: расчетная длина или полная длина до парной линии
                                                min(@intermediate_stroke_map_units, length(@full_line))
                                            )
                                        )
                                    )))
                                )
                            )
                        )
                    )
                )
            ),
            -- Если парная геометрия не найдена, не рисуем ничего
            make_line(make_point(0,0),make_point(0,0))
        )
    )
)
    """,
    "Forced slope": """
-- Собираем все созданные штрихи (основные, промежуточные и дополнительные) в одну геометрию
collect_geometries(
    -- Используем переменную, чтобы один раз найти геометрию парной линии
    with_variable(
        'target_geom',
        -- 1. Находим геометрию объекта в ЭТОМ ЖЕ слое
        geometry(
            get_feature( @layer, map('КОД_КЛАССИФИКАТОРА','512220000', 'SLOPE_ID', attribute($currentfeature, 'SLOPE_ID')))
        ),
        -- 2. Если парная геометрия найдена...
        if (
            @target_geom is not null,
            -- --- БЛОК НАСТРОЙКИ МАСШТАБА И РАЗМЕРОВ ---
            with_variable(
                'target_screen_mm', 2, -- Желаемое расстояние между основными штрихами НА ЭКРАНЕ (в мм)
                with_variable(
                    'intermediate_stroke_mm', 2.5, -- Длина первого промежуточного штриха НА ЭКРАНЕ (в мм)
                    with_variable(
                        'gap_after_stroke_mm', 0.5, -- <<-- НОВАЯ НАСТРОЙКА: Зазор после первого штриха НА ЭКРАНЕ (в мм)
                        with_variable(
                            'second_stroke_mm', 0.7, -- <<-- НОВАЯ НАСТРОЙКА: Длина второго штриха НА ЭКРАНЕ (в мм)
                            with_variable(
                                'step_in_map_units', (@map_scale * @target_screen_mm) / 1000, -- Шаг основных штрихов в единицах карты
                                with_variable(
                                    'intermediate_stroke_map_units', (@map_scale * @intermediate_stroke_mm) / 1000, -- Длина первого штриха в единицах карты
                                    with_variable(
                                        'gap_map_units', (@map_scale * @gap_after_stroke_mm) / 1000, -- Зазор в единицах карты
                                        with_variable(
                                            'second_stroke_map_units', (@map_scale * @second_stroke_mm) / 1000, -- Длина второго штриха в единицах карты

                                            -- 3. Объединяем три массива геометрий
                                            array_cat(
                                                array_cat(
                                                    -- --- БЛОК 1: ОСНОВНЫЕ ШТРИХИ ---
                                                    array_foreach(
                                                        generate_series(0, length($geometry), @step_in_map_units),
                                                        make_line(
                                                            line_interpolate_point($geometry, @element),
                                                            closest_point(@target_geom, line_interpolate_point($geometry, @element))
                                                        )
                                                    ),

                                                    -- --- БЛОК 2: ПЕРВЫЕ ПРОМЕЖУТОЧНЫЕ ШТРИХИ ---
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

                                                -- --- БЛОК 3: ВТОРЫЕ (ДОПОЛНИТЕЛЬНЫЕ) ПРОМЕЖУТОЧНЫЕ ШТРИХИ ---
                                                array_foreach(
                                                    generate_series(@step_in_map_units / 2, length($geometry), @step_in_map_units),
                                                    with_variable('start_pt', line_interpolate_point($geometry, @element),
                                                    with_variable('end_pt_full', closest_point(@target_geom, line_interpolate_point($geometry, @element)),
                                                    with_variable('full_line', make_line(@start_pt, @end_pt_full),
                                                    with_variable('first_stroke_end_pos', min(@intermediate_stroke_map_units, length(@full_line)),
                                                        -- Позиция начала второго штриха = конец первого + зазор
                                                        with_variable('second_stroke_start_pos', @first_stroke_end_pos + @gap_map_units,
                                                            -- Рисуем, только если начало второго штриха не выходит за пределы парной линии
                                                            if (
                                                                @second_stroke_start_pos < length(@full_line),
                                                                make_line(
                                                                    -- Начальная точка второго штриха
                                                                    line_interpolate_point(@full_line, @second_stroke_start_pos),
                                                                    -- Конечная точка второго штриха (ограничена парной линией)
                                                                    line_interpolate_point(
                                                                        @full_line,
                                                                        min(length(@full_line), @second_stroke_start_pos + @second_stroke_map_units)
                                                                    )
                                                                ),
                                                                -- Иначе возвращаем пустую геометрию
                                                                geom_from_wkt('LINESTRING EMPTY')
                                                            )
                                                        )
                                                    ))))
                                                )
                                            )
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
            ),
            -- Если парная геометрия не найдена, не рисуем ничего
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