# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.13.7
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# ## imports

# %%
from datetime import datetime
import re
import json

import pandas as pd
import numpy as np

from lib.data_viz_functions import *

# %%
pd.set_option("display.max_rows", 100)
pd.set_option("display.max_columns", 100)

# %% [markdown]
# ## reading data from disk

# %% tags=[]
train_jane = pd.read_pickle("data/train_df_full_part1.pkl.zip", compression="zip")
train_baseline = pd.read_pickle(
    "data/all_auto_ru_09_09_2020.pkl.zip", compression="zip"
)
test = pd.read_pickle("data/test.pkl.zip", compression="zip")

train_jane.shape, train_baseline.shape, test.shape


# %% [markdown] tags=[]
# ## preprocessing functions

# %%
def parse_ownership_duration(train_str: str) -> float:

    """
    Returns ownership duration in days
    """

    baseline_str = "{'year': 2020, 'month': 9}"

    if not isinstance(train_str, str):
        return np.nan
    elif "year" in str(train_str):
        baseline_dict = json.loads(baseline_str.replace("'", '"'))
        train_dict = json.loads(train_str.replace("'", '"'))

        baseline_date = datetime.strptime(
            f"{baseline_dict['year']}-{baseline_dict['month']}-1", "%Y-%m-%d"
        )
        train_date = datetime.strptime(
            f"{train_dict['year']}-{train_dict['month']}-1", "%Y-%m-%d"
        )
        return (baseline_date - train_date).days
    elif " и " in str(train_str):
        return (
            int(train_str.split(" ")[0]) * 365
            + int(train_str.split(" и ")[1].split(" ")[0]) * 30
        )
    else:
        return int(train_str.split(" ")[0]) * 365


def get_number_of_owners_from_owners(in_str):
    if not isinstance(in_str, str):
        return None
    else:
        result = in_str.replace("\xa0", "")
        return int(re.sub("\D", "", result))
    # return string (to cat)


def get_engine_value(in_str):
    parsed_str = re.findall("(\d+.\d+)", in_str)
    if len(parsed_str):
        return float(parsed_str[0])
    else:
        return None


def get_bodytype(body_type):
    if isinstance(body_type, str):
        if "внедорожник 5 дв." in body_type:
            return "внедорожник 5 дв."
        elif "внедорожник 3 дв." in body_type:
            return "внедорожник 3 дв."
        elif "хэтчбек 5 дв." in body_type:
            return "хэтчбек 5 дв."
        elif "хэтчбек 3 дв." in body_type:
            return "хэтчбек 3 дв."
        elif "седан" in body_type:
            return "седан"
        elif "пикап двойная кабина" in body_type:
            return "пикап двойная кабина"
        elif "пикап полуторная кабина" in body_type:
            return "пикап полуторная кабина"
        elif "пикап одинарная кабина" in body_type:
            return "пикап одинарная кабина"
        elif "микровэн" in body_type:
            return "микровэн"
        elif "кабриолет" in body_type:
            return "кабриолет"
        elif "купе" in body_type:
            return "купе"
        elif "лифтбек" in body_type:
            "лифтбек"

        [
            "лифтбек",
            "внедорожник 5 дв.",
            "хэтчбек 5 дв.",
            "седан",
            "компактвэн",
            "универсал 5 дв.",
            "пикап одинарная кабина",
            "хэтчбек 3 дв.",
            "купе",
            "кабриолет",
            "минивэн",
            "пикап двойная кабина",
            "внедорожник 3 дв.",
            "родстер",
            "микровэн",
            "седан 2 дв.",
            "купе-хардтоп",
            "фастбек",
            "тарга",
            "внедорожник открытый",
            "лимузин",
            "пикап полуторная кабина",
            "седан-хардтоп",
            "фургон",
        ]



# %% [markdown]
# ## quick view

# %%
describe_nums(train_jane.select_dtypes(exclude="object"))

# %%
describe_nums(train_baseline.select_dtypes(exclude="object"))

# %%
describe_nums(test.select_dtypes(exclude="object"))

# %%
train_jane.select_dtypes("object").shape, train_baseline.select_dtypes(
    "object"
).shape, test.select_dtypes("object").shape

