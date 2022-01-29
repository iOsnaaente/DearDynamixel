import dearpygui.dearpygui as dpg 

# GLOBAL THEME 
with dpg.theme( ) as detheme:
    with dpg.theme_component( dpg.mvAll):
        dpg.add_theme_color( dpg.mvThemeCol_Button       , (52, 140, 215), category = dpg.mvThemeCat_Core )
        dpg.add_theme_style( dpg.mvStyleVar_FrameRounding,        5      , category = dpg.mvThemeCat_Core )
        dpg.add_theme_color( dpg.mvThemeCol_ButtonHovered, (40, 120, 200), category = dpg.mvThemeCat_Core )

# CONFIGURAÇÃO DA FONTE e THEMES - INICIO DO COD. 
with dpg.font_registry( ):
    defont = dpg.add_font("fonts\\verdana.ttf", 14 )

#   APPLY DEFAULT THEMES AND FONTS
dpg.bind_theme( detheme )
dpg.bind_font( defont )


# PLOT THEMES 
with dpg.theme( tag = 200_01 ) as plot_blue_line:
    with dpg.theme_component( dpg.mvLineSeries ):
        dpg.add_theme_color( dpg.mvPlotCol_Line, (52, 140, 215), category = dpg.mvThemeCat_Plots )

with dpg.theme( tag = 200_02 ) as plot_red_line:
    with dpg.theme_component( dpg.mvLineSeries ):
        dpg.add_theme_color( dpg.mvPlotCol_Line, (215, 52, 75), category = dpg.mvThemeCat_Plots )

with dpg.theme( tag = 200_03 ) as plot_green_line:
    with dpg.theme_component( dpg.mvLineSeries ):
        dpg.add_theme_color( dpg.mvPlotCol_Line, (140, 215, 52), category = dpg.mvThemeCat_Plots )

with dpg.theme( tag = 200_04 ) as plot_yellow_line:
    with dpg.theme_component( dpg.mvLineSeries ):
        dpg.add_theme_color( dpg.mvPlotCol_Line, (255, 215,  0), category = dpg.mvThemeCat_Plots )


# BUTTON THEMES 
with dpg.theme( tag = 300_04 ) as button_green:
    with dpg.theme_component( dpg.mvButton ):
        dpg.add_theme_color( dpg.mvThemeCol_Button       , (140, 215, 52), category = dpg.mvThemeCat_Core )
        dpg.add_theme_color( dpg.mvThemeCol_ButtonHovered, (120, 200, 40), category = dpg.mvThemeCat_Core )

with dpg.theme( tag = 300_05 ) as button_red:
    with dpg.theme_component( dpg.mvButton ):
        dpg.add_theme_color( dpg.mvThemeCol_Button       , (215, 52, 75), category = dpg.mvThemeCat_Core )
        dpg.add_theme_color( dpg.mvThemeCol_ButtonHovered, (190, 50, 50), category = dpg.mvThemeCat_Core )

with dpg.theme( tag = 300_06 ) as button_default:
    with dpg.theme_component( dpg.mvButton ):
        dpg.add_theme_color( dpg.mvThemeCol_Button       , (52, 140, 215), category = dpg.mvThemeCat_Core )
        dpg.add_theme_color( dpg.mvThemeCol_ButtonHovered, (40, 120, 200), category = dpg.mvThemeCat_Core )

with dpg.theme( tag = 300_07 ) as button_deactive:
    with dpg.theme_component( dpg.mvButton ):
        dpg.add_theme_color( dpg.mvThemeCol_Button, [22, 200, 50, 200] )
        dpg.add_theme_color( dpg.mvThemeCol_ButtonHovered, [44, 240, 70, 200] )

with dpg.theme( tag = 300_08 ) as button_active:
    with dpg.theme_component( dpg.mvButton ):
        dpg.add_theme_color( dpg.mvThemeCol_Button, [200, 20, 50, 200]  )  
        dpg.add_theme_color( dpg.mvThemeCol_ButtonHovered, [240, 40, 70, 200] )

#dpg.add_theme_style(dpg.mvPlotStyleVar_Marker, dpg.mvPlotMarker_Diamond, category=dpg.mvThemeCat_Plots)
#dpg.add_theme_style(dpg.mvPlotStyleVar_MarkerSize, 7, category=dpg.mvThemeCat_Plots)
