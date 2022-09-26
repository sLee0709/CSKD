from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from allauth.models import *
from imagekit.models import ProcessedImageField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
import time
from datetime import date



#model for latest news
class LatestNews(models.Model):
    Title = models.CharField('News Title', max_length=100)
    Slug = models.SlugField('Slug', unique=True, default=time.strftime('%Y-%m-%d_%H_%M_%S'))
    Content = models.TextField('News Content', max_length=500, default="Please enter your news content here.")
    Date_created = models.DateTimeField('Created Date', auto_now_add=True)
    Date_edited = models.DateTimeField('Last Edited Date', auto_now=True)

    class Meta:
        verbose_name = 'Latest News'
        verbose_name_plural = verbose_name
        ordering = ['Date_created']

    def __str__(self):
        return self.Title

#model for downloads
class Downloads(models.Model):
    F_name = models.CharField('File Name', max_length=100)
    F_description = models.TextField('File Description', max_length=300)
    F_upload = models.FileField('Upload File', upload_to='download_files')
    Date_uploaded = models.DateTimeField('First Uploaded Date', auto_now_add=True)
    Date_modified = models.DateTimeField('Last Modified Date', auto_now=True)

    class Meta:
        verbose_name = 'Downloads'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.F_name

#drug model
class Drugs(models.Model):
    Drug_name = models.CharField('Drug Name', max_length=100)
    Drug_type = models.CharField('Type', max_length=100)
    Drug_target = models.CharField('Targets', max_length=150, default='NA')
    Drug_des = models.TextField('Drug Description', max_length=1000)
    Structure = ProcessedImageField(upload_to='drug_imgs', default='drug_imgs/404.jpg', verbose_name='Structure')
    Synonyms = models.CharField('Synonyms', max_length=500)
    Other_info = models.CharField('More Information', max_length=1000)
    slug = models.SlugField('Slug', unique=False, default="Must be unique")

    class Meta:
        verbose_name = 'Drug Information'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.Drug_name

#disease model
class Diseases(models.Model):
    Disease_name = models.CharField('Disease Name', max_length=100)
    Other_names = models.TextField('Synonym', max_length=500, blank=True)
    External_links_OMIM = models.CharField('OMIM ID', max_length=15, blank=True)
    External_links_DOID = models.CharField('Disease Ontology ID', max_length=10, blank=True)
    symptoms = models.CharField('Symptoms', max_length=200, blank=True)
    Description = models.TextField('Other Information', max_length=1000)
    slug = models.SlugField('Slug', unique=False, default="Must be unique")

    class Meta:
        verbose_name = 'Disease Information'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.Disease_name

#model for gene-gene interaction
class CytoInfo(models.Model):
    Gene_name = models.CharField('Gene Name', max_length=10, default='')
    Protein_name = models.CharField('Protein Name', max_length=100, default='Unknown')
    Family_name = models.CharField('Family', max_length=50, default='Unknown')
    Function = models.TextField('Function', max_length=1000, default='Please describe its function here...')
    Biomarkers = models.BooleanField(default=False)
    Target_name = models.CharField('Targets', max_length=300, default='Unknown')
    slug = models.SlugField('Slug', unique=False, default="Must be unique")

    class Meta:
        ordering = ['Gene_name']
        verbose_name = 'Cytokine Information'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.Gene_name



