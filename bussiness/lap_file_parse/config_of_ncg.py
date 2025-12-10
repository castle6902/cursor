class NCGConfig:
    header_map_file_to_template = {
        "日期": "Urinalysis",
        "姓名": "Sample name",

        # "A/C": "A/C",
        # "ALB": "ALB",
        # "BIL": "BIL",
        # "BLD": "BLD",
        # "CLOUD": "CLOUD",
        # "COLOR": "COLOR",
        # "CRE": "CRE",
        # "GLU": "GLU",
        # "KET": "KET",
        # "LEU": "LEU",
        # "NIT": "NIT",
        # "P/C": "P/C",
        # "PH": "PH",
        # "URO": "URO",
        # "S.G": "S.G",
        #  "PRO": "PRO"  # 空键对应"PRO"
    }

    header_map_template_to_dipp = {
        # 这几个在推送的时候才会添加
        # "项目编号字段": "xiangmubianhao",
        # "项目编码字段": "xiangmubianma11",
        # "报告编码字段": "baogaobianma",
        # "时间点字段": "shijiandian",
        "Urinalysis": "date",
        "Sample name": "samplename",
        "A/C": "ac",
        "ALB": "alb",
        "BIL": "bil",
        "BLD": "bld",
        "CLOUD": "cloud",
        "COLOR": "color",
        "CRE": "cre",
        "GLU": "glu",
        "KET": "ket",
        "LEU": "leu",
        "NIT": "nit",
        "P.C": "pc",
        "PH": "ph",
        "PRO": "pro",
        "URO": "uro",
        "S.G": "sg"
    }
