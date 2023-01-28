# job-relocation
Gets location of Iglesia Ni Cristo locales in North America to help determine if jobs nearby can be considered.

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
