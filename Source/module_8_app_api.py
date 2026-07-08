"""
Module 8 — API SCADA tua bin gio bang FastAPI (hoc co che input/output).

API doc du lieu sach Data/output/du_lieu_sach.csv va cung cap cac endpoint tra JSON,
kem endpoint upload de xu ly file CSV nguoi dung tai len.

------------------------------------------------------------------------------
CACH CHAY:
  Vao thu muc Source roi chay:
      cd Source
      uvicorn module_8_app_api:app --reload

  (Hoac chay tu thu muc goc du an:
      uvicorn module_8_app_api:app --host 0.0.0.0 --port 8000 # neu Source la package
   Cach don gian nhat van la: cd Source && uvicorn module_8_app_api:app --reload)

  Sau do mo trinh duyet:
      http://127.0.0.1:8000/docs     -> trang Swagger UI de thu cac endpoint
      http://127.0.0.1:8000/redoc    -> tai lieu dang ReDoc

  Cho may khac trong LAN truy cap:
      uvicorn Source.module_8_app_api:app --host 0.0.0.0 --port 8000
------------------------------------------------------------------------------
"""

import io
import os

import pandas as pd
from fastapi import FastAPI, File, HTTPException, Query, UploadFile

# ----- Duong dan & hang so -----
CSV_INPUT = os.path.join(os.path.dirname(__file__), "..", "Data", "output", "du_lieu_sach.csv")
PHUT_MOI_DIEM = 10          # moi ban ghi cach nhau 10 phut
NGUONG_GIO = 5.0            # gio > 5 m/s
NGUONG_HIEU_SUAT = 0.5      # cong suat < 50% cong suat ly thuyet

# ----- Khoi tao ung dung, dat title/description cho trang /docs -----
app = FastAPI(
    title="API Phan tich SCADA - Tua bin gio",
    description=(
        "API minh hoa co che input/output tren du lieu SCADA tua bin gio da lam sach.\n\n"
        "Dinh nghia **diem nghi su co**: toc do gio > 5 m/s VA cong suat thuc < 50% cong suat "
        "ly thuyet. Moi diem tuong ung 10 phut van hanh.\n\n"
        "Cac nhom endpoint:\n"
        "- `/api/kpi`: chi so tong quan\n"
        "- `/api/su-co`: danh sach diem nghi su co (loc theo thang)\n"
        "- `/api/bieu-do/san-luong`: du lieu san luong theo thang de ve bieu do\n"
        "- `/api/upload`: tai file CSV len va tinh KPI cua chinh file do"
    ),
    version="1.0.0",
)


