from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication,permissions,generics
from .models import *



base_url="127.0.0.1:8000"

class PointhautsnbrApi(APIView):
    """ Home page for GRH REST-APIS it's alist of apis with détails how to use """
    result={
            "availableApis": {
                'nombre_budgetenreg': {
                    'arguments':{"title":'nombre_debudgets',},
                    'descriptions':"Le nombre total des budgets enregistrés",
                    #'Example': "http://{}/GRH/apis?title=sexe_par_structure&id_str=82".format(base_url),
                },

            }
        }
    # authentication_classes = [authentication.SessionAuthentication]
    # permission_classes = [permissions.DjangoModelPermissions]
    """it handels get requests and call the switcher to tell her witch api to use"""
    def get(self,request,format=None):
        param_args= self.request.query_params
        api_title = param_args.get("title")
        self.api_switch(api_title)
        return Response(self.result)

    """get the api title and select the corresponding Api logic."""
    def api_switch(self,api_title):
        if(api_title):
            if(api_title=="nombre_debudgets"):
                self.result=self.nombre_budgetenreg()
            else:
                self.result={"Exception":api_title+ " is not Available!"}
        else:
            return

    """Api that return Gender statistics in a given structur , if no structur were given it returns stats in all organisation"""
    def nombre_budgetenreg(self):
        param_args = self.request.query_params
        result={}
        assos=list(BudgetJournalier.objects.all())
        resultat = len(assos)
        result['nombres pointhauts']= resultat

        return result


######################################################################################################################
class DepenseRecetteChartApi(APIView):
    def get(self, request, format=None):
        # Calculate the date range for the last five days
        today = datetime.now().date()
        last_five_days = [today - timedelta(days=i) for i in range(5)]

        # Retrieve the depenseglobal and recetteglobal values for the last five days
        results = BudgetJournalier.objects.filter(datejournee__in=last_five_days) \
            .values('datejournee') \
            .annotate(depense=Sum('depenseglobal'), recette=Sum('recetteglobal'))

        # Prepare the data for the chart
        labels = [result['datejournee'].strftime('%Y-%m-%d') for result in results]
        depense_data = [result['depense'] for result in results]
        recette_data = [result['recette'] for result in results]

        # Return the data as a JSON response
        data = {
            'labels': labels,
            'depense': depense_data,
            'recette': recette_data
        }
        return Response(data)