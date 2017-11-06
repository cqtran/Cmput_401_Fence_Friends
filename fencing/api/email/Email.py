from flask_mail import Message
from smtplib import SMTPAuthenticationError, SMTPServerDisconnected, \
    SMTPException
from flask import flash
from database.models import Customer, Project
import os

SENDER_EMAIL = 'cmput401fence@gmail.com'

class Email:
	"""Send emails"""

	def send(app, mail, senderName, recipientEmail, subject, message, kind,
		attachmentPath=None, deleteAttachment=False):
		"""Send an email"""
		errorMessage = "Error sending " + kind.lower()

		try:
			m = Message(subject, sender=(senderName, SENDER_EMAIL),
				recipients=[recipientEmail])
			m.html = message

			if attachmentPath is not None:
				with app.open_resource(attachmentPath) as fp:
					m.attach(attachmentPath, "image/png", fp.read())

			mail.send(m)

			if deleteAttachment:
				os.remove(attachmentPath)
			
			flash(kind + " sent", "success")
		
		except SMTPAuthenticationError as e:
			flash(errorMessage + " (SMTPAuthenticationError)", "danger")
			print(str(e))
		
		except SMTPServerDisconnected as e:
			flash(errorMessage + " (SMTPServerDisconnected)", "danger")
			print(str(e))
		
		except SMTPException as e:
			flash(errorMessage + " (SMTPException)", "danger")
			print(str(e))
		
		except BaseException as e:
			flash(errorMessage + " (unknown exception)", "danger")
			print(str(e))
		
		except:
			flash(errorMessage + " (unknown exception)", "danger")