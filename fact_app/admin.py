from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Costumer, Invoice, Article

# Définir l'interface d'administration pour le modèle Costumer
class CostumerAdmin(admin.ModelAdmin):
    # Champs à afficher dans la vue liste
    list_display = ['name', 'email', 'phone', 'address', 'city', 'state', 'zip_code', 'sex']
    # Champs à filtrer dans la vue liste
    list_filter = ['city', 'state', 'zip_code']
    # Champs à rechercher dans la vue liste
    search_fields = ['name', 'email', 'phone']
    # Nombre d'éléments à afficher par page
    list_per_page = 10

# Définir l'interface d'administration pour le modèle Invoice
class InvoiceAdmin(admin.ModelAdmin):
    # Champs à afficher dans la vue liste
    list_display = ['Costumer', 'save_b', 'invoice_date_time', 'invoice_type', 'total', 'last_update', 'paid']
    # Champs à filtrer dans la vue liste
    list_filter = ['invoice_date_time', 'invoice_type', 'last_update', 'paid']
    # Champs à rechercher dans la vue liste
    search_fields = ['Costumer', 'save_b', 'invoice_date_time', 'invoice_type', 'total', 'last_update', 'paid']
    # Nombre d'éléments à afficher par page
    list_per_page = 10

# Enregistrer le modèle Costumer avec l'interface d'administration
admin.site.register(Costumer, CostumerAdmin)

# Enregistrer le modèle Invoice avec l'interface d'administration
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Article)

# Traductions pour l'interface d'administration
class CustomAdminSite(admin.AdminSite):
    site_header = _("Bakayoko Facturation Admin")
    site_title = _("Bakayoko")
    index_title = _("Bienvenue dans l'interface d'administration de Facturation")

    def each_context(self, request):
        context = super().each_context(request)
        context['custom_css'] = 'admin/custom.css'
        return context

# Remplacez le site d'administration par défaut
admin.site = CustomAdminSite()