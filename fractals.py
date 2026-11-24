import numpy as np
import matplotlib.pyplot as plt


class KochAntiSnowflake:
    """Generate and plot an inward-pointing Koch anti-snowflake."""

    def __init__(
        self,
        depth=3,
        size=2.0,
        colour="royalblue",
        line_width=1.5
    ):
        self.depth = depth
        self.size = size
        self.colour = colour
        self.line_width = line_width
        self._validate_parameters()

    def _validate_parameters(self):
        if (
            isinstance(self.depth, bool)
            or not isinstance(self.depth, (int, np.integer))
            or self.depth < 0
        ):
            raise ValueError("depth must be a non-negative integer.")

        if (
            isinstance(self.size, bool)
            or not np.isscalar(self.size)
            or not np.isfinite(self.size)
            or self.size <= 0
        ):
            raise ValueError("size must be a positive finite number.")

        if (
            isinstance(self.line_width, bool)
            or not np.isscalar(self.line_width)
            or not np.isfinite(self.line_width)
            or self.line_width <= 0
        ):
            raise ValueError("line_width must be a positive finite number.")

        if not isinstance(self.colour, str):
            raise ValueError("colour must be a string.")

    def _generate_next_iteration(self, points):
        new_points = []
        angle = np.radians(60)
        rotation = np.array([
            [np.cos(angle), -np.sin(angle)],
            [np.sin(angle), np.cos(angle)]
        ])

        for i in range(len(points) - 1):
            p1 = points[i]
            p2 = points[i + 1]

            one_third = p1 + (p2 - p1) / 3
            two_thirds = p1 + 2 * (p2 - p1) / 3
            direction = two_thirds - one_third

            # The +60 degree rotation creates an inward-pointing notch
            # for the counter-clockwise orientation of the initial triangle.
            peak = one_third + rotation @ direction

            new_points.extend([p1, one_third, peak, two_thirds])

        new_points.append(points[-1])
        return np.asarray(new_points, dtype=float)

    def calculate(self):
        """Return the coordinates of the anti-snowflake boundary."""
        height = np.sqrt(3) * self.size / 2

        points = np.array([
            [0.0, 0.0],
            [self.size, 0.0],
            [self.size / 2, height],
            [0.0, 0.0]
        ])

        for _ in range(self.depth):
            points = self._generate_next_iteration(points)

        return points

    def plot(
        self,
        title="Koch Anti-Snowflake",
        figsize=(8, 8),
        save_path=None,
        dpi=150
    ):
        """Create a Matplotlib figure and return (fig, ax)."""
        points = self.calculate()
        fig, ax = plt.subplots(figsize=figsize)

        ax.plot(
            points[:, 0],
            points[:, 1],
            color=self.colour,
            linewidth=self.line_width
        )
        ax.fill(
            points[:, 0],
            points[:, 1],
            color=self.colour,
            alpha=0.12
        )

        # Keep the viewing window fixed to the app's Size slider range.
        # Otherwise Matplotlib rescales the axes after every redraw, making
        # different size values look almost identical on screen.
        ax.set_xlim(-0.5, 5.5)
        ax.set_ylim(-0.5, 5.0)
        ax.set_title(title)
        ax.set_aspect("equal", adjustable="box")
        ax.axis("off")
        fig.tight_layout()

        if save_path is not None:
            fig.savefig(save_path, dpi=dpi, bbox_inches="tight")

        return fig, ax


