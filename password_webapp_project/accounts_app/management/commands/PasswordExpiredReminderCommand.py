from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
from datetime import timedelta, date
from typing import List, Tuple
from typing import NamedTuple

from password_app.models import Password


class UserPasswordDictType(NamedTuple):
    email: str
    expired_password_objects_list: List[Password]


class Command(BaseCommand):
    help = 'Get passwords that will expired date is less than 1 week'
    users_passwords_dict: UserPasswordDictType = dict()

    def handle(self, *args, **options):
        next_week_date = date.today() + timedelta(days=7)

        # Get expired passwords for all users
        q_filter = ~Q(expiration_date=None) & Q(expiration_date__lte=next_week_date)
        expired_passwords_list: List[Password] = Password.objects.select_related('password_owner').filter(q_filter)

        # Collect users emails from passwords
        users_emails = set([password.password_owner.email for password in expired_passwords_list])

        # Create dict: <user_email>:<user_expired_passwords_list>
        for user_email in users_emails:
            self.users_passwords_dict[user_email] = [password_obj for password_obj in expired_passwords_list if
                                                     password_obj.password_owner.email == user_email]

        # get datatuple for mass mail sending
        datatuple = self.prepare_mail_datatuple()

        # send emails
        self.send_mass_html_mail(datatuple)

        # self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"'))

    def generate_mail_text_message(self, passwords_expired_list: List[Password]) -> str:
        message = "Hi.\nPasswords below will expire soon:\n"
        for password_expired_obj in passwords_expired_list:
            password_desc = password_expired_obj.description
            password_expiration_date = password_expired_obj.expiration_date
            message += f"- Password description: '{password_desc}', Expiration date {password_expiration_date}\n"
        message += "\nLogin to your account to change your passwords\n"
        message += "\n\nPassword Manager"

        return message

    def generate_mail_html_message(self, passwords_expired_list: List[Password]) -> str:
        # Important! template renderer search for template in project 'template' dir
        template_path: str = 'accounts_app/password_reminder_mail_template.html'

        context = {'passwords_objects_list': passwords_expired_list}
        rendered = render_to_string(template_path, context)
        return rendered

    # https://docs.djangoproject.com/en/3.2/topics/email/#send-mass-mail
    # Prepare datatuple for mass mail sending, add extra message_html into tuple
    def prepare_mail_datatuple(self) -> tuple:

        datatuple_elems_list = list()
        for user_email, passwords_expired_list in self.users_passwords_dict.items():
            subject: str = "Your passwords are expired"
            message_text: str = self.generate_mail_text_message(passwords_expired_list)
            message_html: str = self.generate_mail_html_message(passwords_expired_list)
            mail_from: str = "noreply@passwordmanager.com"
            mail_recipient: Tuple[str] = (user_email,)

            datatuple_elem = (subject, message_text, message_html, mail_from, mail_recipient)
            datatuple_elems_list.append(datatuple_elem)

        return tuple(datatuple_elems_list)

    # get from here: https://stackoverflow.com/a/10215091
    def send_mass_html_mail(self, datatuple, fail_silently=False, user=None, password=None,
                            connection=None):
        """
        Given a datatuple of (subject, text_content, html_content, from_email,
        recipient_list), sends each message to each recipient list. Returns the
        number of emails sent.

        If from_email is None, the DEFAULT_FROM_EMAIL setting is used.
        If auth_user and auth_password are set, they're used to log in.
        If auth_user is None, the EMAIL_HOST_USER setting is used.
        If auth_password is None, the EMAIL_HOST_PASSWORD setting is used.

        """
        connection = connection or get_connection(username=user, password=password, fail_silently=fail_silently)
        messages = []
        for subject, text, html, from_email, recipient in datatuple:
            message = EmailMultiAlternatives(subject, text, from_email, recipient)
            message.attach_alternative(html, 'text/html')
            messages.append(message)
        return connection.send_messages(messages)
