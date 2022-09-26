from .models import LatestNews, Downloads,CytoInfo, Data_submission, Drugs, Diseases, Cases
from django.shortcuts import render, get_object_or_404
from django.db.models.aggregates import Count
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.views.generic import ListView
from django.db.models import Q
from django.http import *
from django.utils import timezone
import collections
import json
from django.views.decorators.cache import cache_page
from .tables import BrowseTable, AdvTable
from django_tables2 import RequestConfig

def CSKD_index(request):
    news = LatestNews.objects.all().order_by('-Date_edited')
    all_paginator = Paginator(news, per_page=5)
    page = request.GET.get('page')
    try:
        sets = all_paginator.page(page)
    except PageNotAnInteger:
        sets = all_paginator.page(1)
    except EmptyPage:
        sets = all_paginator.page(all_paginator.num_pages)

    return render(request, 'Index.html', {'sets':sets})

#Simple search
def simple_search(request):
    q = request.GET.get('q')

    if not q:
        err_msg = "Please enter keywords for search!"
        return render(request, 'search_results.html', {'err_msg':err_msg})
    else:
        nq = q.split(' ')
        a_list = Q(CRS_type__icontains=nq[0])
        for i in nq[1:]:
            a_list.add(Q(CRS_type__icontains=nq[0]), a_list.connector)
        queryset = Cases.objects.filter(a_list).distinct()
        counts = queryset.count()
        all_cases = BrowseTable(queryset)
        RequestConfig(request, paginate={"per_page": 10}).configure(all_cases)

        return render(request, 'search_results.html', {'sets':all_cases, 'counts':counts})

#tutorial

def tutorial(request):
    return render(request, 'Tutorial.html')

#Contact us
def contact(request):
    return render(request, 'Contact_us.html')

#About us
def about_us(request):
    return render(request, 'About_us.html')

#advanced search res
def adv_search_res(request):
    all_data = CytoInfo.objects.all().order_by('Gene_name')

    #paginator
    all_paginator = Paginator(all_data, per_page=10)
    page = request.GET.get('page')

    try:
        sets = all_paginator.page(page)
    except PageNotAnInteger:
        sets = all_paginator.page(1)
    except EmptyPage:
        sets = all_paginator.page(all_paginator.num_pages)

    all_source = []
    all_family = []
    all_protein_name = []

    for i in all_data:
        source_genes = i.Gene_name
        families = i.Family_name
        protein_names = i.Protein_name

        all_source.append(source_genes)
        all_family.append(families)
        all_protein_name.append(protein_names)


    all_protein_name = list(set(all_protein_name))
    all_family = list(set(all_family))

    inquiry_json = collections.OrderedDict()
    inquiry_json['code'] = ''
    inquiry_json['message'] = ''
    if request.method == 'GET':
        if request.is_ajax():
            actions = request.GET.get('action')
            if actions == 'filter_gene':
                tar_genes = request.GET.get('inquiry_list')
                if not tar_genes:
                    inquiry_json['code'] = -1
                    inquiry_json['message'] = "Please enter gene names!"
                    return JsonResponse(json.dumps(inquiry_json), safe=False)
                else:
                    inquiry_json['code'] = 1
                    g_list = tar_genes.split(',')
                    info_list = Q(Gene_name__icontains=g_list[0])
                    for i in g_list[1:]:
                        info_list.add(Q(Gene_name__icontains=i), info_list.connector)
                    queryset = all_data.filter(info_list)

                    return JsonResponse(json.dumps(inquiry_json), safe=False)



    return render(request, 'adv_search_res.html', {'all_data':all_data, 'all_source':all_source, 'all_family':all_family, 'all_protein_name':all_protein_name, 'sets':sets})


#adv search clinical
def adv_search(request):
    all_data = Cases.objects.all().order_by('Article_type')
    all_crs = []
    all_dis = []
    all_pat = []
    all_the = []
    for case in all_data:
        all_crs.append(case.CRS_type.split(';'))
        all_dis.append(case.Disease.split(';'))
        all_pat.append(case.Pathogens.split(';'))
        all_the.append(case.Immune_therapy_associated.split(';'))
    all_crs_set = set([crs.lower() for c in all_crs for crs in c])
    all_dis_set = set([dis.lower() for d in all_dis for dis in d])
    all_pat_set = set([pat.lower() for p in all_pat for pat in p])
    all_the_set = set([the.lower() for t in all_the for the in t])


    #paginator
    all_paginator = Paginator(all_data, per_page=10)
    page = request.GET.get('page')

    try:
        sets = all_paginator.page(page)
    except PageNotAnInteger:
        sets = all_paginator.page(1)
    except EmptyPage:
        sets = all_paginator.page(all_paginator.num_pages)

    return render(request, 'adv_search.html', {'sets':sets, 'crs_sets':all_crs_set, 'all_crs_set':all_crs_set, 'all_dis_set':all_dis_set, 'all_pat_set':all_pat_set, 'all_the_set':all_the_set})

