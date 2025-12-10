import chardet


def detect_file_encoding(file_path, sample_size=100):
    """
    检测文件的编码方式

    参数:
        file_path: 文件路径
        sample_size: 用于检测的样本大小（字节），越大越准确但速度稍慢
    返回:
        推测的编码方式（如 'utf-8', 'GB2312', 'ISO-8859-1' 等）
    """
    with open(file_path, 'rb') as f:
        # 读取样本数据（避免读取整个大文件）
        raw_data = f.read(sample_size)

    # 检测编码
    result = chardet.detect(raw_data)
    encoding = result['encoding']
    confidence = result['confidence']  # 可信度（0-1）

    print(f"推测编码: {encoding} (可信度: {confidence:.2f})")
    return encoding