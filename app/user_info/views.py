# /app/user_info/views.py

import string, copy, math, json, random, base64
from email_validator  import validate_email

from django.core.mail import send_mail
from django.core.files.base import ContentFile
 
from django.http      import HttpResponse, HttpResponseRedirect, JsonResponse 
from django.shortcuts import render, redirect # Added for images
from django.template  import loader
from django.urls      import reverse
from django.db.models import Q # used to create complex database queries that involve logical operators such as OR, AND, and NOT
from django.conf      import settings
from django.contrib                 import messages
from django.contrib.auth            import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models     import User, Group
from django.contrib.auth.decorators import login_required

from user_info.models import UserInfo
from mygarden.models  import Garden
from plants.models    import MyPlant, MyPlantToDo

from .forms  import UserProfileForm, UserLoginForm, UserPwdResetForm, EmailVerificationForm

def user_profile_step1(request):
    """ Render the User Profile Page for Gateway Gardens app """
    if request.user.is_authenticated:
        profile_creation = False
    else:
        profile_creation = True

    if request.POST:
        form = UserProfileForm(request.POST)
        if form.is_valid():
            # ----------------------------------------------------------------------
            # Get profile information from request
            # ----------------------------------------------------------------------
            profile_username   = form.cleaned_data.get('profile_username')
            profile_password_1 = form.cleaned_data.get('profile_password_1')
            profile_password_2 = form.cleaned_data.get('profile_password_2')
            profile_email      = form.cleaned_data.get('profile_email')
            profile_first_name = form.cleaned_data.get('profile_first_name')
            profile_last_name  = form.cleaned_data.get('profile_last_name')
            if 'profile_photo' in request.FILES:
                profile_photo = request.FILES['profile_photo']
                # Read binary and encode to base64 string for session storage
                profile_photo_encoded = base64.b64encode(profile_photo.read()).decode('utf-8')
            # ----------------------------------------------------------------------
            # Input validation
            # ----------------------------------------------------------------------
            profile_error_message = ""
            USERNAME_ALLOWED_CHARS  = set(string.ascii_letters + string.digits + "-")
            PASSWORD_ALLOWED_CHARS  = set(string.ascii_letters + string.digits + "!@#$&")
            FIRSTNAME_ALLOWED_CHARS = set(string.ascii_letters + "-")
            LASTNAME_ALLOWED_CHARS  = set(string.ascii_letters + "-")
            # Input validation - Username
            if (profile_error_message == ""):
                profile_error_message = username_validation(profile_creation, profile_username, USERNAME_ALLOWED_CHARS)
            # Input validation - Passwords
            if (profile_error_message == ""):
                profile_error_message = password_validation(profile_password_1, PASSWORD_ALLOWED_CHARS)
            if (profile_error_message == ""):
                profile_error_message = password_validation(profile_password_2, PASSWORD_ALLOWED_CHARS)
            if (profile_error_message == ""):
                profile_error_message = password_match(profile_password_1, profile_password_2)
            # Input validation - email
            if (profile_error_message == ""):
                profile_error_message = email_validation(profile_creation, profile_email)
            # Input validation - first name
            if (profile_error_message == ""):
                profile_error_message = firstname_validation(profile_first_name, FIRSTNAME_ALLOWED_CHARS)
            # Input validation - last name
            if (profile_error_message == ""):
                profile_error_message = lastname_validation(profile_last_name, LASTNAME_ALLOWED_CHARS)
            # ----------------------------------------------------------------------
            # If there is a profile error send message back to client.
            # Else if all profile inputs are valid:
            # 1. Generate MFA code
            # 2. Store user profile inputs in session
            # 3. email MFA code to user 
            # 4. Inform client to open MFA modal
            # ----------------------------------------------------------------------
            if (profile_error_message != ""):
                # Return failure status to client
                response_data = {
                    'status': 'failure',
                    'message': profile_error_message,
                }
                return JsonResponse(response_data)
            else:
                # Generate a random 6-digit OTP code
                otp_code = str(random.randint(100000, 999999))
                print("INFO: MFA code =", otp_code)
                # Store pending user data and OTP in the session (expire in 10 minutes)
                if 'profile_photo' in request.FILES:
                    request.session['pending_user'] = {
                        'profile_username'           : profile_username,
                        'profile_email'              : profile_email,
                        'profile_password_1'         : profile_password_1,
                        'profile_first_name'         : profile_first_name,
                        'profile_last_name'          : profile_last_name,
                        'profile_photo_encoded' : profile_photo_encoded,
                        'profile_photo_name'    : profile_photo.name,
                        'otp_code'                  : otp_code,
                    }
                else:
                    request.session['pending_user'] = {
                        'profile_username'   : profile_username,
                        'profile_email'      : profile_email,
                        'profile_password_1' : profile_password_1,
                        'profile_first_name' : profile_first_name,
                        'profile_last_name'  : profile_last_name,
                        'otp_code'          : otp_code,
                    }
                request.session.set_expiry(600)
                # Send the code via email
                send_mail(
                    subject='Your Verification Code',
                    message=f'Your OTP code is {otp_code}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[profile_email],
                )
                # Return email validation code request to client
                response_data = {
                    'status' : 'email-validation',
                    'message': 'email validation code sent'
                }
                return JsonResponse(response_data)
    else:
        form = UserProfileForm()
        # User profile update or creation
        if request.user.is_authenticated:
            # Obtain the user's saved configuration information
            user_info = request.user.userinfo
            form = UserProfileForm(initial = { 'profile_username'   : request.user.username,
                                               'profile_email'      : request.user.email,
                                               'profile_first_name' : request.user.first_name,
                                               'profile_last_name'  : request.user.last_name
                                             })
            context = { 'form' : form, 'user_info' : user_info }
        else:
            form = UserProfileForm()
            context = { 'form' : form }
        messages.error(request, "")
        return render(request, 'user_info/user_profile_modal_step1.html', context)
  
