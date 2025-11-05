# Prefix2Org
This repository contains the dataset for the paper "Prefix2Org: Mapping Internet Prefixes to Organizations" by Gouda et al., published in ACM Internet Measurement Conference (IMC) 2025. The dataset provides a mapping of BGP routed prefixes to their corresponding organizations, denoted as `Direct Owner` and `Delegated Customers`. For more details, refer to the [paper](https://deepakgouda.github.io/assets/pdf/IMC-2025-Prefix2Org.pdf).

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
```

It is recommended to use a prefix tree like `py-radix` or `pytricia` for efficient prefix lookups. You can install py-radix using pip:

```bash
pip install pyradix
# or
pip install pytricia
```

## Citation
If you use this dataset in your research, please cite the dataset:
```bibtex
@software{gouda_2025_17237945,
  author       = {Gouda, Deepak and
                  Dainotti, Alberto and
                  Testart, Cecilia},
  title        = {Prefix2Org: Mapping BGP Prefixes to Organizations},
  month        = sep,
  year         = 2025,
  publisher    = {Zenodo},
  version      = {v1.0},
  doi          = {10.5281/zenodo.17237945},
  url          = {https://doi.org/10.5281/zenodo.17237945},
  swhid        = {swh:1:dir:7a6e744426503a5e88ba336db206e882916c04ef
                   ;origin=https://doi.org/10.5281/zenodo.17237945;vi
                   sit=swh:1:snp:eaee977231fc014e300f74918ff6aac3e642
                   e6dd;anchor=swh:1:rel:b5b6e4912543ed69d11403945e34
                   c7dd9fecf090;path=ISS-GT-Prefix2Org-0dd56bc
                  },
}
```

If you use find the framework present in the paper useful, please cite the paper:
```bibtex
@inproceedings{10.1145/3730567.3764485,
    author = {Gouda, Deepak and Dainotti, Alberto and Testart, Cecilia},
    title = {Prefix2Org : Mapping BGP Prefixes to Organizations},
    year = {2025},
    isbn = {9798400718601},
    publisher = {Association for Computing Machinery},
    address = {New York, NY, USA},
    url = {https://doi.org/10.1145/3730567.3764485},
    doi = {10.1145/3730567.3764485},
    abstract = {Accurately mapping Internet address space to organizations is critical to understanding the Internet’s organizational ecosystem. Traditional approaches, which rely on individual WHOIS queries often suffer from unclear ownership structure of IP addresses and inconsistent organization names, resulting in ambiguous inferences. Alternative methods that map BGP prefixes to Autonomous Systems Numbers (ASNs) and ASNs to organizations are also inaccurate since ASes often originate prefixes on behalf of their customers. This paper introduces Prefix2Org, a comprehensive prefix-to-organization mapping framework. We introduce a taxonomy for the holders of IP addresses and a methodology to map IP addresses to organizations, based on the operational rights over them. We develop string processing heuristics and leverage RPKI Certificates and routing data to address inconsistencies in organizational names and aggregate prefixes under unified management. Our public dataset covers 99.96% (99.99%) of IPv4 (IPv6) prefixes. We validate 9.3% of routed IPv4 addresses with a 99% recall, and 5.6% of IPv6 prefixes with a 99.34% recall. For the two large organizations where we obtained complete ground truth, Prefix2Org produced no false positives. Finally, in two case studies, (i) we characterize organizations that hold address space without an ASN and (ii) demonstrate how RPKI adoption measured through Prefix2Org differs from the previously used AS-centric view.},
    booktitle = {Proceedings of the 2025 ACM Internet Measurement Conference},
    pages = {397–414},
    numpages = {18},
    keywords = {Prefix-to-Organization Mapping, IP Ownership, BGP, RPKI},
    location = {USA},
    series = {IMC '25}
}
```