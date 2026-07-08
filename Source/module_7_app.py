"""
Module 7 — Ung dung Streamlit: Dashboard dong phan tich du lieu SCADA tua bin gio.

Doc du lieu sach Data/output/du_lieu_sach.csv, cho phep loc tuong tac tren sidebar
(chon thang, nguong toc do gio, nguong hieu suat) va cap nhat KPI + bieu do theo bo loc.

------------------------------------------------------------------------------
CACH CHAY:
  1) Chay local (chi may nay truy cap duoc):
       streamlit run Source/module_7_app.py
     -> Mo trinh duyet tai http://localhost:8501

  2) Cho may khac trong mang LAN truy cap:
       streamlit run Source/module_7_app.py --server.address 0.0.0.0
     -> May khac mo: http://<IP-may-chu>:8501  (vi du http://192.168.1.10:8501)

  Cach lay dia chi IP cua may chu (mo terminal / cmd):
     - Windows:      ipconfig      -> tim dong "IPv4 Address" (vi du 192.168.1.10)
     - Linux/macOS:  ip addr  hoac  ifconfig   (hoac: hostname -I)
  Luu y: dam bao tuong lua (firewall) cho phep cong 8501, va cac may cung mang LAN.
------------------------------------------------------------------------------
"""

import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ----- Duong dan & hang so -----
CSV_INPUT = os.path.join(os.path.dirname(__file__), "..", "Data", "output", "du_lieu_sach.csv")
PHUT_MOI_DIEM = 10       # moi ban ghi cach nhau 10 phut
SO_MAU_SCATTER = 8000    # so diem lay mau cho bieu do duong cong cong suat

# Cau hinh trang (rong toan man hinh)
st.set_page_config(page_title="Dashboard SCADA - Tua bin gio", layout="wide")


@st.cache_data
def doc_du_lieu():
    """Doc du lieu sach mot lan va cache lai (khong doc lai moi lan tuong tac)."""
    df = pd.read_csv(CSV_INPUT, index_col="thoi_gian", parse_dates=True)
    # Cot nhan thang dang MM/YYYY de dung cho bo loc
    df["thang"] = df.index.strftime("%m/%Y")
    return df


# ============================ DOC DU LIEU ============================
df_goc = doc_du_lieu()

# ============================ SIDEBAR: BO LOC ============================
st.sidebar.header("Bo loc")

# (1) Chon thang (hoac Tat ca) — giu thu tu thoi gian
danh_sach_thang = list(dict.fromkeys(df_goc["thang"].tolist()))  # unique, giu thu tu
lua_chon_thang = st.sidebar.selectbox("Chon thang", ["Tat ca"] + danh_sach_thang)

# (2) Nguong toc do gio xet su co (3-10 m/s)
nguong_gio = st.sidebar.slider(
    "Nguong toc do gio xet su co (m/s)", min_value=3.0, max_value=10.0, value=5.0, step=0.5,
)

# (3) Nguong hieu suat xet su co (30-80%)
nguong_hieu_suat_pc = st.sidebar.slider(
    "Nguong hieu suat xet su co (%)", min_value=30, max_value=80, value=50, step=5,
)
nguong_hieu_suat = nguong_hieu_suat_pc / 100.0

st.sidebar.caption(
    "Su co = toc do gio > nguong gio VA cong suat < nguong hieu suat x cong suat ly thuyet."
)

# ============================ AP DUNG BO LOC ============================
# Loc theo thang
if lua_chon_thang == "Tat ca":
    df = df_goc.copy()
else:
    df = df_goc[df_goc["thang"] == lua_chon_thang].copy()

# Gan co diem nghi su co theo nguong nguoi dung chon
df["nghi_su_co"] = (df["toc_do_gio"] > nguong_gio) & \
                   (df["cong_suat_kw"] < nguong_hieu_suat * df["cong_suat_ly_thuyet"])

# ============================ TIEU DE ============================
st.title("Dashboard Phan tich SCADA - Tua bin gio")
st.caption(
    f"Pham vi: {lua_chon_thang}  |  Nguong gio > {nguong_gio} m/s  |  "
    f"Nguong hieu suat < {nguong_hieu_suat_pc}%"
)

