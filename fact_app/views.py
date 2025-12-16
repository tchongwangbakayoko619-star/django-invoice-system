from django.shortcuts import render
from django.views import View
from .models import *  # Importation des modèles
from django.contrib import messages  # Pour afficher des messages de succès ou d'erreur
from django.db import transaction  # Pour gérer les transactions de base de données
from decimal import Decimal  # Pour manipuler les nombres décimaux
from .util import pagination ,get_invoice  # Importation d'une fonction utilitaire pour la pagination
import pdfkit  # Pour générer des fichiers PDF
from django.template.loader import get_template  # Pour charger des templates
from django.http import HttpResponse  # Pour gérer les réponses HTTP
from .decorators import *
from django.utils.translation import gettext as _  # Pour la traduction des chaînes de caractèresz
# Classe pour gérer la vue de la page d'accueil
class HomeView(SuperuserRequiredMixin,View):
    templates_name = 'index.html'  # Nom du template à utiliser pour cette vue
    invoices = Invoice.objects.select_related('Costumer', 'save_b').all()  # Récupération de toutes les factures avec leurs relations
    context = {'invoices': invoices}  # Contexte initial contenant les factures

    # Méthode pour gérer les requêtes GET
    def get(self, request, *ags, **kwargs):
        # Appel de la fonction de pagination pour paginer les factures
        item = pagination(request, self.invoices)
        self.context['invoices'] = item  # Mise à jour du contexte avec les factures paginées
        return render(request, self.templates_name, self.context)  # Rendu du template avec le contexte

    # Méthode pour gérer les requêtes POST
    def post(self, request, *ags, **kwargs):
       
        if request.POST.get('id_supprimer'):
            # Suppression d'une facture
            try:
                
                invoice_id = request.POST.get('id_supprimer')
                print(invoice_id)
                invoice = Invoice.objects.get(id=invoice_id)  # Récupération de la facture à supprimer
                invoice.delete()  # Suppression de la facture
                invoice.article.all().delete()  # Suppression des articles associés à la facture
               
                messages.success(request, _("Invoice deleted successfully"))  # Message de succès
            except Exception as e:
                # Gestion des erreurs
                messages.error(request, f"Sorry, our system detected the following issues: {e}") 
        if request.POST.get('id_modified'):
            paid=request.POST.get('modified')  # Récupération du statut de paiement
            try:
                # Récupération de la facture à modifier
                invoice = Invoice.objects.get(id=request.POST.get('id_modified'))
                if paid:
                    invoice.paid = True
                    invoice.save() 
                else:
                    invoice.paid = False
                    invoice.save()  # Enregistrement des modifications
                messages.success(request,_("Invoice modified successfully") )  # Message de succès
            except Exception as e:
                # Gestion des erreurs
                messages.error(request, f"Sorry, our system detected the following issues: {e}")
        # Appel de la fonction de pagination pour paginer les factures
        item = pagination(request, self.invoices)
        self.context['invoices'] = item  # Mise à jour du contexte avec les factures paginées
        return render(request, self.templates_name, self.context)  # Rendu du template avec le contexte

# Classe pour gérer l'ajout d'un nouveau client
class AddView(SuperuserRequiredMixin,View):
    templates_name = 'add_Costumer.html'  # Nom du template à utiliser pour cette vue

    # Méthode pour gérer les requêtes GET
    def get(self, request, *ags, **kwargs):
        return render(request, self.templates_name)  # Rendu du formulaire pour ajouter un client

    # Méthode pour gérer les requêtes POST
    def post(self, request, *ags, **kwargs):
        # Récupération des données du formulaire
        data = {
            'name': request.POST.get('name'),
            'email': request.POST.get('email'),
            'phone': request.POST.get('phone'),
            'address': request.POST.get('address'),
            'state': request.POST.get('state'),
            'city': request.POST.get('city'),
            'zip_code': request.POST.get('Zip'),
            'sex': request.POST.get('sex'),
            'save_b': request.user  # Utilisateur qui a enregistré le client
        }
        try:
            # Création d'un nouveau client
            created = Costumer.objects.create(**data)
            if created:
                messages.success(request, "Customer added successfully")  # Message de succès
            else:
                messages.error(request, "Sorry, try again. The sent data is corrupt")  # Message d'erreur
        except Exception as e:
            # Gestion des erreurs
            messages.error(request, f"Sorry, our system detected the following issues: {e}")
        return render(request, self.templates_name)  # Rendu du formulaire après soumission