def user_profile_step2(request):
    """ AR: fill this in """

    if request.user.is_authenticated:
        profile_creation = False
    else:
        profile_creation = True

    pending_data = request.session.get('pending_user')

    if not pending_data:
        messages.error(request, 'No registration session found. Please register again.')
        return render(request, 'plants/index.html')
    
    if request.POST:
        form = EmailVerificationForm(request.POST)
        if form.is_valid():
            entered_code = form.cleaned_data.get('entered_code')
            # ----------------------------------------------------------------------
            # If the user entered the MFA code correctly, setup the user
            # ----------------------------------------------------------------------
            if entered_code == pending_data['otp_code']:
                # Retrieve the user information from the session setup in step 1
                profile_username        = pending_data['profile_username']
                profile_password_1      = pending_data['profile_password_1']
                profile_email           = pending_data['profile_email']
                profile_first_name      = pending_data['profile_first_name']
                profile_last_name       = pending_data['profile_last_name']
                if 'profile_photo_name' in  pending_data:
                    profile_photo_name      = pending_data['profile_photo_name']
                    # Decode base64 back to binary
                    profile_photo_unencoded =  base64.b64decode(pending_data['profile_photo_encoded'])
                    # Create a Django ContentFile
                    profile_photo_obj = ContentFile(profile_photo_unencoded, name=profile_photo_name)
                else:
                    profile_photo_obj = None
                #
                if profile_creation:
                    user = User.objects.create_user(profile_username, profile_email, profile_password_1)
                    user.first_name = profile_first_name
                    user.last_name  = profile_last_name
                    user.save()
                else:
                    user = User.objects.get(username = request.user.username)
                    user.username = profile_username
                    user.set_password("profile_password_1")
                    user.email    = profile_email
                    user.first_name = profile_first_name
                    user.last_name  = profile_last_name
                    user.save()
                    # Only update password if it was changed
                    # Keep user logged if if password was changed
                    new_password = "profile_password_1"
                    # Only update if the password is actually different
                    if not user.check_password(new_password):
                        user.set_password(new_password)
                    user.save()
                    update_session_auth_hash(request, user)
                #
                if profile_creation:
                    # Add the user to the "Gardener" group - default
                    group = Group.objects.get(name='Gardener')
                    group.user_set.add(user)
                    # Create a Garden object for the user
                    garden = Garden()
                    garden.owner = profile_username
                    garden.name  = profile_username + "'s Garden"
                    garden.save()
                    # Create a UserInfo object for the user
                    user_info = UserInfo()
                    user_info.user = user
                    if profile_photo_obj is not None and profile_photo_obj != "":
                        user_info.profile_photo = profile_photo_obj
                    user_info.save()
                else:
                    # Obtain the user's saved configuration information
                    user_info = request.user.userinfo
                    if profile_photo_obj is not None and profile_photo_obj != "":
                        user_info.profile_photo = profile_photo_obj
                    user_info.save()
                
                # Clean up session
                del request.session['pending_user']
                # Return success status to client
                if profile_creation:
                    response_data = {
                        'status'  : 'user-creation-success',
                        'message' : 'User creation successful',
                    }
                else:
                    response_data = {
                        'status'  : 'user-profile-update-success',
                        'message' : 'User profile update successful',
                    }
                return JsonResponse(response_data)
            else:
                response_data = {
                    'status'  : 'authentication-failure',
                    'message' : 'User authentication failed',
                }
                return JsonResponse(response_data)
    else:
        form = EmailVerificationForm()
        context = { 'form' : form }
        return render(request, 'user_info/user_profile_modal_step2.html', context)

