import os
from datetime import datetime
from pathlib import Path
from typing import Any

import settings


class XCGConfig:

    def __init__(self):
        self.header_of_template = []
        self.time_uuid = datetime.now().strftime("%Y%m%d_%H%M%S")

    # template 上字段的顺序, 按照这个顺序写入到 excel 中
    # 处理链路  ：  file ==> template ==> dipp
    # 这个要从

    # header_of_template = [
    #     'Hematology', 'Sample name',
    #     "WBC", 'RBC', 'HGB', 'HCT', 'MCV', 'MCH', 'MCHC', 'CHCM', 'CH',
    #     'RDW-CV', 'HDW', 'PLT', 'MPV', '%NEUT', '%LYMP', '%MONO', '%EO',
    #     '%BASO', '%LUC', '%NRBC', '#NEUT', '#LYMP', '#MONO', '#EO',
    #     '#BASO', '#LUC', '#NRBC', '%Retic', '#Retic', 'MCVr', 'CHCMr', 'CHr'
    # ]

    header_map_file_to_template = {
        'ID': 'Sample name',
        'Date': 'Hematology',
        'RDW': 'RDW-CV',  # ==========
        '%LYMPH': '%LYMP',  # ==========
        '%EOS': '%EO',  # ==========
        '#LYMPH': '#LYMP',  # ==========
        '#EOS': '#EO',  # ==========
        '%RETIC': '%Retic',  # ==========
        '#RETIC': '#Retic',  # ==========
    }

    header_map_template_to_dipp = {
        "Hematology": "date",
        "Sample name": "samplename",
        "WBC": "wbc",
        "RBC": "rbc",
        "HGB": "hgb",
        "HCT": "hct",
        "MCV": "mcv",
        "MCH": "mch",
        "MCHC": "mchc",
        "CHCM": "chcm",
        "CH": "ch",
        "RDW-CV": "rdwcv",
        "HDW": "hdw",
        "PLT": "plt",
        "MPV": "mpv",
        "%NEUT": "neut",
        "%LYMP": "lymp",
        "%MONO": "mono",
        "%EO": "eo",  # ======
        "%BASO": "baso",
        "%LUC": "luc",
        "%NRBC": "nrbc",
        "#NEUT": "neut1",
        "#LYMP": "lymp1",
        "#MONO": "mono1",
        "#EO": "eo1",
        "#BASO": "baso1",
        "#LUC": "luc1",
        "#NRBC": "nrbc1",
        "%Retic": "retic",
        "#Retic": "retic1",
        "MCVr": "mcvr",
        "CHCMr": "chcmr",
        "CHr": "chr"
    }



