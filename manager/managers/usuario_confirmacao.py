from django.conf import settings
from django.db import DatabaseError, models, transaction
from django.http import HttpRequest
from django.shortcuts import render
from django.core.mail import send_mail


class UsuarioConfirmacaoManager (models.Manager):

    EMAILS = {
        'email': (
            'Verificação de email - ePlay Commerce',
            'email/verify-email.html',
            True
        ),
        'new_user': (
            'Bem vindo ao ePlay Commerce',
            'email/new-user.html',
            True
        ),
        'reset-password': (
            'Redefinição de senha - ePlay Commerce',
            'email/reset-password.html',
            True
        ),
        'reset-success': (
            'Senha redefinida com sucesso - ePlay Commerce',
            'email/reset-success.html',
            False
        )
    }

    def send_confirmation_email(self, context: HttpRequest, usuario, type, mark_verified=False):
        if type not in self.EMAILS or not self.EMAILS[type][2]:
            raise ValueError('Invalid type')

        if not settings.EMAIL_USE:
            if type == 'email':
                usuario.email_verified = True
                usuario.save()

            return True

        email_info = self.EMAILS[type]

        try:
            with transaction.atomic():
                confirmacao = self.get_or_create(usuario=usuario, type=type)
                confirmacao.redefine()

                if mark_verified:
                    usuario.email_verified = False
                    usuario.save()

                send_mail(
                    email_info[0],
                    render(context, email_info[1], {
                        'usuario': usuario,
                        'confirmacao': confirmacao,
                    }),
                    [usuario.email],
                    settings.EMAIL_NO_REPLY
                )

                confirmacao.save()

                return confirmacao
        except DatabaseError as e:
            pass

        return None

    def verify(self, uid, token):
        try:
            with transaction.atomic():
                confirmacao = self.get(token=token, uid=uid)

                if confirmacao.type == 'email' and not confirmacao.usuario.email_verified:
                    confirmacao.usuario.email_verified = True

                confirmacao.usuario.save(using=self._db)
                confirmacao.delete(using=self._db)

                return True
        except DatabaseError as e:
            pass
        except self.model.DoesNotExist as de:
            pass
        return False