# %%
train_jane.select_dtypes("object").describe().T.sort_values("unique", ascending=False)

# %%
train_baseline.select_dtypes("object").describe().T.sort_values(
    "unique", ascending=False
)

# %%
train_jane["enginePower"] = train_jane["enginePower"].replace("undefined N12", None)
train_jane["enginePower"] = (
    train_jane[~pd.isna(train_jane["enginePower"])]["enginePower"]
    .str.split()
    .str.get(0)
    .astype("int")
)

# %%
train_jane["engineDisplacement"] = train_jane["engineDisplacement"].replace(
    " LTR", None
)
train_jane["engineDisplacement"] = (
    train_jane[~pd.isna(train_jane["engineDisplacement"])]["engineDisplacement"]
    .str.split()
    .str.get(0)
    .astype("float")
)

# %%
train_jane.engineDisplacement.head()

# %%
train_jane["used"] = train_jane["car_url"].str.contains("used")

# %%
train_jane[train_jane["used"] == False].dropna(thresh=24).shape

# %%
test.iloc[34682]

# %%
train_jane["car_url"].str.contains("used").value_counts()

# %%
test.select_dtypes("object").describe().T.sort_values("unique", ascending=False)

# %%
test["fuelType"].value_counts()

# %%
test.groupby("car_url")["image"].count().sort_values(ascending=False).head(10)

# %%
test.iloc[2]["model_info"]

# %%
test[test["vehicleConfiguration"] == "ALLROAD_5_DOORS AUTOMATIC 2.0"].sample(
    5, random_state=42
)

# %%
test["Владельцы"] = test["Владельцы"].apply(get_number_of_owners_from_owners)
train_jane["Владельцы"] = train_jane["Владельцы"].apply(
    get_number_of_owners_from_owners
)

# %%
print(
    "unique object cols in train (Jane's version):",
    set(train_jane.select_dtypes("object").columns.tolist())
    - set(test.select_dtypes("object").columns.tolist()),
    "\nunique object cols in test:",
    set(test.select_dtypes("object").columns.tolist())
    - set(train_jane.select_dtypes("object").columns.tolist()),
)


# %% [markdown]
# ## making train and test similar

# %%
train_jane["model_name"] = train_jane.model_name.apply(lambda x: str(x).lower())
test["model_name"] = test.model_name.apply(lambda x: str(x).lower())

# %%
vendor_voc = (
    test[["brand", "vendor"]].drop_duplicates().set_index("brand").to_dict()["vendor"]
)
vendor_voc

# %%
train_jane.brand.unique().tolist()

# %%
train_baseline.brand.unique().tolist()

# %%
train_jane["vendor"] = train_jane["brand"].map(vendor_voc)
train_baseline["vendor"] = train_baseline["brand"].map(vendor_voc)
train_jane.vendor.unique().tolist(), train_baseline.vendor.unique().tolist()

# %%
print(
    len(train_jane.loc[train_jane.vendor.isna()]["model_name"].unique().tolist()),
    "na of",
    len(train_jane.model_name.unique().tolist()),
)

# %%
train_jane.loc[train_jane.vendor.isna()].shape

# %%
train_jane.priceCurrency.unique()

# %%
train_baseline.columns.sort_values().tolist()

# %% [markdown]
# ## deleting cols which can't be used
#
# at least for now - to re-review later

# %%
del test["car_url"]
del test["complectation_dict"]
del test["equipment_dict"]
del test["image"]
del test["model_info"]
del test["name"]
del test["parsing_unixtime"]
del test["priceCurrency"]
del test["sell_id"]
del test["vehicleConfiguration"]
del test["Состояние"]
del test["Таможня"]
del test["super_gen"]
del train_baseline["hidden"]
del train_baseline["name"]
del train_baseline["start_date"]
del train_baseline["vehicleConfiguration"]
del train_baseline["Комплектация"]
del train_baseline["Состояние"]
del train_baseline["Таможня"]
del train_jane["car_url"]
del train_jane["complectation_dict"]
del train_jane["date_added"]
del train_jane["equipment_dict"]
del train_jane["image"]
del train_jane["model_info"]
del train_jane["name"]
del train_jane["parsing_unixtime"]
del train_jane["priceCurrency"]
del train_jane["region"]
del train_jane["sell_id"]
del train_jane["vehicleConfiguration"]
del train_jane["views"]
del train_jane["Состояние"]
del train_jane["Таможня"]
del train_jane["super_gen"]
del train_jane["used"]

