import concurrent.futures
from typing import Callable, List, Any


class ThreadPoolUtil:
    """线程池工具类，采用单例模式确保全局只有一个线程池实例"""

    _instance = None
    _executor = None

    def __new__(cls, max_workers: int = 10):
        """创建单例实例"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # 初始化线程池，默认最大工作线程数为 10
            cls._executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
        return cls._instance

    @classmethod
    def submit_tasks(cls, tasks: List[Callable]) -> List[Any]:
        """
        提交多个任务到线程池并获取结果

        参数:
            tasks: 任务列表，每个任务是一个可调用对象

        返回:
            任务执行结果的列表，按提交顺序返回
        """
        if not tasks:
            return []

        # 提交所有任务
        futures = [cls._executor.submit(task) for task in tasks]

        # 按提交顺序获取结果
        results = []
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                # 可以根据需要处理异常，这里简单打印
                print(f"任务执行出错: {str(e)}")
                # 可以选择将异常也作为结果返回，或者忽略
                results.append(None)

        return results

    @classmethod
    def shutdown(cls, wait: bool = True) -> None:
        """
        关闭线程池

        参数:
            wait: 是否等待所有任务完成后再关闭
        """
        if cls._executor:
            cls._executor.shutdown(wait=wait)
            cls._instance = None
            cls._executor = None


