# job-relocation

## Setup
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
