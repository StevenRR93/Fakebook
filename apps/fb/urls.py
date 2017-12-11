from django.conf.urls import url
from views import *
urlpatterns = [ 
    url(r'^$', fakebook, name = 'fakebook'), 
    url(r'^verify$', verify, name = 'verify'),
    url(r'^register$', register, name = 'register'),
    url(r'^success/(?P<idnum>\w+)$', success, name = 'success'),
    url(r'^login$', login, name = 'login'),
    url(r'^home$', home, name = 'home'),
    url(r'^users/(?P<idnum>\w+)$', users, name = 'users'),
    url(r'^users/edit/(?P<idnum>\w+)$', edit, name = 'edit'),
    url(r'^search/', search, name = 'search'),
    #url(r'^search/(?P<searchname>.+)$', search, name = 'search'),
    #url(r'^search/(?search=(?P<searchname>.+))$', search, name = 'search'),# (?:page-(?P<page_number>\d+)/)?
    url(r'^friendslist/(?P<idnum>\w+)$', friendslist, name = 'friendslist'),
    url(r'^update$', update, name = 'update'),
    url(r'^messagelist$', messagelist, name = 'messagelist'),
    url(r'^message/(?P<idnum>\w+)$', message, name = 'message'),
    url(r'^post$', post, name = "post"),
    url(r'^comment$', comment, name = 'comment'),
    url(r'^logout$', logout, name = 'logout'),
    url(r'^remove$', remove, name = 'remove'),
    url(r'^add$', add, name = 'add'),
    url(r'^reply$', reply, name = 'reply'),
    url(r'^delete/comment/(?P<idnum>\w+)$', delete_comment, name = 'delete_comment'),
    url(r'^delete/message/(?P<idnum>\w+)$', delete_message, name = 'delete_message'),
    url(r'^delete/post/(?P<idnum>\w+)$', delete_post, name = 'delete_post'),
]