class XYNGConfig:

    header_map_file_to_template = {
        "日期": "Blood Coagulation",
        "条码编号": "Sample name",
        "APTT(Sec)": "APTT",
        "PT(Sec)": "PT",
        # "PT(INR)": "INSULIN",
        "TT(Sec)": "TT",
        "FIB(g/L)": "FIB"
    }

    header_map_template_to_dipp = {
        # "项目编码字段": "xiangmubianma11",
        # "项目编号字段": "xiangmubianhao",
        # "报告编码字段": "baogaobianma",
        # "时间点字段": "shijiandian",
        "Blood Coagulation": "date",
        "Sample name": "samplename",
        "APTT": "aptt",
        "PT": "pt",
        "TT": "tt",
        "FIB": "fib"
    }

