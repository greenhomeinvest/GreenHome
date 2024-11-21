from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

class StatiViewSiteMap(Sitemap):
    
    def items(self):
        # Add URLs you want to include in the sitemap here
        return [
            'home',        # 'home' is the name of the view for the homepage
            'listings',    # 'listings' is the name of the view for the listings page
            'realtors',    # 'realtors' is the name of the view for the realtors page
            'contact',     # 'contact' is the name of the view for the contact page
            'feedback',    # 'feedback' is the name of the view for the feedback page
            # 'inquiry',     # 'inquiry' is the name of the view for the inquiry page
        ]

    def location(self, item):
        return reverse(item)  # Generates the full URL for the named view