#detailed information for specific cases
class Cases(models.Model):
    PMID = models.CharField('PMID', max_length=15)
    Year = models.CharField('Year', max_length=4)
    Article_type = models.CharField('Article Type', max_length=30, default='NA')
    CRS_type = models.CharField('CRS Type', max_length=100, default='NA')
    Source = models.CharField('Source', max_length=50, default='NA')
    Homo_sapiens = 'HS'
    Mus_musculus = 'MM'
    Rattus_norvegicus = 'RN'
    Cell_lines = 'CL'
    Other = 'OT'
    Organism_choices = [(Homo_sapiens, 'Homo sapiens'), (Mus_musculus, 'Mus musculus'), (Rattus_norvegicus, 'Rattus norvegicus'), (Cell_lines, 'Cell Line'),(Other, 'Other'),]
    Organism = models.CharField('Organism', max_length=2, choices=Organism_choices, default=Homo_sapiens)
    Cell_lines = models.CharField('Cell lines', max_length=50, default='NA', blank=True)
    Race = models.CharField('Races', max_length=50, default='NA', blank=True)
    Number = models.IntegerField(default=0, blank=True)
    Male = models.IntegerField(default=0, blank=True)
    Female = models.IntegerField(default=0, blank=True)
    Age = models.CharField('Age range', max_length=15, default='* - *', blank=True)
    Experiment_methods = models.CharField('Experiments', max_length=150, default='NA')
    Disease = models.CharField('Diseases', max_length=150, blank=True)
    Disease_stages = models.CharField('Disease Stages', max_length=30, default='NA')
    Pathogens = models.CharField('Pathogens', max_length=50, default='NA')
    Immune_therapy_associated = models.CharField('Immune Therapy Associated', max_length=30, blank=True)
    Drug_associated = models.CharField('Drugs Associated', max_length=50, blank=True)
    Drug_associated_dose = models.CharField('Drug Associated Dose', max_length=30, blank=True)
    Cytokines_involved = models.CharField('Cytokine Involved', max_length=100, blank=True)
    Cytokines_involved_up = models.CharField('Cytokine Involved Up', max_length=50, blank=True)
    Cytokines_involved_down = models.CharField('Cytokine Involved Down', max_length=50, blank=True)
    Cytokines_involved_other = models.CharField('Cytokine Involved Other', max_length=50, blank=True)
    Symptoms = models.CharField('Symptoms', max_length=300, blank=True)
    Disease_induced = models.CharField('Disease Induced', max_length=100, blank=True)
    Increased = 'Inc'
    Decreased = 'Dec'
    Normal = 'Norm'
    NotMention = 'NM'
    index_choices = [(Increased, 'Increased'),(Decreased,'Decreased'),(Normal,'Normal'),(NotMention, 'Not Mentioned'),]
    C_reactive_protein = models.CharField('C-Reactive Protein', max_length=4, choices=index_choices, default=NotMention)
    Serum_ferritin = models.CharField('Serum Ferritin', max_length=4, choices=index_choices, default=NotMention)
    Procalcitonin = models.CharField('Procalcitonin', max_length=4, choices=index_choices, default=NotMention)
    Erythrocyte_sedimentation_rate = models.CharField('Erythrocyte Sedimentation Rate', max_length=4, choices=index_choices, default=NotMention)
    Leucocytes = models.CharField('Leucocytes', max_length=4, choices=index_choices, default=NotMention)
    Neutrophils = models.CharField('Neutrophils', max_length=4, choices=index_choices, default=NotMention)
    Lymphocytes = models.CharField('Lymphocytes', max_length=4, choices=index_choices, default=NotMention)
    Platelets = models.CharField('Platelets', max_length=4, choices=index_choices, default=NotMention)
    Haemoglobin = models.CharField('Haemoglobin', max_length=4, choices=index_choices, default=NotMention)
    Activated_partial_thromboplastin_time = models.CharField('Activated Partial Thromboplastin Time', max_length=4, choices=index_choices, default=NotMention)
    Prothrombin_time = models.CharField('Prothrombin Time', max_length=4, choices=index_choices, default=NotMention)
    Thrombin_time = models.CharField('Thrombin Time', max_length=4, choices=index_choices, default=NotMention)
    D_dimer = models.CharField('D-Dimer', max_length=4, choices=index_choices, default=NotMention)
    Fibrinogen = models.CharField('Fibrinogen', max_length=4, choices=index_choices, default=NotMention)
    Triglyceride = models.CharField('Triglyceride', max_length=4, choices=index_choices, default=NotMention)
    Soluble_CD25 = models.CharField('Soluble CD25', max_length=4, choices=index_choices, default=NotMention)
    Alanine_transferase = models.CharField('Alanine Transferase (ALT)', max_length=4, choices=index_choices, default=NotMention)
    Aspartate_transferase = models.CharField('Aspartate Transferase (AST)', max_length=4, choices=index_choices, default=NotMention)
    Lactate_dehydrogenase = models.CharField('Lactate Dehydrogenase (LDH)', max_length=4, choices=index_choices, default=NotMention)
    Creatinine = models.CharField('Creatinine (CR/Cre)', max_length=4, choices=index_choices, default=NotMention)
    Temperature = models.CharField('Temperature', max_length=10, blank=True)
    Is_biomarker_reported = models.BooleanField(default=False)
    biomarkers = models.CharField(max_length=100, default='NA')
    NA = 'NA'
    Prediction = 'PR'
    Treatment = 'TR'
    Diagnosis = 'DI'
    Prognosis = 'PG'
    Others = 'OT'
    Biomarker_type_choice = [(Prediction, 'Prediction'), (Treatment, 'Treatment'),(Diagnosis, 'Diagnosis'), (Prognosis, 'Prognosis'), (NA,'NA'), (Others,'Other'),]
    Biomarker_type = models.CharField('Biomarker Type', choices=Biomarker_type_choice, max_length=2, default=NA)
    Drug_for_treatment = models.CharField('Drugs', max_length=100, blank=True)
    Treatment_target = models.CharField('Treatment Targets', max_length=50, blank=True)
    Treatment_dose = models.CharField('Treatment Dose', max_length=30, blank=True)
    Treatment_time = models.CharField('Treatment Time', max_length=10, blank=True)
    Other_treatments = models.CharField('Other Treatment', max_length=30, blank=True)
    Other_treatment_targets = models.CharField('Other Treatment Targets', max_length=50, blank=True)
    Cytokine_up = models.CharField('Cytokine Up', max_length=50, blank=True)
    Cytokine_down = models.CharField('Cytokine Down', max_length=50, blank=True)
    Disease_history = models.TextField('Disease History', max_length=300, default='NA')
    Drug_treatment_history = models.TextField('Drug Treatment History', max_length=300, default='NA')
    Family_history = models.TextField('Family Health History', max_length=300, default='NA')
    Discharge_time = models.CharField('Discharge Time', max_length=10, blank=True)
    Adverse_event = models.TextField('Adverse_event', max_length=100, blank=True)
    Survival_description = models.TextField('Survival Description', max_length=300, blank=True)
    Date_uploaded = models.DateTimeField('First Uploaded Date', auto_now_add=True)
    Date_modified = models.DateTimeField('Last Modified Date', auto_now=True)
    slug = models.SlugField('Slug', unique=False, default="Must be unique")

    class Meta:
        verbose_name = 'Cases'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.PMID

#data_submission
class Data_submission(models.Model):
    Cytokine_names = models.CharField('Cytokines', max_length=100)
    Name = models.CharField('Name', max_length=100)
    Organization = models.CharField('Organization', max_length=150, default='Unknown')
    E_mail = models.CharField('E-mail', max_length=100)
    PMID = models.CharField('PMID', max_length=100)
    Description = models.TextField("Description", max_length=500)
    Date_uploaded = models.DateTimeField('First Uploaded Date', auto_now_add=True)
    Date_modified = models.DateTimeField('Last Modified Date', auto_now=True)
    class Meta:
        verbose_name = "Data Submission"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.Name