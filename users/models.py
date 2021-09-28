from django.db import models

# unique=true로 설정하면 data는 db안에서 유일해야 하게 됨.
# null=true는 입력하지 않아도 되는 field라는 의미.(기본값으로 false)
class User(models.Model):
    name         = models.CharField(max_length=30)
    email        = models.EmailField(max_length=50, unique=True)
    password     = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=30)
    hobby        = models.TextField(max_length=50, null=True)

    # Meta options: https://docs.djangoproject.com/ko/3.2/topics/db/models/#meta-options
    class Meta:
        db_table = 'users'

    # model methods: https://docs.djangoproject.com/ko/3.2/topics/db/models/#model-methods
    def __str__(self):
        return self.name