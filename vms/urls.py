from django.conf.urls import url

from vms import views

urlpatterns= [
    #(r'^login/', views.UserView.as_view()),
    url(r'^$',views.Basic.as_view()),
    url(r'^login/', views.Login.as_view()),
    url(r'^logindetails/', views.LoginDetails.as_view()),
    url(r'^addvisitor/', views.VisitorCreate.as_view()),
    url(r'^viewvisitor/', views.VisitorView.as_view()),
    url(r'^viewvisitee/', views.VisiteeList.as_view()),
    url(r'^history/', views.VisitHistory.as_view()),
    url(r'^check/', views.Check.as_view()),
    url(r'^search/', views.Search.as_view()),
    url(r'^update/', views.Update.as_view()),
    url(r'^gatecreate/', views.GateView.as_view()),
    url(r'^gatelist/', views.GateList.as_view()),
    url(r'^user/', views.UserDetail.as_view()),
    #url(r'^image', views.Imagine.as_view()),


    ]