class JuliaSet:

    def __init__(
        self,
        c_real=-0.7,
        c_imag=0.27,
        x_min=-2.0,
        x_max=2.0,
        y_min=-2.0,
        y_max=2.0,
        max_iterations=100,
        escape_radius=2.0,
        width=800,
        height=800,
        colour_map="magma"
    ):

        # Complex parameter c
        self.c = complex(c_real, c_imag)
        self.c_real = c_real
        self.c_imag = c_imag

        # Complex plane boundaries
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

        # Mathematical parameters
        self.max_iterations = max_iterations
        self.escape_radius = escape_radius

        # Image resolution
        self.width = width
        self.height = height

        # Visualisation settings
        self.colour_map = colour_map

        self._validate_parameters()

    def _validate_parameters(self):
        """Validate all input parameters."""

        if not all(np.isfinite(v) for v in [
            self.c_real, self.c_imag,
            self.x_min, self.x_max,
            self.y_min, self.y_max,
            self.escape_radius
        ]):
            raise ValueError("Parameters must be finite numbers.")

        if self.x_min >= self.x_max:
            raise ValueError("x_min must be smaller than x_max.")

        if self.y_min >= self.y_max:
            raise ValueError("y_min must be smaller than y_max.")

        if (
            isinstance(self.max_iterations, bool)
            or not isinstance(self.max_iterations, (int, np.integer))
            or self.max_iterations < 1
        ):
            raise ValueError("max_iterations must be a positive integer.")

        if self.escape_radius <= 1:
            raise ValueError("escape_radius must be greater than 1.")

        for name, value in [
            ("width", self.width),
            ("height", self.height)
        ]:
            if (
                isinstance(value, bool)
                or not isinstance(value, (int, np.integer))
                or value < 2
            ):
                raise ValueError(f"{name} must be an integer of at least 2.")

        if not isinstance(self.colour_map, str):
            raise ValueError("colour_map must be a string.")

        if self.colour_map not in plt.colormaps():
            raise ValueError(
                f"Unknown colour map: {self.colour_map}"
            )

    def calculate(self):

        x = np.linspace(
            self.x_min,
            self.x_max,
            self.width
        )

        y = np.linspace(
            self.y_min,
            self.y_max,
            self.height
        )

        X, Y = np.meshgrid(x, y)

        Z = X + 1j * Y

        iterations = np.zeros(
            Z.shape,
            dtype=np.int32
        )

        active = np.ones(
            Z.shape,
            dtype=bool
        )

        for i in range(self.max_iterations):

            Z[active] = Z[active] ** 2 + self.c

            escaped = np.abs(Z) > self.escape_radius

            newly_escaped = active & escaped

            iterations[newly_escaped] = i + 1

            active[newly_escaped] = False

            if not np.any(active):
                break

        # Points that did not escape within the limit
        iterations[active] = self.max_iterations

        return iterations

    def plot(
        self,
        colour_map=None,
        show_axes=True,
        show_colorbar=True,
        figsize=(9, 9),
        title="Julia Set",
        save_path=None,
        dpi=150
    ):

        selected_map = (
            colour_map if colour_map is not None
            else self.colour_map
        )

        if selected_map not in plt.colormaps():
            raise ValueError("Unknown colour map.")

        if (
            not isinstance(figsize, (tuple, list))
            or len(figsize) != 2
            or not all(np.isfinite(v) and v > 0 for v in figsize)
        ):
            raise ValueError("figsize must contain two positive numbers.")

        if (
            isinstance(dpi, bool)
            or not isinstance(dpi, (int, np.integer))
            or dpi <= 0
        ):
            raise ValueError("dpi must be a positive integer.")

        iterations = self.calculate()

        fig, ax = plt.subplots(figsize=figsize)

        image = ax.imshow(
            iterations,
            extent=[self.x_min, self.x_max, self.y_min, self.y_max],
            origin="lower",
            cmap=selected_map,
            interpolation="nearest",
            aspect="equal"
        )

        ax.set_title(title)

        if show_axes:
            ax.set_xlabel("Real axis (Re)")
            ax.set_ylabel("Imaginary axis (Im)")
        else:
            ax.set_axis_off()

        if show_colorbar:
            fig.colorbar(
                image,
                ax=ax,
                label="Escape iteration"
            )

        fig.tight_layout()

        if save_path is not None:
            fig.savefig(
                save_path,
                dpi=dpi,
                bbox_inches="tight"
            )


        return fig, ax

