from odoo import fields,tools,models,_,api
from odoo.exceptions import UserError, ValidationError


class CreateProject(models.TransientModel):
    _name = 'project.create'

    project = fields.Many2one('project.project', "Project Template")
    project_name = fields.Char("Project Name")

    def create_project(self):
        active_id = self._context.get('active_id')
        sale_id = self.env['sale.order'].search([('id','=',active_id)])
        task_ids = []
        if self.project_name:
            project_template={'name' : self.project_name,'type_ids':[(6, 0, self.project.type_ids.ids)]}
        else:
            raise ValidationError(_("Please provide the project name first !"))
        new_project = self.env['project.project'].create(project_template)

        for tasks in self.project.tasks:
            task = self.env['project.task'].create({
                'name' : tasks.name,
                'stage_id' : tasks.stage_id.id,
                'project_id':new_project.id
                })
            task_ids.append(task.id)
        new_project.write({'tasks':[(6, 0, task_ids)],
                           'task_ids':[(6, 0, task_ids)]})
        sale_id.sudo().write({'projects' : [(4,new_project.id)],
                       'project' : self.project.id,
                       'project_name' : self.project_name})
        return True
