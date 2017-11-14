from flask_mail import Message
from smtplib import SMTPAuthenticationError, SMTPServerDisconnected, \
    SMTPException
from flask import flash
from flask_security.core import current_user
from weasyprint import HTML
from database.models import Company, Customer, Project
from database.db import dbSession
from api.email.Messages import Messages
import os

SENDER_EMAIL = 'cmput401fence@gmail.com'

class Email:
	"""Send emails"""

	def makeAttachment(filePath, content):
		"""
		Make an attachment and return the file path or None if there was an
		exception
		"""
		try:
			# If there is an old attachment, delete it
			if os.path.isfile(filePath):
				os.remove(filePath)
			
			HTML(string=content).write_pdf(filePath,
				stylesheets=Messages.stylesheets)
			return filePath
		
		except BaseException as e:
			print(str(e))
			flash("Error creating attachment", "danger")
			return None
		
		except:
			flash("Error creating attachment", "danger")
			return None

	def send(app, mail, senderName, recipientEmail, subject, message, kind,
		attachmentPath=None):
		"""Send an email"""
		errorMessage = "Error sending " + kind.lower()

		try:
			company = dbSession.query(Company).filter(
				Company.company_name == current_user.company_name).one()

			m = Message(subject, sender=(senderName, SENDER_EMAIL),
				recipients=[recipientEmail],
				bcc=[company.email])
			m.html = message

			if attachmentPath is not None:
				with app.open_resource(attachmentPath) as fp:
					m.attach(attachmentPath, "image/png", fp.read())

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
		
		except OSError as e:
			flash(errorMessage + " (OSError)", "danger")
			print(str(e))
		
		except BaseException as e:
			flash(errorMessage + " (unknown exception)", "danger")
			print(str(e))
		
		except:
			flash(errorMessage + " (unknown exception)", "danger")