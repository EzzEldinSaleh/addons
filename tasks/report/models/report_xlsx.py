import base64
import io

from odoo import models
class PartnerXlsx(models.AbstractModel):
    _name = 'report.report.report_patient_card_xlx'
    _inherit = 'report.report_xlsx.abstract'
    def generate_xlsx_report(self, workbook, data, partners):

        for obj in partners:
            report_name = obj.name
            # One sheet by partner

            sheet = workbook.add_worksheet(report_name[:31])
            bold = workbook.add_format({'bold': True,'align':'center'})
            value = workbook.add_format({'align':'center'})
            title = workbook.add_format({'bg_color':'yellow','align':'center'})
            sheet.merge_range(0,2,0,1,'ID card',title)
            if obj.image_1920:
                partner_image=io.BytesIO(base64.b64decode(obj.image_1920))
                sheet.insert_image(1,1,'logo.jpeg',{'image_data':partner_image,'x_scale':0.5,'y_scale':0.4})
                sheet.write(6, 1, "Name:", bold)
                sheet.write(6,2, obj.name, value)
                sheet.write(7, 1, "Mobile:", bold)
                sheet.write(7, 2, obj.mobile, value)
            else:

                sheet.write(1, 1, "Name:", bold)
                sheet.write(1, 2, obj.name, value)
                sheet.write(2, 1, "Mobile:", bold)
                sheet.write(2, 2, obj.mobile, value)