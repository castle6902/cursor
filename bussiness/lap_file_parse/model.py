import os
import threading
import uuid
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field
import requests

import settings
from bussiness.dipp.dipp_file_utils import UploadServerError, UploadNetworkError, FileUploadError
from common.utils.df_chain_utils import PandasChain
from logger import log


class LapFileType(Enum):
    # ==========================================
    # template
    # ==========================================
    Template = "template"
    # ==========================================
    # 生化解析的相关信息 - 生化电解质
    # ==========================================
    SHDJZ = "Clinical Chemistry"
    # ==========================================
    # 血常规的相关信息
    # ==========================================
    XCG = "Hematology"
    # ==========================================
    # 临床免疫的相关信息
    # ==========================================
    LCMY = "Clinical Immunoassay"
    # ==========================================
    # 血液凝固的关信息
    # ==========================================
    XYNG = "Coagulation"
    # ==========================================
    # 尿常规的相关信息
    # ==========================================
    NCG = "Urinalysis"
    # ==========================================
    # 空的
    # ==========================================
    EMPTY = ""


class FileInfo(BaseModel):
    # 类型
    type: LapFileType = LapFileType.EMPTY
    # 下载的 url
    download_url: str = ""
    # 下载后保存的路径
    save_path: str = ""
    # # 文件下载保存的目录
    # download_dir: str
    bianma: str = 'utf8'


