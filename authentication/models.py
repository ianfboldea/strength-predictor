from django.db import models

class WorkoutWeek(models.Model):
    end_date = models.DateTimeField('date ended')
    total_calories = models.IntegerField(default=0)
    total_sleep = models.IntegerField(default=0)
    total_chest = models.IntegerField(default=0)
    total_shoulders = models.IntegerField(default=0)
    total_triceps = models.IntegerField(default=0)
    total_protein = models.IntegerField(default=0)
    total_carbs = models.IntegerField(default=0)
    bench_max = models.IntegerField(default=0)

    def __str__(self):
        return str(self.end_date)

    # admin pass is 1234
