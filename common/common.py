from rest_framework.views import APIView
from rest_framework.response import Response

class TaskView(APIView):
    # APIView를 상속받은 TodoView
    # 헤더에 있는 user_id
    user_id = ""
    version = ""

    # dispatch는 클라이언트로 들어온 요청이 어떤 요청(get or post)인지 구분해서 처리하도록 분기해주는 녀석
    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.headers.get('id', False)
        self.version = request.headers.get('version', '1.0')

        # 부모 클래스 dispatch 실행
        return super(TaskView, self).dispatch(request, *args, **kwargs)


# 클라이언트 응답을 정해진 포맷으로 줘야 클라이언트 개발자가 사용하기 편리
# 응답 또한 공통영역에 정의
def CommonResponse(result_code, result_msg, data):
    return Response(status=200,
                    data=dict(
                        result_code=result_code,
                        result_msg=result_msg,
                        data=data
                        )
                    )

def SuccessResponse():
    return Response(status=200,
                    data=dict(
                        result_code=0,
                        result_msg="success"
                    ))


def SuccessResponseWithData(data):
    return Response(status=200,
                    data=dict(
                        result_code=0,
                        result_msg="success",
                        data=data
                    ))


def ErrorResponse():
    return Response(status=200,
                    data=dict(
                        result_code=999,
                        result_msg="error!!!"
                    ))