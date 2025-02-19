import logging

from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError

logger = logging.getLogger(__name__)


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


class WorkTimeManager(BaseUserManager):

    def create_work_time(
        self,
        doctor,
        date,
        start_at,
        end_at,
    ):
        from KiraMeeT.apps.appointment.models import Doctor

        try:
            # Fetch the Doctor instance directly
            doctor_instance = Doctor.objects.get(pk=doctor)
            # print("**************")
            # print(doctor_instance)
            # logger.debug(doctor_instance)

            # Check if the date is valid
            if not date:
                raise ValidationError(
                    "La date est requise pour créer un horaire de travail."
                )

            # Check if start_at and end_at are valid
            if not start_at or not end_at:
                raise ValidationError("Les heures de début et de fin sont requises.")

            # Create a work time entry
            work_time = self.model(
                doctor=doctor_instance,  # Directly assign the Doctor instance
                date=date,
                start_at=start_at,
                end_at=end_at,
            )

            # Save to the database
            work_time.save(using=self._db)
            # print(work_time)
            return work_time

        except Doctor.DoesNotExist:
            raise ValidationError("Le docteur n'existe pas.")

        except ValidationError as e:
            logging.error(f"ValidationError : {e}")
            raise e

        except IntegrityError as e:
            logging.error(f"Erreur d'intégrité : {e}")
            raise ValidationError(
                "Erreur lors de la création de l'horaire de travail, vérifiez les données saisies."
            )
