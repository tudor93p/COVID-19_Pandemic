# COVID-19 Pandemic evolution in Romania

0. First:
    * install the prerequisite libraries in [requirements.txt](./requirements.txt)
    ```console
        pip install -r requirements.txt
    ```

    * add the submodule [python_libraries](./python_libraries), required in step 5.1
    ```console
       git submodule add https://gitlab.phys.ethz.ch/pahomit/python_libraries.git
    ```

    * install  ffmpeg, required for movie generation in step 5.2, e.g. for ubuntu:
    ```console
        sudo apt  install ffmpeg
    ```

1. To test geopandas, run [test_mapplot.py](./Ro_data/test_mapplot.py).

2. To test json, run  [Ro_datelazi.py](./Ro_datelazi.py)

3. To test geopands, run [Ro_counties.py](counties.py)

4. A simple plot: [Ro_plot.py](plot.py)

5.1. Sliders plot: [Ro_plot_sliders.py](plot_sliders.py)

5.2. Make a movie: [Ro_plot_movie.py](plot_movie.py)