from django.db import models
from django.contrib.auth.models import User
from django.views import View
# Modèle représentant un client
class Costumer(models.Model):
    # Types de sexe disponibles pour un client
    Sex_type = (
        (' M ', 'Male'),
        (' F ','Femele'),
         
    )
    
    # Champs du modèle Costumer
    name = models.CharField(max_length=100)  # Nom du client
    email = models.EmailField()  # Email du client
    phone = models.CharField(max_length=15)  # Téléphone du client
    address = models.TextField()  # Adresse du client
    city = models.CharField(max_length=50)  # Ville du client
    state = models.CharField(max_length=50)  # État du client9
    zip_code = models.CharField(max_length=10)  # Code postal du client
    sex = models.CharField(max_length=7, choices=Sex_type)  # Sexe du client
    created_at = models.DateTimeField(auto_now_add=True)  # Date de création du client
    save_b = models.ForeignKey(User, on_delete=models.PROTECT)  # Utilisateur qui a enregistré le client

    class Meta:
        db_table = ''  # Nom de la table dans la base de données
        managed = True  # Indique si Django doit gérer la table
        verbose_name = 'Costumer'  # Nom singulier du modèle
        verbose_name_plural = 'Costumers'  # Nom pluriel du modèle

    def __str__(self):
        return self.name  # Représentation en chaîne de caractères du modèle

# Modèle représentant une facture
class Invoice(models.Model):
    # Statuts disponibles pour une facture
    INNVOICE_STATUS = (
        ('R', 'RECU'),
        ('P', 'PROFAMA FACTURE'),
        ('F', 'FACTURE'),
    )
    
    # Champs du modèle Invoice
    Costumer = models.ForeignKey(Costumer, on_delete=models.PROTECT)  # Client associé à la facture
    save_b = models.ForeignKey(User, on_delete=models.PROTECT)  # Utilisateur qui a enregistré la facture
    invoice_date_time = models.DateTimeField(auto_now_add=True)  # Date et heure de la facture
    invoice_type = models.CharField(max_length=1, choices=INNVOICE_STATUS)  # Type de la facture
    total = models.DecimalField(max_digits=500, decimal_places=2)# Total de la facture
    last_update = models.DateTimeField(null=True, blank=True)  # Dernière mise à jour de la facture
    paid = models.BooleanField(default=False)  # Indique si la facture est payée
    comment = models.TextField(null=True, max_length=1000, blank=True)  # Commentaire sur la facture

    class Meta:
        db_table = ''  # Nom de la table dans la base de données
        managed = True  # Indique si Django doit gérer la table
        verbose_name = 'Invoice'  # Nom singulier du modèle
        verbose_name_plural = 'Invoices'  # Nom pluriel du modèle

    def __str__(self):
        return self.invoice_date_time, self.Costumer.name  # Représentation en chaîne de caractères du modèle
    @property
    def get_total(self):
        articles = self.article_set.all()   
        total = sum(article.get_total for article in articles)
        return total    



# Modèle représentant un article dans une facture
class Article(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='articles')
    name = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=1000, decimal_places=2)
    class Meta:
        db_table = ''  # Nom de la table dans la base de données
        managed = True  # Indique si Django doit gérer la table
        verbose_name = 'Article'  # Nom singulier du modèle
        verbose_name_plural = 'Articles'  # Nom pluriel du modèle

    @property
    def get_total(self):
        total = self.quantity * self.unit_price   
        return total   
