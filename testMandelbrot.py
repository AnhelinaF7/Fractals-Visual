from fractals import MandelbrotSet

# Create a Julia Set object
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

# Generate and display the fractal
mandelbrot.plot()