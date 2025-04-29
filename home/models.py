from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import datetime
from django.contrib.auth.models import User



class Azienda(models.Model):
    def set_path(self,filename):
            #c = Cantiere.objects.get(pk=self.cantiere_id)
            #a = c.cliente.azienda.codcf

            #albumname= re.sub('[^a-zA-Z0-9]+', '', an.nome)
            return str(self.codcf) +'/'+ filename # +albumname +'/'+filename
        
    nome = models.CharField(max_length=60, blank=True, null=True)
    codcf = models.CharField(max_length=60, blank=True, null=True,unique=True)

    logo = models.FileField(upload_to=set_path,null=True,blank=True)

    #logo = models.CharField(max_length=80,blank=True,null=True)
    #current = models.BooleanField(null=True,default=False)
    descrizione = models.TextField(blank=True, null=True)
    ragione_sociale = models.CharField(max_length=100, blank=True, null=True)
    indirizzo = models.CharField(max_length=100,blank=True, null=True)
    cap = models.CharField(max_length=20,blank=True, null=True)
    local = models.CharField(max_length=40,blank=True, null=True)
    prov = models.CharField(max_length=40,blank=True, null=True)
    codfisc = models.CharField(max_length=40,blank=True, null=True)
    partiva = models.CharField(max_length=40,blank=True, null=True)
    telefono = models.CharField(max_length=40, blank=True, null=True)
    cellulare = models.CharField(max_length=40, blank=True, null=True)
    pec = models.CharField(max_length=40, blank=True, null=True)
    fax = models.CharField(max_length=40, blank=True, null=True)
    email = models.EmailField(max_length=40, blank=True, null=True)
    resprap = models.CharField(max_length=40, blank=True, null=True)
    fmemo = models.TextField( blank=True, null=True)
    nome_pf = models.CharField(max_length=40, blank=True, null=True)
    cogn_pf = models.CharField(max_length=40, blank=True, null=True)
    #banca = models.CharField(max_length=40,blank=True, null=True)
    #iban = models.CharField(max_length=40,blank=True, null=True)

    def __str__(self):
        return self.nome

    class Meta:
        managed = True
        db_table = 'azienda'

    def GetFatture(self):

        clienti = self.azienda_cliente.all()
        cantieri=[]
        for one in clienti:
            c = one.cliente_cantiere.all()
            for a in c:
                cantieri.append(a)
        ordini=[]
        for one in cantieri:
            ord = one.cantiere_ordine.all()
            for a in ord:
                ordini.append(a)
        fatture=[]
        for one in ordini:
            fat = one.ordine_fatture.all()
            if fat:
                fatture.append(fat[0])
        return fatture
    
    def GetFattureInScadenza(self):

        fatture = self.GetFatture()
        today=datetime.today()
        fattInScadenza=[]
        for one in fatture:
            if one.data_scadenza >= today.date():
                fattInScadenza.append(one)
            #fattInScadenza = fatture.filter(data_scadenza__gte=today).order_by('data_scadenza')
        return fattInScadenza

    
    def getPersonale(self):
        personale = self.azienda_personale.all()
        return personale
    def getCantieri(self):
        clienti = self.azienda_cliente.all()
        cantieri_id=[]
        for one in clienti:
            c = one.cliente_cantiere.all()
            for a in c:
                cantieri_id.append(a.id)
        cantieri = Cantiere.objects.filter(id__in=cantieri_id)
        return cantieri
    def getOrdini(self):
        clienti = self.azienda_cliente.all()
        cantieri=[]
        for one in clienti:
            c = one.cliente_cantiere.all()
            for a in c:
                cantieri.append(a)
        ordini_id=[]
        for one in cantieri:
            ord = one.cantiere_ordine.all()
            for a in ord:
                ordini_id.append(a.id)
        ordini = Ordine.objects.filter(id__in=ordini_id)
        return ordini

class UsersAzienda(models.Model):
        user = models.ForeignKey(User,null=True,on_delete=models.CASCADE,related_name='userazienda')
        azienda = models.ForeignKey(Azienda,null=True,on_delete=models.CASCADE,related_name='aziendauser')
        
        class Meta:
            managed = True
            db_table = 'usersazienda'
        
class TipologiaLavori(models.Model):
    descrizione = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.descrizione

    class Meta:
        managed = True
        db_table = 'tipologia_lavori'





