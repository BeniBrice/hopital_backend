import logging

from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError


class DoctorManager(BaseUserManager):
    def create_doctor(
        self,
        user,
        longitude,
        latitude,
        specialite,
        appointment_price,
        address,
        cabinet=None,
    ):
        try:
            # Vérifier si l'utilisateur existe
            if not user:
                raise ValidationError("L'utilisateur est requis pour créer un docteur.")

            # Vérifier si la spécialité existe
            if not specialite:
                raise ValidationError(
                    "La spécialité est requise pour créer un docteur."
                )

            # Créer un docteur
            doctor = self.model(
                user=user,
                longitude=longitude,
                latitude=latitude,
                specialite=specialite,
                appointment_price=appointment_price,
                address=address,
                cabinet=cabinet,
            )

            # Sauvegarder dans la base de données
            doctor.save(using=self._db)
            print("hello")
            print(doctor)
            return doctor

        except ObjectDoesNotExist as e:
            logging.error(f"Erreur de création de docteur : {e}")
            raise ValidationError("L'utilisateur ou la spécialité n'existent pas.")

        except ValidationError as e:
            logging.error(f"ValidationError : {e}")
            raise e

        except IntegrityError as e:
            logging.error(f"Erreur d'intégrité : {e}")
            raise ValidationError(
                "Erreur lors de la création du docteur, vérifiez les données saisies."
            )
