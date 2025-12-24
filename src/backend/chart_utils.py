import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

# Cấu hình để in được tiếng Việt trên Console
sys.stdout.reconfigure(encoding='utf-8')

# Tìm đường dẫn file log
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
LOG_FILE_PATH = os.path.join(project_root, "ai_performance_log.csv")

def show_total_time_comparison():
    print(f"Đang đọc log từ: {LOG_FILE_PATH}")
    
    if not os.path.exists(LOG_FILE_PATH):
        print("[LỖI] Chưa có file log. Hãy chơi 1 ván trước.")
        input("Bấm Enter để thoát...")
        return

    try:
        # 1. Đọc dữ liệu
        df = pd.read_csv(LOG_FILE_PATH)
        if df.empty:
            print("[INFO] File log rỗng.")
            return

        # 2. Làm sạch dữ liệu số
        if 'Depth' in df.columns and 'BoardSize' in df.columns:
            df['Depth'] = pd.to_numeric(df['Depth'], errors='coerce')
            df['BoardSize'] = pd.to_numeric(df['BoardSize'], errors='coerce')
            df['Time(s)'] = pd.to_numeric(df['Time(s)'], errors='coerce')
            df = df.dropna(subset=['Depth', 'BoardSize', 'Time(s)'])
        else:
            print("[CẢNH BÁO] File log thiếu cột. Hãy xóa file csv cũ đi.")
            return

        # --- [QUAN TRỌNG] LỌC THEO BÀN CỜ VỪA CHƠI ---
        # Lấy kích thước của dòng dữ liệu cuối cùng (Ván vừa xong)
        last_size = df['BoardSize'].iloc[-1]
        
        print(f"\n>> Đang hiển thị thống kê cho bàn cờ: {int(last_size)}x{int(last_size)}")
        print("(Dữ liệu của các kích thước khác sẽ được ẩn đi để đảm bảo chính xác)\n")

        # Chỉ giữ lại dữ liệu của size này
        df_filtered = df[df['BoardSize'] == last_size]
        # ---------------------------------------------

        # 3. Tính trung bình thời gian theo Depth (trên dữ liệu đã lọc)
        stats = df_filtered.groupby('Depth')['Time(s)'].mean().reset_index()
        stats = stats.sort_values(by='Depth')

        # In ra console để kiểm tra
        print(stats)

        # 4. Vẽ biểu đồ
        plt.style.use('ggplot')
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Vẽ cột
        bars = ax.bar(stats['Depth'].astype(str), stats['Time(s)'], color='#8e44ad', width=0.6)

        # Tiêu đề tự động thay đổi theo size
        ax.set_title(f'TỐC ĐỘ SUY NGHĨ TRUNG BÌNH (SIZE {int(last_size)}x{int(last_size)})', fontsize=14, fontweight='bold')
        ax.set_xlabel('Depth (Độ khó)', fontsize=12)
        ax.set_ylabel('Thời gian (Giây)', fontsize=12)
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        # Hiện số liệu
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.4f}s',
                    ha='center', va='bottom', fontweight='bold', color='black')

        plt.tight_layout()
        plt.show(block=True)

    except Exception as e:
        print(f"[LỖI CHART] {e}")
        import traceback
        traceback.print_exc()
        input("Bấm Enter để thoát...")

if __name__ == "__main__":
    show_total_time_comparison()