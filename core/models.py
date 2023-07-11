from django.db import models

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
    def save(self,*args,**kwargs):
        if self.id_stockglobal and self.id_stockglobal.pk:
            super().save(*args, **kwargs)
class BudgetJournalier(models.Model):
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