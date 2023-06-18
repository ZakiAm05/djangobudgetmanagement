from jet.dashboard.modules import DashboardModule



class pointhaut_map(DashboardModule):
    title = "budget par jour"
    template = './nombre_reliquats.html'
    grid="l6"

class Nombre_budgetenreg(DashboardModule):
    title = "Nombres de budget"
    template = './Nombre_pointhauts.html'
    grid="l6"


