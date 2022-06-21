from .views import ChangePasswordView, ResetPasswordView
from django.contrib.auth import views as auth_views
from django.urls import path
from. import views


urlpatterns = [
    path('register/', views.register, name="user.register"),
    path('login/', views.user_login, name="user.login"),
    path('logout/', views.user_logout, name="user.logout"),
    path('profile/', views.profileShow, name="user.profile"),
    path('profileedit/>', views.profileEdit, name="user.profileedit"),
    path('profileupdate/', views.profileUpdate, name="user.profileupdate"),
    path('passwordchange/', ChangePasswordView.as_view(), name='password_change'),
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='password/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name='password_reset_complete'),

    path('', views.index, name="ShopHome"),
    path("about/", views.about, name="AboutUs"),
    path("contact/", views.contact, name="ContactUs"),
    path("tracker/", views.tracker, name="TrackingStatus"),
    path("search/", views.search, name="Search"),
    path("products/<int:myid>", views.productView, name="ProductView"),
    path("checkout/", views.checkout, name="Checkout"),
    path("cart/", views.cart, name="cart"),
    path("clearcart/", views.clearCart, name="clearcart"),
    path("update_item/", views.updateitem, name="updateitem"),
    path("process_order/", views.processOrder, name="processorder"),

]
