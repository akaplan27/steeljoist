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
    'W2': JoistRound(1*inch),
    'SV': JoistDoubleAngle(1*inch,  0.125*inch, 1*inch),
    'W3': JoistDoubleAngle(1.75*inch,  0.1875*inch, 1.75*inch),
    'W4': JoistDoubleAngle(1.25*inch,  0.125*inch, 1.25*inch),
    'V1': JoistRound(1.25*inch),
    'W5': JoistDoubleAngle(2*inch,  0.1875*inch, 2*inch),
    'W6': JoistDoubleAngle(1.25*inch,  0.125*inch, 1.25*inch),
    'W7': JoistDoubleAngle(1.75*inch,  0.125*inch, 1.75*inch),
    'W8': JoistDoubleAngle(1.50*inch,  0.125*inch, 1.5*inch),
    'W9': JoistDoubleAngle(1.50*inch,  0.1875*inch, 1.5*inch),
    'W10': JoistDoubleAngle(1.25*inch,  0.125*inch, 1.25*inch)
}

joist = Joist(joist_name = 'DG Example 2a',
              span = 42*ft,
              depth = 26*inch,
              truss_type = 'ModifiedWarren',
              top_chord_panel_point_lengths = [2, 36, 32, 26],
              bottom_chord_panel_point_lengths = [50, 46, 52],
              sections = Sections,
              top_chord_section = 'TC',
              bottom_chord_section = 'BC',
              web_sections = ['W2', 'SV', 'W3', 'W4', 'V1', 'W5', 'W6', 'V1', 'W7', 'W8', 'V1', 'W9', 'W10', 'V1'],
              uniform_load = 0.3*349*plf,
              bottom_chord_extension_length = 4)

joist.plot_joist()
joist.saveMASTAN2()

