import sys
import tracemalloc
from src.engine import AIEngine
from src.board.board import BanCo

def test_tailen_memory():
    """Kiểm tra bộ nhớ khi tải nhiều bàn cờ"""
    tracemalloc.start()
    
    # Ghi nhận trạng thái bộ nhớ ban đầu
    snapshot1 = tracemalloc.take_snapshot()
    
    # Tạo 100 bàn cờ
    danh_sach_ban_co = [BanCo() for _ in range(100)]
    
    # Ghi nhận sau khi tạo
    snapshot2 = tracemalloc.take_sapshot()
    
    # Phân tích khác biệt
    stats = snapshot2.compare_to(snapshot1, 'lineno')
    print("[Memory] Tiêu hao cho 100 bàn cờ:", stats[0].size_diff/1024, "KB")

def test_engine_memory():
    """Kiểm tra bộ nhớ cho Engine AI"""
    engine = AIEngine()
    print("[Memory] Kích thước Engine:", sys.getsizeof(engine), "bytes")
    
    # Test memory khi tính nước đi
    tracemalloc.start()
    before = tracemalloc.take_snapshot()
    
    engine.chay(BanCo())
    
    after = tracemalloc.take_snapshot()
    stats = after.compare_to(before, 'lineno')
    print("[Memory] Tiêu hao khi tính nước:", stats[0].size_diff/1024, "KB")

if __name__ == "__main__":
    test_tailen_memory()
    test_engine_memory()