class MandelbrotSet:

    def __init__(
        self,
        x_min=-2.5,
        x_max=1.5,
        y_min=-2.0,
        y_max=2.0,
        max_iterations=100,
        escape_radius=2.0,
        width=800,
        height=800,
        colour_map="magma"
    ):

        # Complex plane boundaries
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

        # Mathematical parameters
        self.max_iterations = max_iterations
        self.escape_radius = escape_radius

        # Image resolution
        self.width = width
        self.height = height

        # Visualisation settings
        self.colour_map = colour_map

        self._validate_parameters()

    def _validate_parameters(self):

        if not all(
            np.isfinite(v) for v in [
                self.x_min,
                self.x_max,
                self.y_min,
                self.y_max,
                self.escape_radius
            ]
        ):
            raise ValueError("Parameters must be finite numbers.")

        if self.x_min >= self.x_max:
            raise ValueError("x_min must be smaller than x_max.")

        if self.y_min >= self.y_max:
            raise ValueError("y_min must be smaller than y_max.")

        if (
            isinstance(self.max_iterations, bool)
            or not isinstance(self.max_iterations, (int, np.integer))
            or self.max_iterations < 1
        ):
            raise ValueError(
                "max_iterations must be a positive integer."
            )

        if self.escape_radius <= 1:
            raise ValueError(
                "escape_radius must be greater than 1."
            )

        for name, value in [
            ("width", self.width),
            ("height", self.height)
        ]:
            if (
                isinstance(value, bool)
                or not isinstance(value, (int, np.integer))
                or value < 2
            ):
                raise ValueError(
                    f"{name} must be an integer of at least 2."
                )

        if not isinstance(self.colour_map, str):
            raise ValueError("colour_map must be a string.")

        if self.colour_map not in plt.colormaps():
            raise ValueError(
                f"Unknown colour map: {self.colour_map}"
            )

    def calculate(self):

        # Create coordinate arrays
        x = np.linspace(
            self.x_min,
            self.x_max,
            self.width
        )

        y = np.linspace(
            self.y_min,
            self.y_max,
            self.height
        )

        # Create a grid of complex numbers c
        X, Y = np.meshgrid(x, y)
        C = X + 1j * Y

        # Initially z = 0 for every point
        Z = np.zeros(C.shape, dtype=np.complex128)

        # Store escape iteration counts
        iterations = np.zeros(
            C.shape,
            dtype=np.int32
        )

        # Track points that have not escaped
        active = np.ones(
            C.shape,
            dtype=bool
        )

        # Iterate the Mandelbrot formula
        for i in range(self.max_iterations):

            Z[active] = (
                Z[active] ** 2 + C[active]
            )

            # Check which points have escaped
            escaped = np.abs(Z) > self.escape_radius

            newly_escaped = active & escaped

            # Record escape iteration
            iterations[newly_escaped] = i + 1

            # Remove escaped points from further calculations
            active[newly_escaped] = False

            if not np.any(active):
                break

        # Points that did not escape within the iteration limit
        iterations[active] = self.max_iterations

        return iterations

    def plot(
        self,
        colour_map=None,
        show_axes=True,
        show_colorbar=True,
        figsize=(9, 9),
        title="Mandelbrot Set",
        save_path=None,
        dpi=150
    ):

        selected_map = (
            colour_map if colour_map is not None
            else self.colour_map
        )

        if selected_map not in plt.colormaps():
            raise ValueError("Unknown colour map.")

        if (
            not isinstance(figsize, (tuple, list))
            or len(figsize) != 2
            or not all(
                np.isfinite(v) and v > 0
                for v in figsize
            )
        ):
            raise ValueError(
                "figsize must contain two positive numbers."
            )

        if (
            isinstance(dpi, bool)
            or not isinstance(dpi, (int, np.integer))
            or dpi <= 0
        ):
            raise ValueError("dpi must be a positive integer.")

        # Calculate the fractal
        iterations = self.calculate()

        # Create the figure
        fig, ax = plt.subplots(figsize=figsize)

        image = ax.imshow(
            iterations,
            extent=[
                self.x_min,
                self.x_max,
                self.y_min,
                self.y_max
            ],
            origin="lower",
            cmap=selected_map,
            interpolation="nearest",
            aspect="equal"
        )

        ax.set_title(title)

        if show_axes:
            ax.set_xlabel("Real axis (Re)")
            ax.set_ylabel("Imaginary axis (Im)")
        else:
            ax.set_axis_off()

        if show_colorbar:
            fig.colorbar(
                image,
                ax=ax,
                label="Escape iteration"
            )

        fig.tight_layout()

        if save_path is not None:
            fig.savefig(
                save_path,
                dpi=dpi,
                bbox_inches="tight"
            )


        return fig, ax

