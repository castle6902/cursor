class ApiResponse:
    def __init__(self, code: int, message: str, data: any = None, success=True):
        self.code = code  # 默认 success
        self.message = message
        self.success = success
        self.data = data

    @staticmethod
    def success():
        """设置为成功状态"""
        # cls.is_success = True
        # cls.code = 200
        # cls.message = "操作成功"
        # return cls  # 返回 self 以支持链式调用
        return ApiResponse(code=200, message="操作成功", data=None)

    @staticmethod
    def fail():
        """设置为失败状态"""
        return ApiResponse(code=500, message="操作异常", data=None, success=False)

    def with_code(self, code):
        """自定义状态码"""
        self.code = code
        return self  # 返回 self 以支持链式调用

    def with_message(self, message):
        """自定义消息"""
        self.message = message
        return self  # 返回 self 以支持链式调用

    def with_data(self, data):
        """填充返回数据"""
        self.data = data
        return self  # 返回 self 以支持链式调用

    def build(self):
        """构建最终返回的字典"""
        return {
            "code": self.code,
            "message": self.message,
            "data": self.data,
            "success": self.success  # 可选：是否返回 success 字段
        }
