"""定义模型的URL模式"""

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^topics/$',views.topics,name='topics'),
    url(r'^topic/(?P<topic_id>\d+)/$',views.topic,name='topic'),
    url(r'^new_topic/$',views.new_topic,name='new_topic'),
    url(r'^edit_topic/(?P<topic_id>\d+)/$',views.edit_topic,name='edit_topic'),
    url(r'^add_content/(?P<topic_id>\d+)/$',views.add_content,name='add_content'),
    url(r'^edit_content/(?P<edit_id>\d+)/$',views.edit_content,name='edit_content'),
    ]
    
