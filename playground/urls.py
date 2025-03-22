from playground.api.urls import urlpatterns as api_urlpatterns
from .views.urls import urlpatterns as view_urlpatterns

urlpatterns = []+view_urlpatterns
urlpatterns+api_urlpatterns