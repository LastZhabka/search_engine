## Web Search Engine for Retrieval-Augmented Generation

This project aims to develop a scalable and efficient web search engine to support Retrieval-Augmented Generation (RAG) systems. The search engine is designed with a modular architecture that allows for easy integration of different indexing and tokenization strategies. Currently it has undergone significant performance optimizations, achieving a 10x speed boost in the indexing process.

## 📰 News

- **[2024.01.05]** The second implementation released.
  [[Technical Report]](docs/report_02.md)

- **[2024.12.27]** The first implementation released.
  [[Technical Report]](docs/report_01.md)

## 🎥 ~Demo video~ RAG Q & A Example

```python
Run rag_query.py script with indexed HKUST webpages in storage.

"""
QUERY: Who participated in ICPC EC Final 2023 ?

ANSWER:
Based on the information provided in the document, Team 1 (Ka Kit Lui, Sin Hang Yeung, Tsz Fung Wong)
and Team 2 (Taimas Korganbayev, Mukhammadarif Sakhmoldin, Raiymbek Baishuak) participated in the 2023
ICPC Asia East Continent Final Contest.

SOURCES:
https://www.cse.ust.hk/News/ACM_ICPC_Asia2023
https://cse.hkust.edu.hk/News/ACM_ICPC_Asia2023
http://www.cse.ust.hk/News/ACM_ICPC_Asia2023
"""

"""
QUERY: Descirbe DSCT Major from HKUST

ANSWER:
The Data Science and Technology (DSCT) major at HKUST is a program that offers a comprehensive curriculum
covering areas such as machine learning, classification, clustering, data mining, database management,
cloud computing, and data visualization. The program is ranked highly in various fields, including:
- #32 in Computer Science and Information Systems (No.1 in Hong Kong)
- #43 in Statistics and Operational Research (No.1 in Hong Kong)
- #47 in Mathematics (No.1 in Hong Kong)
Graduates of the DSCT major are in high demand in today's job market, with career opportunities in sectors
such as IT, engineering, finance, management, sales, and more. Students pursuing an additional major within
the DSCT program have specific requirements to fulfill, including completing certain math and computer
science courses with specific grade requirements. The program also offers opportunities for students to
complete an additional major program with the approval of the relevant major-program coordinators, with
the first major being the degree associated with the student's transcript.

SOURCES:
https://dsct.ust.hk/applications
https://dsct.hkust.edu.hk/applications
https://dsct.ust.hk/admission-route
https://dsct.hkust.edu.hk/admission-route
https://dsct.ust.hk/applications
https://dsct.hkust.edu.hk/applications
https://cse.hkust.edu.hk/ug/additional_major
https://dsct.ust.hk/student-sharing
https://dsct.hkust.edu.hk/student-sharing
https://join.ust.hk/our-programs/joint-school-program/data-science-and-technology-seng
https://join.ust.hk/our-programs/joint-school-program/data-science-and-technology
https://join.hkust.edu.hk/our-programs/joint-school-program/data-science-and-technology-seng
"""
```


## Installation

### Install from Source

TODO

### Use Docker

TODO

## Search

### Search using script

TODO

### Search using config

TODO

```bash
python scripts/search3.py --config configs/sample_vss.yaml
```


## Evaluation

TODO

## Acknowledgement

TODO

