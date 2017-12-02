from weasyprint import CSS
from database.db import dbSession
from database.models import Layout
from priceCalculation.QuoteCalculation import QuoteCalculation
from priceCalculation.MaterialListCalculation import MaterialListCalculation
import priceCalculation.priceCalculation as PriceCalculation
from database.db import dbSession
from database.models import Appearance, Customer, Layout
from diagram.DiagramParser import DiagramParser
import api.layouts as Layouts
import api.appearances as Appearances

class Messages:
	"""Generate email messages formatted with HTML and PDF attachments"""

	quotePath = "attachments/quotes"
	materialListPath = "attachments/materials"

	stylesheets=[CSS(string="""
		table {
			width: 100%;
		}

		table, th, .bordered {
			border-collapse: collapse;
			border: 1px solid black;
		}

		th {
			color: #FFF;
			background-color: #999;
		}

		img {
			max-width: 100%;
			max-height: 7.5in;
		}

		.right {
			text-align: right;
		}

		.tableBreak {
			border-bottom: 5px solid #999;
		}

		.greyCell {
			background-color: #BBB;
			border: none;
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

	def quoteAttachment(project, customer=None, parsed=None):
		"""Generate the content of a quote attachment and return it"""
		if customer is None:
			customer = dbSession.query(Customer).filter(
				Customer.customer_id == project.customer_id).one()
		
		if parsed is None:
			layout = dbSession.query(Layout).filter(
				Layout.layout_id == project.layout_selected).one().layout_info
			parsed = DiagramParser.parse(layout)
		
		appearance = dbSession.query(Appearance).filter(
			Appearance.appearance_id == project.appearance_selected).one()
		appearanceValues = Appearances.getAppearanceValues(appearance)
		prices = QuoteCalculation.prices(parsed, appearanceValues[0],
			appearanceValues[1], appearanceValues[2], appearanceValues[3])
		subtotal = PriceCalculation.subtotal(prices)
		gstPercent = PriceCalculation.gstPercent
		gst = subtotal * gstPercent
		total = subtotal + gst
		priceStrings = []

		for price in prices:
			priceStrings.append(
				'''<tr class="bordered">
					<td class="bordered">{name}</td>
					<td class="right bordered">$ {price}</td>
				</tr>'''.format(name=price[0], price=price[1])
			)

		diagram = dbSession.query(Layout).filter(
			Layout.layout_id == project.layout_selected).one().layout_info

		pageBreak = """
			<p style="page-break-after: always" ></p>
			<p style="page-break-before: always" ></p>
			"""

		return """
			<div style="float:left; width:25%;">
				CAVALRY FENCE
			</div>
			<div style="float:left; width:75%;">
				GREGORY BAKER QUOTE
				<table>
					<tr class="bordered">
						<th>DESCRIPTION</th>
						<th>PRICE</th> 
					</tr>
					{prices}
					<tr class="bordered">
						<td class="right bordered">Subtotal</td>
						<td class="right bordered"><b>$ {subtotal}</b></td>
					</tr>
					<tr class="tableBreak bordered">
						<td class="right bordered">GST {gstPercent}%</td>
						<td class="right bordered"><b>$ {gst}</b></td>
					</tr>
					<tr class="greyCell">
						<td><b>Total</b></td>
						<td class="right"><b>$ {total}</b></td>
					</tr>
				</table>
				<b><span class="bottom">
					Signature:_____________________________________________
				</span></b>
			</div>
			{pageBreak}
			<div style="float:left; width:25%;"><p></p></div>
			<div style="float:left; width:75%;">
				<img src="{diagram}"><br>
				<b><span class="bottom">
					Signature:_____________________________________________
				</span></b>
			</div>
			""".format(pageBreak=pageBreak, diagram=diagram,
				prices="".join(priceStrings), subtotal=subtotal,
				gstPercent=gstPercent, gst=gst, total=total)
	
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