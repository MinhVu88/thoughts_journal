from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
	path('', views.home, name=''),
	path('register', views.register, name='register'),
	path('login', views.login, name='login'),
	path('logout', views.logout, name='logout'),
	path('dashboard', views.dashboard, name='dashboard'),
	path('create-thought', views.create_thought, name='create-thought'),
	path('view-thoughts', views.view_thoughts, name='view-thoughts'),
	path('update-thought/<int:thought_id>', views.update_thought, name='update-thought'),
	path('delete-thought/<int:thought_id>', views.delete_thought, name='delete-thought'),
	path('profile-mgt', views.profile_management, name='profile-mgt'),
	path('delete-account', views.delete_account, name='delete-account'),
 
	# password management
	# 1. allow user to enter his/her email to receive a password-reset link
	path(
		'reset_password',
		auth_views.PasswordResetView.as_view(template_name='journal/password-reset.html'),
		name='reset_password'
	),
 
	# 2. show a success message confirming that such an email's been sent
	path(
		'reset_password_sent',
		auth_views.PasswordResetDoneView.as_view(template_name='journal/password-reset-sent.html'),
		name='password_reset_done'
	),
 
	# 3. send the password-reset link
	path(
		'reset/<uidb64>/<token>/',
		auth_views.PasswordResetConfirmView.as_view(template_name='journal/password-reset-form.html'),
		name='password_reset_confirm'
	),
 
	# 4. show a success message confirming that password's been changed
	path(
		'password_reset_complete',
		auth_views.PasswordResetCompleteView.as_view(template_name='journal/password-reset-complete.html'),
		name='password_reset_complete'
	)
]