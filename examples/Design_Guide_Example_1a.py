from steeljoist import Joist, JoistDoubleAngle, JoistRound

inch = 1
kip = 1
ft = 12*inch
lbs = 0.001*kip
plf = lbs/ft
pcf = lbs/ft**3

Sections = {
    'TC': JoistDoubleAngle(1.75*inch, 0.143*inch, 13/16*inch),
    'BC': JoistDoubleAngle(1.50*inch,  9/64*inch, 13/16*inch),
    'W2': JoistRound(13/16*inch),
    'SV': JoistRound(5/8*inch),
    'W3': JoistRound(5/8*inch),
    'W4': JoistRound(5/8*inch),
    'W5': JoistRound(5/8*inch),
    'W6': JoistRound(5/8*inch),
    'W7': JoistRound(5/8*inch),
    'W8': JoistRound(5/8*inch),
    'W9': JoistRound(5/8*inch),
    'W10': JoistRound(9/16*inch),
    'W11': JoistRound(9/16*inch),
    'W12': JoistRound(9/16*inch),
    'W13': JoistRound(9/16*inch),
    'W14': JoistRound(9/16*inch),
}

joist = Joist(joist_name = '16K6',
              span = 32*ft,
              depth = 16*inch,
              truss_type = 'warren',
              top_chord_panel_point_lengths = [2, 34, 24],
              bottom_chord_panel_point_lengths = [48, 24],
              sections = Sections,
              top_chord_section = 'TC',
              bottom_chord_section = 'BC',
              web_sections = ['W2', 'SV', 'W3', 'W4', 'W5', 'W6', 'W7', 'W8', 'W9', 'W10', 'W11', 'W12', 'W13', 'W14'],
              uniform_load = 0.3*349*plf,
              bottom_chord_extension_length = 4,
              maximum_top_chord_element_length = 8,
              maximum_bottom_chord_element_length = 10,
              maximum_web_member_element_length = 12)

joist.plot_joist()
joist.saveMASTAN2(model_title = "Example 1a")

