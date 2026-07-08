"""
Unit test — Nhanh 1: XU LY DU LIEU (tach dac trung / muc tieu).

Kiem tra ham dung chung tao_X_y trong mo_hinh_du_bao.py:
- Tach dung cot dac trung va muc tieu.
- Bo dong thieu du lieu (NaN).
- Bao loi ro rang khi thieu cot bat buoc.
"""
import numpy as np
import pandas as pd
import pytest

import mo_hinh_du_bao as mh


def test_tao_X_y_dung_cot_va_kich_thuoc(df_gia_lap):
    """X phai gom dung COT_DAC_TRUNG; y la cot muc tieu; so dong khop nhau."""
    X, y = mh.tao_X_y(df_gia_lap)
    assert list(X.columns) == mh.COT_DAC_TRUNG
    assert y.name == mh.COT_MUC_TIEU
    assert len(X) == len(y) == len(df_gia_lap)


def test_tao_X_y_bo_dong_thieu_du_lieu():
    """Dong co NaN o dac trung hoac muc tieu phai bi loai."""
    df = pd.DataFrame({
        "toc_do_gio": [5.0, np.nan, 8.0],
        "huong_gio": [100.0, 200.0, 300.0],
        "cong_suat_kw": [400.0, 500.0, np.nan],
    })
    X, y = mh.tao_X_y(df)
    # Chi con 1 dong hop le (dong dau tien)
    assert len(X) == 1
    assert y.iloc[0] == 400.0


def test_tao_X_y_thieu_cot_bao_loi():
    """Thieu cot bat buoc -> ValueError co ten cot bi thieu."""
    df = pd.DataFrame({"toc_do_gio": [5.0], "huong_gio": [100.0]})  # thieu cong_suat_kw
    with pytest.raises(ValueError, match="cong_suat_kw"):
        mh.tao_X_y(df)
