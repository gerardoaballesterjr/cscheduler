from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from core import models, genetic
import json

class SemesterConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.created_at = None

    def connect(self):
        if self.scope['user'].is_authenticated:
            self.slug = self.scope['url_route']['kwargs']['slug']
            try:
                self.semester = models.Semester.objects.get(slug=self.slug)
                self.user = self.scope['user']
                async_to_sync(self.channel_layer.group_add)(self.slug, self.channel_name)
                self.accept()

                models.Schedule.objects.filter(section__semester=self.semester, section__course__department=self.user.department).delete()

                object = genetic.Genetic(semester=self.semester, user=self.user)
                object.initialize()

                if object.error:
                    async_to_sync(self.channel_layer.group_send)(
                        self.slug,
                        {
                            'type': 'send_data',
                            'context': object.error,
                        }
                    )
                else:
                    for _ in range(object.max_generation):
                        object.evaluate()
                        solution = object.solution()
                        if solution:
                            object.save()
                            async_to_sync(self.channel_layer.group_send)(
                                self.slug,
                                {
                                    'type': 'send_data',
                                    'context': 'Generating schedule successfully!',
                                }
                            )
                            break
                        object.crossover()
                        object.mutate()

            except models.Semester.DoesNotExist:
                self.close()
        else:
            self.close()

    def send_data(self, text_data):
        self.send(text_data=text_data['context'])