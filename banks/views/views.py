from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as login_user, \
                                logout as logout_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import FormView, CreateView, DeleteView, UpdateView 
from django.views.generic import DetailView
from django.views.generic.list import ListView

from django.http import JsonResponse, HttpResponse
from dis import dis 
import inspect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.urls import resolve
from django.contrib.auth import update_session_auth_hash



from banks.forms.BankForm import BankForm
from banks.forms.BranchForm import BranchForm
from banks.models.banks import Bank
from banks.models.branches import Branch





# adding bank to database 
class AddBankView(LoginRequiredMixin, CreateView):
    model = Bank
    form_class = BankForm
    template_name = 'banks/create.html'
    success_url = reverse_lazy('banks:bank_details')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, 'Bank created successfully.')
        return super().form_valid(form)
    
    def get_object(self):
        return self.request.user.id
    
    def get_success_url(self):
        return reverse('banks:bank_details', args=[self.object.pk])
    
    # to handle the case where a non-loggedin User tries to edit branch info of a branch 
    def handle_no_permission(self):
        return HttpResponse(status=401)






# getting current banks details 

class ShowDetailView(DetailView):
    model = Bank
    template_name = 'banks/detail.html'
    success_url = reverse_lazy('banks:bank_details')

    # I could've re implemented get_object() for this class but I realized if I just override this
    # attribute, instead of looking for a pk variable in the url (in the base get_object() method) it will look for the bank_id variable
    # which is what we want instead of the "pk" variable 
    pk_url_kwarg = "bank_id"


    # the base get_object() method already takes care of the 404 error (when the specified bank does not exist)
    def get_success_url(self):
        

        # here we are passing in the argument to the url that requires bank_id 
        # we do this by first accessing it using the self.object.pk parameter
        return reverse('banks:bank_details', args=[self.object.pk])
    

# get all banks 

class ListAllBanksView(ListView): 
    model = Bank
    template_name = 'banks/list.html'










# add a branch 

class AddBranchView(CreateView):
    model = Branch
    form_class = BranchForm
    template_name = 'banks/createbranch.html'
    pk_url_kwarg = "bank_id"
    # success_url = reverse_lazy('banks:branch_details')



    def dispatch(self, request, *args, **kwargs):

        # get the bank_id from the url
        bank_id = self.kwargs['bank_id']
        

        # get the bank from the bank_id & assign it to this branch's bank attribute 
        self.bank = get_object_or_404(Bank, pk=bank_id) # takes care of the 404 error || self.bank is just so we have access to the Bank object in this View

        # this checks if the user is loggedin or not, if not loggedin (you should not be able to add a branch) hence 401 error
        if not self.request.user.is_authenticated:
            return HttpResponse(status=401)

        # validate if the bank owner is the same as the loggedin user - user A cannot add a branch for a bank owned by user B hence 403 forbidden
        if self.bank.owner != self.request.user: # self.request.user is always the loggedin user
            return HttpResponse(status=403)


        return super().dispatch(request, *args, **kwargs)
    

    def form_valid(self, form):

        # set the bank foreign key for the branch
        form.instance.bank = self.bank # this view takes BranchForm, BranchForm takes Branch

        print(type(form.instance), 'lets get piped')
        
        messages.success(self.request, 'Branch created successfully.')
        return super().form_valid(form)

    def get_success_url(self):
        # redirect to the bank details page for the bank associated with the new branch


        # return reverse('banks:bank_details', args=[self.object.bank.pk])
        return reverse('banks:branch_details', kwargs={'branch_id': self.object.id})
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['bank_id2'] = self.bank.pk
        return context
    

    # to handle the case where a non-loggedin User tries to edit branch info of a branch 
    def handle_no_permission(self):
        return HttpResponse(status=401)


    
# getting branch details 

def branchdetails(request, branch_id):
    """ """
    # resolve the url to get the int value of the branch
    # resolved_url = resolve(request.path_info)
    # branch_id = resolved_url.kwargs['branch_id']

    # retrieve the branch 
    branch = get_object_or_404(Branch, pk=branch_id)


    # serialize the data
    data = {
        "id": branch.id,
        "name": branch.name,
        "transit_num": branch.transit_num,
        "address": branch.address,
        "email": branch.email,
        "capacity": branch.capacity,
        "last_modified": branch.last_modified.isoformat(),
    }

    return JsonResponse(data, status=200)


