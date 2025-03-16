from .api import urls as api_urls
from .views import urls as view_urls

urlpatterns = []+view_urls.urlpatterns+api_urls.urlpatterns