def adv_search_clinical_res(request):

    if request.method == "GET":
        queryset = Cases.objects.filter(Article_type__icontains="Case Report")
        q_crs = request.GET.get('crs_selected')
        q_gender = request.GET.get('gender')
        q_cause_the = request.GET.get('cause_the_search')
        q_cause_pat = request.GET.get('cause_pat_search')
        q_cause_dis = request.GET.get('cause_dis_search')

        c_reactive_protein = request.GET.get('c_reactive_protein')
        erythrocyte_sedimentation_rate = request.GET.get('erythrocyte_sedimentation_rate')
        procalcitonin = request.GET.get('procalcitonin')
        leucocytes = request.GET.get('leucocytes')
        neutrophils = request.GET.get('neutrophils')
        lymphocytes = request.GET.get('lymphocytes')
        platelets = request.GET.get('platelets')
        haemoglobin = request.GET.get('haemoglobin')
        prothrombin_time = request.GET.get('prothrombin_time')
        fibrinogen = request.GET.get('fibrinogen')
        d_dimer = request.GET.get('D-dimer')
        activated_partial_thromboplastin_time = request.GET.get('activated_partial_thromboplastin_time')
        thrombin_time = request.GET.get('thrombin_time')
        creatinine = request.GET.get('creatinine')
        lactate_dehydrogenase = request.GET.get('lactate_dehydrogenase')
        alanine_transferase = request.GET.get('alanine_transferase')
        aspartate_transferase = request.GET.get('aspartate_transferase')
        triglyceride = request.GET.get('triglyceride')
        serum_ferritin = request.GET.get('serum_ferritin')
        soluble_CD25 = request.GET.get('soluble_CD25')
        if q_gender == 'male':
            queryset = Cases.objects.filter(Q(Male__gte=1),
                                            Q(CRS_type__icontains=q_crs),
                                            Q(Disease__icontains=q_cause_dis),
                                            Q(Pathogens__icontains=q_cause_pat),
                                            Q(Immune_therapy_associated__icontains=q_cause_the),
                                            Q(C_reactive_protein__icontains=c_reactive_protein),
                                            Q(Erythrocyte_sedimentation_rate__icontains=erythrocyte_sedimentation_rate),
                                            Q(Procalcitonin__icontains=procalcitonin),
                                            Q(Leucocytes__icontains=leucocytes),
                                            Q(Neutrophils__icontains=neutrophils),
                                            Q(Lymphocytes__icontains=lymphocytes),
                                            Q(Platelets__icontains=platelets),
                                            Q(Haemoglobin__icontains=haemoglobin),
                                            Q(Prothrombin_time__icontains=prothrombin_time),
                                            Q(Fibrinogen__icontains=fibrinogen),
                                            Q(D_dimer__icontains=d_dimer),
                                            Q(Activated_partial_thromboplastin_time__icontains=activated_partial_thromboplastin_time),
                                            Q(Thrombin_time__icontains=thrombin_time),
                                            Q(Creatinine__icontains=creatinine),
                                            Q(Lactate_dehydrogenase__icontains=lactate_dehydrogenase),
                                            Q(Alanine_transferase__icontains=alanine_transferase),
                                            Q(Aspartate_transferase__icontains=aspartate_transferase),
                                            Q(Triglyceride__icontains=triglyceride),
                                            Q(Serum_ferritin__icontains=serum_ferritin),
                                            Q(Soluble_CD25__icontains=soluble_CD25),
                                            )
        elif q_gender == 'female':
            queryset = Cases.objects.filter(Q(Female__gte=1),
                                            Q(CRS_type__icontains=q_crs),
                                            Q(Disease__icontains=q_cause_dis),
                                            Q(Pathogens__icontains=q_cause_pat),
                                            Q(Immune_therapy_associated__icontains=q_cause_the),
                                            Q(C_reactive_protein__icontains=c_reactive_protein),
                                            Q(Erythrocyte_sedimentation_rate__icontains=erythrocyte_sedimentation_rate),
                                            Q(Procalcitonin__icontains=procalcitonin),
                                            Q(Leucocytes__icontains=leucocytes),
                                            Q(Neutrophils__icontains=neutrophils),
                                            Q(Lymphocytes__icontains=lymphocytes),
                                            Q(Platelets__icontains=platelets),
                                            Q(Haemoglobin__icontains=haemoglobin),
                                            Q(Prothrombin_time__icontains=prothrombin_time),
                                            Q(Fibrinogen__icontains=fibrinogen),
                                            Q(D_dimer__icontains=d_dimer),
                                            Q(Activated_partial_thromboplastin_time__icontains=activated_partial_thromboplastin_time),
                                            Q(Thrombin_time__icontains=thrombin_time),
                                            Q(Creatinine__icontains=creatinine),
                                            Q(Lactate_dehydrogenase__icontains=lactate_dehydrogenase),
                                            Q(Alanine_transferase__icontains=alanine_transferase),
                                            Q(Aspartate_transferase__icontains=aspartate_transferase),
                                            Q(Triglyceride__icontains=triglyceride),
                                            Q(Serum_ferritin__icontains=serum_ferritin),
                                            Q(Soluble_CD25__icontains=soluble_CD25),

                                            )
        else:
            queryset = Cases.objects.filter(Q(CRS_type__icontains=q_crs),
                                            Q(Disease__icontains=q_cause_dis),
                                            Q(Pathogens__icontains=q_cause_pat),
                                            Q(Immune_therapy_associated__icontains=q_cause_the),
                                            Q(C_reactive_protein__icontains=c_reactive_protein),
                                            Q(Erythrocyte_sedimentation_rate__icontains=erythrocyte_sedimentation_rate),
                                            Q(Procalcitonin__icontains=procalcitonin),
                                            Q(Leucocytes__icontains=leucocytes),
                                            Q(Neutrophils__icontains=neutrophils),
                                            Q(Lymphocytes__icontains=lymphocytes),
                                            Q(Platelets__icontains=platelets),
                                            Q(Haemoglobin__icontains=haemoglobin),
                                            Q(Prothrombin_time__icontains=prothrombin_time),
                                            Q(Fibrinogen__icontains=fibrinogen),
                                            Q(D_dimer__icontains=d_dimer),
                                            Q(Activated_partial_thromboplastin_time__icontains=activated_partial_thromboplastin_time),
                                            Q(Thrombin_time__icontains=thrombin_time),
                                            Q(Creatinine__icontains=creatinine),
                                            Q(Lactate_dehydrogenase__icontains=lactate_dehydrogenase),
                                            Q(Alanine_transferase__icontains=alanine_transferase),
                                            Q(Aspartate_transferase__icontains=aspartate_transferase),
                                            Q(Triglyceride__icontains=triglyceride),
                                            Q(Serum_ferritin__icontains=serum_ferritin),
                                            Q(Soluble_CD25__icontains=soluble_CD25),

                                            )
    all_cases = AdvTable(queryset)
    RequestConfig(request, paginate={"per_page": 10}).configure(all_cases)
    return render(request, 'adv_search_clincal_res.html', {'queryset':all_cases })


