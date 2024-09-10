#!/usr/bin/env python3
import svgwrite
from dataclasses import dataclass
from typing import Optional, Tuple, List
from jinja2 import Environment, FileSystemLoader
import os

@dataclass
class PatternPoint:
    origin: Tuple[float, float]
    control_ccw: Optional[Tuple[float, float]]
    control_cw: Optional[Tuple[float, float]]        

    def scale(self, factor: float) -> 'PatternPoint':
        """Scale the pattern point by a given factor."""
        origin = (self.origin[0] * factor, self.origin[1] * factor)
        control_ccw = (self.control_ccw[0] * factor, self.control_ccw[1] * factor) if self.control_ccw else None
        control_cw = (self.control_cw[0] * factor, self.control_cw[1] * factor) if self.control_cw else None
        return PatternPoint(origin, control_ccw, control_cw)

@dataclass
class CupSize:
    size_no: int
    over_breast_measurement: str

    def line_length(self) -> float:
        size_index = self.size_no - 1
        return line_length_base + size_index * line_length_step

    def scale_factor(self) -> float:
        return self.line_length() / reference_cup_size.line_length()

# Pattern points data
pattern_points = [
    PatternPoint(
        origin=(0.0, 0.0), 
        control_ccw=(14.0407, 25.0918),
        control_cw=(-14.5372, 22.8171),
    ),
    PatternPoint(
        origin=(-65.0, 57.7614), 
        control_ccw=(-40.1933, 43.6463),
        control_cw=(-83.4987, 37.6504),
    ),
    PatternPoint(
        origin=(-97.7787, -29.8535), 
        control_ccw=(-106.1128, 11.0309),
        control_cw=(-96.0463, -38.3517),
    ),
    PatternPoint(
        origin=(-88.9743, -54.2035), 
        control_ccw=(-92.8233, -46.481),
        control_cw=(-67.1478, -60.2205),
    ),
    PatternPoint(
        origin=(-41.9367, -107.5931),
        control_ccw=(-57.6472, -75.3583),
        control_cw=None),
    PatternPoint(
        origin=(78.7962, -46.7356),
        control_ccw=None, 
        control_cw=(100.4121, -14.4459),
    ),
    PatternPoint(
        origin=(62.7811, 59.2765),
        control_ccw=(87.6192, 32.6349),
        control_cw=(39.5943, 43.9509),
    ),
]

# Base "line 1" length for size 4 (11.57 cm)
line_length_base = 11.57

# Step for "line 1" (1.07 cm)
line_length_step = 1.07

# Defining the cup sizes with their ratios and measurements
cup_sizes = [
    CupSize(
        size_no=1,
        over_breast_measurement="14.1cm to 14.7cm",
    ),
    CupSize(
        size_no=2,
        over_breast_measurement="15.8cm to 16.4cm",
    ),
    CupSize(
        size_no=3,
        over_breast_measurement="17.5cm to 18.1cm",
    ),
    CupSize(
        size_no=4,
        over_breast_measurement="19.2cm to 19.8cm",
    ),
    CupSize(
        size_no=5,
        over_breast_measurement="20.9cm to 21.5cm",
    ),
    CupSize(
        size_no=6,
        over_breast_measurement="22.6cm to 23.2cm",
    ),
    CupSize(
        size_no=7,
        over_breast_measurement="24.3cm to 24.9cm",
    ),
    CupSize(
        size_no=8,
        over_breast_measurement="26.0cm to 26.6cm",
    ),
    CupSize(
        size_no=9,
        over_breast_measurement="27.7cm to 28.3cm",
    ),
    CupSize(
        size_no=10,
        over_breast_measurement="29.4cm to 30.0cm",
    ),
    CupSize(
        size_no=11,
        over_breast_measurement="31.1cm to 31.7cm",
    ),
    CupSize(
        size_no=12,
        over_breast_measurement="32.8cm to 33.4cm",
    ),
    CupSize(
        size_no=13,
        over_breast_measurement="34.5cm to 35.1cm",
    ),
    CupSize(
        size_no=14,
        over_breast_measurement="36.2cm to 36.8cm",
    ),
    CupSize(
        size_no=15,
        over_breast_measurement="37.9cm to 38.5cm",
    ),
    CupSize(
        size_no=16,
        over_breast_measurement="39.6cm to 40.2cm",
    ),
    CupSize(
        size_no=17,
        over_breast_measurement="41.3cm to 41.9cm",
    ),
    CupSize(
        size_no=18,
        over_breast_measurement="43.0cm to 43.6cm",
    ),
    CupSize(
        size_no=19,
        over_breast_measurement="44.7cm to 45.3cm",
    ),
    CupSize(
        size_no=20,
        over_breast_measurement="46.4cm to 47.0cm",
    ),
    CupSize(
        size_no=21,
        over_breast_measurement="48.1cm to 48.7cm",
    ),
    CupSize(
        size_no=22,
        over_breast_measurement="49.8cm to 50.4cm",
    ),
    CupSize(
        size_no=23,
        over_breast_measurement="51.5cm to 52.1cm",
    ),
    CupSize(
        size_no=24,
        over_breast_measurement="53.2cm to 53.8cm",
    ),
    CupSize(
        size_no=25,
        over_breast_measurement="54.9cm to 55.5cm",
    ),
    CupSize(
        size_no=26,
        over_breast_measurement="56.6cm to 57.2cm",
    ),
    CupSize(
        size_no=27,
        over_breast_measurement="58.3cm to 58.9cm",
    ),
    CupSize(
        size_no=28,
        over_breast_measurement="60.0cm to 60.6cm",
    ),
    CupSize(
        size_no=29,
        over_breast_measurement="61.7cm to 62.3cm",
    ),
]

