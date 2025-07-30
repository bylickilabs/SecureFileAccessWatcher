import pandas as pd

def export_log(df, path, fmt="csv"):
    if fmt == "csv":
        df.to_csv(path, index=False)
    elif fmt == "json":
        df.to_json(path, orient="records", force_ascii=False)