# get all branches 

# function based view to get all branches for a given bank 
def branchall(request, bank_id):

    # get the bank
    bank2 = get_object_or_404(Bank, pk=bank_id)

    # get all the branches from the database 
    branches = Branch.objects.filter(bank=bank2)
    allbranches = []
    for branch in branches: 
        data = {
        "id": branch.id,
        "name": branch.name,
        "transit_num": branch.transit_num,
        "address": branch.address,
        "email": branch.email,
        "capacity": branch.capacity,
        "last_modified": branch.last_modified.isoformat(),
        }
        allbranches.append(data)
    
    return JsonResponse(allbranches, status=200, safe=False)


# class based view to get get all branches for a given bank 
class ListAllBranchesView(ListView): 
    model = Branch
    # pk_url_kwarg = "bank_id"
    # template_name = 'banks/listbranch.html' - dont need template name since we are rendering a Jsonresponse 


    def get_queryset(self):
        
        # every 
        bank2 = get_object_or_404(Bank, pk=self.kwargs['bank_id'])

        
        # list of all btanches with bank_id=bank2.id
        branches = Branch.objects.filter(bank=bank2)


        return branches
    
    def render_to_response(self, context, **response_kwargs):
        
        # its an object and not a dict
        branches = context['object_list'] # listView automatically gives object_list in the context

        # values turns the query_set object into a quersyset object, that we need to typecast to list() 
        branch_list_of_dicts = list(branches.values('id', 'name', 'transit_num', 'address', 'email', 'capacity', 'last_modified'))
        

        return JsonResponse(branch_list_of_dicts, safe=False, status=200)
    
    
    

    









# editing a branches details 
# PROBLEMS 
# - 
class BranchEditView(LoginRequiredMixin, UpdateView):
    # this should just take us to a JSON update version of this branch 
    model = Branch
    form_class = BranchForm
    template_name = 'banks/edit_branch.html'
    # success_url = reverse_lazy('accounts:branch_details') # how do I pass in a keyword argument here? A: override get_success_url()
    pk_url_kwarg = "branch_id"
    

    # to take care of the case where a loggedin user tries to change the branch_info of a branch he doesnt own 
    def dispatch(self, request, *args, **kwargs):

        # get the branch_id from the url
        branch_id = self.kwargs['branch_id']

        # get branch from branch_id
        branch = get_object_or_404(Branch, pk=branch_id)

        # from branch, get bank
        self.bank = get_object_or_404(Bank, pk=branch.bank.id)

        # this is to check whether the current user is loggedin or not, needed to add this since line 281 was being executed for this edge case, where 403 is not what applies there  
        # line 281 is strictly for when the loggedin user is not the one who owns the bank for which we create this bank 
        if not self.request.user.is_authenticated:
            return HttpResponse(status=401)

        # validate if the bank owner is the same as the loggedin user - if not return a 403 error 
        if self.bank.owner != self.request.user: # self.request.user is always the loggedin user
            return HttpResponse(status=403)
        
        return super().dispatch(request, *args, **kwargs)
    

    def form_valid(self, form):
        return super().form_valid(form)
    
    # to ensure the data is prefilled 
    # get_object must get an instance of the model from the database if we want prefilled data 
    def get_object(self, queryset=None):

        # "Branch.objects.filter(id=self.kwargs['branch_id'])" gets us a Queryset instead of an instance 
        branch = Branch.objects.get(id=self.kwargs['branch_id'])

        return branch

    # override this to pass in the keyword argument 
    def get_success_url(self): 
        return reverse('banks:branch_details', args=[self.kwargs['branch_id']])
    
    # to handle the case where a non-loggedin User tries to edit branch info of a branch 
    def handle_no_permission(self):
        return HttpResponse(status=401)
    
    # to pass in the keyword argument to the template 
    def get_context_data(self, **kwargs):

        # get the context 
        context = super().get_context_data(**kwargs)

        # add the branch_id into the context as branch_id2
        context['branch_id2'] = self.kwargs['branch_id']

        return context


