import datetime
import PIL
import pytz
from typing import Dict, Any

import gspread as gs
import pandas as pd
import streamlit as st


def get_image() -> PIL.Image:
    return PIL.Image.open(f"resources/images/{st.session_state.name}.jpg")


def get_sheet() -> gs.Worksheet:
    gc = gs.service_account_from_dict(st.secrets["gcp_service_account"])
    return gc.open_by_url(st.secrets["private_gsheets_url"]).worksheet("ranking")


def get_ranking(sheet: gs.Worksheet) -> pd.DataFrame:
    return pd.DataFrame(sheet.get_all_records())


def exists_user(user: str, df: pd.DataFrame = None, sheet: gs.Worksheet = None) -> bool:
    if sheet is None:
        sheet = get_sheet()
    if df is None:
        df = get_ranking(sheet)

    df = df[df["Nom"] == user]
    return len(df) > 0


def write_new_row(row: Dict[str, Any], df: pd.DataFrame, sheet: gs.Worksheet) -> pd.DataFrame:
    if sheet is None:
        sheet = get_sheet()
    if df is None:
        df = get_ranking(sheet)
    
    df = (
        df
        .append(row, ignore_index=True)
        .sort_values("Punts", ascending=False)
        .reset_index(drop=True)
    )

    sheet.update([df.columns.values.tolist()] + df.values.tolist())
    return df


def get_date() -> str:
    timezone = pytz.timezone("Europe/Madrid")
    return datetime.datetime.now(timezone).strftime("%d/%m/%Y")


def get_time() -> str:
    timezone = pytz.timezone("Europe/Madrid")
    return datetime.datetime.now(timezone).strftime("%H:%M:%S")