class SierpinskiTriangle:

    def __init__(
        self,
        depth=5,
        size=2.0,
        colour="royalblue",
        background_colour="white"
    ):

        self.depth = depth
        self.size = size
        self.colour = colour
        self.background_colour = background_colour

        self._validate_parameters()

    def _validate_parameters(self):
        """Validate all input parameters."""

        if (
            isinstance(self.depth, bool)
            or not isinstance(self.depth, (int, np.integer))
            or self.depth < 0
        ):
            raise ValueError("depth must be a non-negative integer.")

        if not np.isfinite(self.size) or self.size <= 0:
            raise ValueError("size must be a positive finite number.")

        if not isinstance(self.colour, str):
            raise ValueError("colour must be a string.")

        if not isinstance(self.background_colour, str):
            raise ValueError("background_colour must be a string.")

    def _midpoint(self, point1, point2):
        """Calculate the midpoint between two points."""

        return (point1 + point2) / 2

    def calculate(self):
        """
        Generate all triangles in the Sierpinski Triangle.

        Returns:
            A list of triangles, each containing three vertices.
        """

        height = self.size * np.sqrt(3) / 2

        initial_triangle = np.array([
            [-self.size / 2, -height / 3],
            [self.size / 2, -height / 3],
            [0, 2 * height / 3]
        ])

        triangles = [initial_triangle]

        for _ in range(self.depth):

            new_triangles = []

            for triangle in triangles:

                a, b, c = triangle

                ab = self._midpoint(a, b)
                bc = self._midpoint(b, c)
                ca = self._midpoint(c, a)

                new_triangles.extend([
                    np.array([a, ab, ca]),
                    np.array([ab, b, bc]),
                    np.array([ca, bc, c])
                ])

            triangles = new_triangles

        return triangles

    def plot(
        self,
        colour=None,
        background_colour=None,
        show_axes=False,
        figsize=(9, 9),
        title="Sierpinski Triangle",
        save_path=None,
        dpi=150
    ):
        """Visualise the Sierpinski Triangle."""

        selected_colour = colour or self.colour
        selected_background = (
            background_colour or self.background_colour
        )

        triangles = self.calculate()

        fig, ax = plt.subplots(figsize=figsize)

        ax.set_facecolor(selected_background)

        for triangle in triangles:

            closed_triangle = np.vstack([
                triangle,
                triangle[0]
            ])

            ax.fill(
                closed_triangle[:, 0],
                closed_triangle[:, 1],
                color=selected_colour
            )

        # Fixed viewport makes the Size slider visibly change the triangle.
        ax.set_xlim(-3.0, 3.0)
        ax.set_ylim(-2.0, 2.0)
        ax.set_title(title)
        ax.set_aspect("equal", adjustable="box")

        if show_axes:
            ax.set_xlabel("X")
            ax.set_ylabel("Y")
        else:
            ax.set_axis_off()

        fig.tight_layout()

        if save_path is not None:
            fig.savefig(
                save_path,
                dpi=dpi,
                bbox_inches="tight"
            )


        return fig, ax

