from weasyprint import CSS
from flask_security.core import current_user
from database.db import dbSession
from database.models import Layout
from priceCalculation.QuoteCalculation import QuoteCalculation
from priceCalculation.MaterialListCalculation import MaterialListCalculation
import priceCalculation.priceCalculation as PriceCalculation
from database.db import dbSession
from database.models import Appearance, Customer, Layout, Company
from diagram.DiagramParser import DiagramParser
import api.layouts as Layouts
import api.appearances as Appearances
from decimal import Decimal
import datetime

class Messages:
	"""Generate email messages formatted with HTML and PDF attachments"""

	quotePath = "attachments/quotes"
	materialListPath = "attachments/materials"

	stylesheets=[CSS(string="""
		* {
			font-family: Arial, Helvetica, "Times New Roman";
			font-size: 10pt;
		}

		.companyName {
			font-size: 12pt !important;
		}

		table {
			width: 100%;
		}

		table, th, .bordered {
			border-collapse: collapse;
		}

		.bordered {
			border-top: 1px solid black;
			border-bottom: 1px solid black;
		}

		.bordered-right {
			border-right: 1px solid black;
		}

		.bordered-white {
			border-right: 1px solid white;
		}

		th {
			color: #FFF;
			background-color: #919191;
			text-align: center;
			padding: 5pt;
		}

		td {
			font-size: 12pt !important;
			padding: 5pt;
		}

		img {
			max-width: 100%;
			max-height: 5in;
		}

		.right {
			text-align: right;
		}

		.tableBreak {
			border-bottom: 5px solid #919191;
		}

		.tableBreakTop {
			border-top: 5px solid #919191;
		}

		.greyCell {
			background-color: #DDD;
			border: none !important;
		}

		.greyText {
			color: #999;
		}

		.bold {
			font-weight: bold;
		}

		.bottom {
			position: absolute;
			bottom: 0px;
		}
		""")]

	def quoteMessage(customer, company):
		"""Generate a quote email message"""
		return """
			Dear {customer_first_name},<br>
			<br>
			Please find your attached quote.<br>
			<br>
			Please do not respond to this email. You can contact us at
			{company_email}
			""".format(customer_first_name=customer.first_name,
				company_email=company.email)
	
	def materialListMessage(company):
		"""Generate a material list email message"""
		return """
			Please find our required materials attached.<br>
			<br>
			Please do not respond to this email. You can contact us at
			{company_email}
			""".format(company_email=company.email)

	def quoteAttachment(project, customer=None, parsed=None, misc=None,
		notes=None, misc_modifier_label=None, payment=None, description=None,
		invoice=None):
		"""Generate the content of a quote attachment and return it"""
		if customer is None:
			customer = dbSession.query(Customer).filter(
				Customer.customer_id == project.customer_id).one()
		
		if parsed is None:
			layout = dbSession.query(Layout).filter(
				Layout.layout_id == project.layout_selected).one().layout_info
			parsed = DiagramParser.parse(layout)
		
		if notes is None:
			notes = ""
		
		if payment is None:
			payment = ""
		
		if description is None:
			description = ""
		
		if invoice is None:
			invoice = project.project_id
		
		appearance = dbSession.query(Appearance).filter(
			Appearance.appearance_id == project.appearance_selected).one()
		appearanceValues = Appearances.getAppearanceValues(appearance)
		prices = QuoteCalculation.prices(parsed, appearanceValues[0],
			appearanceValues[1], appearanceValues[2], appearanceValues[3])
		subtotal = PriceCalculation.subtotal(prices)

		if misc:
			subtotal += misc

		gstPercent = PriceCalculation.gstPercent()
		gst = subtotal * gstPercent
		total = subtotal + gst
		priceStrings = []

		for price in prices:
			priceStrings.append(
				'''<tr class="bordered">
					<td class="bordered bordered-right">{name}</td>
					<td class="right bordered">$ {price}</td>
				</tr>'''.format(name=price[0],
				price=PriceCalculation.priceString(price[1]))
			)
		
		if misc:
			if misc_modifier_label is None:
				misc_modifier_label = ""

			if misc_modifier_label.strip() == "":
				misc_modifier_label = "Adjustments"

			priceStrings.append(
				'''<tr class="bordered">
					<td class="bordered bordered-right">{label}</td>
					<td class="right bordered">$ {price}</td>
				</tr>'''.format(price=PriceCalculation.priceString(misc),
					label=misc_modifier_label)
			)

		diagram = dbSession.query(Layout).filter(
			Layout.layout_id == project.layout_selected).one().layout_info
		
		company = dbSession.query(Company).filter(
			Company.company_name == current_user.company_name).one()
		
		now = datetime.datetime.now()
		date = "{0} {1}, {2}".format(now.strftime("%b"), now.day, now.year)

		pageBreak = """
			<p style="page-break-after: always" ></p>
			<p style="page-break-before: always" ></p>
			"""

		return """
			<div style="float:left; width:30%;">
				<p class="greyText bold companyName">{companyName}</p>
				<br>
				<p class="greyText">
					<span class="bold">Email</span><br>
					{companyEmail}
				</p>
			</div>
			<div style="float:left; width:70%;">
				<p>
					<span class="greyText bold">DATE</span><br>
					{date}
				</p><br>
				<p>
					<span class="greyText bold">TO</span><br>
					{customerName}<br>
					{customerAddress}<br>
					{customerPhone}
				</p><br>
				<p class="bold">
					<span class="greyText">PROJECT TITLE: </span>
					{projectName}<br>
					<span class="greyText">DESCRIPTION: </span>
					{description}<br>
					<span class="greyText">INVOICE NUMBER: </span>
					{invoice}<br>
					<span class="greyText">PAYMENT: </span>
					{payment}
				</p><br>
				<table>
					<tr>
						<th class="bordered-white">DESCRIPTION</th>
						<th>PRICE</th> 
					</tr>
					{prices}
					<tr class="tableBreakTop bordered">
						<td class="right bordered bordered-right">Subtotal</td>
						<td class="right bordered"><b>$ {subtotal}</b></td>
					</tr>
					<tr class="tableBreak bordered">
						<td class="right bordered bordered-right">GST {gstPercent}%</td>
						<td class="right bordered"><b>$ {gst}</b></td>
					</tr>
					<tr class="greyCell right">
						<td><b>Total</b></td>
						<td class="right"><b>$ {total}</b></td>
					</tr>
				</table>
				<p class="bold">{notes}</p>
				<b><span class="bottom">
					Signature:_____________________________________________
				</span></b>
			</div>
			{pageBreak}
			<div style="float:left; width:30%;">
				<p class="greyText bold companyName">{companyName}</p>
				<br>
				<p class="greyText">
					<span class="bold">Email</span><br>
					{companyEmail}
				</p>
			</div>
			<div style="float:left; width:70%;">
				<p class="bold">Site Map:</p>
				<img src="{diagram}"><br>
				<p class="bold">Payment is due on day installation is completed. 2 Year Workmanship Warranty does not include: damage done to fence product by homeowner, pedestrians, or act of God, nor damage due to frost heave on posts and concrete; coverage of the Westech Product Lifetime Warranty. Cavalry Fence Inc. reserves the right to alter pricing for any requested changes or alterations to this quote above. In the event Cavalry Fence Inc. is required to hand expose: gas lines, electrical lines, water lines, etc. after government inspection, Cavalry Fence Inc. reserves the right to charge an additional $50 per hour until exposure is complete. In this event, Cavalry Fence Inc. will notify the homeowner and request permission to proceed with exposure of the line with the additional charge.</p>
				<b><span class="bottom">
					Signature:_____________________________________________
				</span></b>
			</div>
			""".format(pageBreak=pageBreak,
				diagram=diagram,
				prices="".join(priceStrings),
				subtotal=PriceCalculation.priceString(subtotal),
				gstPercent=round(gstPercent * Decimal("100"), 0),
				gst=PriceCalculation.priceString(gst),
				total=PriceCalculation.priceString(total),
				companyName=company.company_name.upper(),
				companyEmail=company.email,
				date=date,
				customerName=customer.first_name,
				customerAddress=project.address,
				customerPhone=customer.cellphone,
				projectName=project.project_name,
				invoice=invoice,
				notes=notes,
				payment=payment,
				description=description)
	
	def makeMaterialDictionary(material_types, material_amounts):
		amounts = {}

		for material in material_types:
			amounts[material] = material_amounts[material]
		
		return amounts
	
	def materialListAttachment(project, material_types=None,
		material_amounts=None):
		"""Generate the content of a material list attachment and return it"""
		layout = dbSession.query(Layout).filter(
			Layout.layout_id == project.layout_selected).one()
		
		if material_types is None or material_amounts is None:
			materials = Layouts.getMaterialAmount(layout)
		
		else:
			materials = Messages.makeMaterialDictionary(material_types,
				material_amounts)

		categories = {}
		categoryStrings = []

		for material in materials:
			raw = material

			if str(materials[material]) == '0':
				continue

			material = Layouts.materialString(material)

			if material.startswith("Metal "):
				category = "Metal"
			
			elif material.startswith("Plastic "):
				category = "Plastic"
			
			else:
				category = "Other"
			
			if category not in categories:
				categories[category] = []
			
			categories[category].append("<b>{amount}</b> {material}".format(
				amount=materials[raw], material=material))

		for category in categories:
			materialStrings = []
			categoryString = "<h2>{0}</h2>".format(category)
			
			for material in categories[category]:
				materialStrings.append(material)
			
			categoryString += "<br>".join(materialStrings)
			categoryStrings.append(categoryString)
		
		return "<br><br>".join(categoryStrings)