def user_profile_mfa(request):
    """ Provide new authorization code """
    session_data = request.session.get('pending_user')
    if not session_data:
        messages.error(request, 'No registration session found. Please register again.')
        # return redirect('register_view')
        return render(request, 'plants/index.html')
    
    if request.method == 'GET':
        # Generate a random 6-digit OTP code
        otp_code = str(random.randint(100000, 999999))
        print("INFO: otp_code = ", otp_code)
        # Store pending user OTP in the current session (expire in 10 minutes)
        request.session['pending_user']['otp_code'] = otp_code
        # Force Django to save the changes
        request.session.modified = True 
        # Reset expiration for 10 minutes
        request.session.set_expiry(600)
        # Retrieve all data for the current session
        session_data = request.session.get('pending_user')
        
        # Send the code via email
        profile_email = session_data['profile_email']
        send_mail(
            subject='Your Verification Code',
            message=f'Your OTP code is {otp_code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[profile_email],
        )
        response_data = {
            'status' : 'auth-code-resent',
            'message': 'Authentication code sent via email'
        }
        return JsonResponse(response_data)
    else:
        response_data = {
            'status' : 'auth-code-failure',
            'message': 'Authentication code failure'
        }
        return JsonResponse(response_data)
   
def user_pwd_rst_step1(request):
    """ Render the User Password Reset Page for Gateway Gardens app """
    if request.POST:
        form = UserPwdResetForm(request.POST)
        if form.is_valid():
            # ----------------------------------------------------------------------
            # Get password reset information from request
            # ----------------------------------------------------------------------
            pwd_rst_password_1 = form.cleaned_data.get('pwd_rst_password_1')
            pwd_rst_password_2 = form.cleaned_data.get('pwd_rst_password_2')
            pwd_rst_email      = form.cleaned_data.get('pwd_rst_email')
            # ----------------------------------------------------------------------
            # Input validation
            # ----------------------------------------------------------------------
            pwd_rst_error_message = ""
            PASSWORD_ALLOWED_CHARS  = set(string.ascii_letters + string.digits + "!@#$&")
            # Input validation - Passwords
            if (pwd_rst_error_message == ""):
                pwd_rst_error_message = password_validation(pwd_rst_password_1, PASSWORD_ALLOWED_CHARS)
            if (pwd_rst_error_message == ""):
                pwd_rst_error_message = password_validation(pwd_rst_password_2, PASSWORD_ALLOWED_CHARS)
            if (pwd_rst_error_message == ""):
                pwd_rst_error_message = password_match(pwd_rst_password_1, pwd_rst_password_2)
            # Input validation - email
            try:
                emailinfo = validate_email(pwd_rst_email, check_deliverability=False)
                pwd_rst_email= emailinfo.normalized
            except:
                pwd_rst_error_message = "invalid e-mail address"
            # ----------------------------------------------------------------------
            # If all password reset inputs are valid:
            # 1. Generate MFA code
            # 2. Store user password input and MFA code in session
            # 3. email MFA code to user 
            # 4. Inform client to open MFA modal
            # ----------------------------------------------------------------------
            if (pwd_rst_error_message != ""):
                print("INFO: input validation failure")
                # Return failure status to client
                response_data = {
                    'status': 'failure',
                    'message': pwd_rst_error_message,
                }
                return JsonResponse(response_data)
            else:
                print("INFO: input validation success")
                # Generate a random 6-digit OTP code
                otp_code = str(random.randint(100000, 999999))
                print("INFO: MFA code =", otp_code)
                request.session['pending_user'] = { 'pwd_rst_password_1' : pwd_rst_password_1 }
                request.session['pending_user'] = { 'pwd_rst_email'      : pwd_rst_email }
                request.session['pending_user'] = { 'otp_code'           : otp_code }

                request.session['pending_user'] = {
                    'pwd_rst_email'      : pwd_rst_email,
                    'pwd_rst_password_1' : pwd_rst_password_1,
                    'otp_code'           : otp_code
                }

                request.session.set_expiry(600)
                # Send the code via email
                send_mail(
                    subject='Your Verification Code',
                    message=f'Your OTP code is {otp_code}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[pwd_rst_email],
                )
                # Return email validation code request to client
                response_data = {
                    'status' : 'email-validation',
                    'message': 'email validation code sent'
                }
                return JsonResponse(response_data)
    else:
        form = UserPwdResetForm()
        context = { 'form' : form }
        return render(request, 'user_info/pwd_rst_modal_step1.html', context)

