from flask_mail import Message
from smtplib import SMTPAuthenticationError, SMTPServerDisconnected, \
    SMTPException
from flask import flash

SENDER_EMAIL = 'cmput401fence@gmail.com'

class Email:
	"""Send emails"""

	def send(mail, senderName, recipientEmail, subject, message, kind):
		"""Send an email"""
		errorMessage = "Error sending " + kind.lower()

		try:
			m = Message(subject, sender=(senderName, SENDER_EMAIL),
				recipients=[recipientEmail])
			m.html = message
			mail.send(m)
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