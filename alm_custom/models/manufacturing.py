from odoo import api, fields, models, _, tools
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError

class Manufacturing(models.Model):
    _inherit = 'mrp.production'

    project = fields.Many2one('project.project',"Project")

    @api.onchange('project')
    def set_mo_in_project(self):
        if self.project:
            self.project.manufacturing_order = self.id.origin


class WorkOrders(models.Model):
    _inherit = 'mrp.workorder'

    project_task = fields.Many2one('project.task',"Project Task")

    @api.onchange('project_task')
    def set_wo_in_tasks(self):
        if self.project_task:
            self.project_task.work_order = self.id.origin

    @api.depends('production_id.project')
    def set_tasks_domain(self):
        if self.production_id.project:
            res = {}
            self.tasks_domain = True
            self.project_id = self.production_id.project.id
            res['domain'] = {'project_task': [('project_id.id', '=', self.production_id.project.id)]}
            return res
        else:
            self.tasks_domain = False

    project_id = fields.Integer(store=True,string="Project ")
    tasks_domain = fields.Boolean(compute='set_tasks_domain')

    def button_finish(self):
        for workorder in self:
            if workorder.project_task:
                if (workorder.workcenter_id.is_subcontracted and workorder.project_task.kanban_state == 'done') or (not workorder.workcenter_id.is_subcontracted):
                    end_date = datetime.now()
                    if workorder.state in ('done', 'cancel'):
                        continue
                    workorder.end_all()
                    vals = {
                        'state': 'done',
                        'date_finished': end_date,
                        'date_planned_finished': end_date
                    }
                    if not workorder.project_task.kanban_state == 'done':
                        workorder.project_task.kanban_state = 'done'
                    if not workorder.date_start:
                        vals['date_start'] = end_date
                    if not workorder.date_planned_start or end_date < workorder.date_planned_start:
                        vals['date_planned_start'] = end_date
                    workorder.write(vals)

                    workorder._start_nextworkorder()
                    return True
                else:
                    raise ValidationError(_("Please finish the corresponding task first !"))
            elif workorder.workcenter_id.is_subcontracted and not workorder.project_task:
                raise ValidationError(_("Please select a task !"))

            elif not workorder.workcenter_id.is_subcontracted and not workorder.project_task:
                end_date = datetime.now()
                if workorder.state in ('done', 'cancel'):
                    continue
                workorder.end_all()
                vals = {
                    'state': 'done',
                    'date_finished': end_date,
                    'date_planned_finished': end_date
                }
                if not workorder.date_start:
                    vals['date_start'] = end_date
                if not workorder.date_planned_start or end_date < workorder.date_planned_start:
                    vals['date_planned_start'] = end_date
                workorder.write(vals)

                workorder._start_nextworkorder()
                return True



class MrpWorkcenter(models.Model):
    _inherit = 'mrp.workcenter'

    is_subcontracted = fields.Boolean("Is Subcontracted")