#CODPAG;DESC;RATAIVA;TIPORATE;GGSCDFIX;TIPOPAG;NUMRATE;GG1RATA;GGRATE;TIPOSCAD;GGFIXANT;GGDOPOFM
class CondizioniPagamento(models.Model):
   
    codpag = models.CharField(max_length=10,unique=True)
    desc = models.CharField(max_length=70, blank=True, null=True)
    rataiva = models.IntegerField(blank=True, null=True)
    tiporate = models.CharField(max_length=2,blank=True, null=True)
    ggscdfix = models.IntegerField(blank=True, null=True)
    tipopag = models.IntegerField(blank=True, null=True)
    numrate = models.IntegerField(blank=True, null=True)
    gg1rata = models.IntegerField(blank=True, null=True)
    ggrate = models.IntegerField(blank=True, null=True)
    tiposcad = models.CharField(max_length=3, blank=True, null=True)
    ggfixant = models.CharField(max_length=3, blank=True, null=True)
    ggdopofm = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'condizionipagamento'
    
#CLFR;CODCF;RAGSOC;RAGSOC1;INDIR;CAP;LOCAL;PROV;CODFISC;PARTIVA;CODPAG;PERSOC;TEL;TEL2;FAX;EMAIL;RESPRAP;FMEMO;NOME_PF;COGN_PF;SESSO;PEC_FE;BANCA


class Fornitori(models.Model):
    
    class ClienteFornitore(models.TextChoices):
        CLIENTE = "C"
        FORNITORE = "F"
    class Sesso(models.TextChoices):
        MASCHIO='M'
        FEMMINA='F'
    class PersonaSocieta(models.TextChoices):
        Persona='P'
        Societa='S'

#    clfr = models.CharField(max_length=2, choices=ClienteFornitore.choices,
#        default=ClienteFornitore.CLIENTE, blank=True, null=True)
    codcf = models.CharField(max_length=60, blank=True, null=True)
    ragione_sociale = models.CharField(max_length=100, blank=True, null=True)
    indirizzo = models.CharField(max_length=100,blank=True, null=True)
    cap = models.CharField(max_length=20,blank=True, null=True)
    local = models.CharField(max_length=40,blank=True, null=True)
    prov = models.CharField(max_length=40,blank=True, null=True)
    codfisc = models.CharField(max_length=40,blank=True, null=True)
    partiva = models.CharField(max_length=40,blank=True, null=True)
    descrizione = models.TextField(blank=True, null=True)
    #codpag = models.CharField(max_length=10, blank=True, default="", unique=True)
    codpag = models.ForeignKey(CondizioniPagamento,null=True,on_delete=models.CASCADE,related_name='pppp',to_field='codpag')
    persoc = models.CharField(max_length=2,blank=True, null=True,choices=PersonaSocieta.choices)

    telefono = models.CharField(max_length=40, blank=True, null=True)
    cellulare = models.CharField(max_length=40, blank=True, null=True)
    pec_fe = models.CharField(max_length=40, blank=True, null=True)
    fax = models.CharField(max_length=40, blank=True, null=True)
    email = models.CharField(max_length=40, blank=True, null=True)
    resprap = models.CharField(max_length=40, blank=True, null=True)
    fmemo = models.TextField( blank=True, null=True)
    nome_pf = models.CharField(max_length=40, blank=True, null=True)
    cogn_pf = models.CharField(max_length=40, blank=True, null=True)
    sesso = models.CharField(max_length=2, blank=True, null=True,choices=Sesso.choices)

    banca = models.CharField(max_length=40,blank=True, null=True)
    iban = models.CharField(max_length=40,blank=True, null=True)
    azienda = models.ForeignKey(Azienda,null=True,on_delete=models.CASCADE,related_name='azienda_fornitore')

    def __str__(self):
        return self.codcf
    class Meta:
        managed = True
        db_table = 'fornitori'

class Sesso(models.TextChoices):
        MASCHIO='M'
        FEMMINA='F'

class Cliente(models.Model):
    class ClienteFornitore(models.TextChoices):
        CLIENTE = "C"
        FORNITORE = "F"
    
    class PersonaSocieta(models.TextChoices):
        Persona='P'
        Societa='S'