class LapRequestModel(BaseModel):
    # template 中中列的顺序,
    # 处理链路  ：  file ==> template ==> dipp

    time_uuid: str = Field(
        default_factory=lambda: datetime.now().strftime("%Y%m%d_%H%M%S")
    )

    # 每次请求文件保存的位置
    file_download_dir: Path = ""

    # 需要 dipp 系统传递过来，那一行的数据，就是序号
    record: int = 0

    # 项目编号
    project_num: str

    # 项目编码
    project_code: str

    # 时间点
    time_point: str

    #
    host: str = "https://dipptest.wuxiapptec.com"  # 生产或者测试环境的 host， 【可以固定下来】

    # token
    token: str

    # 报告编码
    report_id: str

    # ==========================================
    # template
    # ==========================================

    # 模板文件下载的路径
    template_file_download_url: str

    # 模板文件上传到 dipp 中，保存的字段 excelbaogao
    template_upload_field_of_dipp: str = "excelbaogao"
    # spaceId=self.space_id, formId=self.form_id, recordId=self.record,
    #                                                    fieldName=self.template_file_upload_field
    template_space_id: str = "d665e561-06ad-4cee-99f5-213ccec2adde"  # 模板文件所在的空间名称
    template_form_id: str = "d7523909-acf0-4c2b-a160-5d924e513281"  # 模板文件所在的表单名称

    # ==========================================
    # 生化解析的相关信息 - 电化学
    # ==========================================
    clinical_chemistry_file_download_url: str
    # ==========================================
    # 血常规的相关信息
    # ==========================================
    hematology_file_download_url: str
    # ==========================================
    # 临床免疫的相关信息
    # ==========================================
    clinical_immunoassay_file_download_url: str
    # ==========================================
    # 血液凝固的相关信息
    # ==========================================
    blood_coagulation_file_download_url: str
    # ==========================================
    # 尿常规的相关信息
    # ==========================================
    urinalysis_file_download_url: str

    def init(self):
        self.file_download_dir = Path(
            os.path.join(str(settings.PARENT_PROJECT_PATH), "source_tmp", "lap_file_parse", self.time_uuid))

    # 这种解析模式是，指定文件的下载名称
    def parse_file_info_with_ext(self, file_url: str, type: LapFileType, file_ext: str = ".csv") -> list[FileInfo]:
        """
        针对每一个 url 解析出来所有的文件信息
        :param file_ext: 
        :param file_url:
        :param type:
        :return:
        """
        file_url = file_url.replace("$V(", "").replace(")$", "").strip()
        complete_file_download_urls = []
        if len(file_url) != 0:
            file_download_urls = file_url.split(',')

            # ===============================================================================
            # 文件下载的 url
            # ===============================================================================

            for file_path in file_download_urls:
                base_download_url = self.host + file_path
                file_info = FileInfo()
                file_info.type = type
                file_info.download_url = base_download_url
                file_info.save_path = Path(
                    os.path.join(self.file_download_dir, f"{str(type)}_{str(uuid.uuid4())}{file_ext}"))
                complete_file_download_urls.append(file_info)

        return complete_file_download_urls

    def parse_all_file_url(self) -> list[FileInfo]:
        """
        解析获取到的 url, 然后规范为
        res: {
         type: {
            download: []
            downloadPath: []
            csv- url
            }
        }
        :return:
        """
        res = []
        self.file_download_dir.mkdir(parents=True, exist_ok=True)  # parents=True 创建多级目录
        # ==============================================================
        # template 模板, 除了 template 是 xlsx 文件，其他的都是 csv 文件
        # ==============================================================
        if len(self.template_file_download_url) == 0:
            raise Exception("模板不能为空，否则无法保存写入的信息")
        else:
            template_file_infos = self.parse_file_info_with_ext(self.template_file_download_url,
                                                                type=LapFileType.Template, file_ext=".xlsx")
            res = res + template_file_infos
        # ==========================================
        # 生化解析的相关信息 - 生化电解质
        # ==========================================
        if len(self.clinical_chemistry_file_download_url) != 0:
            hxdjz_file_infos = self.parse_file_info_with_ext(self.clinical_chemistry_file_download_url,
                                                             type=LapFileType.SHDJZ)
            res = res + hxdjz_file_infos
        # ==========================================
        # 血常规的相关信息
        # ==========================================
        if len(self.hematology_file_download_url) != 0:
            xcg_file_infos = self.parse_file_info_with_ext(self.hematology_file_download_url, type=LapFileType.XCG,
                                                           file_ext=".xlsx")
            res = res + xcg_file_infos
        # ==========================================
        # 临床免疫的相关信息
        # ==========================================
        if len(self.clinical_immunoassay_file_download_url) != 0:
            lcmy_file_infos = self.parse_file_info_with_ext(self.clinical_immunoassay_file_download_url,
                                                            type=LapFileType.LCMY)
            res = res + lcmy_file_infos
        # ==========================================
        # 血液凝固的相关信息
        # ==========================================

        if len(self.blood_coagulation_file_download_url) != 0:
            xyng_file_infos = self.parse_file_info_with_ext(self.blood_coagulation_file_download_url,
                                                            type=LapFileType.XYNG)
            res = res + xyng_file_infos
        # ==========================================
        # 尿常规的相关信息
        # ==========================================

        if len(self.urinalysis_file_download_url) != 0:
            ncg_file_infos = self.parse_file_info_with_ext(self.urinalysis_file_download_url, type=LapFileType.NCG,
                                                           file_ext=".xlsx")
            res = res + ncg_file_infos

        return res

    def upload_template_file_to_dipp(self):
        base_url = (
            "/magicflu/service/s/{spaceId}/forms/{formId}/records/{recordId}/{fieldName}/attachments?htmlFileInput")
        template_file_upload_to_dipp_url = self.host + base_url.format(spaceId=self.template_space_id,
                                                                       formId=self.template_form_id,
                                                                       recordId=self.record,
                                                                       fieldName=self.template_upload_field_of_dipp)

        return template_file_upload_to_dipp_url

    def upload_data_url_to_SHDJZ(self):
        shdjz_data_upload_url: str = "/magicflu/service/s/jsonv2/d665e561-06ad-4cee-99f5-213ccec2adde/forms/cd96ea0d-2542-43e5-a829-089b2fd69a71/bulk/records"
        return self.host + shdjz_data_upload_url

    def upload_data_url_to_XCG(self):
        xcg_data_upload_url: str = "/magicflu/service/s/jsonv2/d665e561-06ad-4cee-99f5-213ccec2adde/forms/a6c461f1-8550-4fea-b93c-5659ed8e1d89/bulk/records"
        return self.host + xcg_data_upload_url

    def upload_data_url_to_LCMY(self):
        lcmy_data_upload_url: str = "/magicflu/service/s/jsonv2/d665e561-06ad-4cee-99f5-213ccec2adde/forms/c45b25d6-aba4-4179-bd95-ce2d45181b3b/bulk/records"
        return self.host + lcmy_data_upload_url

    def upload_data_url_to_XYNG(self):
        xyng_data_upload_url: str = "/magicflu/service/s/jsonv2/d665e561-06ad-4cee-99f5-213ccec2adde/forms/198993cc-417b-4783-ba50-18ccc07c17de/bulk/records"
        return self.host + xyng_data_upload_url

    def upload_data_url_to_NCG(self):
        ncg_data_upload_url: str = "/magicflu/service/s/jsonv2/d665e561-06ad-4cee-99f5-213ccec2adde/forms/ae065ec7-2691-4894-9bca-9090a31b72ce/bulk/records"
        return self.host + ncg_data_upload_url

    def upload_template_file(self, template_save_path):

        try:
            # 获取文件名
            file_name = os.path.basename(template_save_path)

            # 读取文件内容
            with open(template_save_path, 'rb') as file:
                files = {
                    'file': (file_name, file)
                }

                headers = {
                    "Authorization": f"Bearer {self.token}",
                    # "Content-Type": "multipart/form-data"
                }

                base_url = (
                    "/magicflu/service/s/{spaceId}/forms/{formId}/records/{recordId}/{fieldName}/attachments?htmlFileInput")
                template_file_upload_to_dipp_url = self.host + base_url.format(spaceId=self.template_space_id,
                                                                               formId=self.template_form_id,
                                                                               recordId=self.record,
                                                                               fieldName=self.template_upload_field_of_dipp)

                # 发送请求
                response = requests.post(
                    # response = requests.put(
                    url=template_file_upload_to_dipp_url,
                    files=files,
                    # data=data,
                    headers=headers,
                    timeout=30000  # 设置超时时间
                )

            log.info(
                f"\n=== 向 dipp 上传 excel ，请求响应 ===\n"
                f"URL: {response.request.url}\n"
                f"状态码: {response.status_code}\n"
                f"耗时: {response.elapsed.total_seconds():.2f}s\n"
                f"响应头: {dict(response.headers)}\n"
                f"响应体: {response.text[:500] + ('...' if len(response.text) > 500 else '')}"
            )
        except requests.exceptions.Timeout:
            error_msg = f"文件上传超时: {template_save_path}"
            log.error(error_msg)
            raise UploadNetworkError(error_msg)
        except requests.exceptions.ConnectionError:
            error_msg = f"网络连接错误: {template_save_path}"
            log.error(error_msg)
            raise UploadNetworkError(error_msg)
        except UploadServerError:
            # 已处理的服务器错误，直接向上传递
            raise
        except Exception as e:
            # 捕获其他未预料的异常，包装为业务异常
            error_msg = f"文件上传失败: {str(e)}"
            log.error(f"{error_msg}, 文件: {template_save_path}")
            raise FileUploadError(error_msg)


