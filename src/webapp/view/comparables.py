from django.shortcuts import redirect
from django.shortcuts import render

from src.WebAppraisal.forms import *
from src.WebAppraisal.zillow1 import *




def search_view(request):
    if request.method == "POST":
        if 'search_comps' in request.POST:
            form = ComparableSearchForm(request.POST)
            if form.is_valid():
                zip_code = form.cleaned_data.get('zip')
                return redirect('/comparables/' + str(zip_code))
            else:
                return render(request, 'comparable_search.html', context={'errors': True, 'form': ComparableSearchForm()})

        else:
            return redirect('/comparables')
    else:
        form = ComparableSearchForm()
    return render(request, "comparable_search.html", {"form": form })


def comparables_results_view(request, zip_code):
    comparables_list = find_my_comparables(zip_code)
    return render(request, "comparable_results.html", context={'comparables': comparables_list, 'errors': False})