#download
def downloads(request):
    files = Downloads.objects.all()
    return render(request, 'Download.html', {'files':files})
#submit
def submit_data(request):
    responses = collections.OrderedDict()
    responses['code'] = ''
    responses['message'] = ''
    if request.method == 'POST':
        if request.is_ajax():
            try:
                s_name = request.POST.get('S_name')
                s_organization = request.POST.get('S_organization')
                s_email = request.POST.get('S_email')
                s_cytokines = request.POST.get('S_cytokines')
                s_PMID = request.POST.get('S_PMID')
                s_description = request.POST.get('S_description')
                submission = Data_submission(Name=s_name, Organization=s_organization, E_mail=s_email, Cytokine_names=s_cytokines, PMID=s_PMID, Description=s_description)
                submission.save()

                responses['code'] = '1'
                responses['message'] = 'Your data has been submitted successfully, Thank you!'
                return JsonResponse(json.dumps(responses), safe=False)
            except Exception as e:
                responses['code'] = '-1'
                responses['message'] = str(e)
                return JsonResponse(json.dumps(responses), safe=False)

    return render(request, 'Submit.html')

#cytoscape_network
def network_construction(request):
    all_data = CytoInfo.objects.all()
    gene_list = []
    target_list = []
    for i in all_data:
        gene_list.append(i.Gene_name)
        target_list.append(i.Target_name)

    target_pool = []
    all_bi_tuple = []
    for li in target_list:
        target_pool.append(li.split(","))

    for k in range(len(gene_list)):
        for j in range(len(target_pool[k])):
            all_bi_tuple.append((gene_list[k], target_pool[k][j]))

    relationships = json.dumps(all_bi_tuple)

    s_tar =','.join(str(x) for x in target_list)
    s_sour = ','.join(str(y) for y in gene_list)
    all_genes_str =s_tar+','+s_sour
    all_genes_list = list(set(all_genes_str.split(",")))

    style_res = collections.OrderedDict()
    style_res['code'] = ""
    style_res['style'] = ""
    style_res['sg'] = ""
    if request.method == "GET":
        if request.is_ajax():
            specific_gene = request.GET.get('specific_gene_list')
            actions = request.GET.get('action')
            if actions == 'change_style':
                tar_style = request.GET.get('new_style')
                tar_style = str(tar_style).lower()
                style_res['code'] = 1
                style_res['style'] = tar_style
                style_res['sg'] = specific_gene.split(',')
                return JsonResponse(json.dumps(style_res), safe=False)
            if actions == 'specific_genes_highlights':
                tar_style = request.GET.get('new_style')
                tar_style = str(tar_style).lower()
                style_res['code'] = 2
                style_res['style'] = tar_style
                style_res['sg'] = specific_gene.split(',')
                return JsonResponse(json.dumps(style_res), safe=False)
    return render(request, 'Network.html', {'relationships':relationships, 'genes':all_genes_list, 'source_genes':gene_list.sort(), 'source_genes':gene_list})

