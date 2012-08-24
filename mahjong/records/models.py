# -*- coding: utf8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Record(models.Model):
    players = models.ManyToManyField(User, related_name="records", through="Player")
    extra_point = models.IntegerField(default=0)

    match_type = models.IntegerField(default=2) # 1 for tonn / 2 for hann

    valid = models.BooleanField(default = True)
    uploaded = models.DateTimeField(auto_now = True)

    def __unicode__(self):
        result = u"Record : "
        for player in self.player_set.all():
            result += " %s" % player.user.first_name
        return result

    def order_rank(self):
        rank = []
        for player in self.player_set.all():
            rank.append([player, player.point])
        rank = sorted(rank, key=lambda player: -player[1])

        for element in rank:
            element.append(rank.index(element)+1)

        i = 1
        while i < len(rank):
            try:
                if rank[i][1] == rank[i-1][1]:
                    rank[i][2] == rank[i-1][2]
                i += 1
            except IndexError:
                break

        for element in rank:
            element[0].rank = element[2]
            element[0].save()

    def normalize(self):
        point_sum = 0
        for player in self.player_set.all():
            point_sum += player.point

        total = point_sum + self.extra_point

        if total == 0:
            return True
        else:
            if total % 10000 == 0 and total % 4 == 0:
                point_to_minus = total / 4
                for player in self.player_set.all():
                    player.point -= point_to_minus
                    player.save()
                self.extra_point = 0
                self.save()
                return True
            else:
                self.valid = False
                self.save()
                return False

    class Meta:
        permissions = (
            ("submit_records", "Can submit a record."),
        )

class Player(models.Model):
    user = models.ForeignKey(User)
    record = models.ForeignKey(Record)

    kaze = models.CharField(max_length=4)
    point = models.IntegerField()
    rank = models.IntegerField(default=0)

    class Meta:
        ordering = ['rank']

def post_save_player(sender, instance, created, **kwargs):
    if created:
        if instance.record.players.count() == 4:
            instance.record.order_rank()
            instance.record.normalize()

post_save.connect(post_save_player, sender=Player)
