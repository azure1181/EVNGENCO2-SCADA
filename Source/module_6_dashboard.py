"""
Module 6 (bản dashboard) — Sinh trang dashboard HTML tĩnh cho dữ liệu SCADA tua bin gió.

Đọc dữ liệu sạch Data/output/du_lieu_sach.csv, tạo các biểu đồ Plotly tương tác
(zoom, di chuột xem giá trị) và giao diện Bootstrap, rồi ghép thành một file HTML
duy nhất Report/dashboard.html — mở được bằng trình duyệt mà KHÔNG cần server.

Cách chạy:  python Source/module_6_dashboard.py
"""

import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

# ----- Đường dẫn & hằng số -----
CSV_INPUT = os.path.join(os.path.dirname(__file__), "..", "Data", "output", "du_lieu_sach.csv")
HTML_OUTPUT = os.path.join(os.path.dirname(__file__), "..", "Report", "dashboard.html")
PHUT_MOI_DIEM = 10   # mỗi bản ghi cách nhau 10 phút
SO_MAU_SCATTER = 8000  # số điểm lấy mẫu cho biểu đồ đường cong công suất


def doc_du_lieu():
    """Đọc dữ liệu sạch và gắn cờ điểm nghi sự cố."""
    df = pd.read_csv(CSV_INPUT, index_col="thoi_gian", parse_dates=True)
    # Điểm nghi sự cố: gió > 5 m/s và công suất < 50% công suất lý thuyet
    df["nghi_su_co"] = (df["toc_do_gio"] > 5) & (df["cong_suat_kw"] < 0.5 * df["cong_suat_ly_thuyet"])
    return df


def tinh_kpi(df):
    """Tính các chỉ số KPI tổng quan."""
    so_diem_su_co = int(df["nghi_su_co"].sum())
    return {
        "tong_ban_ghi": len(df),
        "cong_suat_tb": df["cong_suat_kw"].mean(),
        "toc_do_gio_tb": df["toc_do_gio"].mean(),
        "so_diem_su_co": so_diem_su_co,
        "tong_gio_su_co": so_diem_su_co * PHUT_MOI_DIEM / 60,
    }


def bieu_do_duong_cong(df):
    """Biểu đồ 1: đường cong công suất (scatter), tô màu theo cờ nghi sự cố."""
    # Lấy mẫu ~8000 điểm để trang nhẹ mà vẫn giữ hình dạng phân phối
    df_mau = df.sample(n=min(SO_MAU_SCATTER, len(df)), random_state=42).copy()
    df_mau["Trang thai"] = df_mau["nghi_su_co"].map({True: "Nghi su co", False: "Binh thuong"})

    fig = px.scatter(
        df_mau, x="toc_do_gio", y="cong_suat_kw",
        color="Trang thai",
        color_discrete_map={"Binh thuong": "#4C9BE8", "Nghi su co": "#E24A4A"},
        labels={"toc_do_gio": "Tốc độ gió (m/s)", "cong_suat_kw": "Công suất thực (kW)"},
        title="Đường cong công suất (mẫu ~8000 điểm)",
        opacity=0.5,
    )
    fig.update_traces(marker=dict(size=5))
    fig.update_layout(margin=dict(l=40, r=20, t=50, b=40), legend_title_text="")
    return fig


def bieu_do_san_luong_thang(df):
    """Biểu đồ 2: tổng sản lượng điện theo tháng (biểu đồ cột)."""
    theo_thang = df["cong_suat_kw"].resample("ME").sum() * PHUT_MOI_DIEM / 60 / 1000  # -> MWh
    nhan_thang = theo_thang.index.strftime("%m/%Y")

    fig = go.Figure(go.Bar(
        x=nhan_thang, y=theo_thang.values, marker_color="#4C9BE8",
        hovertemplate="Tháng %{x}<br>Sản lượng: %{y:.1f} MWh<extra></extra>",
    ))
    fig.update_layout(
        title="Sản lượng điện theo tháng (MWh)",
        xaxis_title="Tháng", yaxis_title="Sản lượng (MWh)",
        margin=dict(l=40, r=20, t=50, b=40),
    )
    return fig


def bieu_do_cong_suat_theo_ngay(df):
    """Biểu đồ 3: công suất trung bình theo ngày (biểu đồ đường)."""
    theo_ngay = df["cong_suat_kw"].resample("D").mean()

    fig = go.Figure(go.Scatter(
        x=theo_ngay.index, y=theo_ngay.values, mode="lines",
        line=dict(color="#5FA85F", width=1.5),
        hovertemplate="Ngày %{x|%d/%m/%Y}<br>Công suất TB: %{y:.1f} kW<extra></extra>",
    ))
    fig.update_layout(
        title="Công suất trung bình theo ngày (kW)",
        xaxis_title="Thời gian", yaxis_title="Công suất TB (kW)",
        margin=dict(l=40, r=20, t=50, b=40),
    )
    return fig


