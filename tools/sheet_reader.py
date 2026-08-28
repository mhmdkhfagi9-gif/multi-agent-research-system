"""
Structured data tool: reads Excel/CSV files (or a public Google Sheets
export URL) and converts rows into readable text records.
Used by the Sheet sub-agent inside retrieval_agent.py.
"""

import os
import pandas as pd


def read_sheet(source: str) -> str:
    """
    source: a local .csv/.xlsx/.xls path, OR a Google Sheets export URL
    (e.g. ".../export?format=csv").
    Returns one text record per row: "col1: val1 | col2: val2 | ..."
    """
    if source.endswith((".xlsx", ".xls")):
        df = pd.read_excel(source)
    else:
        df = pd.read_csv(source)

    df = df.fillna("")
    df.columns = [str(c).strip() for c in df.columns]

    rows_as_text = []
    for _, row in df.iterrows():
        parts = [f"{col}: {str(row[col]).strip()}" for col in df.columns if str(row[col]).strip()]
        row_text = " | ".join(parts)
        if row_text:
            rows_as_text.append(row_text)

    return "\n".join(rows_as_text)


def read_all_sheets(directory: str) -> dict:
    """Reads every CSV/Excel file in a directory. Returns {filename: text}."""
    results = {}
    if not os.path.isdir(directory):
        return results

    for filename in os.listdir(directory):
        if filename.lower().endswith((".csv", ".xlsx", ".xls")):
            path = os.path.join(directory, filename)
            try:
                results[filename] = read_sheet(path)
            except Exception as e:
                results[filename] = f"[ERROR reading {filename}: {e}]"
    return results
