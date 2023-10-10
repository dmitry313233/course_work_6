import datetime

from django.conf import settings
from django.core.mail import send_mail

from client.models import MailingSettings, MailingLog


def _send_email(mailing_settings, client):
    result = send_mail(
        subject=mailing_settings.message.subject,
        message=mailing_settings.message.message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[client.email],
        fail_silently=False
    )

    MailingLog.objects.create(
        status=MailingLog.STATUSES[0][0] if result else MailingLog.STATUSES[1][0],
        settings=mailing_settings,
        client=client,
        answer=result
    )


def send_mails():
    datetime_now = datetime.datetime.now(datetime.timezone.utc)
    for mailing_setting in MailingSettings.objects.exclude(status=MailingSettings.STATUSES[2][0]):
        if (datetime_now > mailing_setting.start_time) and (datetime_now < mailing_setting.end_time):
            mailing_setting.status = MailingSettings.STATUSES[1][0]
            for mailing_client in mailing_setting.clients.all():

                mailing_log = MailingLog.objects.filter(client=mailing_client,
                                                        settings=mailing_setting)
                if mailing_log.exists():
                    last_try_date = mailing_log.order_by('-last_try').first().last_try

                    if mailing_setting.period == MailingSettings.PERIODS[0][0]:
                        if (datetime_now - last_try_date).days >= 1:
                            _send_email(mailing_setting, mailing_client)
                    elif mailing_setting.period == MailingSettings.PERIODS[1][0]:
                        if (datetime_now - last_try_date).days >= 7:
                            _send_email(mailing_setting, mailing_client)
                    elif mailing_setting.period == MailingSettings.PERIODS[2][0]:
                        if (datetime_now - last_try_date).days >= 30:
                            _send_email(mailing_setting, mailing_client)

                else:
                    _send_email(mailing_setting, mailing_client)
        else:
            mailing_setting.status = MailingSettings.STATUSES[2][0]
        mailing_setting.save()