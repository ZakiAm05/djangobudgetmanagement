from django.db import models


class Budget(models.Model):
    dateBudget=models.DateField(db_column='DateBudget')
    depense=models.IntegerField(db_column='Depense',blank=True, null=True)
    recette=models.IntegerField(db_column='Recette',blank=True, null=True)
    reamrque = models.TextField(db_column='Remarque', null=True, blank=True)
    creepar = models.CharField(db_column='CreateurEtat', max_length=100, blank=True, null=True,verbose_name="Createur de Budget journalier'")
    modifierpar = models.CharField(db_column='QuiModifEtat', max_length=100, blank=True, null=True,verbose_name="Modificateur de Budget journalier")

    def __str__(self):
        return "{}".format(self.dateBudget)
    class Meta:
        verbose_name="Budget Journalier"