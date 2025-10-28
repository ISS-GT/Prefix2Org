# Prefix2Org

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.17237945.svg)](https://doi.org/10.5281/zenodo.17237945)

## Downloading the Latest Release
To download the latest release of Prefix2Org, you can use the following command in your terminal:

If you do not have Git LFS installed, please refer to the [Git LFS installation guide](https://git-lfs.github.com/) before proceeding.

```bash
git clone git@github.com:ISS-GT/Prefix2Org.git
cd Prefix2Org/data
git lfs pull
```

## Loading the dataset in Python
To load the dataset in Python, you can use the following code snippet:

```python
import pandas as pd

# Load the dataset
data = pd.read_parquet("data/prefix2org_2025-04-01.parquet")

# Display the first few rows
print(data.head())