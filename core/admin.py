from django.contrib import admin,messages
from.models import *
# Register your models here.
from inline_actions.admin import InlineActionsModelAdminMixin
from django.shortcuts import redirect
from django.http import HttpResponse
from decimal import Decimal



admin.site.site_header="Gestion de magasin"
admin.site.site_title="Gestion de magasin"
admin.site.index_title="Gestion de magasin"

class EntreeStockGlobalinline(admin.TabularInline):
    model = EntreeStockGlobal
    extra = 0

class EntreeStockMagasininline(admin.TabularInline):
    model = EntreeStockMagasin
    extra = 0
class RecetteMagasinJrinline(admin.TabularInline):
    model = RecetteMagasinJr
    extra = 0
class DepenseMagasinJrinline(admin.TabularInline):
    model = DepenseMagasinJr
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
    list_display = ["display_article","libellestockglobal","quantiteglobalstock"]

    def display_article(self, obj):
        return '{}-{}'.format(obj.article.codearticle, obj.article.nomarticle)

    display_article.short_description = 'Article'
    search_fields = ("quantiteglobalstock","article__nomarticle","article__codearticle",)
    #readonly_fields = ('quantiteglobalstock',)
    inlines = (EntreeStockGlobalinline,)

@admin.register(StockMagasin)
class StockMagasinAdmin(InlineActionsModelAdminMixin,admin.ModelAdmin):
    #list_display = ["libellestockmagasin","quantitemagasin"]
    list_display = ("display_magasin",'display_article','libellestockmagasin', 'quantitemagasin',)


    def display_magasin(self, obj):
        return obj.magasin.libmagasin

    display_magasin.short_description = 'Magasin'
    def display_article(self, obj):
        return '{}-{}'.format(obj.article.codearticle, obj.article.nomarticle)

    display_article.short_description = 'Article'

    search_fields = ("libellestockmagasin","article__nomarticle","article__codearticle","magasin__libmagasin",)
    inlines = (EntreeStockMagasininline,)


    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        new_quantiteentred=0
        for instance in instances:
            if instance.quantiteentredmg:
                new_quantiteentred = new_quantiteentred + instance.quantiteentredmg
        for obj in formset.deleted_objects:
            obj.delete()
        if len(instances) > 0:
            last_instance = instances[-1]
            stock_global = StockGlobal.objects.get(article=last_instance.id_stockmagasin.article)
            stock_magasin = last_instance.id_stockmagasin
            if new_quantiteentred  > stock_global.quantiteglobalstock :
                messages.set_level(request, messages.ERROR)
                messages.error(request, "Insufficient global stock quantity.Please Ckeck your Global Stock article quantity !")
            else:
                new_quantitemagasin = last_instance.id_stockmagasin.quantitemagasin + new_quantiteentred
                stock_magasin.quantitemagasin = new_quantitemagasin
                stock_magasin.save()
                stock_global.quantiteglobalstock = stock_global.quantiteglobalstock - new_quantiteentred
                stock_global.save()
                for instance in instances:
                    instance.save()

        formset.save_m2m()



##############################################################################################
@admin.register(BudgetJournalier)
class BudgetJournalierAdmin(InlineActionsModelAdminMixin,admin.ModelAdmin):
    list_display = ["datejournee", "depenseglobal", "recetteglobal"]
    search_fields = ("datejournee","depenseglobal","recetteglobal",)
    readonly_fields = ('creepar', 'modifierpar',)
    inlines = (RecetteMagasinJrinline,DepenseMagasinJrinline,)
    actions = ["print_budget",]

    def print_budget(self, request, queryset):
        bdgs = list(queryset)
        if bdgs:
            html_response = redirect("/budget/budgetjour/" + bdgs.__getitem__(0).pk.__str__() + "/reporting")
            return html_response
        else:
            return HttpResponse("Etat de budget non trouvé")


    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, RecetteMagasinJr):
                stock_magasin = StockMagasin.objects.get(Q(article=instance.id_article) & Q(magasin=instance.id_budgetj.magasin))
                instance.montantrecette = round(Decimal(stock_magasin.prixvente) * instance.quantitout, 2)
                if instance.quantitout > stock_magasin.quantitemagasin:
                    messages.set_level(request, messages.ERROR)
                    messages.error(request,"Insufficient magasin stock quantity.Please Ckeck your magasin Stock article quantity !")
                else:
                    stock_magasin.quantitemagasin = stock_magasin.quantitemagasin - instance.quantitout
                    stock_magasin.save()
                    instance.save()
            elif isinstance(instance, DepenseMagasinJr):
                instance.save()

        for obj in formset.deleted_objects:
            obj.delete()

        formset.save_m2m()

    def save_model(self, request, obj, form, change):
        if change:
            agent = request.user.username
            obj.modifierpar = agent
            super().save_model(request, obj, form, change)

        else:
            agent = request.user.username
            obj.creepar = agent
            super().save_model(request, obj, form, change)