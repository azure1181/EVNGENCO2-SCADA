"""
Unit test — API DU BAO (FastAPI TestClient, chay tren code that).

Kiem tra endpoint /api/du-bao va /api/model/thong-tin:
- Ca hop le: tra 200 + du bao dung chieu.
- Ca loi: sai duoi file (400), thieu cot (422), file rong (400).

Luu y: can co san model/power_curve_model.joblib (chay notebook module_9 truoc).
Neu chua co model, cac test nay se bi bo qua (skip) thay vi bao that bai.
"""
import os

import pytest
from fastapi.testclient import TestClient

import app_du_bao as a
import mo_hinh_du_bao as mh

# Neu chua huan luyen model thi bo qua toan bo file test nay
pytestmark = pytest.mark.skipif(
    not os.path.exists(mh.MODEL_MAC_DINH),
    reason="Chua co model .joblib — hay chay notebook module_9_huan_luyen_mo_hinh.ipynb truoc.",
)


@pytest.fixture(scope="module")
def client():
    return TestClient(a.app)


def test_thong_tin_model(client):
    """GET /api/model/thong-tin -> 200 va co metrics."""
    r = client.get("/api/model/thong-tin")
    assert r.status_code == 200
    body = r.json()
    assert body["cot_dac_trung"] == mh.COT_DAC_TRUNG
    assert "r2" in body["metrics"]


def test_du_bao_csv_hop_le(client):
    """POST /api/du-bao voi CSV hop le -> 200, du bao tang theo toc do gio."""
    csv = "toc_do_gio,huong_gio\n3,180\n8,180\n15,180\n"
    r = client.post("/api/du-bao", files={"file": ("gio.csv", csv, "text/csv")})
    assert r.status_code == 200
    body = r.json()
    assert body["so_dong"] == 3
    cs = [d["cong_suat_du_doan_kw"] for d in body["du_bao"]]
    assert all(x >= 0 for x in cs)          # khong am
    assert cs[0] < cs[1] < cs[2]            # dung chieu


def test_du_bao_sai_duoi_file(client):
    """File khong phai .csv -> 400."""
    r = client.post("/api/du-bao", files={"file": ("gio.txt", "a,b\n1,2", "text/plain")})
    assert r.status_code == 400
    assert ".csv" in r.json()["detail"]


def test_du_bao_thieu_cot(client):
    """CSV thieu cot dac trung -> 422 kem ten cot thieu."""
    r = client.post("/api/du-bao", files={"file": ("x.csv", "toc_do_gio\n8", "text/csv")})
    assert r.status_code == 422
    assert "huong_gio" in r.json()["detail"]


def test_du_bao_file_rong(client):
    """File rong -> 400."""
    r = client.post("/api/du-bao", files={"file": ("rong.csv", "", "text/csv")})
    assert r.status_code == 400
