from fractals import JuliaSet

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

julia.plot()
