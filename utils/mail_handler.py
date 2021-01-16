import win32com.client
from pywintypes import com_error
from tkinter import messagebox



class MailHandler:

    @staticmethod
    def compose_mail(path):
        try:
            otl = win32com.client.Dispatch('outlook.application')
            mail = otl.CreateItem(0)
            mail.To = ''
            mail.Subject = ''
            mail.HTMLBody = f'<br><br><img src="{path}">'
            mail.Display(False)
        except com_error:
            messagebox.showerror("Mail client not found",
                                 "There is no default mail client configured for this machine. "
                                 "Please choose a default email client (eg.Outlook) and try again.")
