from django.db import DatabaseError, models, transaction


class UsuarioConfirmacaoManager (models.Manager):

    def send_verify_email(self, usuario, type, mark_verified=False):
        try:
            with transaction.atomic():
                confirmacao = self.create(usuario=usuario, type=type)
                if mark_verified:
                    usuario.email_verified = False
                    usuario.save()
                confirmacao.save()
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
