from django.db import models
from django.conf import settings


class Message(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="chat_messages",
    )

    # course = models.ForeignKey(
    #     "courses.Course",
    #     on_delete=models.PROTECT,
    #     related_name="chat_messages",
    # )
    room = models.IntegerField()

    content = models.TextField()
    sent_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} on {self.room} at {self.sent_on}"  