# The reference size (size 4)
reference_cup_size = cup_sizes[3]

def scale_pattern_points(pattern_points: List[PatternPoint], scale_factor: float) -> List[PatternPoint]:
    """Scale the pattern points by a given factor."""
    return [point.scale(scale_factor) for point in pattern_points]

def generate_cup_pattern_svg(pattern_points: List[PatternPoint], file_name: str, width: float, height: float):
    # Create the SVG drawing
    dwg = svgwrite.Drawing(
        file_name,
        profile='tiny',
        size=(f'{width}mm', f'{height}mm'),
        viewBox=f"0 0 {width} {height}",
    )

    # Move to the first point
    start_point = pattern_points[0].origin
    path_data = f'M {start_point[0]},{start_point[1]} '

    # Iterate through the points and create path data
    n = len(pattern_points)
    for i in range(n):
        current = pattern_points[i]
        next_point = pattern_points[(i + 1) % n]

        if current.control_cw and next_point.control_ccw:
            # Cubic Bezier curve
            path_data += f'C {current.control_cw[0]},{current.control_cw[1]} '
            path_data += f'{next_point.control_ccw[0]},{next_point.control_ccw[1]} '
            path_data += f'{next_point.origin[0]},{next_point.origin[1]} '
        else:
            # Line to the next point
            path_data += f'L {next_point.origin[0]},{next_point.origin[1]} '

    # Close the path
    path_data += 'Z'

    # Add the path to the drawing inside a <g> element with translation
    g = dwg.g(transform=f'translate({width/2},{height/2})')
    g.add(dwg.path(d=path_data, fill='none', stroke='black'))
    dwg.add(g)

    # Save the SVG file
    dwg.save()

# For the reference cup size, the image is A4-sized. For other cup sizes, it's scaled respectively.
base_width = 210
base_height = 297

# Create output directories if they don't exist
os.makedirs('_site/assets', exist_ok=True)

# Generate SVG files for each cup size
for cup_size in cup_sizes:
    scale_factor = cup_size.scale_factor()

    scaled_points = scale_pattern_points(pattern_points, scale_factor)

    file_name = f'_site/assets/cup_size_{cup_size.size_no}.svg'

    generate_cup_pattern_svg(
        scaled_points,
        file_name,
        width=base_width * scale_factor,
        height=base_height * scale_factor,
    )

# Generate the index.html file
env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('template.html')

html_content = template.render(cup_sizes=cup_sizes)

with open('_site/index.html', 'w') as f:
    f.write(html_content)

print("Website generated successfully in the '_site' directory.")
