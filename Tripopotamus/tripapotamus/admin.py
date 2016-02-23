from django.contrib import admin
from django.db.models.query import QuerySet

from .models import Member, Trip, Scoreboard, Bookmark, TaxiRate

class MemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'moneySaved', 'distanceTravelled', 'distance_street', 'distance_ocean', 'distance_marathon', 'distance_space', 'distance_denmark', 'distance_texas', 'distance_sahara', 'distance_tourdefrance', 'distance_moon', 'distance_world', 'money_1', 'money_10', 'money_25', 'money_50', 'money_100', 'twitter_posted')
    search_fields = ['moneySaved', 'distanceTravelled', 'distance_street', 'distance_ocean', 'distance_marathon', 'distance_space', 'distance_denmark', 'distance_texas', 'distance_sahara', 'distance_tourdefrance', 'distance_moon', 'distance_world', 'money_1', 'money_10', 'money_25', 'money_50', 'money_100', 'twitter_posted']

admin.site.register(Member, MemberAdmin)

class TripAdmin(admin.ModelAdmin):
    list_display = ('id', 'time', 'user', 'startPoint', 'endPoint', 'moneySaved', 'distanceTravelled',)
    search_fields = ['id', 'startPoint', 'endPoint',]
    list_filter = ['user']
    date_hierarchy = 'time'
    
    actions = ['delete_selected',]

    def delete_selected(self, request, queryset):
        for obj in queryset.all():
            obj.delete()
        
        
admin.site.register(Trip, TripAdmin)

admin.site.register(Scoreboard)

class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('id', 'startPoint', 'endPoint',)
    search_fields = ['id', 'startPoint', 'endPoint',]

admin.site.register(Bookmark, BookmarkAdmin)

class TaxiRateAdmin(admin.ModelAdmin):
    list_display = ('city', 'state', 'country', 'base_fare', 'distance_fare', 'time_fare', 'minimum_fare', 'service_fee', 'surge_multiplier',)

admin.site.register(TaxiRate, TaxiRateAdmin)