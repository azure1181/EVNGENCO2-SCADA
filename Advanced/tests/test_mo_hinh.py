"""
Unit test — Nhanh 2: MO HINH (huan luyen, du bao, luu/nap).

Kiem tra:
- huan_luyen tra ve model + metrics hop le; R2 du tot tren tap kiem tra.
- du_bao: dung chieu (gio cao -> cong suat cao), khong am, dung so dong.
- du_bao bao loi khi thieu cot dac trung.
- luu_model / nap_model giu nguyen ket qua du bao (round-trip).
"""
import numpy as np
import pandas as pd
import pytest

import mo_hinh_du_bao as mh


def test_huan_luyen_tra_ve_metrics_hop_le(model_da_luyen):
    """metrics phai co du khoa va R2 nam trong khoang hop ly, du tot."""
    metrics = model_da_luyen["metrics"]
    for khoa in ["r2", "mae", "rmse", "n_train", "n_test"]:
        assert khoa in metrics
    # Du lieu gia lap co quan he ro rang -> R2 phai cao
    assert metrics["r2"] > 0.9
    assert metrics["n_train"] > metrics["n_test"] > 0


def test_du_bao_dung_chieu_va_khong_am(model_da_luyen):
    """Gio cao phai cho cong suat du doan cao hon gio thap; khong gia tri am."""
    model = model_da_luyen["model"]
    mau = pd.DataFrame({"toc_do_gio": [2.0, 8.0, 15.0], "huong_gio": [180, 180, 180]})
    du_doan = mh.du_bao(model, mau)
    assert len(du_doan) == 3
    assert (du_doan >= 0).all()
    assert du_doan[0] < du_doan[1] < du_doan[2]


def test_du_bao_thieu_cot_bao_loi(model_da_luyen):
    """Thieu cot dac trung -> ValueError."""
    model = model_da_luyen["model"]
    mau = pd.DataFrame({"toc_do_gio": [8.0]})  # thieu huong_gio
    with pytest.raises(ValueError, match="huong_gio"):
        mh.du_bao(model, mau)


def test_luu_nap_model_giu_nguyen_ket_qua(model_da_luyen, tmp_path):
    """Luu roi nap lai, du bao phai giong het (round-trip)."""
    model = model_da_luyen["model"]
    metrics = model_da_luyen["metrics"]
    duong_dan = str(tmp_path / "model_test.joblib")

    mh.luu_model(model, metrics, duong_dan)
    goi = mh.nap_model(duong_dan)

    assert goi["cot_dac_trung"] == mh.COT_DAC_TRUNG
    assert goi["metrics"] == metrics

    mau = pd.DataFrame({"toc_do_gio": [3.0, 10.0], "huong_gio": [90, 90]})
    np.testing.assert_array_almost_equal(
        mh.du_bao(model, mau), mh.du_bao(goi["model"], mau)
    )


def test_nap_model_thieu_file_bao_loi(tmp_path):
    """Nap model tu duong dan khong ton tai -> FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        mh.nap_model(str(tmp_path / "khong_ton_tai.joblib"))
