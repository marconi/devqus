from redisco import models


class Message(models.Model):
    mid = models.IntegerField(required=False, indexed=True)
    body = models.Attribute(required=True, indexed=False)
    author = models.Attribute(required=True)
    created = models.DateTimeField(auto_now_add=True)

    def save(self):
        super(Message, self).save()
        if not self.mid:
            self.mid = int(self.id)
            super(Message, self).save()
