from fractals import JuliaSet
from fractals import MandelbrotSet
from fractals import SierpinskiTriangle
from fractals import KochSnowflake
from fractals import FractalTree
from fractals import NewtonFractal

julia = JuliaSet(
    c_real=-0.7,
    c_imag=0.27,
    x_min=-2,
    x_max=2,
    y_min=-2,
    y_max=2,
    max_iterations=100,
    width=800,
    height=800,
    colour_map="magma"
)

mandelbrot = MandelbrotSet(
    x_min=-2.5,
    x_max=1.5,
    y_min=-2.0,
    y_max=2.0,
    max_iterations=100,
    escape_radius=2.0,
    width=800,
    height=800,
    colour_map="magma"
)

sierpinski = SierpinskiTriangle(
    depth=5,
    size=2,
    colour="violet"
)

koch = KochSnowflake(
    depth=4,
    size=2,
    colour="blue",
    line_width=1.5
)

tree = FractalTree(
    depth=9,
    length=1,
    branch_angle=30,
    length_ratio=0.7,
    colour="forestgreen"
)

newton = NewtonFractal(
    max_iterations=50,
    tolerance=1e-6,
    width=800,
    height=800,
    colour_map="magma"
)

julia.plot()
mandelbrot.plot()
sierpinski.plot()
koch.plot()
tree.plot()
newton.plot()