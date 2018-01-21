from django.db import models


class PracticeSession(models.Model):
  start = models.DateTimeField()
  finish = models.DateTimeField(null=True, blank=True)
  type = models.CharField(max_length=20)

  def __str__(self):
    return str.format('{0} {1}', self.type, self.start)