#Functional enrichment

def functional_enrichment(request):
    return render(request, 'Enrichment.html')

#browse


def browse(request):
    all_cases = BrowseTable(Cases.objects.all().order_by('-Year'))
    RequestConfig(request, paginate={"per_page": 10}).configure(all_cases)

    return render(request, 'Browse.html', {'sets':all_cases})

#Gene detailed

def gene_detailed(request, slug):
    gene_detail = get_object_or_404(CytoInfo, slug=slug)
    tar_gene_name = gene_detail.Gene_name
    case_all = Cases.objects.all()
    satisfied_list = []
    for case in case_all:
        if tar_gene_name in case.Cytokines_involved or tar_gene_name in case.Cytokine_down or tar_gene_name in case.Cytokine_up:
            satisfied_list.append(case.PMID)
    if satisfied_list == []:
        satisfied_list = "None"


    return render(request, 'Cytokine_detail.html', {'gene_detail':gene_detail, 'satisfied_list':satisfied_list, 'methods':tar_gene_name, 'satisfied_list':satisfied_list})

#case_detail

def case_detail(request, slug):
    case_info = get_object_or_404(Cases, slug=slug)
    exps = case_info.Experiment_methods.split(';')
    cyto_invol = case_info.Cytokines_involved.split(';')
    cyto_in_up = case_info.Cytokines_involved_up.split(';')
    cyto_in_down = case_info.Cytokines_involved_down.split(';')
    cyto_in_other = case_info.Cytokines_involved_other.split(';')
    symptoms = case_info.Symptoms.split(';')
    disease_induced = case_info.Disease_induced.split(';')
    return render(request, 'Case_detail.html', {'case_info':case_info, 'exps':exps, 'cyto_invol':cyto_invol, 'cyto_in_up':cyto_in_up, 'cyto_in_down':cyto_in_down, 'cyto_in_other':cyto_in_other, 'symptoms':symptoms, 'disease_induced':disease_induced})

#404 error
def page_not_found(request, exception):

    return render(request, '404.html')

#测试
def testpage(request):
    ttt = CytoInfo.objects.all()
    objs_paginator = Paginator(ttt, per_page=1)
    page = request.GET.get('page')

    try:
        sets = objs_paginator.page(page)
    except PageNotAnInteger:
        sets = objs_paginator.page(1)
    except EmptyPage:
        sets = objs_paginator.page(objs_paginator.num_pages)
    return render(request, 'test.html', {'sets':sets})


