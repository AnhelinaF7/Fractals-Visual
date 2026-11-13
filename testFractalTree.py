from fractals import FractalTree

tree = FractalTree(
    depth=9,
    length=1,
    branch_angle=30,
    length_ratio=0.7,
    colour="forestgreen"
)

tree.plot()