# %% [markdown]
# ## view again

# %%
describe_nums(train_jane.select_dtypes(exclude="object"))

# %%
describe_nums(train_baseline.select_dtypes(exclude="object"))

# %%
describe_nums(test.select_dtypes(exclude="object"))

# %%
train_jane.select_dtypes("object").shape, train_baseline.select_dtypes(
    "object"
).shape, test.select_dtypes("object").shape

# %%
train_jane.select_dtypes("object").describe().T.sort_values("unique", ascending=False)

# %%
train_baseline.select_dtypes("object").describe().T.sort_values(
    "unique", ascending=False
)

# %%
test.select_dtypes("object").describe().T.sort_values("unique", ascending=False)[
    "top"
].head(1).tolist()

# %%
test.sample(3).T

# %%
train_jane.loc[train_jane.price.isna()].shape[0], train_jane.price.shape[
    0
], train_jane.loc[train_jane.price.isna()].shape[0] / train_jane.price.shape[0]


# %% [markdown]
# ## conclusion - to do about variables
#
# $y = price$ - dropna, multiply for date course based coefficient for each dataset, take a log
#
# - [ ] **description** - to tokenize - to read more about tokenize
# - [ ] **engineDisplacement** - convert to float
# - [ ] **enginePower** - convert to integer
# - [ ] **Владельцы** - convert to integer
# - [ ] **Владение** - calculate number of day
# - [ ] **used** - is it possible to create this from urls or something for other datasets?
# - [ ] **super_gen** - do we have something to extract? We have no such col in baseline
# - [ ] **bodyType**, **color**, **brand**, **fuelType**, **vehicleTransmission**, **Привод**, **ПТС**, **Руль** - _temporary keep as is_
#
# more
#
# - [ ] mileage rename
# - [ ] compare with existing features
# - [ ] compare 4 dicts (equepment, complactation) train - test
# Numerics - fill na, log if tailed, standartize
# https://www.kaggle.com/datasets/gmbitz/all-auto-ru-09-09-2020

# %% [markdown]
# ## more to do
#
# check NA <= 5 () (new column)
# make new or used column
# electric - drop
#
# make t-sne plot new-used - is it differ?

# %% [markdown]
# ## checking datasets similarity

# %%
train_jane.shape, train_baseline.shape, test.shape

# %%
train_jane[train_jane.columns.sort_values().tolist()].sample(3, random_state=42).T

# %%
train_baseline.rename(columns={"model": "model_name"}, inplace=True)
train_baseline[train_baseline.columns.sort_values().tolist()].sample(
    3, random_state=42
).T

# %%
test[test.columns.sort_values().tolist()].sample(3, random_state=42).T

# %% [markdown]
# ## comments on further train_baseline processing
#
# - [ ] bodyType - no doors specified
# - [ ] color - hexified
# - [ ] model_name - more standartified
# - [ ] productionDate - different dtype
# - [x] Владение - to convert to number of days
# - [ ] vehicleTransmission - to standartize naming
# - [ ] ПТС - to standartize naming
# - [ ] Руль - to standartize naming

# %% [markdown]
# ## merging train datasets

# %%
train_jane['sample'] = 1
train_baseline['sample'] = 2
train = pd.concat([train_jane, train_baseline])

# %%
train["Владение"] = train.Владение.apply(parse_ownership_duration)

# %%
train["Владение"].value_counts().head(5)

# %% [markdown]
# ## ------------------------

# %%
train.drop_duplicates(inplace=True)
train.dropna(subset=['price'], inplace = True)

# %%
train['bodyType'] = train['bodyType'].str.lower()

# %%
test['bodyType'].unique()

# %%
train['bodyType'] = train['bodyType'].apply(get_bodytype)

# %%
train['bodyType']

# %%
train.shape

# %%
train[pd.isna(train['brand'])].count()
