from django.core.management.base import BaseCommand
from serverDev.models import Task
from datetime import datetime

# 배치 프로그램
# 배치 프로그램은 일반적으로 특정 시간에 자동으로 실행
# ex) crontab, jenkins 프로그램 사용
class Command(BaseCommand):
    def handle(self, *args, **options):
        print("테스트 배치 프로그램 실행")
        task_list = Task.objects.all()

        for task in task_list:
            if task.end_date < datetime.now().date():
                task.state = 3
                task.save()
                print(task.id, task.name, '만료되었습니다.')