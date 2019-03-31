from django.contrib.sitemaps import Sitemap
from listings.models import Listing
from django.shortcuts import reverse

class ListingSitemap(Sitemap):
    def items(self):
        return Listing.objects.all()

class StaticViewSitemap(Sitemap):
    def items(self):
        return ['pages:index','pages:about','listings:listings','accounts:dashboard','accounts:register','accounts:login','accounts:logout']

    def location(self, item):
        return reverse(item)