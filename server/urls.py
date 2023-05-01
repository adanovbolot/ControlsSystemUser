from django.urls import path
from . import views


urlpatterns = [
    path('user/create/', views.UserCreate.as_view()),
    path('user/login/', views.UserAuthorization.as_view()),
    path('user/logout/', views.UserLogout.as_view()),
    path('user/sending/reset/code/', views.UserSendingResetCode.as_view()),
    path('user/reset/send/code/', views.UserResetConfirmation.as_view()),

    path('profile/update/', views.UserDataUpdate.as_view()),
    path('profile/all/', views.DataOutputUser.as_view()),
    path('profile/update/delete/status/<int:pk>/', views.UserStatusUpdate.as_view()),

    path('access/all/', views.UserAccessAllGet.as_view()),
    path('access/update/delete/<int:pk>/', views.UserAccessUpdateDelete.as_view()),

    path('session/all/get/', views.UserSessionAllGet.as_view()),
    path('session/update/delete/<int:pk>/', views.UserSessionUpdateDelete.as_view()),

    path('server/settings/list/create/', views.ServerSettingsGetCreate.as_view()),
    path('server/settings/retrieve/update/delete/<int:pk>/', views.ServerSettingsRetrieveUpdateDestroy.as_view()),

    path('proxy/server/create/all/list/', views.ServerSettingsGetCreate.as_view()),
    path('proxy/server/update/delete/<int:pk>/', views.ServerSettingsRetrieveUpdateDestroy.as_view()),
]
