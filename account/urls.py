from django.urls import path

from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [

  path('sign-up', views.sign_up, name='sign-up'),
  
  path('sign-in', views.sign_in, name='sign-in'),
  
  path('sign-out', views.sign_out, name='sign-out'),
  
  # Dashboard / profile 
 
  path('dashboard', views.dashboard, name='dashboard'),
  
  path('profile-management', views.profile_management, name='profile-management'),
  
  path('delete-account', views.delete_account, name='delete-account'),
  
  
  # Email verification Url's 
 
  path('email-verification/<str:uidb64>/<str:token>/', views.email_verification, name='email-verification'),
  
  path('email-verification-sent', views.email_verification_sent, name='email-verification-sent'),
  
  path('email-verification-success', views.email_verification_success, name='email-verification-success'),
  
  path('email-verification-failed', views.email_verification_failed, name='email-verification-failed'),
  
  
  # Password forms urls/views 
  
  # 1 Submit email form
  path('reset_password', auth_views.PasswordResetView.as_view(template_name='account/password/password-reset.html'), name='reset_password'),
  
  #2 Success manage stating that a password reset was sent
  path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(template_name='account/password/password-reset-sent.html'), name='password_reset_done'),
  
  # #3 Password reset link
  path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='account/password/password-reset-form.html'), name='password_reset_confirm'),
  
  # #4 Success message
  path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(template_name='account/password/password-reset-complete.html'), name='password_reset_complete'),
  
  # Manage Shipping
  
  path('manage-shipping', views.manage_shipping, name = 'manage-shipping'),
  
  path('track-orders', views.track_orders, name = 'track-orders'),
  
]