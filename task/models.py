from django.db import models

from datetime import datetime

class Task(models.Model):
    user_id = models.IntegerField(null=True)
    name = models.CharField(max_length=200)
    deadline = models.DateTimeField('deadline')
    description = models.TextField(default=None, blank=True, null=True)

    def str_type(self):
        delta_time = (self.deadline.replace(tzinfo=None) - datetime.now()).total_seconds()
    
        deta_time_str = ''

        seconds = int(delta_time % 60)
        delta_time /= 60

        minutes = int(delta_time % 60)
        delta_time /= 60

        hours = int(delta_time % 24)
        delta_time /= 24

        days = int(delta_time)

        big_delay = False
        if days!=0:
            deta_time_str += f"{days} days "
            big_delay = True

        if hours!=0:
            deta_time_str += f"{hours} hours "
            big_delay = True
        
        if not big_delay:
            if minutes!=0:
                deta_time_str += f"{minutes} minutes "
            
            if seconds!=0:
                deta_time_str += f"{seconds} seconds "
        
        if days<=1:
            label_type = 'danger'
        elif days>=2:
            label_type = 'warning'
        else: 
            label_type = 'success'

        return deta_time_str, label_type