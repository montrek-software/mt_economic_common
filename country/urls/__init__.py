from .country_api_credentials_urls import urlpatterns as country_api_credentials_urls
from .country_urls import urlpatterns as country_urls

urlpatterns = country_urls + country_api_credentials_urls
