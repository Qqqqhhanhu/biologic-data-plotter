# BioLogic Data Plotter

A Python tool for selecting, cleaning, summarizing, and plotting battery data exported from BioLogic.

## Project Description

This project aims to transform my existing battery data analysis scripts into a more structured, reusable, and user-friendly Python tool.

The program allows users to:
- Select one or more BioLogic CSV or mpt files through a file dialog
- Automatically detect available parameters such as time, Ewe, Ece, current, capacity, and cycle number etc
- Optionally export a cleaned version of the data
- Generate data summaries including charge/discharge capacity, coulombic efficiency (CE), and capacity retention
- Create customizable plots using any detected or derived parameter as x or y axis

The current version is designed for common BioLogic-exported CSV/mpt formats and may require further adaptation for all experiment types.
