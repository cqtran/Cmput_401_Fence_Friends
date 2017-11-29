from weasyprint import CSS
from database.db import dbSession
from database.models import Layout
from priceCalculation.QuoteCalculation import QuoteCalculation
from priceCalculation.MaterialListCalculation import MaterialListCalculation
import priceCalculation.priceCalculation as priceCalculation
from database.db import dbSession
from database.models import Appearance

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
		supplier = "Your face"
		return """
			Dear {supplier},<br>
			<br>
			Please find our required materials attached.<br>
			<br>
			Please do not respond to this email. You can contact us at
			{company_email}
			""".format(supplier=supplier,
				company_email=company.email)

	def quoteAttachment(project, customer, parsed):
		"""Generate the content of a quote attachment and return it"""
		appearance = dbSession.query(Appearance).filter(
			Appearance.appearance_id == project.appearance_selected)
		prices = QuoteCalculation.prices(parsed, appearance)
		subtotal = PriceCalculation.subtotal(prices)
		gstPercent = QuoteCalculation.gstPercent
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
	
	def materialListAttachment(project):
		"""Generate the content of a material list attachment and return it"""
		return """
			<b>Steel</b><br>
			7 steel posts<br>
			5 steel uchannel<br>
			1 L steel<br>
			<br>
			<b>Plastic Posts</b><br>
			1 corner<br>
			4 line<br>
			2 end<br>
			1 blank<br>
			<br>
			<b>Plastic</b><br>
			12 rails<br>
			12 u channels<br>
			46 T&G<br>
			14 collars<br>
			8 caps
			"""