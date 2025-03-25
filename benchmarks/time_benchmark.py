import argparse
import time
from src.engine import AIEngine
from src.board.board import BanCo

def benchmark_hethong():
    """Chạy benchmark hệ thống với các test case tiêu chuẩn"""
    test_cases = [
        ("Khai cuộc", "kaiju"), # Khai cuộc (开局)
        ("Trung cuộc", "zhongpan"), # Trung cuộc (中局)
        ("Tàn cuộc", "canju") # Tàn cuộc (残局)
    ]

    for ten, loai in test_cases:
        ban_co = BanCo.setup_tu_vi_tri(loai)
        engine = AIEngine(shendu=4)
        
        start = time.perf_counter()
        engine.chay(ban_co)
        thoi_gian = time.perf_counter() - start
        
        print(f"[{ten}] Độ sâu 4: {thoi_gian:.2f}s")

def benchmark_dacbiet():
    """Các thế cờ đặc biệt (特殊棋局 - Tèshū Qíjú)"""
    # Test thế "Song Xa Vấn Sát" (双车问杀 - Shuāng Jū Wèn Shā)
    ban_co = BanCo.setup_tu_vi_tri("shuangche")
    engine = AIEngine(shendu=5)
    
    start = time.perf_counter()
    engine.chay(ban_co)
    print(f"Song Xa Vấn Sát: {time.perf_counter() - start:.2f}s")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Benchmark AI Cờ Tướng')
    parser.add_argument('--loai', type=str, default='hethong', help='Loại benchmark (hethong/dacbiet)')
    args = parser.parse_args()
    
    if args.loai == 'hethong':
        benchmark_hethong()
    else:
        benchmark_dacbiet()