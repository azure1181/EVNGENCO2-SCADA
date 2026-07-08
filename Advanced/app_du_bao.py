"""
Advanced — API du bao cong suat tua bin gio (FastAPI).

Nap model power-curve da huan luyen (power_curve_model.joblib) va cung cap endpoint
de nguoi dung TAI FILE CSV (co cot toc_do_gio, huong_gio) len -> nhan cong suat DU DOAN.

------------------------------------------------------------------------------
CACH CHAY:
  Buoc 1 (mot lan): huan luyen & luu model bang notebook
      module_9_huan_luyen_mo_hinh.ipynb   (tao ra model/power_curve_model.joblib)

  Buoc 2: chay API — chon MOT trong hai cach (ca hai deu chay duoc).
  Dung cong 8001 de KHONG de len module_8_app_api (dang dung 8000):
      # Cach 1 — tu trong Advanced/ (app KHONG co tien to):
      cd Advanced
      uvicorn app_du_bao:app --reload --port 8001
      # Cach 2 — tu thu muc goc du an (app CO tien to "Advanced." — dau cham, khong phai /):
      uvicorn Advanced.app_du_bao:app --reload --port 8001
  Mo trinh duyet:
      http://127.0.0.1:8001/docs   -> Swagger UI, bam "Try it out" o /api/du-bao de tai CSV

  Cho may khac trong LAN (them --host 0.0.0.0):
      uvicorn Advanced.app_du_bao:app --host 0.0.0.0 --port 8001
      -> may khac mo http://<IP-may-chu>:8001/docs
      (Lay IP: Windows -> ipconfig; Linux/macOS -> hostname -I)
------------------------------------------------------------------------------
"""

import io
import os
import sys

import pandas as pd
from fastapi import FastAPI, File, HTTPException, UploadFile

# Cho phep import mo_hinh_du_bao du chay tu Advanced/ (uvicorn app_du_bao:app)
# hay tu thu muc goc du an (uvicorn Advanced.app_du_bao:app): tu them thu muc
# chua file nay vao sys.path.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import mo_hinh_du_bao as mh

# ----- Khoi tao ung dung + title/description cho trang /docs -----
app = FastAPI(
    title="API Du bao cong suat - Tua bin gio",
    description=(
        "Nap mo hinh hoi quy **power curve** da huan luyen va du doan cong suat thuc "
        "tu dac trung khi tuong lai (toc do gio, huong gio).\n\n"
        "**Cong dung:** biet du bao gio -> uoc luong cong suat/san luong; hoac so sanh "
        "cong suat thuc te vs du doan de phat hien tua bin chay duoi muc.\n\n"
        "Endpoint chinh: `POST /api/du-bao` — tai file CSV (cot `toc_do_gio`, `huong_gio`) "
        "len va nhan lai cong suat du doan cho tung dong."
    ),
    version="1.0.0",
)

# Cache model trong bo nho (nap 1 lan). Nap "luoi bieng" (lazy) o lan goi dau tien.
_goi_model = None


def lay_model():
    """
    Nap goi model (model + metadata) va cache lai.
    Neu chua huan luyen (chua co file .joblib) -> tra loi HTTP 503 ro rang.
    """
    global _goi_model
    if _goi_model is None:
        try:
            _goi_model = mh.nap_model()
        except FileNotFoundError as e:
            raise HTTPException(status_code=503, detail=str(e))
    return _goi_model


# ============================ ENDPOINT: THONG TIN MODEL ============================
@app.get("/api/model/thong-tin", tags=["Model"], summary="Thong tin mo hinh da huan luyen")
def thong_tin_model():
    """
    Input : khong co.
    Output: JSON gom dac trung dau vao, muc tieu, va cac chi so danh gia (R2, MAE, RMSE)
            cua model dang su dung.
    """
    goi = lay_model()
    return {
        "cot_dac_trung": goi["cot_dac_trung"],
        "cot_muc_tieu": goi["cot_muc_tieu"],
        "metrics": goi["metrics"],
    }


# ============================ ENDPOINT: DU BAO TU FILE CSV ============================
@app.post("/api/du-bao", tags=["Du bao"], summary="Tai CSV len va du doan cong suat")
async def du_bao_tu_csv(
    file: UploadFile = File(..., description="File CSV co cot toc_do_gio, huong_gio"),
):
    """
    Input : file CSV (multipart/form-data) co it nhat cac cot dac trung
            (toc_do_gio, huong_gio). Moi dong la mot kich ban gio can du doan.
    Output: JSON gom:
            - ten_file
            - so_dong
            - tong_san_luong_du_bao_mwh: gia su moi dong = 1 buoc 10 phut
            - du_bao: mang cac ban ghi {toc_do_gio, huong_gio, cong_suat_du_doan_kw}

    Kiem tra: duoi file .csv; doc duoc; du cot dac trung; neu loi tra HTTP kem thong bao ro.
    """
    # 1) Kiem tra duoi file
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="File khong hop le: chi chap nhan file .csv")

    # 2) Doc noi dung
    noi_dung = await file.read()
    if not noi_dung:
        raise HTTPException(status_code=400, detail="File rong, khong co du lieu.")
    try:
        df = pd.read_csv(io.BytesIO(noi_dung))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Khong doc duoc file CSV: {e}")

    # 3) Du bao (bat loi thieu cot / gia tri khong hop le)
    goi = lay_model()
    try:
        du_doan = mh.du_bao(goi["model"], df)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

    # 4) Ghep ket qua tra ve
    ket_qua = df[mh.COT_DAC_TRUNG].copy()
    ket_qua["cong_suat_du_doan_kw"] = du_doan.round(2)
    # San luong du bao (MWh) neu coi moi dong la 1 buoc 10 phut
    tong_mwh = round(float(du_doan.sum()) * 10 / 60 / 1000, 3)

    return {
        "ten_file": file.filename,
        "so_dong": int(len(ket_qua)),
        "tong_san_luong_du_bao_mwh": tong_mwh,
        "du_bao": ket_qua.to_dict(orient="records"),
    }


# ============================ ENDPOINT GOC ============================
@app.get("/", tags=["Goc"], summary="Thong tin nhanh")
def goc():
    """Loi chao + goi y mo /docs."""
    return {"thong_bao": "API du bao cong suat tua bin gio. Mo /docs de thu /api/du-bao."}
