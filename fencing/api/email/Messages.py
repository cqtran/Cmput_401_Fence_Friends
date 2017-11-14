from weasyprint import CSS
from database.db import dbSession
from database.models import Quote

class Messages:
	"""Generate email messages formatted with HTML and PDF attachments"""

	quotePath = "Quote.pdf"
	materialListPath = "Material List.pdf"

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

	def quoteAttachment(project, customer):
		"""Generate the content of a quote attachment and return it"""
		diagram = dbSession.query(Quote).filter(
			Quote.project_id == project.project_id).one().project_info

		pageBreak = """
			<p style="page-break-after: always" ></p>
			<p style="page-break-before: always" ></p>
			"""

		return """
			<div style="float:left; width:25%;">
				HELLO
			</div>
			<div style="float:left; width:75%;">
				OH HELLO
				<table>
					<tr class="bordered">
						<th>DESCRIPTION</th>
						<th>PRICE</th> 
					</tr>
					<tr class="bordered">
						<td class="bordered">4'6" North Line (West of garage)</td>
						<td class="right bordered">$ 207.00</td>
					</tr>
					<tr class="tableBreak bordered">
						<td class="bordered">38' North Line (East of garage 7'+(5x6')+1')</td>
						<td class="right bordered">$ 1,748.00</td>
					</tr>
					<tr class="bordered">
						<td class="right bordered">Subtotal</td>
						<td class="right bordered"><b>$ 12,003.00</b></td>
					</tr>
					<tr class="tableBreak bordered">
						<td class="right bordered">GST 5.00%</td>
						<td class="right bordered"><b>$ 600.15</b></td>
					</tr>
					<tr class="greyCell">
						<td><b>Total (Plain Rails, Picket only on Front Gate)</b></td>
						<td class="right"><b>$ 12,603.15</b></td>
					</tr>
					<tr class="greyCell">
						<td><b>Total (Deco Rails, Picket only on Front Gate)</b></td>
						<td class="right"><b>$ 13,001.10</b></td>
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
			""".format(pageBreak=pageBreak, diagram=diagram)
	
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