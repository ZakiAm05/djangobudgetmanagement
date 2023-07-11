from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages
class Magasin(models.Model):
    refmagasin = models.CharField(db_column='RefMagasin', max_length=250, blank=True, null=True,verbose_name="Référence Magasin Article")
    libmagasin=models.CharField(db_column='LibelleMagasin', max_length=250, blank=True, null=True,verbose_name="Libellé Magasin")
    lieumagasin = models.TextField(db_column='LieuMagasin',max_length=250, null=True, blank=True,verbose_name="Lieu Magasin")

    def __str__(self):
        return "{}".format(self.libmagasin)
    class Meta:
        verbose_name="Magasin"

class Article(models.Model):
    codearticle = models.CharField(db_column='CodeArticle', max_length=250, blank=True, null=True,verbose_name="Code Article")
    nomarticle=models.CharField(db_column='LibelleArticle', max_length=250, blank=True, null=True,verbose_name="Libellé Article")
    prixunitaire=models.IntegerField(db_column='PrixUnitaire',blank=True, null=True,verbose_name="Prix Unitaire")
    designation = models.TextField(db_column='Designation', null=True, blank=True)

    def __str__(self):
        return "{} {}".format(self.codearticle,self.nomarticle)
    class Meta:
        verbose_name="Article"

class Fournissuer(models.Model):
    numfournisseur = models.IntegerField(db_column='NumFournisseur',blank=True, null=True,verbose_name="Numéro fournisseur")
    nomfournisseur=models.CharField(db_column='NomFournisseur', max_length=250, blank=True, null=True,verbose_name="Nom Fournissuer")
    addressfournisseur = models.TextField(db_column='AddressFournisseur',max_length=250, null=True, blank=True,verbose_name="Adress de Fournisseur")

    def __str__(self):
        return "{}".format(self.nomfournisseur)
    class Meta:
        verbose_name="Fournisseur"

class StockGlobal(models.Model):
    article = models.ForeignKey(to='Article',on_delete=models.CASCADE,db_column='ArticleInStock', blank=True, null=True,verbose_name="Article")
    quantiteglobalstock = models.IntegerField(db_column='QteGlobalStock', blank=True, null=True)
    libellestockglobal = models.CharField(db_column='LibelleStkG', max_length=250, blank=True, null=True,verbose_name="Libelle de Stock Global")
    def __str__(self):
        return "{}".format(self.article.codearticle)
    class Meta:
        verbose_name="Stock Global"


class EntreeStockGlobal(models.Model):
    id_stockglobal=models.ForeignKey(to='StockGlobal',on_delete=models.CASCADE,db_column='StockGlobalArticle', blank=True, null=True,related_name='linked_stocks')
    idfournisseur=models.ForeignKey(to='Fournissuer',on_delete=models.CASCADE,db_column='FournisseurArticle', blank=True, null=True,related_name='linked_fournisseurs',verbose_name="Fournisseur article")
    dateentree=models.DateField(db_column='DateEntreeStck',blank=True, null=True,verbose_name="Date Entree Au Stock")
    quantiteentree=models.IntegerField(db_column='QteEntred',blank=True, null=True,verbose_name="Quantite Entree Au Stock")

    class Meta:
        verbose_name="Entree Au Stock"
        db_table = 'Entree_Stock_Global'

    def delete(self, *args, **kwargs):
        stock_global = self.id_stockglobal
        stock_global.quantiteglobalstock = stock_global.quantiteglobalstock - self.quantiteentree
        stock_global.save()

        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Update quantiteglobalstock in StockGlobal
        stock_global = self.id_stockglobal
        stock_global.quantiteglobalstock = stock_global.quantiteglobalstock + self.quantiteentree
        stock_global.save()



#######################################################################################################################################
class StockMagasin(models.Model):
    libellestockmagasin = models.CharField(db_column='LibelleMagasin', max_length=250, blank=True, null=True,verbose_name="Libelle de Stock Magasin")
    magasin = models.ForeignKey(to='Magasin', on_delete=models.CASCADE, db_column='MagasinStock', blank=True,null=True, verbose_name="Magasin")
    article = models.ForeignKey(to='Article',on_delete=models.CASCADE,db_column='ArticleInStock', blank=True, null=True,verbose_name="Article")
    quantitemagasin = models.IntegerField(db_column='QteMagasin', blank=True, null=True,verbose_name="Quantite Article Dans Magasin")

    def __str__(self):
        return "{} {}".format(self.magasin.libmagasin,self.article.nomarticle)
    class Meta:
        verbose_name="Stock Magasin"

