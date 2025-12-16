from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import * # Importation des modèles
import datetime  # Pour manipuler les dates et heures

def pagination(request,invoices):
    default_page= 1
    page= request.GET.get('page',default_page)
    items_per_page=5
    paginator= Paginator(invoices,items_per_page)
    try:
        invoices= paginator.page(page)
    except PageNotAnInteger:
          invoices= paginator.page(default_page)
    except EmptyPage:
          invoices= paginator.page(paginator.num_pages)
    return invoices  
def get_invoice(pk):
    
        invoice = Invoice.objects.get(pk=pk)
        articles = invoice.article_set.all() # Récupération des articles associés à la facture
       
        context = {
            'obj':invoice,  # Facture à afficher
            'articles': articles  # Articles associés à la facture
        }
        context['date'] = datetime.datetime.now()  # Date actuelle pour l'affichage
        return context  # Retourne le contexte contenant la facture et ses articles
        
  
    