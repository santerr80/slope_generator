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
collect_geometries(
  with_variable(
    'vars',
    map(
      'target_geom', geometry(
        get_feature(
          @layer,
          map(
            'КОД_КЛАССИФИКАТОРА','512220000',
            'SLOPE_ID', attribute($currentfeature,'SLOPE_ID')
          )
        )
      ),
      'target_screen_mm', 2,
      'intermediate_stroke_mm', 2.5,
      'gap_after_stroke_mm', 1,
      'second_stroke_mm', 1.5,
      'step', (@map_scale * 2) / 1000,
      'intermediate', (@map_scale * 2.5) / 1000,
      'gap', (@map_scale * 1) / 1000,
      'second', (@map_scale * 1.5) / 1000
    ),

    if(
      map_get(@vars,'target_geom') is null,
      make_line(make_point(0,0), make_point(0,0)),

      -- объединяем три массива через вложенные array_cat
      array_cat(
        array_cat(
          -- БЛОК 1: ОСНОВНЫЕ ШТРИХИ
          array_foreach(
            generate_series(0, length($geometry), map_get(@vars,'step')),
            make_line(
              line_interpolate_point($geometry, @element),
              closest_point(map_get(@vars,'target_geom'), line_interpolate_point($geometry, @element))
            )
          ),

          -- БЛОК 2: ПЕРВЫЕ ПРОМЕЖУТОЧНЫЕ ШТРИХИ
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

        -- БЛОК 3: ВТОРЫЕ (ДОПОЛНИТЕЛЬНЫЕ) ПРОМЕЖУТОЧНЫЕ ШТРИХИ
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