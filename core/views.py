from django.shortcuts import render
from django.utils import timezone
from .models import *




def etat_budgets(request,id):
    etatjournalier=Budget.objects.get(pk=id)
    # dmd=DemandeAbsence.objects.get(pk=id).prefetch_related('aprovers')
    date=timezone.now().date()


    context = {
        "etatjournalier":  etatjournalier,
        "date": date,
    }

    return render(request, "Reports/Etat.html", context)
