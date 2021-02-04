from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError, ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.depends('projects')
    def compute_project_count(self):
        self.project_count = len(self.projects)

    guarantee_accounting_reference = fields.Char("Guarantee Accounting Reference")
    bank_guarantee_reference = fields.Char("Bank Guarantee")
    bank_guarantee_validity = fields.Date("Bank Guarantee Validity")
    bank_guarantee_amount = fields.Monetary("Bank Guarantee Amount")
    tender_date = fields.Date("Tender Date")
    tender_name = fields.Char("Tender Name")
    tender_reference = fields.Char("Tender Reference")
    insurance_accounting_reference = fields.Char("Insurance Accounting Reference")
    insurance_amount = fields.Monetary("Insurance Amount")
    insurance_reference = fields.Char("Insurance Reference")
    insurance_validity = fields.Date("Insurance Validity")
    project = fields.Many2one('project.project',"Project Template")
    project_name = fields.Char("Project Name")
    projects = fields.Many2many('project.project',store=True)
    project_count = fields.Integer(compute='compute_project_count')

    def create_project_wizard(self):
        form_rec = self.env.ref('alm_custom.view_project_create')
        return {
            'view_id': [form_rec.id],
            'res_model': 'project.create',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'target': 'new',
            'context': self.env.context,
        }

    def action_view_projects(self):
        action = self.env["ir.actions.actions"]._for_xml_id("project.open_view_project_all")
        # projects = self.mapped('project_ids')
        action['domain'] = [('id', 'in', self.projects.ids)]
        return action