# ============================ HANG KPI (st.metric) ============================
so_ban_ghi = len(df)
so_diem_su_co = int(df["nghi_su_co"].sum())
cong_suat_tb = df["cong_suat_kw"].mean() if so_ban_ghi else 0
toc_do_gio_tb = df["toc_do_gio"].mean() if so_ban_ghi else 0

c1, c2, c3, c4 = st.columns(4)
c1.metric("So ban ghi", f"{so_ban_ghi:,}")
c2.metric("Cong suat TB (kW)", f"{cong_suat_tb:,.1f}")
c3.metric("Toc do gio TB (m/s)", f"{toc_do_gio_tb:,.2f}")
c4.metric("So diem su co", f"{so_diem_su_co:,}")

st.divider()

# ============================ BIEU DO 1: DUONG CONG CONG SUAT ============================
st.subheader("Duong cong cong suat")
if so_ban_ghi:
    # Lay mau ~8000 diem cho nhe (neu du lieu it hon thi lay het)
    df_mau = df.sample(n=min(SO_MAU_SCATTER, so_ban_ghi), random_state=42).copy()
    df_mau["Trang thai"] = df_mau["nghi_su_co"].map({True: "Nghi su co", False: "Binh thuong"})

    fig_scatter = px.scatter(
        df_mau, x="toc_do_gio", y="cong_suat_kw", color="Trang thai",
        color_discrete_map={"Binh thuong": "#4C9BE8", "Nghi su co": "#E24A4A"},
        labels={"toc_do_gio": "Toc do gio (m/s)", "cong_suat_kw": "Cong suat thuc (kW)"},
        opacity=0.5,
    )
    fig_scatter.update_traces(marker=dict(size=5))
    fig_scatter.update_layout(legend_title_text="", margin=dict(l=40, r=20, t=10, b=40))
    st.plotly_chart(fig_scatter, use_container_width=True)
else:
    st.info("Khong co du lieu trong pham vi da chon.")

# ============================ BIEU DO 2 & 3: CANH NHAU ============================
col_trai, col_phai = st.columns(2)

# Bieu do cot: san luong theo thang (luon tinh tren toan bo pham vi da loc)
with col_trai:
    st.subheader("San luong theo thang (MWh)")
    if so_ban_ghi:
        san_luong = df["cong_suat_kw"].resample("ME").sum() * PHUT_MOI_DIEM / 60 / 1000
        nhan_thang = san_luong.index.strftime("%m/%Y")
        fig_bar = go.Figure(go.Bar(
            x=nhan_thang, y=san_luong.values, marker_color="#4C9BE8",
            hovertemplate="Thang %{x}<br>%{y:.1f} MWh<extra></extra>",
        ))
        fig_bar.update_layout(
            xaxis_title="Thang", yaxis_title="San luong (MWh)",
            margin=dict(l=40, r=20, t=10, b=40),
        )
        st.plotly_chart(fig_bar, use_container_width=True)

# Bieu do duong: cong suat trung binh theo ngay
with col_phai:
    st.subheader("Cong suat trung binh theo ngay (kW)")
    if so_ban_ghi:
        theo_ngay = df["cong_suat_kw"].resample("D").mean()
        fig_line = go.Figure(go.Scatter(
            x=theo_ngay.index, y=theo_ngay.values, mode="lines",
            line=dict(color="#5FA85F", width=1.5),
            hovertemplate="Ngay %{x|%d/%m/%Y}<br>%{y:.1f} kW<extra></extra>",
        ))
        fig_line.update_layout(
            xaxis_title="Thoi gian", yaxis_title="Cong suat TB (kW)",
            margin=dict(l=40, r=20, t=10, b=40),
        )
        st.plotly_chart(fig_line, use_container_width=True)

st.divider()

# ============================ BANG DANH SACH DIEM SU CO ============================
st.subheader(f"Danh sach diem su co ({so_diem_su_co:,} diem)")
diem_su_co = (
    df.loc[df["nghi_su_co"], ["toc_do_gio", "cong_suat_kw", "cong_suat_ly_thuyet", "huong_gio"]]
    .rename(columns={
        "toc_do_gio": "Toc do gio (m/s)",
        "cong_suat_kw": "Cong suat thuc (kW)",
        "cong_suat_ly_thuyet": "Cong suat ly thuyet (kWh)",
        "huong_gio": "Huong gio (do)",
    })
    .round(2)
)
st.dataframe(diem_su_co, use_container_width=True)
