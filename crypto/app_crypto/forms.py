from django.contrib.auth.forms import UserCreationForm
from app_crypto.models import CustomUser


class MyForm(UserCreationForm):
    """
    Класс - переопределяющий стандартный класс django UserCreationForm.
    Форма регистрации пользователя.
    """

    class Meta:
        model = CustomUser
        fields = ('partner_id', 'token', 'operator_id', 'operator_name', 'username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Имя пользователя:'
        self.fields['password1'].label = 'Пароль:'
        self.fields['password1'].widget.attrs.update({'id': 'id_password'})
        self.fields['password2'].label = 'Подтверждение пароля:'
        self.fields['password2'].widget.attrs.update({'id': 'id_password'})
        self.fields['token'].label = 'TG Токен партнера:'
        self.fields['token'].widget.attrs.update({'id': 'id_username'})
        self.fields['partner_id'].label = 'ID партнера:'
        self.fields['partner_id'].widget.attrs.update({'id': 'id_username'})
        self.fields['operator_id'].label = 'ID оператора:'
        self.fields['operator_id'].widget.attrs.update({'id': 'id_username'})
        self.fields['operator_name'].label = 'Username оператора:'
        self.fields['operator_name'].widget.attrs.update({'id': 'id_username'})
