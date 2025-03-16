import json
from rest_framework.response import Response


class JSONResponseMiddleware:
    """
    中间件用于拦截返回的 JSON 格式响应，
    并对其进行统一的包装：添加 status 和 message。
    根据返回数据是字典还是数组来设置不同的 key (`data` 或 `datas`).
    """

    def __init__(self, get_response):
        # 初始化时，获取到 Django 视图的响应处理函数
        self.get_response = get_response

    def __call__(self, request):
        # 在请求之前处理
        response = self.get_response(request)

        # 仅处理 DRF 的 Response 响应
        if isinstance(response, Response):
            # 获取 Response 对象的数据部分
            response_data = response.data

            # 判断返回数据是字典还是数组
            if isinstance(response_data, dict):
                response_data = {
                    "status": "success" if  200 <= response.status_code < 300 else "error",
                    "data": response_data,  # 使用 data 作为 key
                    "message": "Request was successful" if 200 <= response.status_code < 300 else "An error occurred"
                }
            elif isinstance(response_data, list):
                response_data = {
                    "status": "success" if 200 <= response.status_code < 300 else "error",
                    "datas": response_data,  # 使用 datas 作为 key
                    "message": "Request was successful" if 200 <= response.status_code < 300 else "An error occurred"
                }

            # 将处理后的数据设置回 response 并返回
            response.data = response_data
            response.content = json.dumps(response_data)

        return response