# ============================ HAM DUNG CHUNG ============================
def chuan_bi_du_lieu(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ham dung chung: chuan hoa DataFrame va tinh cot 'nghi_su_co'.

    Input : DataFrame co cac cot cong_suat_kw, toc_do_gio, cong_suat_ly_thuyet, huong_gio
            va chi muc thoi gian (hoac cot 'thoi_gian').
    Output: DataFrame co them cot 'nghi_su_co' (bool) va chi muc la datetime.
    """
    df = df.copy()

    # Neu 'thoi_gian' con la cot thi dua ve chi muc datetime
    if "thoi_gian" in df.columns:
        df["thoi_gian"] = pd.to_datetime(df["thoi_gian"])
        df = df.set_index("thoi_gian")
    else:
        df.index = pd.to_datetime(df.index)

    # Kiem tra cac cot bat buoc
    cot_bat_buoc = {"cong_suat_kw", "toc_do_gio", "cong_suat_ly_thuyet"}
    thieu = cot_bat_buoc - set(df.columns)
    if thieu:
        raise ValueError(f"File thieu cot bat buoc: {', '.join(sorted(thieu))}")

    # Ep kieu so cho cac cot can tinh toan
    for cot in ["cong_suat_kw", "toc_do_gio", "cong_suat_ly_thuyet"]:
        df[cot] = pd.to_numeric(df[cot], errors="coerce")

    # Tinh cot nghi su co theo dinh nghia chung
    df["nghi_su_co"] = (df["toc_do_gio"] > NGUONG_GIO) & \
                       (df["cong_suat_kw"] < NGUONG_HIEU_SUAT * df["cong_suat_ly_thuyet"])
    return df


def doc_du_lieu_mac_dinh() -> pd.DataFrame:
    """Doc file du_lieu_sach.csv mac dinh va chuan bi san."""
    if not os.path.exists(CSV_INPUT):
        raise HTTPException(status_code=500, detail=f"Khong tim thay file du lieu: {CSV_INPUT}")
    df = pd.read_csv(CSV_INPUT)
    return chuan_bi_du_lieu(df)


def tinh_kpi(df: pd.DataFrame) -> dict:
    """Tinh cac chi so KPI tong quan tu DataFrame da co cot 'nghi_su_co'."""
    so_diem_su_co = int(df["nghi_su_co"].sum())
    return {
        "tong_ban_ghi": int(len(df)),
        "cong_suat_tb_kw": round(float(df["cong_suat_kw"].mean()), 2) if len(df) else 0.0,
        "toc_do_gio_tb_ms": round(float(df["toc_do_gio"].mean()), 2) if len(df) else 0.0,
        "so_diem_nghi_su_co": so_diem_su_co,
        "tong_gio_su_co": round(so_diem_su_co * PHUT_MOI_DIEM / 60, 2),
    }


# ============================ ENDPOINT 1: KPI ============================
@app.get("/api/kpi", tags=["Chi so"], summary="Chi so tong quan")
def get_kpi():
    """
    Input : khong co.
    Output: JSON cac chi so tong quan cua toan bo du lieu mac dinh:
            - tong_ban_ghi
            - cong_suat_tb_kw
            - toc_do_gio_tb_ms
            - so_diem_nghi_su_co
            - tong_gio_su_co (gio)
    """
    df = doc_du_lieu_mac_dinh()
    return tinh_kpi(df)


# ============================ ENDPOINT 2: DANH SACH SU CO ============================
@app.get("/api/su-co", tags=["Su co"], summary="Danh sach diem nghi su co (loc theo thang)")
def get_su_co(
    thang: str | None = Query(
        default=None,
        description="Loc theo thang, dinh dang YYYY-MM (vi du 2018-03). Bo trong = tat ca.",
        pattern=r"^\d{4}-\d{2}$",
    )
):
    """
    Input : tham so tuy chon 'thang' dang YYYY-MM.
    Output: JSON gom:
            - thang: gia tri loc (hoac 'tat ca')
            - so_diem: so diem nghi su co sau khi loc
            - danh_sach: mang cac ban ghi {thoi_gian, toc_do_gio, cong_suat_kw,
              cong_suat_ly_thuyet, huong_gio}
    """
    df = doc_du_lieu_mac_dinh()
    df_su_co = df[df["nghi_su_co"]].copy()

    # Loc theo thang neu co tham so
    if thang:
        df_su_co = df_su_co[df_su_co.index.strftime("%Y-%m") == thang]

    # Chuan bi danh sach ban ghi de tra JSON (dua thoi_gian ve cot chuoi)
    cot_tra = ["toc_do_gio", "cong_suat_kw", "cong_suat_ly_thuyet"]
    if "huong_gio" in df_su_co.columns:
        cot_tra.append("huong_gio")
    df_out = df_su_co[cot_tra].round(2).reset_index()
    df_out["thoi_gian"] = df_out["thoi_gian"].dt.strftime("%Y-%m-%d %H:%M:%S")

    return {
        "thang": thang if thang else "tat ca",
        "so_diem": int(len(df_out)),
        "danh_sach": df_out.to_dict(orient="records"),
    }


# ============================ ENDPOINT 3: DU LIEU BIEU DO SAN LUONG ============================
@app.get("/api/bieu-do/san-luong", tags=["Bieu do"], summary="Du lieu san luong theo thang")
def get_san_luong_thang():
    """
    Input : khong co.
    Output: JSON mang cac thang, moi phan tu gom:
            - thang (YYYY-MM)
            - tong_san_luong_mwh (tong cong suat quy ra MWh)
            - toc_do_gio_tb_ms (toc do gio trung binh thang)
            Client dung du lieu nay de ve bieu do cot / duong.
    """
    df = doc_du_lieu_mac_dinh()

    theo_thang = df.resample("ME").agg(
        tong_cong_suat=("cong_suat_kw", "sum"),
        toc_do_gio_tb=("toc_do_gio", "mean"),
    )
    ket_qua = []
    for ts, row in theo_thang.iterrows():
        ket_qua.append({
            "thang": ts.strftime("%Y-%m"),
            "tong_san_luong_mwh": round(row["tong_cong_suat"] * PHUT_MOI_DIEM / 60 / 1000, 2),
            "toc_do_gio_tb_ms": round(row["toc_do_gio_tb"], 2),
        })
    return {"so_thang": len(ket_qua), "du_lieu": ket_qua}


# ============================ ENDPOINT 4: UPLOAD CSV ============================
@app.post("/api/upload", tags=["Upload"], summary="Tai file CSV len va tinh KPI cua file do")
async def upload_csv(file: UploadFile = File(..., description="File CSV cung cau truc du lieu SCADA")):
    """
    Input : file CSV (multipart/form-data) cung cau truc voi du_lieu_sach.csv
            (co cac cot: thoi_gian, cong_suat_kw, toc_do_gio, cong_suat_ly_thuyet, huong_gio).
    Output: JSON gom ten file va KPI tinh tren chinh file do.

    Kiem tra: duoi file phai la .csv; noi dung phai doc duoc va du cot bat buoc,
    neu khong se tra loi HTTP kem thong bao ro rang.
    """
    # 1) Kiem tra duoi file
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="File khong hop le: chi chap nhan file .csv")

    # 2) Doc noi dung file
    noi_dung = await file.read()
    if not noi_dung:
        raise HTTPException(status_code=400, detail="File rong, khong co du lieu.")

    try:
        df = pd.read_csv(io.BytesIO(noi_dung))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Khong doc duoc file CSV: {e}")

    # 3) Chuan bi du lieu + tinh cot nghi su co (bat loi thieu cot)
    try:
        df = chuan_bi_du_lieu(df)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Du lieu khong hop le: {e}")

    # 4) Tra KPI cua chinh file da tai len
    return {"ten_file": file.filename, "kpi": tinh_kpi(df)}


# ============================ ENDPOINT GOC (tien loi) ============================
@app.get("/", tags=["Goc"], summary="Thong tin nhanh")
def goc():
    """Tra ve loi chao va goi y mo /docs de thu API."""
    return {"thong_bao": "API SCADA tua bin gio. Mo /docs de thu cac endpoint."}
