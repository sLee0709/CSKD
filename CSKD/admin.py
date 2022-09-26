from django.contrib import admin
from .models import LatestNews,Downloads,CytoInfo, Data_submission, Drugs, Diseases, Cases

@admin.register(LatestNews)
class LatestNewsAdmin(admin.ModelAdmin):
    list_display = ('Title', 'Date_created', 'Date_edited')
    list_per_page = 10
    list_filter = ('Date_created',)

@admin.register(Downloads)
class DownloadsAdmin(admin.ModelAdmin):
    list_display = ['F_name','F_upload','Date_uploaded','Date_modified']
    list_filter = ('Date_modified',)

@admin.register(CytoInfo)
class GGIAdmin(admin.ModelAdmin):
    list_display = ['Gene_name','Family_name','Target_name']
    list_per_page = 20
    list_filter = ('Biomarkers',)
    search_fields = ['Gene_name', 'Family_name', 'Target_name']

@admin.register(Data_submission)
class DataSubmissionAdmin(admin.ModelAdmin):
    list_display = ['Cytokine_names','Name','Organization','E_mail','Date_uploaded','Date_modified']

@admin.register(Drugs)
class DrugAdmin(admin.ModelAdmin):
    list_display = ['Drug_name', 'Drug_type','Synonyms', 'Other_info']
    list_filter = ('Drug_type',)

@admin.register(Diseases)
class DiseaseAdmin(admin.ModelAdmin):
    list_display = ['Disease_name','Other_names']

@admin.register(Cases)
class CaseAdmin(admin.ModelAdmin):
    list_display = ['PMID']