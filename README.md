# Project 6: predicting car prices

Skillfactory, Data Science PRO course, [kaggle competition](https://www.kaggle.com/c/sf-dst-car-price-prediction)

Made by:

- Petr Polyakov - [Kaggle](https://www.kaggle.com/xelorrelin), [GitHub](https://github.com/XelorR), [GitLab](https://gitlab.com/XelorR)
- Michael Vasiliev - [Kaggle](https://www.kaggle.com/michaelvasiliev), [GitHub](https://github.com/MichaelDockers)

## Setup and requirements

```bash
git clone https://github.com/XelorR/sf_project_6
cd sf_project_6

python3 -m venv venv
source venv/bin/activate
./venv/bin/python3 -m pip install -r requirements.txt
```

## Data

### Train-test-submission

- [data/train_df_full_part1.pkl.zip](data/train_df_full_part1.pkl.zip) - **train** dataset by [Jane Voytik](https://www.kaggle.com/datasets/eugeniavoytik/final-car-price-prediction-df-parsed-sep-2021)
- [data/all_auto_ru_09_09_2020.pkl.zip](data/all_auto_ru_09_09_2020.pkl.zip) - **train** dataset from baseline
- [data/test.pkl.zip](data/test.pkl.zip) - **test**
- [data/sample_submission.csv](data/sample_submission.csv) - submission example

### Preprocessed

- to do

### Temporary saved states

- [data/parsed_first_pages.pkl.zip](data/parsed_first_pages.pkl.zip) - 366 rows, first try
- [data/20220326_valid_data.pkl.zip](data/20220326_valid_data.pkl.zip) - car data parsed from auto.ru (infinity only)
- [data/20220326_catalog_data.pkl.zip](data/20220326_catalog_data.pkl.zip) - catalog data parsed from auto.ru (infinity only)

## Notebooks

- [UsedCars_Project_Module_6_parser.ipynb](UsedCars_Project_Module_6_parser.ipynb) - [366 rows saved](data/parsed_first_pages.pkl.zip)
- [2022-03-19_train-test_comparison.ipynb](2022-03-19_train-test_comparison.ipynb) - first view
- [UsedCars_Project_Module_6.ipynb](UsedCars_Project_Module_6.ipynb) - updated parser
- [20220327_model_counts.ipynb](20220327_model_counts.ipynb) - how many cars to parse

## TO DO

- [x] org - Petr create repo, organize access
- [x] new - Petr - search for external datasets
- [x] new - Michael - create basic parser (first pages only)
- [x] new - Michael - expand parser to all pages for each model
- [x] new - Petr - compare Jane's train with test and insure feature consistency
- [x] org - both - align how to split and run parser on multiple machines 
- [ ] fix - Michael - **get_urls_for_model_in_region** falling into infinite loop in case of too many pages
- [x] new - Petr - analyze [number of cars](20220327_model_counts.ipynb) to parse for each model and propose model split
- [ ] new - both - run parser separately on several machines
    - [x] spb except bmw, mercedes, wolkswagen, mitsubishi
    - [ ] spb mitsubishi
    - [ ] spb bmw, mercedes, wolkswagen
    - [x] msk volvo, lexus, honda, infinity - include 
    - [ ] the rest
    - [ ] 
- [ ] new - combine parsed datasets
- [ ] new - make parsed compatible with test
- [x] org - Petr - form a Kaggle Team
- [x] new - Petr - add "baseline" train dataset and ensure having same set of cols for all 3
- [ ] new - Petr - implement feature-related comments from [2022-03-19_train-test_comparison.ipynb](2022-03-19_train-test_comparison.ipynb)
