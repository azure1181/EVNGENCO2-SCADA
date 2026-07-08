"""
Cau hinh chung cho pytest.

Them thu muc Advanced/ vao sys.path de import truc tiep mo_hinh_du_bao va app_du_bao
khi chay pytest tu bat ky thu muc nao. Cung cung cap cac fixture du lieu mau.
"""
import os
import sys

import numpy as np
import pandas as pd
import pytest

# Thu muc Advanced/ (cha cua thu muc tests/)
ADVANCED_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ADVANCED_DIR not in sys.path:
    sys.path.insert(0, ADVANCED_DIR)


@pytest.fixture(scope="session")
def df_gia_lap():
    """
    Tao DataFrame gia lap co quan he power-curve ro rang (gio cao -> cong suat cao),
    du de mo hinh hoc duoc va cho R2 cao. Khong phu thuoc file du lieu that.
    """
    rng = np.random.default_rng(0)
    gio = rng.uniform(0, 25, size=2000)
    huong = rng.uniform(0, 360, size=2000)
    # Cong suat theo dang bao hoa + nhieu nhe
    cong_suat = np.clip(3600 / (1 + np.exp(-(gio - 9))) + rng.normal(0, 40, size=2000), 0, 3600)
    return pd.DataFrame({
        "cong_suat_kw": cong_suat,
        "toc_do_gio": gio,
        "cong_suat_ly_thuyet": cong_suat * 1.05,
        "huong_gio": huong,
    })


@pytest.fixture(scope="session")
def model_da_luyen(df_gia_lap):
    """Huan luyen san mot model tren du lieu gia lap (dung lai cho nhieu test)."""
    import mo_hinh_du_bao as mh
    return mh.huan_luyen(df_gia_lap)
