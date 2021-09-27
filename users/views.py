import json, re

from django.http            import JsonResponse
from django.views           import View
# from django.core.exceptions import ValidationError

from users.models                 import User

# # 회원가입 시에만 쓸것이기 때문에 별도의 파일로 만들지 않음.
# def validation_email(email):
#     # 쓰고싶었던 코드: if not '@' and '.' in email:
#     # 이메일 정규식 검사: 계정(+, -, _, .가능)@도메인(-가능).최상위도메인
#     # 정규식 참고: https://dojang.io/mod/page/view.php?id=2439
#     email_regx = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
#     if not email_regx.match(email):
#         raise ValidationError(('Invalid email form'), code='invalid_email')

# def validation_password(password):
#     # 비밀번호 정규식 검사: 특수문자, 문자, 숫자 포함 8~15자리
#     password_regx = re.compile('/^(?=.*\d)(?=.*[a-zA-Z])[0-9a-zA-Z!@#$%^&*]{8,20}$/')
#     if not password_regx.match(password):
#         raise ValidationError(('Invalid password form'), code='invalid_password')
    

class SignUp(View):
    def post(self, request):
        data          = json.loads(request.body)
        # 이메일 정규식 검사: 계정(+, -, _, .가능)@도메인(-가능).최상위도메인
        # 비밀번호 정규식 검사: 특수문자, 문자, 숫자 포함 8~15자리
        email_regx    = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        password_regx = re.compile('^(?=.*\d)(?=.*[a-zA-Z])[0-9a-zA-Z!@#$%^&*]{8,20}$')

        try: 
            if User.objects.filter(user_email=data['user_email']).exists():
                return JsonResponse({'MESSAGE': 'THIS_EMAIL_ALREADY_SIGNUP'}, status=400)
            
            # 참고: https://docs.python.org/3/library/re.html#module-contents
            if not re.match(email_regx, data['user_email']):
                return JsonResponse({'MESSAGE': 'INVALID_EMAIL_FORM'}, status=400)

            if not re.match(password_regx, data['user_password']):
                return JsonResponse({'MESSAGE': 'INVALID_PASSWORD_FORM'}, status=400)

            User.objects.create(
                user_name        = data['user_name'],
                user_email       = data['user_email'],
                user_password    = data['user_password'],
                user_phone_num   = data['user_phone_num'],
                user_hobby       = data['user_hobby']
            )
            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=201)

        # 매핑(딕셔너리) 키가 기존 키 집합에서 발견되지 않을 때 발생.
        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)