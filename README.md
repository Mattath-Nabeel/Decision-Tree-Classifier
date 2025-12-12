## Elementary Logic Gate Classifier Using Decision Tree

This repository provides the Python code used to build a graphical tool for classifying molecular logic gates based on normalized fluorescence or absorbance data. The tool offers a reproducible computational workflow for molecular‐logic research and supports the experimental framework reported in the associated manuscript.

---

## Manuscript Information

**Multi-Molecular Logic Framework Based on Morse Code, ASCII Logic, and Beale’s Cipher for Advanced Crypto-Steganography**
**Authors:** Mohamed Nabeel Mattath, Yingying Lu, Ajith Manayil Parambil, Yan Gao, Tian-Ming Yao, Jing-Jing Li, Rui-Min Zang, Song Hu*, and Shuo Shi*
**Journal:** *Small* (Wiley), Submitted
Corresponding Author: **Song Hu, Shuo Shi**

If you use this code, please cite the manuscript above.

---

## Overview

This tool implements a **Tkinter-based GUI** that classifies elementary molecular logic gates using a **Decision Tree model** trained on normalized logic gate truth tables.

Users can input four intensity values corresponding to binary inputs (00, 01, 10, 11), specify the maximum intensity and threshold if needed, and obtain a predicted logic gate identity.

Supported logic functions include YES, NOT, INH, IMP, OR, NOR, PASS, XOR, XNOR, AND, and NAND types.

---

## Requirements

**Python version:**

* Python 3.13+

**Dependencies:**

* pandas
* numpy
* scikit-learn
* matplotlib
* tkinter *(bundled with standard Python distributions)*

---

## Contact

For research questions or collaborations:

**Corresponding Author:**
Prof. Shuo Shi
Tongji University, Shanghai, China
Email: [shishuo@tongji.edu.cn](mailto:shishuo@tongji.edu.cn)

**Repository Maintainer:**
Mohamed Nabeel Mattath

---

## License

This code is made available for **academic and research use**.
Please contact the corresponding author for commercial use.

