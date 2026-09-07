"""Shared utilities for the offline UPI fraud detection project."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Iterable

import joblib
import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
MERGED_DATA_DIR = DATA_DIR / "merged"
MODELS_DIR = PROJECT_ROOT / "models"
REPORTS_DIR = PROJECT_ROOT / "reports"


def get_logger(name: str) -> logging.Logger:
    """Return a configured module logger."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    return logging.getLogger(name)


def ensure_project_dirs() -> None:
    """Create expected project directories if they are missing."""
    for directory in [
        RAW_DATA_DIR,
        PROCESSED_DATA_DIR,
        MERGED_DATA_DIR,
        MODELS_DIR,
        REPORTS_DIR,
        PROJECT_ROOT / "notebooks",
        PROJECT_ROOT / "app" / "components",
    ]:
        directory.mkdir(parents=True, exist_ok=True)


def validate_columns(df: pd.DataFrame, required_columns: Iterable[str]) -> None:
    """Raise a clear error when a dataframe is missing required columns."""
    missing = [column for column in required_columns if column not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")


def save_dataframe(df: pd.DataFrame, path: Path | str) -> None:
    """Save a dataframe as CSV or Parquet based on the file extension."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.suffix.lower() == ".parquet":
        df.to_parquet(output_path, index=False)
    else:
        df.to_csv(output_path, index=False)


def load_dataframe(path: Path | str) -> pd.DataFrame:
    """Load a dataframe from CSV, Parquet, or Excel."""
    input_path = Path(path)
    suffix = input_path.suffix.lower()

    if suffix == ".csv":
        return pd.read_csv(input_path)
    if suffix == ".parquet":
        return pd.read_parquet(input_path)
    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(input_path)

    raise ValueError(f"Unsupported file type: {input_path.suffix}")


def save_joblib(obj: object, path: Path | str) -> None:
    """Persist a Python object with joblib."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(obj, output_path)


def _patch_sklearn_compat(obj: object) -> object:
    """Ensure backward-compatibility for estimators across scikit-learn versions."""
    if obj is None:
        return obj

    visited: set[int] = set()

    def _patch(item: object) -> None:
        if item is None:
            return
        item_id = id(item)
        if item_id in visited:
            return
        visited.add(item_id)

        # Patch SimpleImputer missing _fill_dtype (scikit-learn 1.6+ compatibility)
        cls_name = getattr(getattr(item, "__class__", None), "__name__", "")
        if "SimpleImputer" in cls_name:
            if not hasattr(item, "_fill_dtype"):
                fit_dtype = getattr(item, "_fit_dtype", None)
                if fit_dtype is None and hasattr(item, "statistics_") and hasattr(item.statistics_, "dtype"):
                    fit_dtype = item.statistics_.dtype
                setattr(item, "_fill_dtype", fit_dtype if fit_dtype is not None else object)

        # Traverse ColumnTransformer / Pipeline
        if hasattr(item, "transformers_"):
            for entry in getattr(item, "transformers_", []):
                if isinstance(entry, (list, tuple)) and len(entry) >= 2:
                    _patch(entry[1])
        if hasattr(item, "named_steps") and isinstance(item.named_steps, dict):
            for step in item.named_steps.values():
                _patch(step)
        if hasattr(item, "steps") and isinstance(item.steps, (list, tuple)):
            for step in item.steps:
                if isinstance(step, (list, tuple)) and len(step) >= 2:
                    _patch(step[1])

        # Traverse object __dict__
        if hasattr(item, "__dict__"):
            for val in list(item.__dict__.values()):
                if isinstance(val, (list, tuple, set)):
                    for sub in val:
                        if hasattr(sub, "__dict__") or "SimpleImputer" in getattr(getattr(sub, "__class__", None), "__name__", ""):
                            _patch(sub)
                elif isinstance(val, dict):
                    for sub in val.values():
                        if hasattr(sub, "__dict__") or "SimpleImputer" in getattr(getattr(sub, "__class__", None), "__name__", ""):
                            _patch(sub)
                elif hasattr(val, "__dict__") or "SimpleImputer" in getattr(getattr(val, "__class__", None), "__name__", ""):
                    _patch(val)

    _patch(obj)
    return obj


def load_joblib(path: Path | str) -> object:
    """Load a joblib object with scikit-learn cross-version compatibility."""
    obj = joblib.load(Path(path))
    return _patch_sklearn_compat(obj)


def safe_datetime(series: pd.Series) -> pd.Series:
    """Convert a series to pandas datetime while tolerating invalid values."""
    converted = pd.to_datetime(series, errors="coerce", utc=True, format="mixed")
    return converted.dt.tz_localize(None)


def make_transaction_ids(prefix: str, length: int, start: int = 0) -> pd.Series:
    """Create deterministic transaction ids for datasets that do not provide one."""
    return pd.Series([f"{prefix}_{idx:08d}" for idx in range(start, start + length)])


def numeric_columns(df: pd.DataFrame, exclude: Iterable[str] | None = None) -> list[str]:
    """Return numeric columns, excluding any provided names."""
    excluded = set(exclude or [])
    return [
        column
        for column in df.select_dtypes(include=[np.number]).columns
        if column not in excluded
    ]


def categorical_columns(df: pd.DataFrame, exclude: Iterable[str] | None = None) -> list[str]:
    """Return categorical columns, excluding any provided names."""
    excluded = set(exclude or [])
    return [
        column
        for column in df.select_dtypes(include=["object", "category", "bool"]).columns
        if column not in excluded
    ]
