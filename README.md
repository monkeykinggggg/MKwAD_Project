# MKwAD_Project

## Confidential Medical Data Analysis with Fully Homomorphic Encryption
Implementation of a system in which a hospital can outsource the computation of statistical indicators (e.g., mean, standard devation, covariance, and other aggregate statistics) on patient medical data to an external server — without revealing the raw data thanks to FHE. The computations were performed on the [Heart Disease Dataset]( https://www.kaggle.com/datasets/johnsmith88/heart-disease-dataset).

The system uses the CKKS Fully Homomorphic Encryption (FHE) scheme implemented with TenSEAL, enabling encrypted computations on floating-point vectors on untrusted computational cloud server. Patient data is encrypted on the medical server before being transmitted to the cloud computation service. The cloud server never has access to the plaintext records.


## System Architecture
```text
+-------------------+                                  +-----------------------+
| SQLite Database   |                                  |                       |
+--------+----------+                                  |  Compute Server       |
         |                                             |                       |
         v                                             |                       |
+-------------------+    1. Send HE Public Context     |                       |
|                   | -------------------------------> |                       |
|  Medical Server   |                                  |                       |
|  (FastAPI)        |    2. HTTP POST (Encrypted Data) |                       |
|                   | -------------------------------> |                       |
|                   | <------------------------------- |                       |
+--------+----------+    3. HTTP Response (Enc. Result)|                       |
         ^                                             +-----------------------+
         |
         | HTTP GET/POST (Plaintext JSON)
         v
+-------------------+
| Medical Frontend  |
| (Streamlit)       |
+-------------------+
```

## Development Plan
| Task | Status |
|------|--------|
| Data inspection and cleaning | DONE |
| Implementation of the distributed system (two backend servers + medical frontend): architecture and implementation |  DONE |
| Initial local encryption tests |  DONE |
| Fully functional encryption across the entire system | ✅ DONE |
| Development of the medical system, including: <br> • adding observations to the database <br> • submitting synamic client-side filtering queries allowing to construct complex, multi-variable queries (e.g., calculating the average value of a metric only for patients diagnosed with heart disease) | ✅ DONE |
| Development of the computation service, communication with the medical service, and returning the appropriate results | ✅ DONE |

## Running the Project
To check on more detailed run isntructions from side of each server please refer to their README.md files.



## Technology Stack
- FastAPI
- SQLite
- TenSEAL
- Streamlit
- Docker

## References  
Theory:
- https://courses.csail.mit.edu/6.857/2022/projects/Facen-Fang-Shepard-Viera.pdf
- https://ethz.ch/content/dam/ethz/special-interest/infk/inst-infsec/appliedcrypto/education/theses/semester-project_junzhen-lou.pdf
- https://pyfhel.readthedocs.io/en/latest/_autoexamples/index.html

Encryption Libraries:  
- https://github.com/jonaschn/awesome-hes