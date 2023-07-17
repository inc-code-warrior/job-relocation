# job-relocation
Personal project that scraped LinkedIn jobs and a church website to retrieve location data.  This data was later manually imported into Google Maps to look at distances between job openings and chapel locations.

## Setup
1. Install chromedriver from
    https://chromedriver.chromium.org/downloads and move to folder in path
    ```
    mv ~/Downloads/chromedriver_mac64 /usr/local/bin
    ```

1. Install miniconda https://docs.conda.io/en/latest/miniconda.html
    - Initial env creation:
        ```
        conda create --name dev
        conda activate dev
        conda install selenium
        conda env export > environment.yml
        ```

    - If env already created:

        ```
        conda env create -f environment.yml
        conda activate dev
        ```