#    clfr = models.CharField(max_length=2, choices=ClienteFornitore.choices,
#        default=ClienteFornitore.CLIENTE, blank=True, null=True)
    codcf = models.CharField(max_length=60, blank=True, null=True)
    ragione_sociale = models.CharField(max_length=100, blank=True, null=True)
    indirizzo = models.CharField(max_length=100,blank=True, null=True)
    cap = models.CharField(max_length=20,blank=True, null=True)
    local = models.CharField(max_length=40,blank=True, null=True)
    prov = models.CharField(max_length=40,blank=True, null=True)
    codfisc = models.CharField(max_length=40,blank=True, null=True)
    partiva = models.CharField(max_length=40,blank=True, null=True)
    persoc = models.CharField(max_length=2,blank=True, null=True,choices=PersonaSocieta.choices)

    telefono = models.CharField(max_length=40, blank=True, null=True)
    cellulare = models.CharField(max_length=40, blank=True, null=True)
    pec_fe = models.CharField(max_length=40, blank=True, null=True)
    fax = models.CharField(max_length=40, blank=True, null=True)
    email = models.CharField(max_length=40, blank=True, null=True)
    fmemo = models.TextField( blank=True, null=True)
    nome_pf = models.CharField(max_length=40, blank=True, null=True)
    cogn_pf = models.CharField(max_length=40, blank=True, null=True)
    sesso = models.CharField(max_length=2, blank=True, null=True,choices=Sesso.choices)

    #banca = models.CharField(max_length=40,blank=True, null=True)
    #iban = models.CharField(max_length=40,blank=True, null=True)
    
    azienda = models.ForeignKey(Azienda,null=True,on_delete=models.CASCADE,related_name='azienda_cliente')

    def __str__(self):
        return self.codcf

    class Meta:
        managed = True
        db_table = 'cliente'

    def getSesso(self):
        
        return getattr(self.Countries, self.name)

#class AziendeClienti(models.Model):
#    azienda = models.ForeignKey(Azienda,null=True,on_delete=models.CASCADE,related_name='azienda')
#    cliente = models.ForeignKey(Cliente,null=True,on_delete=models.CASCADE,related_name='cliente')

#    class Meta:
##        managed = True
#        db_table = 'aziendeclienti'

class Cantiere(models.Model):
    nome   = models.CharField(max_length=40, blank=True, null=True)
    descrizione = models.TextField(blank=True, null=True)
    ubicazione = models.CharField(max_length=100, blank=True, null=True)
    status = models.BooleanField(null=True,default=True)
    valore_commessa =  models.DecimalField(max_digits=14,blank=True,null=True,decimal_places=2) #MoneyField(max_digits=14, decimal_places=2, default_currency='EUR')
    data_inizio_lavori = models.DateField(blank=True, null=True)
    data_fine_lavori = models.DateField(blank=True, null=True)
    cliente = models.ForeignKey(Cliente,null=True,on_delete=models.CASCADE,related_name='cliente_cantiere')

    def __str__(self):
        return self.nome
    class Meta:
        managed = True
        db_table = 'cantiere'

    def GetOrdini(self):
        ordini = self.cantiere_ordine.all()
        return ordini
    
    def GetFatture(self):
        ordini = self.GetOrdini()
        f_id=[]
        for one in ordini:
            f = one.ordine_fatture.all()
            if f:
                f_id.append(f[0].id)
        fatture = Fatture.objects.filter(id__in=f_id)
        return fatture
    
    def GetPersonale(self):

        pers_ass = self.cantiere_assegnato.all()
        pers = []
        for one in pers_ass:
            pers.append(one.personale)
        return pers
    
    def getResponsabile(self):
        pers_ass = self.cantiere_assegnato.all()
        pers = []
        for one in pers_ass:
            if one.responsabile:
                return one.personale
            #pers.append(one.personale)
        return None

class Personale(models.Model):
    
    nome = models.CharField(max_length=40, blank=True, null=True)
    cognome = models.CharField(max_length=40, blank=True, null=True)
    tipologia_lavoro = models.ForeignKey(TipologiaLavori,null=True,on_delete=models.CASCADE,related_name='tipolavoro_personale')
    responsabile = models.BooleanField(null=False,default=False)
    #ore_lavorate =  models.DecimalField(max_digits=5,blank=True,null=True,decimal_places=2) 
    wage_lordo = models.DecimalField(max_digits=19,blank=True,null=True,decimal_places=2) 
    wage_netto = models.DecimalField(max_digits=19,blank=True,null=True,decimal_places=2) 

    azienda = models.ForeignKey(Azienda,null=True,on_delete=models.CASCADE,related_name='azienda_personale')

    def __str__(self):
        return self.cognome
    
    class Meta:
        managed = True
        db_table = 'personale'

    def assegnato_a(self):
        
        return self.personale_assegnato.all()
    