def tao_kpi_card(tieu_de, gia_tri, mau):
    """Tạo một thẻ KPI (Bootstrap card) dạng chuỗi HTML."""
    return f"""
      <div class="col">
        <div class="card text-center shadow-sm h-100 border-0">
          <div class="card-body">
            <h6 class="card-subtitle mb-2 text-muted">{tieu_de}</h6>
            <p class="card-text fs-4 fw-bold" style="color:{mau};">{gia_tri}</p>
          </div>
        </div>
      </div>"""


def main():
    df = doc_du_lieu()
    kpi = tinh_kpi(df)

    # ----- Tạo 3 biểu đồ Plotly -----
    fig1 = bieu_do_duong_cong(df)
    fig2 = bieu_do_san_luong_thang(df)
    fig3 = bieu_do_cong_suat_theo_ngay(df)

    # Chuyển từng figure thành <div>. Chỉ biểu đồ ĐẦU nhúng plotly.js (include_plotlyjs=True),
    # các biểu đồ sau dùng chung thư viện đã nhúng (include_plotlyjs=False) để file gọn hơn.
    div1 = pio.to_html(fig1, include_plotlyjs=True, full_html=False)
    div2 = pio.to_html(fig2, include_plotlyjs=False, full_html=False)
    div3 = pio.to_html(fig3, include_plotlyjs=False, full_html=False)

    # ----- Hàng KPI cards -----
    kpi_cards = "".join([
        tao_kpi_card("Tổng bản ghi", f"{kpi['tong_ban_ghi']:,}", "#1F4E79"),
        tao_kpi_card("Công suất TB (kW)", f"{kpi['cong_suat_tb']:,.1f}", "#1F4E79"),
        tao_kpi_card("Tốc độ gió TB (m/s)", f"{kpi['toc_do_gio_tb']:,.2f}", "#1F4E79"),
        tao_kpi_card("Số điểm sự cố", f"{kpi['so_diem_su_co']:,}", "#E24A4A"),
        tao_kpi_card("Tổng giờ sự cố", f"{kpi['tong_gio_su_co']:,.1f}", "#E24A4A"),
    ])

    # ----- Ghép toàn bộ trang HTML -----
    html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Dashboard Phân tích SCADA - Tua bin gió</title>
  <!-- Bootstrap qua CDN -->
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
  <!-- 1. Navbar tiêu đề -->
  <nav class="navbar navbar-dark bg-primary shadow">
    <div class="container-fluid">
      <span class="navbar-brand mb-0 h1">Dashboard Phân tích SCADA - Tua bin gió</span>
    </div>
  </nav>

  <div class="container-fluid py-4">
    <!-- 2. Hàng KPI cards -->
    <div class="row row-cols-2 row-cols-md-5 g-3 mb-4">
      {kpi_cards}
    </div>

    <!-- 3. Ba biểu đồ Plotly tương tác -->
    <div class="row g-3">
      <div class="col-12">
        <div class="card shadow-sm"><div class="card-body">{div1}</div></div>
      </div>
      <div class="col-lg-6">
        <div class="card shadow-sm"><div class="card-body">{div2}</div></div>
      </div>
      <div class="col-lg-6">
        <div class="card shadow-sm"><div class="card-body">{div3}</div></div>
      </div>
    </div>

    <p class="text-muted text-center mt-4 mb-0">
      Điểm nghi sự cố = gió &gt; 5 m/s và công suất &lt; 50% công suất lý thuyết; mỗi điểm tương ứng 10 phút.
    </p>
  </div>
</body>
</html>"""

    # ----- Ghi ra file -----
    os.makedirs(os.path.dirname(HTML_OUTPUT), exist_ok=True)
    with open(HTML_OUTPUT, "w", encoding="utf-8") as f:
        f.write(html)

    # Thông báo sau khi tạo xong
    duong_dan = os.path.abspath(HTML_OUTPUT)
    print("Da tao dashboard HTML thanh cong!")
    print(f"  - File: {duong_dan}")
    print(f"  - Kich thuoc: {os.path.getsize(HTML_OUTPUT) / 1024:.1f} KB")
    print("  - Mo bang trinh duyet (khong can server): nhap dup vao file hoac keo tha vao trinh duyet.")


if __name__ == "__main__":
    main()
