from odoo import api, fields, models, _, tools


class ProjectInherit(models.Model):
    _inherit = 'project.project'

    manufacturing_order = fields.Many2one('mrp.production',string="Manufacturing Order")
    is_template = fields.Boolean("Is a template")

    @api.onchange('manufacturing_order')
    def set_project_in_mo(self):
        if self.manufacturing_order:
            self.manufacturing_order.project = self.id.origin


class ProjectTask(models.Model):
    _inherit = 'project.task'

    work_order = fields.Many2one('mrp.workorder', string="Work Order")
    responsibility = fields.Selection([('ppc','PPC'),('design','Design'),('manufacturing','Manufacturing')],"Responsibility")
    start_date = fields.Date("Date Start",default=fields.Datetime.now)
    inc_sequence = fields.Char()
    planned_start = fields.Datetime(string="Planned Start Date")
    planned_completion = fields.Datetime(string="Planned Completion Date")
    actual_start = fields.Datetime(string="Actual Start Date")
    actual_completion = fields.Datetime(string="Actual Completion Date")
    set_date = fields.Boolean(compute='set_dates')

    @api.depends('work_order')
    def set_dates(self):
        if self.work_order:
            self.planned_start = self.work_order.date_planned_start
            self.planned_completion = self.work_order.date_planned_finished
            self.actual_start = self.work_order.date_start
            self.actual_completion = self.work_order.date_finished
            self.set_date=True
        else:
            self.set_date=False

    @api.model
    def create(self, vals):
        vals['inc_sequence'] = self.env['ir.sequence'].next_by_code('project.task')
        result = super(ProjectTask, self).create(vals)
        return result

    @api.onchange('work_order')
    def set_task_in_wo(self):
        if self.work_order:
            self.work_order.project_task = self.id.origin

    # @api.depends('work_order.state')
    # def update_task_stage(self):
    #     if self.work_order.state:
    #         if self.work_order.state == 'progress':
    #             self.wo_status = True
    #             self.kanban_state = 'normal'
    #         elif self.work_order.state == 'done':
    #             self.wo_status = True
    #             self.kanban_state = 'done'
    #         else:
    #             self.wo_status = False
    #     else:
    #         self.wo_status = False

    @api.depends('project_id.manufacturing_order')
    def set_wo_domain(self):
        if self.project_id.manufacturing_order:
            res = {}
            self.wo_domain = True
            self.mo_id = self.project_id.manufacturing_order.id
            res['domain'] = {'work_order': [('production_id.id', '=', self.project_id.manufacturing_order.id)]}
            return res
        else:
            self.wo_domain = False


    # wo_status = fields.Boolean(compute='update_task_stage')
    wo_domain = fields.Boolean(compute='set_wo_domain')
    mo_id = fields.Integer(help="Used to apply domain for work order")


