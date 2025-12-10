from datetime import datetime

from fastapi import APIRouter

from bussiness.lap_file_parse.config_of_djz import DJZConfig
from bussiness.lap_file_parse.config_of_xcg import XCGConfig
from bussiness.lap_file_parse.model import LapFileTransfer, LapRequestModel
from bussiness.lap_file_parse.service.gateParse import parse_file


from logger import log
from common.APIResponse import ApiResponse

router = APIRouter(
    prefix="/lap",
    tags=["LAP自动化临检数据整理"]
)

"""
目前的模式不能进行文件的处理，用处上传文件，然后我处理文件，把处理过的数据送回到 dipp 中
"""


#
# # 血常规
# @router.post("/xcg/fileParse")
# def parse_xuechanggui_excel_file(request: LapFileTransfer):
#     try:
#         xcg_config = XcgConfig()
#         request.time_uuid = xcg_config.time_uuid
#         request.host = xcg_config.download_data_file_host
#         request.space_id = xcg_config.download_data_file_space_id
#         request.form_id = xcg_config.download_data_file_form_id
#         request.template_file_upload_field = xcg_config.template_file_upload_field
#
#         # /magicflu/service/s/jsonv2/d665e561-06ad-4cee-99f5-213ccec2adde/forms/a6c461f1-8550-4fea-b93c-5659ed8e1d89/records
#
#         xcg_parse_excel_file(request, xcg_config)
#         # return ApiResponse.fail().with_message("调度成功")
#         return ApiResponse.success().with_message("血常规接口调度成功")
#     except Exception as e:
#         log.error(f"血常规接口调度异常， ${e}")
#         return ApiResponse.fail().with_message(f"血常规接口调度异常， ${e}")
#
#
# # 化学电解质
# @router.post("/hxdjz/fileParse")
# def parse_dianjiezhi_csv_file(request: LapFileTransfer):
#     # try:
#     #
#     #     djz_config = DJZConfig()
#     #     request.time_uuid = djz_config.time_uuid
#     #     request.host = djz_config.download_data_file_host
#     #     request.space_id = djz_config.download_data_file_space_id
#     #     request.form_id = djz_config.download_data_file_form_id
#     #     request.template_file_upload_field = djz_config.template_file_upload_field
#     #
#     #
#     #     djz_parse_csv_file(request, djz_config)
#     #     return ApiResponse.success().with_message("化学电解质接口调度成功")
#     # except Exception as e:
#     #     log.error(f"化学电解质调度异常， ${e}")
#     #     return ApiResponse.fail().with_message(f"化学电解质接口调度异常， ${e}")
#     djz_config = DJZConfig()
#     request.time_uuid = djz_config.time_uuid
#     request.host = djz_config.download_data_file_host
#     request.space_id = djz_config.download_data_file_space_id
#     request.form_id = djz_config.download_data_file_form_id
#     request.template_file_upload_field = djz_config.template_file_upload_field
#
#
#     return ApiResponse.success().with_message("化学电解质接口调度成功")

# 血常规
@router.post("/csv_parser")
def parse_xuechanggui_excel_file(request_body: LapRequestModel):
    try:
        request_body.init()
        log.info(request_body)
        parse_file(request_body)
        return ApiResponse.success().with_message("血常规接口调度成功")
    except Exception as e:
        log.error(f"血常规接口调度异常， ${e}")
        return ApiResponse.fail().with_message(f"血常规接口调度异常， ${e}")


@router.post("/hxdjz/fileParse")
def test_pdms():
    pass
