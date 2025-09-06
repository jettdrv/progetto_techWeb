from django.contrib import admin
from .models import StudyGroup, GroupMembership, GroupDiscussion, Comment
admin.site.register(StudyGroup)
admin.site.register(GroupMembership)
admin.site.register(GroupDiscussion)
admin.site.register(Comment)
