# utils/csv_handler.py
# 职责：提供CSV文件的读取和写入功能


def read_csv(file_path, encoding="gbk", has_header=True, skip_empty=True):
    """
    读取CSV文件并返回数据

    参数:
        file_path (str): CSV文件路径
        encoding (str): 文件编码，默认gbk
        has_header (bool): 第一行是否为表头，默认True
        skip_empty (bool): 是否跳过空行，默认True

    返回:
        tuple: (header, rows)
            - header: 表头列表（若has_header=False则返回None）
            - rows: 数据行列表，每行为一个列表（字段已去除换行符）
    """
    rows = []
    header = None

    with open(file_path, "r", encoding=encoding) as f:
        lines = f.readlines()

    # 去除每行末尾换行符，并跳过空行（若skip_empty为True）
    cleaned_lines = []
    for line in lines:
        stripped = line.rstrip("\n").rstrip("\r")  # 兼容Windows换行
        if skip_empty and stripped == "":
            continue
        cleaned_lines.append(stripped)

    # 如果没有数据，直接返回空
    if not cleaned_lines:
        return header, rows

    # 处理表头
    if has_header:
        header = cleaned_lines[0].split(",")
        data_lines = cleaned_lines[1:]
    else:
        data_lines = cleaned_lines

    # 解析数据行
    for line in data_lines:
        fields = line.split(",")
        rows.append(fields)

    return header, rows


def write_csv(file_path, rows, header=None, encoding="gbk"):
    """
    将数据写入CSV文件

    参数:
        file_path (str): 输出文件路径
        rows (list): 数据行列表，每行为一个列表（字段值）
        header (list): 表头列表，若提供则写入第一行
        encoding (str): 文件编码，默认gbk
    """
    with open(file_path, "w", encoding=encoding) as f:
        # 写入表头（如果提供）
        if header is not None:
            f.write(",".join(header) + "\n")

        # 写入数据行
        for row in rows:
            # 将每个字段转为字符串（防止数字等非字符串类型报错）
            str_row = [str(item) for item in row]
            f.write(",".join(str_row) + "\n")


def read_csv1(file_path, encoding="gbk"):
    try:
        with open(file_path, "r", encoding=encoding) as f:
            list1 = f.readlines()
            print(len(list1))  # 行数
            zong = 0
            total_count = 0  # 数字总个数
            for line in list1:
                str_num = line.strip().split(",")  # csv文件读取的列表会有/n和逗号的问题
                int_num = [int(i) for i in str_num]
                zong += sum(int_num)
                total_count += len(int_num)
            if total_count == 0:
                pingjun = 0
                print("无有效数字")
            else:
                pingjun = zong / total_count
            print(pingjun)
    except FileNotFoundError:
        print("文件错误")
