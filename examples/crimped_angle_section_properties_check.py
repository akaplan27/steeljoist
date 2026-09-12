import matplotlib.pyplot as plt
from steeljoist import HotRolledCrimpedAngle
from shapely import Polygon
from sectionproperties.pre import Geometry
from sectionproperties.analysis import Section
from math import sqrt

section = HotRolledCrimpedAngle(1.500, 0.125)

# Properties from the class
cls_props = dict()
cls_props['A'] = section.A
cls_props['Ix'] = section.Ix
cls_props['Iy'] = section.Iy
cls_props['J'] = section.J
cls_props['yp'] = section.yp
cls_props['Zx'] = section.Zx
cls_props['Zy'] = section.Zy
cls_props['rx'] = section.rx
cls_props['ry'] = section.ry
cls_props['Asx'] = section.Asx
cls_props['Asy'] = section.Asy

# Properties from sectionproperties
sp_props = dict()
for p in cls_props.keys():
    sp_props[p] = []
    
mesh_size_factors = [10,1,0.1,0.01,0.001]
for i, mesh_size_factor in enumerate(mesh_size_factors):
    geom = Geometry(geom=Polygon(section.cross_section_points()))
    #geom.plot_geometry()
    geom.create_mesh(mesh_sizes=mesh_size_factor*(section.t)**2)
    sec = Section(geometry=geom)
    #sec.plot_mesh()
    sec.calculate_geometric_properties()
    sec.calculate_warping_properties()
    sec.calculate_plastic_properties()
    #sec.disp_propslay_results()

    sp_props['A'].append(float(sec.get_area()))
    #sp_props['x_bar'].append(float(sec.get_c()[0]))
    #sp_props['y_bar'].append(float(sec.get_c()[1]))
    sp_props['Ix'].append(float(sec.get_ic()[0]))
    sp_props['Iy'].append(float(sec.get_ic()[1]))
    #sp_props['Iz'].append(float(sec.get_ip()[1]))
    sp_props['J'].append(float(sec.get_j()))
    #sp_props['Cw'].append(float(sec.get_gamma()))
    sp_props['yp'].append(float(-sec.get_pc()[1]))
    sp_props['Zx'].append(float(sec.get_s()[0]))
    sp_props['Zy'].append(float(sec.get_s()[1]))
    sp_props['rx'].append(sqrt(sp_props['Ix'][-1]/sp_props['A'][-1]))
    sp_props['ry'].append(sqrt(sp_props['Iy'][-1]/sp_props['A'][-1]))
    #sp_props['rz'].append(sqrt(sp_props['Iz'][-1]/sp_props['A'][-1]))
    sp_props['Asx'].append(float(sec.get_as()[0]))
    sp_props['Asy'].append(float(sec.get_as()[1]))
    
# Plot
for prop in cls_props.keys():
    plt.figure()
    plt.axhline(cls_props[prop], color='k', linestyle='--', label='class')
    plt.plot(sp_props[prop],'o', label = 'sectionproperties')
    for i, sp_prop in enumerate(sp_props[prop]):
        percent_diff = 100*(cls_props[prop]-sp_prop)/sp_prop
        plt.text(i,sp_prop,f'{percent_diff:.2f}%',ha='center',va='baseline')
    plt.xlabel('Mesh Size Factor')
    plt.ylabel(prop)
    plt.xticks(ticks=list(range(0, len(mesh_size_factors))), labels=mesh_size_factors)
    plt.xlim(-0.5,len(mesh_size_factors)-0.5)
    ymin,ymax = plt.ylim()
    if ymin > 0.99*ymax:
        plt.ylim(0.9*ymin,1.1*ymax)
    plt.show()