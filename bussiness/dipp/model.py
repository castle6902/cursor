from pydantic import BaseModel


class DippFileTransfer(BaseModel):
    # 请求的类型，血常规：xcg, 生化分析：shfx
    type: str = ""  # 如果需要一个接口能够解析不同的文件，就需要把这个写进来，否则就需要点不同的按钮

    # 需要 dipp 系统传递过来，那一行的数据，就是序号
    record: int = 0


    # 要下的文件的路径的合集
    files_download_url: str = ""
    # 要下载的文件的名称合集
    files_download_name: str = ""

    # 附件的表单字段，这个就是我形成的结果文件传递到哪个字段上【可以固定下来】
    file_upload_form_field: str = ""  # 需要 dipp 系统传递过来，

    host: str = """https://dipptest.wuxiapptec.com"""  # 生产或者测试环境的 host， 【可以固定下来】

    # 空间id, 这个都是在同一个空间， 【可以固定下来】
    space_id: str = "72eb107c-8faf-4d28-bfc9-13e09746d425"

    # 表单 id,需要 dipp 系统传递过来， 返回给不同的表单
    form_id: str = "716d00a6-06d4-4fa5-993a-723b457439e5"  #

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

    def upload_file_url(self):
        """ 上传到 dipp 表单中文件 """

        base_url = ("/magicflu/service/s/{spaceId}/forms/{formId}/records/{recordId}/{"
                    "fieldName}/attachments?htmlFileInput")
        return self.host + base_url.format(spaceId=self.space_id, formId=self.form_id, recordId=self.record,
                                           fieldName=self.file_upload_form_field)



    """
    2 更新附件  PUT
    请求的Content-Type必须是multipart/form-data

    更新的接口不可用
    """
    def update_file_url(self):
        """ 更新附件文件 """
        # base_url = "/magicflu/service/s/{spaceId}/forms/{formId}/records/{recordId}/{fieldName}/attachments/r/{attachmentId}?htmlFileInput"
        base_url = "/magicflu/service/s/{spaceId}/forms/{formId}/records/{recordId}/{fieldName}/attachment/replace/{attachmentId}?htmlFileInput"
        # base_url = "/magicflu/service/s/{spaceId}/forms/{formId}/records/{recordId}/{fieldName}/attachments/r/{attachmentId}"
        return self.host + base_url.format(spaceId=self.space_id, formId=self.form_id, recordId=self.record,
                                           fieldName=self.file_upload_form_field, attachmentId=self.attachment_id)

    """
     3 删除附件 DELETE
    """

    def delete_file_url(self):
        """ 删除附件文件 """
        base_url = "/magicflu/service/s/{spaceId}/forms/{formId}/records/{recordId}/{fieldName}/attachments/{attachmentId}"
        return self.host + base_url.format(spaceId=self.space_id, formId=self.form_id, recordId=self.record,
                                           fieldName=self.file_upload_form_field, attachmentId=self.attachment_id)

    """
    4 下载附件 GET
    """

    def download_file_url(self):
        """ 删除附件文件 """
        base_url = "/magicflu/service/s/{spaceId}/forms/{formId}/records/{recordId}/{fieldName}/attachments/download/{attachmentId}"
        return self.host + base_url.format(spaceId=self.space_id, formId=self.form_id, recordId=self.record,
                                           fieldName=self.file_upload_form_field, attachmentId=self.attachment_id)
