# Fractal Explorer

An interactive educational application for exploring mathematical fractals. The project allows users to visualise different fractals, experiment with mathematical parameters, change colours, zoom into visualisations and download generated images.

## 1. Project Features

The application currently supports six types of fractals:

- **Julia Set** – explores complex dynamical systems using a fixed complex parameter.
- **Mandelbrot Set** – visualises the famous Mandelbrot set.
- **Sierpinski Triangle** – demonstrates recursive geometric patterns.
- **Koch Snowflake** – explores recursive curve construction.
- **Fractal Tree** – generates branching structures using recursion.
- **Newton Fractal** – visualises the basins of attraction of Newton's method.

Users can:
- Select a fractal from the home page.
- Adjust mathematical parameters using interactive controls.
- Change colour maps and visualisation settings.
- Zoom in and change the position of the complex plane.
- Download generated fractals as PNG images.

## 2. Requirements

Before running the project, make sure you have installed:

- Python 3.13 or newer (recommended).
- Git.
- pip (Python package installer).

## 3. Download the Project from GitHub

Open your terminal (or the terminal in PyCharm) and run:

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
```

Replace `YOUR-USERNAME` and `YOUR-REPOSITORY` with the actual GitHub username and repository name.

Navigate into the downloaded project folder:

```bash
cd Fractal-Explorer
```

## 4. Create a Virtual Environment (Recommended)

A virtual environment keeps the project's dependencies separate from other Python projects.

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

After activation, you should see `(.venv)` in your terminal.

## 5. Install Dependencies

Install the libraries required by the application:

```bash
python -m pip install --upgrade pip
python -m pip install numpy matplotlib streamlit
```

These packages are used for:

- **NumPy** – numerical calculations and array operations.
- **Matplotlib** – generating and displaying fractal visualisations.
- **Streamlit** – building the interactive web application.

## 6. Run the Application

Make sure you are in the main project directory and that your virtual environment is activated.

Run:

```bash
streamlit run app.py
```

Streamlit will start a local development server and usually open the application automatically in your web browser.

If it does not open automatically, copy the local URL displayed in the terminal (usually `http://localhost:8501`) into your browser.

## 7. Project Structure

The project should have the following structure:

```text
Fractal-Explorer/
│
├── app.py
│
├── fractals.py
│
├── Pictures/
│   ├── JuliaSetPic.jpeg
│   ├── MandelbrotSetPic.jpeg
│   ├── SierpinskiTrianglePic.jpeg
│   ├── KochSnowflakePic.jpeg
│   ├── FractalTreePic.jpeg
│   └── NewtonFractalPic.jpeg
│
├── README.md
│
└── test_fractals.py
```

**Important:** Keep `app.py`, `fractals.py` and the `Pictures` folder in the same main project directory. Do not rename or move the image files unless you also update their paths in `app.py`.



## 8. Stopping the Application

To stop the local Streamlit server, return to the terminal and press:

```text
Ctrl + C
```

## 9. Contributing to the Project

All group members are welcome to explore the code, test the fractal algorithms, identify bugs and suggest improvements.

Before making changes, it is recommended to pull the latest version of the repository:

```bash
git pull
```

After making changes, remember to test the application before committing your work.

---

**Fractal Explorer**  
*An educational project in computational mathematics.*  
Developed by the Sacrobosco group.
