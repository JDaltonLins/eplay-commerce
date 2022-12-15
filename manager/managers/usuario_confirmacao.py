from django.db import DatabaseError, models, transaction
from django.shortcuts import render


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

    def send_verify_email(self, usuario, type, mark_verified=False):
        if type not in self.EMAILS or not self.EMAILS[type][2]:
            raise ValueError('Invalid type')

        email_info = self.EMAILS[type]

        try:
            with transaction.atomic():
                confirmacao = self.create(usuario=usuario, type=type)
                if mark_verified:
                    usuario.email_verified = False
                    usuario.save()
                confirmacao.save()

                send_mail(
                    email_info[0],
                    render(email_info[1], {
                        'usuario': usuario,
                        'confirmacao': confirmacao,
                    })
                    'noreply@teste.com.br',
                )

                return confirmacao
        except DatabaseError as e:
            pass

        return None

    def verify(self, type, uid, token):
        try:
            with transaction.atomic():
                confirmacao = self.get(
                    type=type, token=token, uid=uid)

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
