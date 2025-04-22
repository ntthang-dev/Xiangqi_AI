import unittest
import time
from src.board.board import BanCo # Bàn cờ (棋盘 - Qípán)
from src.search.alphabeta import AlphaBeta

class TestPerformanceZh(unittest.TestCase):
    def test_shendu_3(self):
        """Test thời gian với độ sâu 3 (深度测试 - Shēndù Cèshì)"""
        ban_co = BanCo() # Khởi tạo bàn cờ
        engine = AlphaBeta(shendu=3)
        
        start_time = time.perf_counter()
        nuoc_di, _ = engine.tim_nuoc_di(ban_co)
        elapsed = time.perf_counter() - start_time
        
        self.assertLess(elapsed, 5.0, "Độ trễ phải <5s cho độ sâu 3")

    def test_shuangpao_lianhuan(self):
        """Test thế trận Song Pháo liên hoàn (双炮连环 - Shuāng Pào Liánhuán)"""
        ban_co = BanCo.setup_tu_vi_tri("shuangpao") # Setup từ vị trí có sẵn
        engine = AlphaBeta(shendu=4)
        
        start = time.perf_counter()
        engine.tim_nuoc_di(ban_co)
        print(f"Thời gian xử lý Song Pháo: {time.perf_counter() - start:.2f}s")
