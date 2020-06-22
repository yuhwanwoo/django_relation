from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.pk}번째 글, {self.title}-{self.content}'

class Comment(models.Model):
    # models.ForeignKey(상속받을 클래스명, Article이 삭제되었을때 어떻게 할것인지)
    # 멤버 변수 = models.외래키(참조하는 객체)
    article=models.ForeignKey(Article, on_delete=models.CASCADE) # 역참조 값 설정 related_name='comments'
    content=models.CharField(max_length=200)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Article:{self.article}, {self.pk}-{self.content}'