class LCMYConfig:
    header_map_file_to_template = {
        "A_Date": "Clinical Immunoassay",
        "S_ID": "Sample name",
        "43": "CK-MB",
        "44": "TP1NP",
        # "120": "INSULIN",
        "120": "INS",
        "127": "CROSSL",
        "302": "FT4",
        "574": "PBNPX",
        "627": "TSH",
        "ERROR": "error"
    }

    header_map_template_to_dipp = {
        # "项目编码字段": "xiangmubianma11",
        # "项目编号字段": "xiangmubianhao",
        # "报告编码字段": "baogaobianma",
        # "时间点字段": "shijiandian",
        "Clinical Immunoassay": "date",
        "Sample name": "samplename",
        "CK-MB": "ckmb",
        "TP1NP": "tp1np",
        "INS": "ins",
        "CROSSL": "crossl",
        "FT4": "ft4",
        "PBNPX": "pbnpx",
        "TSH": "tsh",
        "ERROR": "error"
    }
