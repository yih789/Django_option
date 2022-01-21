from django.shortcuts import render

from .models import Task

from rest_framework.views import APIView
from rest_framework.response import Response

# swagger
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# serialize
from .serialize import TodoSerializer

# 페이지 분할
from django.core.paginator import Paginator

# 로그
import logging
logger = logging.getLogger('test')

# 공통 영역
from common.common import TaskView

''' APIView를 상속받은 TaskView를 상속받은 TaskCreate 객체 생성 '''
''' todo를 생성하는 API 정의'''
''' API 문서화: INPUT(user_id, name), OUPUT(id) 정의 '''
class TaskCreate(TaskView):
    """
        여기에 주석으로 뭔가 쓰면 swagger에 마크다운 형식으로 추가설명이 반영됩니다.
        ---
        # TO-DO를 생성할 때 사용하는 API
            - user_id : 사용자 ID
            - name : To-Do 이름
    """
     # Output schema 정의
    id_field = openapi.Schema(
        title='id',
        description='To-Do가 생성되면 자동으로 채번되는 ID값',
        type=openapi.TYPE_INTEGER
    )
    success_response = openapi.Schema(
        title='response',
        type=openapi.TYPE_OBJECT,
        properties={
            'id': id_field
        }
    )
    # swagger 정의: 일반적으로 input을 serialize로 보낸다.
    @swagger_auto_schema(tags=['TODO 만들기'],
                         request_body=TodoSerializer,
                         query_serializer=TodoSerializer,
                         responses={
                             200: success_response,
                             403: '인증 에러',
                             400: '입력값 유효성 검증 실패',
                             500: '서버 에러'
                         })
    def post(self, request):
        # user_id = request.data.get('user_id', "")
        # 공통영역에 정의한 상위 TaskView에 user_id를 미리 정의해뒀기 때문에 self로 가져다 사용할 수 있다.
        user_id = self.user_id
        todo_id = Task.objects.all().count() + 1
        name = request.data.get('name', "")
        logger.error('log test')
        """
        end_date = request.data.get('end_date', None)
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        """
        task = Task.objects.create(id=todo_id, user_id=self.user_id, name=name)
        return Response(data=dict(id=todo_id))


class Pagination(APIView):
    def get(self, request):
        tasks = Task.objects.all().order_by('-id')

        paginator = Paginator(tasks, 6)

        # 사용자에게 받은 page 파라미터에 해당하는 paginator 객체 생성
        page = request.GET.get('page')
        items = paginator.get_page(page)

        # paginator 아이콘 생성을 위해 필요한 변수들
        row = items.number // 5 + 1  # 요청 받은 페이지가 속한 열의 num
        if (items.number % 5 == 0):
            row = items.number // 5

        left = row * 5 - 5  # 왼쪽 화살표 생성을 위한 변수
        right = row * 5 + 1  # 오른쪽 화살표 생성을 위한 변수
        range_for = range(row * 5 - 4, row * 5 + 1)  # n개의 숫자(페이지 번호)를 생성을 위한 변수
        print(items.number, row)

        context = {
            'contents': items,
            'row': row,
            'left': left,
            'right': right,
            'range_for': range_for,
            'total_page_num': paginator.num_pages,  # 총 페이지
            'request_page': items.number,  # 현재 페이지

        }
        return render(request, 'serverDev/Home.html', context)