class EntreeStockMagasin(models.Model):
    id_stockmagasin=models.ForeignKey(to='StockMagasin',on_delete=models.CASCADE,db_column='StockMagasinArticle', blank=True, null=True,related_name='linked_magasinstocks')
    dateentredmg=models.DateField(db_column='DateEntreeStckMg',blank=True, null=True,verbose_name="Date Entree Au Stock Magasin")
    quantiteentredmg=models.IntegerField(db_column='QteEntredMg',blank=True, null=True,verbose_name="Quantite Entree Au Stock Magasin")

    class Meta:
        verbose_name="Entree Au Stock de Magasin"
        db_table = 'Entree_Stock_Magasin'

    def delete(self, *args, **kwargs):
        stock_magasin = self.id_stockmagasin
        stock_magasin.quantitemagasin = stock_magasin.quantitemagasin - self.quantiteentredmg
        stock_magasin.save()

        super().delete(*args, **kwargs)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Update quantiteglobalstock in StockGlobal
        stock_magasin = self.id_stockmagasin
        stock_global = StockGlobal.objects.get(article=stock_magasin.article)
        new_quantitemagasin = stock_magasin.quantitemagasin + self.quantiteentredmg
        stock_magasin.quantitemagasin = new_quantitemagasin
        stock_magasin.save()

        if self.quantiteentredmg > stock_global.quantiteglobalstock:
            messages.error("Insufficient global stock quantity. Cannot save the entry.")
        else:
            stock_global.quantiteglobalstock = stock_global.quantiteglobalstock - self.quantiteentredmg
            stock_global.save()

#############################################################################################################################################
class BudgetJournalier(models.Model):
    magasin=models.ForeignKey(to='Magasin',on_delete=models.CASCADE,db_column='MagasinInBJ', blank=True, null=True,related_name='linked_magasins')
    datejournee=models.DateField(db_column='DateJournee',verbose_name="Date de la journee")
    depenseglobal=models.IntegerField(db_column='Depense',blank=True, null=True)
    recetteglobal=models.IntegerField(db_column='Recette',blank=True, null=True)
    reamrque = models.TextField(db_column='Remarque', null=True, blank=True)
    creepar = models.CharField(db_column='CreateurEtat', max_length=100, blank=True, null=True,verbose_name="Createur de Budget journalier'")
    modifierpar = models.CharField(db_column='QuiModifEtat', max_length=100, blank=True, null=True,verbose_name="Modificateur de Budget journalier")

    def __str__(self):
        return "{}".format(self.datejournee)
    class Meta:
        verbose_name="Budget Journalier"



class RecetteMagasinJr(models.Model):
    id_budgetj=models.ForeignKey(to='BudgetJournalier',on_delete=models.CASCADE,db_column='id_budgetJ', blank=True, null=True,related_name='linked_budgetsjrs')
    id_article=models.ForeignKey(to='Article',on_delete=models.CASCADE,db_column='id_articleBJ', blank=True, null=True,related_name='linked_articles',verbose_name="article")
    quantitout=models.IntegerField(db_column='QteOuted',blank=True, null=True,verbose_name="Quantite Vendu")
    montantrecette=models.IntegerField(db_column='MontantArticle',blank=True, null=True,verbose_name="Montant de recette par article")

    class Meta:
        verbose_name="Recettes de Magasin"
        db_table = 'Recettes_Magasin'
    def save(self,*args,**kwargs):
        if self.id_budgetj and self.id_budgetj.pk:
            super().save(*args, **kwargs)


class DepenseMagasinJr(models.Model):
    id_budgetj=models.ForeignKey(to='BudgetJournalier',on_delete=models.CASCADE,db_column='id_budgetJ', blank=True, null=True,related_name='linked_budgets')
    naturedepense=models.TextField(db_column='NatureDepense', null=True, blank=True,verbose_name="Nature de depenses")
    montantdepense=models.IntegerField(db_column='MontantDepense',blank=True, null=True,verbose_name="Montant de depenses")

    class Meta:
        verbose_name="Depenses de Magasin"
        db_table = 'Depenses_Magasin'
    def save(self,*args,**kwargs):
        if self.id_budgetj and self.id_budgetj.pk:
            super().save(*args, **kwargs)




########################################################################################################################
@receiver(post_save, sender=StockGlobal)
def initialize_quantiteglobalstock(sender, instance, created, **kwargs):
    if created:
        instance.quantiteglobalstock = 0
        instance.save()
@receiver(post_save, sender=StockMagasin)
def initialize_quantitestockmagasin(sender, instance, created, **kwargs):
    if created:
        instance.quantitemagasin = 0
        instance.save()