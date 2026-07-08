"""
Advanced — Core logic mo hinh du bao cong suat theo duong cong cong suat (power curve).

Bai toan hoi quy: du doan cong suat thuc (cong_suat_kw) tu dac trung khi tuong lai
(toc_do_gio, huong_gio). Dung de:
  - Uoc luong san luong khi biet du bao gio.
  - So sanh cong suat thuc te vs du doan -> phat hien tua bin chay duoi muc (bat thuong).

File nay chi chua HAM DUNG CHUNG (khong tu chay). Duoc goi boi:
  - module_9_huan_luyen_mo_hinh.ipynb  (huan luyen + luu model)
  - app_du_bao.py                       (API nap model + du bao)
  - tests/                              (unit test)
"""

import os

import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# ----- Hang so cau hinh -----
# Dac trung dau vao (X) va muc tieu can du doan (y)
COT_DAC_TRUNG = ["toc_do_gio", "huong_gio"]
COT_MUC_TIEU = "cong_suat_kw"

# Duong dan mac dinh (tuong doi so voi file nay, nam trong Advanced/)
_THU_MUC = os.path.dirname(__file__)
CSV_MAC_DINH = os.path.join(_THU_MUC, "..", "Data", "output", "du_lieu_sach.csv")
MODEL_MAC_DINH = os.path.join(_THU_MUC, "model", "power_curve_model.joblib")


def doc_du_lieu_sach(duong_dan: str = CSV_MAC_DINH) -> pd.DataFrame:
    """Doc file du_lieu_sach.csv (da lam sach o Module 2) voi chi muc thoi gian."""
    if not os.path.exists(duong_dan):
        raise FileNotFoundError(
            f"Khong tim thay du lieu sach: {duong_dan}. "
            "Hay chay Module 2 (lam sach) truoc de tao du_lieu_sach.csv."
        )
    return pd.read_csv(duong_dan, index_col="thoi_gian", parse_dates=True)


def tao_X_y(df: pd.DataFrame):
    """
    Tach dac trung X va muc tieu y tu DataFrame (dung khi HUAN LUYEN).

    Input : DataFrame co cac cot COT_DAC_TRUNG + COT_MUC_TIEU.
    Output: (X, y) da ep kieu so va bo cac dong thieu du lieu.
    Loi   : ValueError neu thieu cot bat buoc.
    """
    can_co = COT_DAC_TRUNG + [COT_MUC_TIEU]
    thieu = [c for c in can_co if c not in df.columns]
    if thieu:
        raise ValueError(f"Thieu cot bat buoc de huan luyen: {', '.join(thieu)}")

    du_lieu = df[can_co].apply(pd.to_numeric, errors="coerce").dropna()
    X = du_lieu[COT_DAC_TRUNG]
    y = du_lieu[COT_MUC_TIEU]
    return X, y


def _tinh_chi_so(y_that, y_du_doan) -> dict:
    """Tinh cac chi so danh gia hoi quy: R2, MAE, RMSE."""
    return {
        "r2": round(float(r2_score(y_that, y_du_doan)), 4),
        "mae": round(float(mean_absolute_error(y_that, y_du_doan)), 2),
        "rmse": round(float(np.sqrt(mean_squared_error(y_that, y_du_doan))), 2),
    }


def huan_luyen(df: pd.DataFrame, test_size: float = 0.2, random_state: int = 42) -> dict:
    """
    Huan luyen mo hinh RandomForest du doan cong suat tu (toc_do_gio, huong_gio).

    Input : DataFrame du lieu sach.
    Output: dict gom:
            - "model"  : mo hinh sklearn da huan luyen
            - "metrics": {r2, mae, rmse, n_train, n_test} tren tap kiem tra (held-out)
    """
    X, y = tao_X_y(df)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    # Ràng buộc độ sâu & số mẫu tối thiểu mỗi lá: chống overfit và giữ file model nhỏ (~5 MB)
    model = RandomForestRegressor(
        n_estimators=60, max_depth=14, min_samples_leaf=20,
        random_state=random_state, n_jobs=-1,
    )
    model.fit(X_train, y_train)

    # Danh gia tren tap kiem tra (du lieu model chua tung thay)
    chi_so = _tinh_chi_so(y_test, model.predict(X_test))
    chi_so["n_train"] = int(len(X_train))
    chi_so["n_test"] = int(len(X_test))

    return {"model": model, "metrics": chi_so}


def du_bao(model, df: pd.DataFrame) -> np.ndarray:
    """
    Du doan cong suat cho DataFrame dau vao (dung khi DU BAO).

    Input : model da huan luyen + DataFrame co cac cot COT_DAC_TRUNG.
    Output: mang numpy cong suat du doan (kW), da chan >= 0 (cong suat khong am).
    Loi   : ValueError neu thieu cot dac trung.
    """
    thieu = [c for c in COT_DAC_TRUNG if c not in df.columns]
    if thieu:
        raise ValueError(f"Thieu cot dac trung de du bao: {', '.join(thieu)}")

    X = df[COT_DAC_TRUNG].apply(pd.to_numeric, errors="coerce")
    if X.isna().any().any():
        raise ValueError("Du lieu dau vao co gia tri khong hop le (khong ep duoc ve so).")

    du_doan = model.predict(X)
    return np.clip(du_doan, 0, None)  # cong suat khong the am


def luu_model(model, metrics: dict, duong_dan: str = MODEL_MAC_DINH) -> str:
    """Luu model + metadata (dac trung, muc tieu, metrics) ra file .joblib."""
    os.makedirs(os.path.dirname(duong_dan), exist_ok=True)
    goi = {
        "model": model,
        "cot_dac_trung": COT_DAC_TRUNG,
        "cot_muc_tieu": COT_MUC_TIEU,
        "metrics": metrics,
    }
    joblib.dump(goi, duong_dan)
    return duong_dan


def nap_model(duong_dan: str = MODEL_MAC_DINH) -> dict:
    """
    Nap goi model tu file .joblib.

    Output: dict {model, cot_dac_trung, cot_muc_tieu, metrics}.
    Loi   : FileNotFoundError neu chua huan luyen (chua co file model).
    """
    if not os.path.exists(duong_dan):
        raise FileNotFoundError(
            f"Chua co file model: {duong_dan}. "
            "Hay chay notebook module_9_huan_luyen_mo_hinh.ipynb de huan luyen va luu model."
        )
    return joblib.load(duong_dan)
