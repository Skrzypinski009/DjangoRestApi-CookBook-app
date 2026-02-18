from django.apps import AppConfig


class CookbookSiteConfig(AppConfig):
    name = "cookbook_site"

    def ready(self):
        import cookbook_site.signals
