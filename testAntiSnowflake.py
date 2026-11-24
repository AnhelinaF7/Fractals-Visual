
from fractals import KochAntiSnowflake


def test_anti_snowflake_creation():

    fractal = KochAntiSnowflake()

    assert fractal.depth == 3
    assert fractal.size == 2.0


def test_anti_snowflake_calculate():

    fractal = KochAntiSnowflake(
        depth=2,
        size=2
    )

    result = fractal.calculate()

    assert result.shape == (3 * 4**2 + 1, 2)


def test_anti_snowflake_different_depths():

    fractal_1 = KochAntiSnowflake(depth=1)
    fractal_2 = KochAntiSnowflake(depth=2)

    result_1 = fractal_1.calculate()
    result_2 = fractal_2.calculate()

    assert len(result_1) == 13
    assert len(result_2) == 49


def test_anti_snowflake_invalid_depth():

    try:
        KochAntiSnowflake(depth=-1)
    except ValueError:
        return

    assert False, "Negative depth should raise ValueError"


if __name__ == "__main__":

    test_anti_snowflake_creation()
    test_anti_snowflake_calculate()
    test_anti_snowflake_different_depths()
    test_anti_snowflake_invalid_depth()

    print("All Koch Anti-Snowflake tests passed!")
