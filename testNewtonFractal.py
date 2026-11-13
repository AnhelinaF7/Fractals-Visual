from fractals import NewtonFractal

newton = NewtonFractal(
    max_iterations=50,
    tolerance=1e-6,
    width=800,
    height=800,
    colour_map="magma"
)

newton.plot()