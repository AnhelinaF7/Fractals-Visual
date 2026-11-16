from fractals import MandelbrotSet

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

mandelbrot.plot()