def user_pwd_rst_step2(request):
    """ AR: fill this in """

    pending_data = request.session.get('pending_user')

    if not pending_data:
        messages.error(request, 'No registration session found. Please register again.')
        return render(request, 'plants/index.html')

    if request.POST:
        form = EmailVerificationForm(request.POST)
        if form.is_valid():
            entered_code = form.cleaned_data.get('entered_code')
            # ----------------------------------------------------------------------
            # If the user entered the MFA code correctly, setup the user
            # ----------------------------------------------------------------------
            if entered_code == pending_data['otp_code']:
                # Retrieve the user information from the session setup in step 1
                pwd_rst_password_1 = pending_data['pwd_rst_password_1']
                pwd_rst_email      = pending_data['pwd_rst_email']
                #
                user = User.objects.get(email = pwd_rst_email)
                user.set_password(pwd_rst_password_1)
                user.save()
                #
                update_session_auth_hash(request, user)
                # Clean up session
                del request.session['pending_user']
                # Return success status to client
                response_data = {
                    'status'  : 'pwd_rst-success',
                    'message' : 'User password reset successful',
                }
                return JsonResponse(response_data)
            else:
                print("INFO: user_pwd_rst_step2 - codes do not match")
                response_data = {
                    'status'  : 'pwd_rst-failure',
                    'message' : 'User password reset failed',
                }
                return JsonResponse(response_data)
    else:
        form = EmailVerificationForm()
        context = { 'form' : form }
        return render(request, 'plants/pwd_rst_modal_step2.html', context)
    
def user_pwd_rst_mfa(request):
    """ Provide new authorization code """
    pending_data = request.session.get('pending_user')
    if not pending_data:
        messages.error(request, 'No registration session found. Please register again.')
        # return redirect('register_view')
        return render(request, 'plants/index.html')
    
    if request.method == 'GET':
        # Generate a random 6-digit OTP code
        otp_code = str(random.randint(100000, 999999))
        print("INFO: otp_code = ", otp_code)
        # Store pending user OTP in the current session (expire in 10 minutes)
        request.session['pending_user']['otp_code'] = otp_code
        # Force Django to save the changes
        request.session.modified = True 
        # Reset expiration for 10 minutes
        request.session.set_expiry(600)
        # Retrieve all data for the current session
        pending_data = request.session.get('pending_user')
        
        # Send the code via email
        pwd_rst_email = pending_data['pwd_rst_email']
        send_mail(
            subject='Your Verification Code',
            message=f'Your OTP code is {otp_code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[pwd_rst_email],
        )
        response_data = {
            'status' : 'auth-code-resent',
            'message': 'Authentication code sent via email'
        }
        return JsonResponse(response_data)
    else:
        response_data = {
            'status' : 'auth-code-failure',
            'message': 'Authentication code failure'
        }
        return JsonResponse(response_data)