class Assegnato_Cantiere(models.Model):
        personale = models.ForeignKey(Personale,null=True,on_delete=models.CASCADE,related_name='personale_assegnato')
        cantiere = models.ForeignKey(Cantiere,null=True,on_delete=models.CASCADE,related_name='cantiere_assegnato')
        responsabile = models.BooleanField(null=False,default=False)
        ore_lavorate =  models.DecimalField(max_digits=5,blank=True,null=True,default=0.0,decimal_places=2) 

        def __str__(self):
            return self.personale.cognome
        
        class Meta:
            unique_together = ('personale', 'cantiere')
            managed = True
            db_table = 'assegnato_cantiere'
            
        def totale_lordo(self):
            tl = self.ore_lavorate * self.personale.wage_lordo
            return tl
        def totale_netto(self):
            tl = self.ore_lavorate * self.personale.wage_netto
            return tl




class Ordine(models.Model):
    
    """
    class TipologiaFornitore(models.TextChoices):
        SERVIZIO = "SE",_("Servizio")
        MATERIALE = "MA",_("Materiale")
        MACCHINARI = "NO",_("Noleggio")
        
        def __str__(self):
            return self.value
    """
    TipologiaFornitore =(
        ('SE','SERVIZIO'),
        ('MA','MATERIALE'),
        ('NO','NOLEGGIO')
    )
    data_ordine = models.DateField(blank=True, null=True)
    importo = models.DecimalField(max_digits=14,blank=True,null=True,decimal_places=2) #MoneyField(max_digits=14, decimal_places=2, default_currency='EUR',default=0.0)
    fornitore = models.ForeignKey(Fornitori,null=True,on_delete=models.CASCADE,related_name='fornitori_ordine')
    cantiere = models.ForeignKey(Cantiere,null=True,on_delete=models.CASCADE,related_name='cantiere_ordine')
    mestesso = models.BooleanField(null=False,default=False)
    magazzino = models.BooleanField(null=False,default=False)
    tipologia = models.CharField(max_length=2, choices=TipologiaFornitore) #,
                    #default=TipologiaFornitore.MATERIALE, blank=True, null=True)

    def __str__(self):
        return str(self.id)+'_'+str(self.data_ordine)

    class Meta:
        managed = True
        db_table = 'ordine'




class Articoli(models.Model):
    descrizione = models.TextField(blank=True, null=True)
    quantita = models.IntegerField(blank=True, null=True)
    prezzo_unitario = models.DecimalField(max_digits=19,blank=True,null=True,decimal_places=2)
    importo_totale = models.DecimalField(max_digits=19,blank=True,null=True,decimal_places=2) #MoneyField(max_digits=14, decimal_places=2, default_currency='EUR')
    ordine = models.ForeignKey(Ordine,null=True,on_delete=models.CASCADE,related_name='ordine_articoli')


    class Meta:
        managed = True
        db_table = 'articoli'

class Magazzino(models.Model):
    quantita = models.IntegerField(blank=True, null=True)
    descrizione = models.TextField(blank=True, null=True)
    quantita = models.IntegerField(blank=True, null=True)
    prezzo_unitario = models.DecimalField(max_digits=19,blank=True,null=True,decimal_places=2)
    importo_totale = models.DecimalField(max_digits=19,blank=True,null=True,decimal_places=2) 
    azienda = models.ForeignKey(Azienda,null=True,on_delete=models.CASCADE,related_name='azienda_magazzino')

    class Meta:
        managed = True
        db_table = 'magazzino'


class Fatture(models.Model):
    ragione_sociale = models.CharField(max_length=100, blank=True, null=True)
    n_fattura = models.CharField(db_column='n_fattura', max_length=40, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    data_fattura = models.DateField(blank=True, null=True)
    importo =  models.DecimalField(max_digits=14,blank=True,null=True,decimal_places=2)#MoneyField(max_digits=14, decimal_places=2, default_currency='EUR')
    pagato =  models.DecimalField(max_digits=14,blank=True,null=True,decimal_places=2)#MoneyField(max_digits=14, decimal_places=2, default_currency='EUR')
    data_scadenza = models.DateField(blank=True, null=True)
    ordine = models.ForeignKey(Ordine,null=True,on_delete=models.CASCADE,related_name='ordine_fatture')

    class Meta:
        managed = True
        db_table = 'fatture'








