# thread_pool.py
from concurrent.futures import ThreadPoolExecutor
import atexit  # 用于应用退出时关闭线程池


class GlobalThreadPool:
    _instance = None  # 类级变量，存储唯一实例

    def __new__(cls, *args, **kwargs):
        # 确保只创建一个实例
        if not cls._instance:
            cls._instance = super().__new__(cls)
            # 初始化线程池（仅首次创建实例时执行）
            cls._instance.executor = ThreadPoolExecutor(
                max_workers=10,  # 线程数，根据需求调整（IO密集型可设大些）
                thread_name_prefix="global-thread-"  # 线程名前缀，方便日志调试
            )
            # 注册退出钩子：应用关闭时自动关闭线程池，释放资源
            atexit.register(cls._instance.executor.shutdown, wait=True)
        return cls._instance

    def get_executor(self):
        """提供线程池执行器的访问接口"""
        return self._instance.executor


# 初始化单例实例（应用启动时执行一次，后续导入直接使用此实例）
global_thread_pool = GlobalThreadPool()
