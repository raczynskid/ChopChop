import win32com.client


class MailHandler:

    @staticmethod
    def compose_mail(path):
        otl = win32com.client.Dispatch('outlook.application')
        mail = otl.CreateItem(0)
        mail.To = ''
        mail.Subject = ''
        mail.HTMLBody = f'<br><br><img src="{path}">'
        mail.Display(False)