class KochSnowflake:


    def __init__(
            self,
            depth=3,
            size=2.0,
            colour="royalblue",
            line_width=1.5
    ):

        self.depth = depth
        self.size = size
        self.colour = colour
        self.line_width = line_width

        self._validate_parameters()

    def _validate_parameters(self):
        """Validate all input parameters."""

        if (
                isinstance(self.depth, bool)
                or not isinstance(self.depth, (int, np.integer))
                or self.depth < 0
        ):
            raise ValueError("depth must be a non-negative integer.")

        if not np.isfinite(self.size) or self.size <= 0:
            raise ValueError("size must be positive and finite.")

        if (
                not np.isfinite(self.line_width)
                or self.line_width <= 0
        ):
            raise ValueError("line_width must be positive.")

        if not isinstance(self.colour, str):
            raise ValueError("colour must be a string.")

    def calculate(self):
        """
        Generate the coordinates of the Koch Snowflake.

        Returns:
            A NumPy array containing the snowflake vertices.
        """

        height = self.size * np.sqrt(3) / 2

        points = [
            np.array([0.0, 0.0]),
            np.array([self.size, 0.0]),
            np.array([self.size / 2, height])
        ]

        for _ in range(self.depth):

            new_points = []

            for i in range(len(points)):
                p1 = points[i]
                p2 = points[(i + 1) % len(points)]

                vector = p2 - p1

                first = p1 + vector / 3
                second = p1 + 2 * vector / 3

                # Rotate the middle segment by -60 degrees
                angle = -np.pi / 3

                rotation = np.array([
                    [np.cos(angle), -np.sin(angle)],
                    [np.sin(angle), np.cos(angle)]
                ])

                peak = first + rotation @ (vector / 3)

                new_points.extend([
                    p1,
                    first,
                    peak,
                    second
                ])

            points = new_points

        points.append(points[0])

        return np.array(points)

    def plot(
            self,
            colour=None,
            line_width=None,
            show_axes=False,
            figsize=(9, 9),
            title="Koch Snowflake",
            save_path=None,
            dpi=150
    ):
        """Visualise the Koch Snowflake."""

        selected_colour = colour or self.colour
        selected_width = (
            line_width if line_width is not None
            else self.line_width
        )

        if (
                not np.isfinite(selected_width)
                or selected_width <= 0
        ):
            raise ValueError("line_width must be positive.")

        points = self.calculate()

        fig, ax = plt.subplots(figsize=figsize)

        ax.plot(
            points[:, 0],
            points[:, 1],
            color=selected_colour,
            linewidth=selected_width
        )

        # Fixed viewport makes the Size slider visibly change the snowflake.
        # The Koch construction extends below the original triangle's base.
        ax.set_xlim(-0.5, 5.5)
        ax.set_ylim(-2.0, 5.0)
        ax.set_title(title)
        ax.set_aspect("equal", adjustable="box")

        if show_axes:
            ax.set_xlabel("X")
            ax.set_ylabel("Y")
        else:
            ax.set_axis_off()

        fig.tight_layout()

        if save_path is not None:
            fig.savefig(
                save_path,
                dpi=dpi,
                bbox_inches="tight"
            )


        return fig, ax

