from django.contrib import admin,messages
from.models import *
# Register your models here.
from inline_actions.admin import InlineActionsModelAdminMixin
from django.shortcuts import redirect
from django.http import HttpResponse




admin.site.site_header="Gestion de magasin"
admin.site.site_title="Gestion de magasin"
admin.site.index_title="Gestion de magasin"



@admin.register(Budget)
class PointHautAdmin(InlineActionsModelAdminMixin,admin.ModelAdmin):
    list_display = ["dateBudget", "depense", "recette"]
    search_fields = ("dateBudget","depense","recette",)
    readonly_fields = ('creepar', 'modifierpar',)
    actions = ["print_budget",]

    def print_budget(self, request, queryset):
        bdgs = list(queryset)
        if bdgs:
            html_response = redirect("/budget/budgetjour/" + bdgs.__getitem__(0).pk.__str__() + "/reporting")
            return html_response
        else:
            return HttpResponse("Etat de budget non trouvé")

    def save_model(self, request, obj, form, change):
        if change:
            agent = request.user.username
            obj.modifierpar = agent
            super().save_model(request, obj, form, change)

        else:
            agent = request.user.username
            obj.creepar = agent
            super().save_model(request, obj, form, change)