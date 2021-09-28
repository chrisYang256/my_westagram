import json, re

from django.http            import JsonResponse
from django.views           import View
# from django.core.exceptions import ValidationError

from users.models           import User

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
        # 정규표현식을 사용할 경우, 자주 사용되는 경우가 아니라면 compile()해서 사용하지 않고,
        # match()를 사용하는 것을 공식 문서에서 추천하고 있습니다.
        REGX_EMAIL    = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        REGX_PASSWORD = '^(?=.*\d)(?=.*[a-zA-Z])[0-9a-zA-Z!@#$%^&*]{8,20}$'

        try: 
            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'MESSAGE': 'THIS_EMAIL_ALREADY_SIGNUP'}, status=400)
            
            # 참고: https://docs.python.org/3/library/re.html#module-contents
            if not re.match(REGX_EMAIL, data['email']):
                return JsonResponse({'MESSAGE': 'INVALID_EMAIL_FORM'}, status=400)

            if not re.match(REGX_PASSWORD, data['password']):
                return JsonResponse({'MESSAGE': 'INVALID_PASSWORD_FORM'}, status=400)

            User.objects.create(
                name           = data['name'],
                email          = data['email'],
                password       = data['password'],
                phone_number   = data['phone_number'],
                hobby          = data['hobby']
            )
            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=201)

        # 매핑(딕셔너리) 키가 기존 키 집합에서 발견되지 않을 때 발생.
        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)



# 로그인 정보: email, password

# 계정이나 패스워드 키가 전달되지 않았을 경우, {"message": "KEY_ERROR"}, status code 400 을 반환합니다.
# 계정을 잘 못 입력한 경우 {"message": "INVALID_USER"}, status code 401을 반환합니다.
# 비밀번호를 잘 못 입력한 경우 {"message": "INVALID_USER"}, status code 401을 반환합니다.

# 로그인이 성공하면 {"message": "SUCCESS"}, status code 200을 반환합니다.

class LogIn(View):
    def get(self, request):
        data = json.loads(request.body)

        try:
            # check email
            if not User.objects.filter(email=data['email']).exists():
                return JsonResponse({'MESSAGE': 'DON\'T_EXIST_USER'}, status=401)

            # email OK, check password
            password_check = User.objects.get(email=data['email']).password
            if not password_check == data['password']:
                return JsonResponse({'MESSAGE': 'INVALID_PASSWORD'}, status=401)

            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY_ERROR'}, status=400)
