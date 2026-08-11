"""20X 玻片拼接核心 demo:重叠区相位相关对齐 + 坐标映射。

纯 numpy,无第三方图像库依赖。生成两张带重叠的合成图,
用相位相关求出真实偏移,拼接,并输出每像素→物理坐标映射。

运行:python stitch_demo.py
ponytail: 单线程、两图拼接。多图/实时流水线/金字塔切片待验证后加。
"""
import numpy as np

# 像素→物理坐标标定参数(真实设备需用标尺片实测)
PIXEL_UM = 0.5      # 每个像素对应多少微米
OVERLAP_PX = 40     # 相邻图重叠像素(设计步长决定)

def synth_tile(seed, size=256):
    """生成带唯一标记的合成图,模拟 20X 细胞视野。"""
    rng = np.random.default_rng(seed)
    tile = rng.random((size, size)) * 0.2 + 0.1
    for _ in range(rng.integers(20, 40)):          # 随机"细胞"
        y, x = rng.integers(10, size - 10, 2)
        r = rng.integers(2, 6)
        yy, xx = np.ogrid[-r:r, -r:r]
        tile[yy + y, xx + x] += 0.7 * np.exp(-(yy**2 + xx**2) / (2 * r))
    return tile

def phase_corr_offset(a, b):
    """相位相关求 b 相对 a 的 (dy, dx) 平移,亚像素。"""
    fa, fb = np.fft.fft2(a), np.fft.fft2(b)
    cross = fa * np.conj(fb)
    cc = np.fft.ifft2(cross / (np.abs(cross) + 1e-10))
    peak = np.unravel_index(np.argmax(np.abs(cc)), cc.shape)
    h, w = a.shape
    dy = (peak[0] + h // 2) % h - h // 2
    dx = (peak[1] + w // 2) % w - w // 2
    return dy, dx

def stitch(tiles, overlap_px):
    """沿 X 方向拼接 tile 序列,返回拼接图 + 每像素物理坐标 X 映射。"""
    assert overlap_px < min(t.shape[1] for t in tiles)
    offsets = [0.0]                      # 每个 tile 左边缘在拼接图里的 X
    for i in range(1, len(tiles)):
        dy, dx = phase_corr_offset(tiles[i - 1][:, -2 * overlap_px:],
                                   tiles[i][:, :2 * overlap_px])
        # 用重叠区测出的位移换算出 tile 起点(忽略 Y 向,演示只拼一行)
        offsets.append(offsets[-1] + tiles[i].shape[1] - (overlap_px - dx))
    total_w = int(offsets[-1] + tiles[-1].shape[1])
    h = tiles[0].shape[0]
    canvas = np.zeros((h, total_w))
    for t, off in zip(tiles, offsets):
        canvas[:, int(off):int(off) + t.shape[1]] = t
    # 坐标映射:X 像素 → 物理微米(每像素 * 标定)
    phys_x = np.arange(total_w) * PIXEL_UM
    return canvas, offsets, phys_x

def main():
    # 模拟两次拍照:X 方向移动(size - overlap),有重叠
    size = 256
    t1, t2 = synth_tile(1), synth_tile(2)
    shift = size - OVERLAP_PX
    t2_shifted = np.roll(t2, shift, axis=1)      # 物理上平移后拍的第二张
    t2_shifted[:, :shift] = 0                     # 左侧本无内容,模拟视野外
    t2_shifted = np.roll(t2_shifted, shift, axis=1)  # 再拼一步演示两图重叠
    t1b = t1.copy(); t1b[:, :shift] = 0
    canvas, offsets, phys_x = stitch([t1b, t2_shifted], OVERLAP_PX)

    # 自检:估计的位移应接近真实 shift
    dy, dx = phase_corr_offset(t1b[:, -2 * OVERLAP_PX:], t2_shifted[:, :2 * OVERLAP_PX])
    est_shift = size - (OVERLAP_PX - dx)
    assert abs(est_shift - shift) <= 2, f"对齐误差过大: est={est_shift}, real={shift}"
    assert canvas.shape[1] == shift + size, f"拼接宽度错: {canvas.shape[1]} vs {shift + size}"
    print(f"对齐 OK: 估计位移={est_shift}, 真实={shift}")
    print(f"拼接尺寸: {canvas.shape[0]}x{canvas.shape[1]}")
    print(f"第二张 tile 起点 X={int(offsets[1])}px → 物理 {offsets[1]*PIXEL_UM:.1f}µm")
    print("坐标映射示例: 像素X=[0,100,200] → 物理µm=", [round(x,1) for x in phys_x[[0,100,200]]])

if __name__ == "__main__":
    main()