def user_login(request):
    """ Render the User Login Page for Gateway Gardens app """
    if request.POST:
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username   = form.cleaned_data.get('username')
            password   = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            # Login the user if they have been authenticated else indicate login failure
            if user is not None:
                login(request, user)
                return render(request, 'plants/index.html')
            else:
                # AR: Indicate on password input form that the username and/or password was invalid
                return render(request, 'plants/index.html')
    else:
        form = UserLoginForm()
        context = { 'form' : form }
        return render(request, 'user_info/user_login_modal.html', context)
    
def user_logout(request):
    """ User Logout function for Gateway Gardens app """
    logout(request)
    return render(request, 'plants/index.html')

def user_admin(request):
    """ Render the User Admin page for Gateway Gardens app """
    if request.user.username == "Brent":
        users = User.objects.all()
        context = { 'users' : users, }
        return render(request, 'user_info/user_admin.html', context)
    else:
        return HttpResponseRedirect(reverse('plants:index'))

def user_delete(request, id):
    """ Delete selected user from the User database table """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:index'))
    user = User.objects.get(id=id)
    if request.POST:
        # Delete the user's "To Do" items
        user_todos = MyPlantToDo.objects.get(owner = user.username)
        user_todos.delete()
        # Delete the user's "My Plants"
        user_plants = MyPlant.objects.get(owner = user.username)
        user_plants.delete()
        # Delete the user's garden photos and database information
        user_garden = Garden.objects.get(owner = user.username)
        for i in range(1, 9):
            image_field = getattr(user_garden, f"image_{i}", None)
            if image_field:
                image_field.delete(save=False)
        user_garden.delete()
        # Delete the user's profile photo and auxilliary database information
        user_info = UserInfo.objects.get(user = user)
        if (user_info.profile_photo):
            user_info.profile_photo.delete(save=False)
        user_info.delete()
        # Delete the user
        user.delete()
        return HttpResponseRedirect(reverse('plants:index')) 
    else:
        context = {'user': user}
        return render(request, 'user_info/user_delete_modal.html', context)

def username_validation(profile_creation, username, USERNAME_ALLOWED_CHARS):
    error_message = ""
    if (username == ""):
        error_message = "Username is required"
    elif profile_creation and User.objects.filter(username = username).exists():
        error_message = "Username has already been taken"
    elif (len(username) < 4):
        error_message = "Username must be at least 4 characters long"
    elif (not all(char in USERNAME_ALLOWED_CHARS for char in username)):
        error_message = "Username can only contain letters, numbers and -"
    return (error_message)
    
def password_validation(password, PASSWORD_ALLOWED_CHARS):
    error_message = ""
    if (not all(char in PASSWORD_ALLOWED_CHARS for char in password)):
        error_message = "password can only contain letters, numbers and @#$&!"
    elif (len(password) < 8):
        error_message = "password must be at least 8 characters long"
    elif not any(char.isupper() for char in password):
        error_message = "password requires at least one uppercase letter"
    elif not any(char.islower() for char in password):
        error_message = "password requires at least one lowercase letter"
    elif not any(char.isdigit() for char in password):
        error_message = "password requires at least one number"
    elif not any(char in "!@#$%^&*()(_+)" for char in password):
        error_message = "password requires at least one special character '@#$&!'"  
    return (error_message)

def password_match(password_1, password_2):
    error_message = ""
    if (password_1 != password_2):
        error_message = "passwords do not match"
    return (error_message)
    
def email_validation(profile_creation, email):
    error_message = ""
    if profile_creation and User.objects.filter(email = email).exists():
        error_message = "Email address has already been taken"
    else:
        try:
            emailinfo = validate_email(email, check_deliverability=False)
            # profile_email= emailinfo.normalized
        except:
            error_message = "Invalid e-mail address"
    return (error_message)

def firstname_validation(firstname, FIRSTNAME_ALLOWED_CHARS):
    error_message = ""
    if (firstname == ""):
        error_message = "First name is required"
    elif (not all(char in FIRSTNAME_ALLOWED_CHARS for char in firstname)):
        error_message = "First name can only contain letters, numbers and -"
    return (error_message)

def lastname_validation(lastname, LASTNAME_ALLOWED_CHARS):
    error_message = ""
    if (lastname == ""):
        error_message = "Last name is required"
    elif (not all(char in LASTNAME_ALLOWED_CHARS for char in lastname)):
        error_message = "Last name can only contain letters, numbers and -"
    return (error_message)