# class DippFileTransfer(BaseModel):
class LapFileTransfer(BaseModel):
    # 需要 dipp 系统传递过来，那一行的数据，就是序号
    record: int = 0

    # 每一次请求过来的时候，获取当前的时间戳，方便进行文件标注
    time_uuid: str = ""

    # 请求的类型，血常规：xcg, 生化分析：shfx
    type: str = ""  # 如果需要一个接口能够解析不同的文件，就需要把这个写进来，否则就需要点不同的按钮

    host: str = "https://dipptest.wuxiapptec.com"  # 生产或者测试环境的 host， 【可以固定下来】

    # 空间id, 这个都是在同一个空间， 【可以固定下来】
    space_id: str = "72eb107c-8faf-4d28-bfc9-13e09746d425"

    # 表单 id,需要 dipp 系统传递过来， 返回给不同的表单
    form_id: str = "716d00a6-06d4-4fa5-993a-723b457439e5"  #

    # 需要 dipp 系统传递过来，那一行的数据，就是序号
    record: int = 0

    # 要下的文件的路径的合集
    files_download_url: str = ""

    # 要下载的文件的名称合集
    files_download_name: str = ""

    # 模板文件下载的 url
    template_file_download_url: str = ""

    # 模板文件上传到 dipp 中的字段
    template_file_upload_field: str = ""

    # 附件的表单字段，这个就是我形成的结果文件传递到哪个字段上【可以固定下来】
    file_upload_form_field: str = ""  # 需要 dipp 系统传递过来，

    # 想的是，python 程序，不做任何的账号密码记录，所有记录都放到 ESB 程序中
    token: str = ""  # 需要传递过来，这个由 dipp 这样子的话，是不是方便切换到生产或者测试环境，

    # 这个参数暂时用不到， 下载的时候，使用的是全路径下载的
    attachment_id: str = ""

    """
        上传附件
        方式： post
        url： /magicflu/service/s/{spaceId}/forms/{formId}/records/{recordId}/{fieldName}/attachments?htmlFileInput
        要求： 请求的Content-Type必须是multipart/form-data

        """

    def template_file_upload_to_dipp_url(self):
        """ 上传到 dipp 表单中文件 """

        base_url = (
            "/magicflu/service/s/{spaceId}/forms/{formId}/records/{recordId}/{fieldName}/attachments?htmlFileInput")
        return self.host + base_url.format(spaceId=self.space_id, formId=self.form_id, recordId=self.record,
                                           fieldName=self.template_file_upload_field)

    """
    4 下载附件 GET
    """

    def parse_data_file_url(self):
        """
        用来获取所有的数据文件的下载地址
        $V(/magicflu/service/s/d665e561-06ad-4cee-99f5-213ccec2adde/forms/7608fe97-9b18-4641-b788-79f25ea205dd/records/1/yuanshishuju/attachments/download/429273f3-120e-4216-9951-ab5551a1b263,/magicflu/service/s/d665e561-06ad-4cee-99f5-213ccec2adde/forms/7608fe97-9b18-4641-b788-79f25ea205dd/records/1/yuanshishuju/attachments/download/6b8902ee-0cf9-4e49-9ab4-4420f9a8ac9d,/magicflu/service/s/d665e561-06ad-4cee-99f5-213ccec2adde/forms/7608fe97-9b18-4641-b788-79f25ea205dd/records/1/yuanshishuju/attachments/download/60a9f5e4-550f-470f-8885-c7d81cbf3775)$"
        :param file_url: 就是
        :return:
        """
        file_download_urls = self.files_download_url.replace("$V(", "").replace(")$", "").split(',')

        # ===============================================================================
        # 文件下载的 url
        # ===============================================================================
        complete_file_download_urls = []
        for file_path in file_download_urls:
            complete_file_download_urls.append(self.host + file_path)

        return complete_file_download_urls

    def parse_template_file_url(self):
        """
        用来获取模板的下载地址
        $V(/magicflu/service/s/d665e561-06ad-4cee-99f5-213ccec2adde/forms/7608fe97-9b18-4641-b788-79f25ea205dd/records/1/yuanshishuju/attachments/download/429273f3-120e-4216-9951-ab5551a1b263,/magicflu/service/s/d665e561-06ad-4cee-99f5-213ccec2adde/forms/7608fe97-9b18-4641-b788-79f25ea205dd/records/1/yuanshishuju/attachments/download/6b8902ee-0cf9-4e49-9ab4-4420f9a8ac9d,/magicflu/service/s/d665e561-06ad-4cee-99f5-213ccec2adde/forms/7608fe97-9b18-4641-b788-79f25ea205dd/records/1/yuanshishuju/attachments/download/60a9f5e4-550f-470f-8885-c7d81cbf3775)$"
}
        :return:
        """

        file_download_url = self.template_file_download_url.replace("$V(", "").replace(")$", "")

        # ===============================================================================
        # 文件下载的 url
        # ===============================================================================

        return self.host + file_download_url

    def fetch_data_file_save_path(self, save_dir):
        """
        如果需要吧文件下载下来，然后再进行解析，这个就是文件下载下来保存的位置
        :param save_dir:
        :return:
        """

        # $V(类别1.csv,类别2.csv,类别3.csv)$
        download_file_names = []
        download_file_names = self.files_download_name.replace("$V(", "").replace(")$", "").split(',')
        for i, download_file_name in enumerate(download_file_names):
            download_file_names[i] = os.path.join(save_dir, download_file_name)

        return download_file_names