# Classe pour gérer l'ajout d'une nouvelle facture
class AddInvoiceView(SuperuserRequiredMixin,View):
    templates_name = 'add_invoice.html'  # Nom du template à utiliser pour cette vue
    customers = Costumer.objects.select_related('save_b').all()  # Récupération de tous les clients
    context = {'customers': customers}  # Contexte initial contenant les clients

    # Méthode pour gérer les requêtes GET
    def get(self, request, *args, **kwargs):
        return render(request, self.templates_name, self.context)  # Rendu du formulaire pour ajouter une facture

    # Méthode pour gérer les requêtes POST (avec gestion des transactions)
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        item = []  # Liste pour stocker les articles de la facture
        try:
            # Récupération des données du formulaire
            paid = request.POST.get('paid')  # Statut de paiement
            costumer_id = request.POST.get('customer')  # ID du client
            invoice_type = request.POST.get('invoice_type')  # Type de facture
            articles = request.POST.getlist('article')  # Liste des noms d'articles
            prices = request.POST.getlist('price')  # Liste des prix unitaires
            quantities = request.POST.getlist('quantity')  # Liste des quantités
            totals = request.POST.getlist('total')  # Liste des totaux
            grand_total = request.POST.get('grand_total')  # Total général
            comment = request.POST.get('comment')  # Commentaire

            # Récupération de l'objet client
            costumer = Costumer.objects.get(id=costumer_id)

            # Création de l'objet facture
            invoice_object = {
                'Costumer': costumer,
                'invoice_type': invoice_type,
                # 'total': grand_total,  # Ce champ est commenté, vérifier s'il est nécessaire
                'comment': comment,
                'save_b': request.user,  # Utilisateur qui a enregistré la facture
                'paid': paid
            }
            invoice = Invoice.objects.create(**invoice_object)  # Création de la facture

            # Boucle pour créer les objets Article associés à la facture
            for index, article in enumerate(articles):
                data = Article(
                    invoice=invoice,
                    name=article,
                    quantity=Decimal(quantities[index]),
                    unit_price=Decimal(prices[index]),
                    total=Decimal(totals[index])
                )
                item.append(data)

            # Création des objets Article en une seule fois
            Article.objects.bulk_create(item)

            # Message de succès
            messages.success(request, "Invoice added successfully")
        except Costumer.DoesNotExist:
            # Gestion du cas où le client n'existe pas
            messages.error(request, "The selected customer does not exist.")
        except Exception as e:
            # Gestion des autres erreurs
            messages.error(request, f"An error occurred: {e}")

        # Rendu du formulaire après soumission
        return render(request, self.templates_name, self.context)
class InvoiceDetailView(View,SuperuserRequiredMixin):
    templates_name = 'invoice-template.html'  # Nom du template à utiliser pour cette vue

    # Méthode pour gérer les requêtes GET
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        context = get_invoice(pk)  # Récupération de la facture et de ses articles
        return render(request, self.templates_name, context)
@login_superuser_required    
def get_invoice_pdf(request,*args, **kwargs):   
    pk=kwargs.get('pk')
    context=get_invoice(pk)  # Récupération de la facture et de ses articles
    template= get_template('invoicepdf.html')  # Chargement du template
    render= template.render(context)  # Rendu du template avec le contexte
    option={
        'page-size':'A4',
        'encoding':'UTF-8',
        'margin-top':'0.5in',
        'margin-right':'0.5in',
        'margin-bottom':'0.5in',
        'margin-left':'0.5in',
        'enable-local-file-access': None,  # Permet l'accès aux fichiers locaux
    }
     # Configuration de pdfkit avec le chemin de wkhtmltopdf
    config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe')
    pdf=pdfkit.from_string(render,False,options=option,configuration=config)  # Génération du PDF à partir du rendu
    reponse=HttpResponse(pdf,content_type='application/pdf')  # Création de la réponse HTTP avec le PDF
    reponse['Content-Disposition']=f'attachment;filename=invoice_{pk}.pdf'  # Définition du nom du fichier PDF
    return reponse  # Retour de la réponse HTTP contenant le PDF
    
    
       
        