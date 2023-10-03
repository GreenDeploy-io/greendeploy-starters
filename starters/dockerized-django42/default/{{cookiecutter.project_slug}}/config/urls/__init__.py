from config.urls.base_urls import urlpatterns as base_urlpatterns
from config.urls.complements_urls import urlpatterns as complements_urlpatterns
from config.urls.domains_urls import urlpatterns as domains_urlpatterns

urlpatterns = base_urlpatterns + complements_urlpatterns + domains_urlpatterns
