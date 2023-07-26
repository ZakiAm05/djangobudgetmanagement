from jet.dashboard.modules import DashboardModule



class continous_recette_depense(DashboardModule):
    title = "recette et depense derneier 5 jour continue"
    template = './recettedepensecontinu.html'
    grid="l6"

class Nombre_budgetenreg(DashboardModule):
    title = "Nombres de budget"
    template = './Nombre_pointhauts.html'
    grid="l6"


