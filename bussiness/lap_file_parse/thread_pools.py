from concurrent.futures import ThreadPoolExecutor
import atexit

# # 线程池1：用于文件下载（5个线程）
# download_pool = ThreadPoolExecutor(
#     max_workers=5,
#     thread_name_prefix="download-"
# )

# 线程池2：用于数据解析（3个线程）
parse_pool = ThreadPoolExecutor(
    max_workers=15,
    thread_name_prefix="lap-parse-"
)

# # 线程池3：用于其他任务（2个线程）
# other_pool = ThreadPoolExecutor(
#     max_workers=2,
#     thread_name_prefix="other-"
# )


# 应用退出时关闭所有线程池
def shutdown_all_pools():
    # download_pool.shutdown(wait=True)
    parse_pool.shutdown(wait=True)
    # other_pool.shutdown(wait=True)


atexit.register(shutdown_all_pools)
