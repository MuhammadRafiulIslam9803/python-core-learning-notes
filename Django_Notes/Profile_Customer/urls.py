from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import (
    LoginForm,
    MyPasswordChangeForm,
    MyPasswordResetForm,
    MySetPasswordForm,
)

urlpatterns = [
    # Home URL
    path("", views.ProductView.as_view(), name="home"),
    # Product URL
    path(
        "product/<int:id>/", views.ProductDetailsView.as_view(), name="productDetails"
    ),
    # Category URL
    path(
        "category/<str:category>/",
        views.categoryView.as_view(),
        name="categoryProducts",
    ),
    # Registration URL
    path(
        "registration/", views.CustomerRegistrationView.as_view(), name="registration"
    ),
    # Login URL
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="shop/login.html", authentication_form=LoginForm
        ),
        name="login",
    ),
    # Logout URL
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
    # password change urls
    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(
            template_name="shop/password_change.html",
            form_class=MyPasswordChangeForm,
            success_url="/password_change/done/",
        ),
        name="password_change",
    ),
    path(
        "password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="shop/password_change_done.html"
        ),
        name="password_change_done",
    ),
    # password reset urls or forgot password urls
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="shop/password_reset.html",
            form_class=MyPasswordResetForm,
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="shop/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="shop/password_reset_confirm.html",
            form_class=MySetPasswordForm,
        ),
        name="password_reset_confirm",
    ),
    path(
        "password_reset/complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="shop/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("address/", views.AddressView.as_view(), name="address"),
    # add to cart
    path(
        "product/<int:id>/add-to-cart/",
        views.AddToCartView.as_view(),
        name="add_to_cart",
    ),
    # cart view
    path(
        "cart/",
        views.CartView.as_view(),
        name="cart",
    ),
    # increment cart item quantity and decrement cart item quantity
    # add remove cart item view
    path(
        "cart/<int:id>/increase/",
        views.IncreaseCartView.as_view(),
        name="increase_cart",
    ),
    path(
        "cart/<int:id>/decrease/",
        views.DecreaseCartView.as_view(),
        name="decrease_cart",
    ),
    path(
        "cart/<int:id>/remove/",
        views.RemoveCartView.as_view(),
        name="remove_cart",
    ),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