class FractalTree:

    def __init__(
        self,
        depth=8,
        length=1.0,
        branch_angle=30,
        length_ratio=0.7,
        colour="forestgreen",
        line_width=1.5
    ):

        self.depth = depth
        self.length = length
        self.branch_angle = branch_angle
        self.length_ratio = length_ratio
        self.colour = colour
        self.line_width = line_width

        self._validate_parameters()

    def _validate_parameters(self):
        """Validate all input parameters."""

        if (
            isinstance(self.depth, bool)
            or not isinstance(self.depth, (int, np.integer))
            or self.depth < 0
        ):
            raise ValueError("depth must be a non-negative integer.")

        if not np.isfinite(self.length) or self.length <= 0:
            raise ValueError("length must be positive.")

        if (
            not np.isfinite(self.branch_angle)
            or not 0 < self.branch_angle < 90
        ):
            raise ValueError(
                "branch_angle must be between 0 and 90 degrees."
            )

        if (
            not np.isfinite(self.length_ratio)
            or not 0 < self.length_ratio < 1
        ):
            raise ValueError(
                "length_ratio must be between 0 and 1."
            )

        if not isinstance(self.colour, str):
            raise ValueError("colour must be a string.")

        if (
            not np.isfinite(self.line_width)
            or self.line_width <= 0
        ):
            raise ValueError("line_width must be positive.")

    def _generate_branch(
        self,
        x,
        y,
        length,
        angle,
        depth,
        segments
    ):
        """Generate branches using recursion."""

        if depth == 0:
            return

        angle_radians = np.radians(angle)

        # Calculate the end point of the branch
        x_end = x + length * np.sin(angle_radians)
        y_end = y + length * np.cos(angle_radians)

        segments.append([
            (x, y),
            (x_end, y_end)
        ])

        # Calculate the length of the next branches
        new_length = length * self.length_ratio

        # Generate the left branch
        self._generate_branch(
            x_end,
            y_end,
            new_length,
            angle - self.branch_angle,
            depth - 1,
            segments
        )

        # Generate the right branch
        self._generate_branch(
            x_end,
            y_end,
            new_length,
            angle + self.branch_angle,
            depth - 1,
            segments
        )

    def calculate(self):
        """
        Generate all tree branches.

        Returns:
            A list of line segments.
        """

        segments = []

        self._generate_branch(
            x=0,
            y=0,
            length=self.length,
            angle=0,
            depth=self.depth,
            segments=segments
        )

        return segments

    def plot(
        self,
        colour=None,
        line_width=None,
        show_axes=False,
        figsize=(9, 9),
        title="Fractal Tree",
        save_path=None,
        dpi=150
    ):
        """Visualise the Fractal Tree."""

        selected_colour = colour or self.colour

        selected_width = (
            line_width if line_width is not None
            else self.line_width
        )

        if (
            not np.isfinite(selected_width)
            or selected_width <= 0
        ):
            raise ValueError("line_width must be positive.")

        segments = self.calculate()

        fig, ax = plt.subplots(figsize=figsize)

        for segment in segments:

            start, end = segment

            ax.plot(
                [start[0], end[0]],
                [start[1], end[1]],
                color=selected_colour,
                linewidth=selected_width
            )

        ax.set_title(title)
        ax.set_aspect("equal")

        if show_axes:
            ax.set_xlabel("X")
            ax.set_ylabel("Y")
        else:
            ax.set_axis_off()

        fig.tight_layout()

        if save_path is not None:
            fig.savefig(
                save_path,
                dpi=dpi,
                bbox_inches="tight"
            )


        return fig, ax

