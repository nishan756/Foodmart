from django.core.mail import EmailMultiAlternatives
from typing import List , Dict , Any
from django.conf import settings
from django.template.loader import render_to_string

from typing import Any
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


class EmailService:

    @staticmethod
    def send_email(
        subject: str,
        email_to: list[str],
        body: str = "",
        template_name: str | None = None,
        attachments: list[str] | None = None,
        context: dict[str, Any] | None = None,
        email_from: str | None = None,
    ):

        if not email_to:
            raise ValueError("You must provide receiver email")

        email_from = email_from or settings.EMAIL_HOST_USER
        context = context or {}
        attachments = attachments or []

        email = EmailMultiAlternatives(
            subject=subject,
            body=body,
            from_email=email_from,
            to=email_to,
        )

        if template_name:
            html_template = render_to_string(
                template_name,
                context
            )

            email.attach_alternative(
                html_template,
                "text/html"
            )

        for attachment in attachments:
            email.attach_file(attachment)

        return email.send()