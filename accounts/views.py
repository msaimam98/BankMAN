from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as login_user, \
                                logout as logout_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import FormView, CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from .forms import LoginForm, SignupForm, EditProfileForm
from django.http import JsonResponse, HttpResponse
from dis import dis 
import inspect
from django.contrib.auth import update_session_auth_hash




# LOGIN, LOGOUT, AND REGISTER VIEWS 
class LoginView(FormView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    # this URL sends us to their profile page
    success_url = reverse_lazy('accounts:profile_view')

    def form_valid(self, form):
        login_user(self.request, form.cleaned_data['user'])
        self.request.session['from'] = 'login'
        return super().form_valid(form)


class SignupView(CreateView):
    form_class = SignupForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')
    
    # note that ModelForm saves object automatically
    def form_valid(self, form):
        self.request.session['from'] = 'register' 
        return super().form_valid(form)
    
def logout(request):
    logout_user(request)
    request.session['from'] = 'logout'
    return redirect(reverse('accounts:login'))


# just need this view for the delete buttons on the admin.html page - dont need!!!
class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = User
    login_url = reverse_lazy('accounts:login')
    success_url = reverse_lazy('accounts:admin')
    

@login_required(login_url=reverse_lazy('accounts:login'))
def admin(request):
    keyword = request.GET.get('filter', '')
    return render(request, "accounts/admin.html", {
        'user_list' : User.objects.filter(username__icontains=keyword),
    })


















# PROFILE VIEWS 

def profile(request):
    """ """

    # first we get the user 
    # then we serialize his data (only id, username, email, firstname, lastname)
    # return a json response


    # is_authenticated is a read-only attribute which is always True 
    # (as opposed to AnonymousUser.is_authenticated which is always False). This is a way to tell if the user has been authenticated.
    # Note: if the current user in self.request.user is loggedin, django will see it has a User, otherwise as AnonymousUser
     
    # took care of the 401 error 
    if request.user.is_authenticated:
        data = {
        'id': request.user.id,
        'username': request.user.username,
        'email': request.user.email, 
        'first_name': request.user.first_name,
        'last_name': request.user.last_name
        }
    else: 
        return HttpResponse("UNAUTHORIZED", status=401)
    
    return JsonResponse(data, status=200)


class ProfileEditView(UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('accounts:profile_view')

    def dispatch(self, request, *args, **kwargs):

        # check if the user trying to access this URL is loggedin, if not then return 401 unauthorized error 
        if not self.request.user.is_authenticated:
            return HttpResponse(status=401)

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):

        # form.instance gets us the User 
        # if a new password was submitted, it will be in the cleaned_data (without errors ofcourse), else it wont
        if 'password1' in form.cleaned_data and 'password1' != '':

            new_password = form.cleaned_data['password1']
            
            if len(new_password) > 0:
                form.instance.set_password(new_password)

            # what does this do? this is updating the authentication hash
            # so what happens is when the password is changed using line 125, the current users session auth hash changes 
            # according to django, this user is no longer logged in (becomes AnonymousUser) therefore we need to update the session authentication hash 
            # where we are setting the new password 
            update_session_auth_hash(self.request, form.instance)
        
        # self.request.session['from'] = 'profile_edit' - we dont need this, just tells template that 
        # you are being rendered from profile_edit
        return super().form_valid(form)
    
    def get_object(self, queryset=None):
        # print(self.request.user.email, 'bruhhhhhhh')
        return self.request.user
    
    































































    # override the get and post methods for this form view 

    # def get(self, request, *args, **kwargs):
        
    #     # what django does in the UpdateView Class is retrieve the current user 
    #     # 1st way: retrieve the object that is specified in the url 
    #     # 2nd way: we override the get_object() method and pass in the current user by passing in self.request.user

    #     # Note that the line below is in BaseUpdateView Class, wherein it uses the first way if we dont override the get_object method 
    #     self.object = self.get_object()

    #     # if request.method == "GET" --> we need to pass in the values already 
    #     my_form = self.form_class(instance=self.request.user)
        
    #     # print(self.get_context_data(form=my_form), 'hello maaaaan')
    #     context = self.get_context_data(form=my_form)
        
    #     context['form'] = my_form
    #     to_return = self.render_to_response(context)


    #     return to_return
    









































    



    


