class NewtonFractal:

    def __init__(
            self,
            x_min=-2.0,
            x_max=2.0,
            y_min=-2.0,
            y_max=2.0,
            max_iterations=50,
            tolerance=1e-6,
            width=800,
            height=800,
            colour_map="viridis"
    ):

        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

        self.max_iterations = max_iterations
        self.tolerance = tolerance

        self.width = width
        self.height = height

        self.colour_map = colour_map

        self._validate_parameters()

    def _validate_parameters(self):

        if not all(
                np.isfinite(v) for v in [
                    self.x_min,
                    self.x_max,
                    self.y_min,
                    self.y_max,
                    self.tolerance
                ]
        ):
            raise ValueError("Parameters must be finite numbers.")

        if self.x_min >= self.x_max:
            raise ValueError("x_min must be smaller than x_max.")

        if self.y_min >= self.y_max:
            raise ValueError("y_min must be smaller than y_max.")

        if (
                isinstance(self.max_iterations, bool)
                or not isinstance(self.max_iterations, (int, np.integer))
                or self.max_iterations < 1
        ):
            raise ValueError(
                "max_iterations must be a positive integer."
            )

        if self.tolerance <= 0:
            raise ValueError("tolerance must be positive.")

        for name, value in [
            ("width", self.width),
            ("height", self.height)
        ]:
            if (
                    isinstance(value, bool)
                    or not isinstance(value, (int, np.integer))
                    or value < 2
            ):
                raise ValueError(
                    f"{name} must be an integer of at least 2."
                )

        if not isinstance(self.colour_map, str):
            raise ValueError("colour_map must be a string.")

        if self.colour_map not in plt.colormaps():
            raise ValueError(
                f"Unknown colour map: {self.colour_map}"
            )

    def calculate(self):

        x = np.linspace(
            self.x_min,
            self.x_max,
            self.width
        )

        y = np.linspace(
            self.y_min,
            self.y_max,
            self.height
        )

        X, Y = np.meshgrid(x, y)

        Z = X + 1j * Y

        # Three roots of z^3 - 1 = 0
        roots = np.array([
            1 + 0j,
            -0.5 + 1j * np.sqrt(3) / 2,
            -0.5 - 1j * np.sqrt(3) / 2
        ])

        # -1 means not yet converged
        root_indices = np.full(
            Z.shape,
            -1,
            dtype=np.int32
        )

        active = np.ones(
            Z.shape,
            dtype=bool
        )

        for _ in range(self.max_iterations):

            if not np.any(active):
                break

            # Newton's method:
            # z(n+1) = z(n) - (z(n)^3 - 1) / (3*z(n)^2)

            current = Z[active]

            denominator = 3 * current ** 2

            # Avoid division by zero
            safe = np.abs(denominator) > 1e-14

            updated = np.zeros_like(current)

            updated[safe] = (
                    current[safe]
                    - (current[safe] ** 3 - 1)
                    / denominator[safe]
            )

            Z[active] = updated

            # Find which root each point approaches
            distances = np.abs(
                Z[active, None] - roots[None, :]
            )

            nearest_roots = np.argmin(
                distances,
                axis=1
            )

            minimum_distances = np.min(
                distances,
                axis=1
            )

            converged = (
                    minimum_distances < self.tolerance
            )

            # A point with a zero denominator is not updated
            converged[~safe] = False

            active_indices = np.where(active)

            root_indices[
                active_indices[0][converged],
                active_indices[1][converged]
            ] = nearest_roots[converged]

            # Remove converged points
            active[
                active_indices[0][converged],
                active_indices[1][converged]
            ] = False

            # Remove points with an unsafe denominator
            invalid = ~safe

            active[
                active_indices[0][invalid],
                active_indices[1][invalid]
            ] = False

        return root_indices

    def plot(
            self,
            colour_map=None,
            show_axes=True,
            show_colorbar=True,
            figsize=(9, 9),
            title="Newton Fractal",
            save_path=None,
            dpi=150
    ):

        selected_map = (
            colour_map if colour_map is not None
            else self.colour_map
        )

        if selected_map not in plt.colormaps():
            raise ValueError("Unknown colour map.")

        root_indices = self.calculate()

        fig, ax = plt.subplots(figsize=figsize)

        # Display each root's basin of attraction
        image = ax.imshow(
            root_indices,
            extent=[
                self.x_min,
                self.x_max,
                self.y_min,
                self.y_max
            ],
            origin="lower",
            cmap=selected_map,
            interpolation="nearest",
            aspect="equal",
            vmin=-1,
            vmax=2
        )

        ax.set_title(title)

        if show_axes:
            ax.set_xlabel("Real axis (Re)")
            ax.set_ylabel("Imaginary axis (Im)")
        else:
            ax.set_axis_off()

        if show_colorbar:
            colorbar = fig.colorbar(image, ax=ax)
            colorbar.set_label("Converged root index")

            colorbar.set_ticks([-1, 0, 1, 2])

        fig.tight_layout()

        if save_path is not None:
            fig.savefig(
                save_path,
                dpi=dpi,
                bbox_inches="tight"
            )


        return fig, ax

