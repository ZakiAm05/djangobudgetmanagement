# Generated by Django 3.0.6 on 2023-07-11 18:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_entreestockglobal'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='stockglobal',
            options={'verbose_name': 'Stock Global'},
        ),
        migrations.RemoveField(
            model_name='entreestockglobal',
            name='id_stockglobal',
        ),
        migrations.AddField(
            model_name='budgetjournalier',
            name='magasin',
            field=models.ForeignKey(blank=True, db_column='MagasinInBJ', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='linked_magasins', to='core.Magasin'),
        ),
        migrations.AddField(
            model_name='entreestockglobal',
            name='id_stockmagasin',
            field=models.ForeignKey(blank=True, db_column='StockGlobalArticle', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='linked_stocks', to='core.StockGlobal'),
        ),
        migrations.CreateModel(
            name='StockMagasin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libellestockmagasin', models.CharField(blank=True, db_column='LibelleMagasin', max_length=250, null=True, verbose_name='Libelle de Stock Magasin')),
                ('quantitemagasin', models.IntegerField(blank=True, db_column='QteMagasin', null=True, verbose_name='Quantite Article Dans Magasin')),
                ('article', models.ForeignKey(blank=True, db_column='ArticleInStock', null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Article', verbose_name='Article')),
                ('magasin', models.ForeignKey(blank=True, db_column='MagasinStock', null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Magasin', verbose_name='Magasin')),
            ],
            options={
                'verbose_name': 'Stock Magasin',
            },
        ),
        migrations.CreateModel(
            name='RecetteMagasinJr',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantitout', models.IntegerField(blank=True, db_column='QteOuted', null=True, verbose_name='Quantite Vendu')),
                ('montantrecette', models.IntegerField(blank=True, db_column='MontantArticle', null=True, verbose_name='Montant de recette par article')),
                ('id_article', models.ForeignKey(blank=True, db_column='id_articleBJ', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='linked_articles', to='core.Article', verbose_name='article')),
                ('id_budgetj', models.ForeignKey(blank=True, db_column='id_budgetJ', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='linked_budgetsjrs', to='core.BudgetJournalier')),
            ],
            options={
                'verbose_name': 'Recettes de Magasin',
                'db_table': 'Recettes_Magasin',
            },
        ),
        migrations.CreateModel(
            name='EntreeStockMagasin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateentredmg', models.DateField(blank=True, db_column='DateEntreeStckMg', null=True, verbose_name='Date Entree Au Stock Magasin')),
                ('quantiteentredmg', models.IntegerField(blank=True, db_column='QteEntredMg', null=True, verbose_name='Quantite Entree Au Stock Magasin')),
                ('id_stockmagasin', models.ForeignKey(blank=True, db_column='StockMagasinArticle', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='linked_magasinstocks', to='core.StockMagasin')),
            ],
            options={
                'verbose_name': 'Entree Au Stock de Magasin',
                'db_table': 'Entree_Stock_Magasin',
            },
        ),
        migrations.CreateModel(
            name='DepenseMagasinJr',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naturedepense', models.TextField(blank=True, db_column='NatureDepense', null=True, verbose_name='Nature de depenses')),
                ('montantdepense', models.IntegerField(blank=True, db_column='MontantDepense', null=True, verbose_name='Montant de depenses')),
                ('id_budgetj', models.ForeignKey(blank=True, db_column='id_budgetJ', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='linked_budgets', to='core.BudgetJournalier')),
            ],
            options={
                'verbose_name': 'Depenses de Magasin',
                'db_table': 'Depenses_Magasin',
            },
        ),
    ]