from django.db import models


class PracticeSession(models.Model):
  start = models.DateTimeField()
  finish = models.DateTimeField(null=True, blank=True)
  type = models.CharField(max_length=20)
  rating = models.SmallIntegerField(null=True)
  feel = models.CharField(max_length=20, null=True)
  attemptCount = models.IntegerField(null=True)

  def __str__(self):
    return str.format('{0} {1}', self.type, self.start)
