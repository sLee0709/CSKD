import django_tables2 as tables
from .models import Cases
from django_tables2 import A

class BrowseTable(tables.Table):
    PMID = tables.LinkColumn('case_detail', args=[A('PMID')], attrs={'a': {'target': '_blank'}})
    class Meta:
        model = Cases
        fields = ("PMID", "Year", "Article_type", "CRS_type", "Organism", "Source")
        template_name = 'django_tables2/semantic.html'

class AdvTable(tables.Table):
    Detail = tables.LinkColumn('case_detail', text='Link', args=[A('PMID')], attrs={'a': {'target': '_blank', 'style':'font-weight: bold', 'class':'ui mini grey button'}})

    class Meta:
        model = Cases
        fields = ("PMID", "Year", "Article_type", "Age", "CRS_type", "Organism")
        template_name = 'django_tables2/semantic.html'