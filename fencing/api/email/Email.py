from flask_mail import Message
from smtplib import SMTPAuthenticationError, SMTPServerDisconnected, \
    SMTPException
from flask import flash
from flask_security.core import current_user
from weasyprint import HTML
from database.models import Company, Customer, Project
from database.db import dbSession
from api.email.Messages import Messages
import os, traceback, uuid

SENDER_EMAIL = 'cmput401fence@gmail.com'

class Email:
	"""Send emails"""

	staticFolder = None

	def makeAttachment(folderPath, content):
		"""
		Make an attachment and return the file path or None if there was an
		exception
		"""
		try:
			filePath = folderPath + "/" + str(uuid.uuid4()) + ".pdf"
			fullPath = Email.staticFolder + filePath
			HTML(string=content).write_pdf(fullPath,
				stylesheets=Messages.stylesheets)
			return filePath
		
		except:
			flash("Error creating attachment", "danger")
			traceback.print_exc()
			return None

	def send(app, mail, senderName, recipientEmail, subject, message, kind,
		attachmentPath=None):
		"""Send an email"""
		if recipientEmail is None:
			flash("No email to send " + kind.lower() + " to", "danger")
			return

		errorMessage = "Error sending " + kind.lower()

		try:
			company = dbSession.query(Company).filter(
				Company.company_name == current_user.company_name).one()

			m = Message(subject, sender=(senderName, SENDER_EMAIL),
				recipients=[recipientEmail],
				bcc=[company.email])
			m.html = message

			if attachmentPath is not None:
				attachmentPath = Email.staticFolder + attachmentPath

				with app.open_resource(attachmentPath) as fp:
					m.attach(attachmentPath, "image/png", fp.read())
				
				try:
					os.remove(attachmentPath)
				
				except:
					print("Warning: could not delete attachment")

			mail.send(m)
			
			flash(kind + " sent", "success")
		
		except SMTPAuthenticationError as e:
			flash(errorMessage + " (SMTPAuthenticationError)", "danger")
			traceback.print_exc()
		
		except SMTPServerDisconnected as e:
			flash(errorMessage + " (SMTPServerDisconnected)", "danger")
			traceback.print_exc()
		
		except SMTPException as e:
			flash(errorMessage + " (SMTPException)", "danger")
			traceback.print_exc()
		
		except OSError as e:
			flash(errorMessage + " (OSError)", "danger")
			traceback.print_exc()
		
		except:
			flash(errorMessage + " (unknown exception)", "danger")
			traceback.print_exc()