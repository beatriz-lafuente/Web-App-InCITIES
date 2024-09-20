from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('data_charts/', include('data_charts.urls')),
    path('indicators_list/', include('indicators_list.urls')),
]