from django.contrib import admin,messages
from.models import *
# Register your models here.
from inline_actions.admin import InlineActionsModelAdminMixin
from django.shortcuts import redirect
from django.http import HttpResponse




admin.site.site_header="Gestion de magasin"
admin.site.site_title="Gestion de magasin"
admin.site.index_title="Gestion de magasin"

class EntreeStockGlobalinline(admin.TabularInline):
    model = EntreeStockGlobal
    extra = 0
@admin.register(Magasin)
class MagasinAdmin(InlineActionsModelAdminMixin,admin.ModelAdmin):
    list_display = ["refmagasin","libmagasin","lieumagasin"]
    search_fields = ("refmagasin","libmagasin","lieumagasin",)
@admin.register(Article)
class ArticleAdmin(InlineActionsModelAdminMixin,admin.ModelAdmin):
    list_display = ["codearticle","nomarticle"]
    search_fields = ("codearticle","nomarticle",)
@admin.register(Fournissuer)
class ArticleAdmin(InlineActionsModelAdminMixin,admin.ModelAdmin):
    list_display = ["numfournisseur","nomfournisseur"]
    search_fields = ("numfournisseur","nomfournisseur",)

@admin.register(StockGlobal)
class StockGlobalAdmin(InlineActionsModelAdminMixin,admin.ModelAdmin):
    list_display = ["libellestockglobal","quantiteglobalstock"]
    search_fields = ("libellestockglobal","article__nomarticle",)
    inlines = (EntreeStockGlobalinline,)
@admin.register(BudgetJournalier)
class BudgetJournalierAdmin(InlineActionsModelAdminMixin,admin.ModelAdmin):
    list_display = ["datejournee", "depenseglobal", "recetteglobal"]
    search_fields = ("datejournee","depenseglobal","recetteglobal",)
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