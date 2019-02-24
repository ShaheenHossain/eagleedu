# -*- coding: utf-8 -*-

from odoo import fields, models, _, api
from odoo.exceptions import ValidationError


class EagleeduApplication(models.Model):
    _name = 'eagleedu.application'
    _inherit = ['mail.thread']
    _description = 'Applications for the admission'
    _order = 'id desc'

    student_name = fields.Char(string='Student Name', required=True, help="Enter name of Student")
    student_name_b = fields.Char("নামের প্রথম অংশ")

    image = fields.Binary(string='Image', help="Provide the image of the Student")
    academic_year_id = fields.Many2one('education.academic.year', related='register_id.academic_year',string='Academic Year',
    application_date = fields.Datetime('application Date',default=lambda self: fields.datetime.now()) #, default=fields.Datetime.now, required=True
    application_no = fields.Char(string='Application  No', required=True, copy=False, readonly=True,
                       index=True, default=lambda self: _('New'))

    nationality = fields.Many2one('res.country', string='Nationality', ondelete='restrict',default=19,
    cur_address = fields.Char(string='Present Address', help="Enter the Present Address")
    cur_area = fields.Char(string='Area', help="Enter the Area name")
    cur_police_station = fields.Char(string='Police Station 1', help="Enter the Police Station name")
    cur_city = fields.Char(string='City', help="Enter the City name")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict',default=19,
    is_same_address = fields.Boolean(string="Permanent Address same as above", default=True,
                                     help="Tick the field if the Present and permanent address is same")
    per_address = fields.Char(string='Permanent Address 2', help="Enter the Permenent Address")
    per_vill = fields.Char(string='Village 2', help="Enter the Village Name")
    per_po = fields.Char(string='Post Office 2', help="Enter the Post Office Name")
    per_ps = fields.Char(string='Police Station 2', help="Enter the Permanent Police Station name")
    per_dist = fields.Char(string='District 2', help="Enter the Permanent District name")
    per_country_id = fields.Many2one('res.country', string='Country', ondelete='restrict',default=19,
    date_of_birth = fields.Date(string="Date Of birth", required=True, help="Enter your DOB")
    guardian_relation = fields.Many2one('gurdian.student.relation', string="Relation to Guardian",

    #### guardian Details
    guardian_name = fields.Char(string="guardian's Name", help="Proud to say my guardian is",required=True)
    guardian_mobile = fields.Char(string="guardian's Mobile No", help="guardian's Mobile No")
    description = fields.Text(string="Note")

    #### Father Details
    father_name = fields.Char(string="Father's Name", help="Proud to say my father is",required=True)
    father_name_b = fields.Char(string="বাবার নাম", help="Proud to say my father is")
    father_NID = fields.Char(string="Father's NID", help="Father's NID")
    father_mobile = fields.Char(string="Father's Mobile No", help="Father's Mobile No")
    father_car_no = fields.Char(string="Father's Car No", help="Father's Car No")

    #### Mother Details
    mother_name = fields.Char(string="mother's Name", help="Proud to say my mother is",required=True)
    mother_name_b = fields.Char(string="মা এর নাম", help="Proud to say my mother is")
    mother_NID = fields.Char(string="mother's NID", help="mother's NID")
    mother_mobile = fields.Char(string="mother's Mobile No", help="mother's Mobile No")

    religion_id = fields.Many2one('religion.religion', string="Religion", help="My Religion is ")
    # class_id = fields.Many2one('education.class.division', string="Class")
    # active = fields.Boolean(string='Active', default=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
                              string='Gender', required=True, default='male', track_visibility='onchange',
    blood_group = fields.Selection([('a+', 'A+'), ('a-', 'A-'), ('b+', 'B+'), ('o+', 'O+'), ('o-', 'O-'),
                                    ('ab-', 'AB-'), ('ab+', 'AB+')],
                                   string='Blood Group', required=True, track_visibility='onchange',
                                   help="Your Blood Group is ")
    #state = fields.Selection([('draft', 'Draft'), ('verification', 'Verify'),
    #                          ('approve', 'Approve'), ('reject', 'Reject'), ('done', 'Done')],
    #                        string='State', required=True, default='draft', track_visibility='onchange')

    #_sql_constraints = [
    #    ('unique_student_id', 'unique(student_id)', 'Student Id must be unique'),
    #]

    @api.onchange('guardian_relation')
    def guardian_relation_changed(self):
        for rec in self:
            if rec.guardian_relation.name:
                if  rec.guardian_relation.name=='Father':
                    rec.guardian_NID=rec.father_NID
                    rec.guardian_mobile=rec.father_mobile
                    rec.guardian_car_no=rec.father_car_no
                    rec.guardian_name=rec.father_name
                elif  rec.guardian_relation.name=='Mother':
                    rec.guardian_NID = rec.mother_NID
                    rec.guardian_mobile = rec.mother_mobile
                    rec.guardian_car_no = rec.mother_car_no
                    rec.guardian_name = rec.mother_name

    @api.model
    def create(self, vals):
        """Overriding the create method and assigning the the sequence for the record"""
        if vals.get('application_no', _('New')) == _('New'):
            vals['application_no'] = self.env['ir.sequence'].next_by_code('education.application') or _('New')
        res = super(StudentApplication, self).create(vals)
        return res



    @api.multi
    def create_student(self):
        """Create student from the application and data and return the student"""
        for rec in self:
            father_id=self.env['res.partner']
            if father_id.id:
                father =father_id.id
            else:
                new_father_id=father_id.create({'name': rec.father_name,
                                                'nid_no': rec.father_NID,
                                                'mobile': rec.father_mobile,
                                                'car_no': rec.father_car_no,
                                                'name_b': rec.father_name_b,
                                                'gender': 'male',
                                                'is_parent': True})
                father=new_father_id.id
            mother_id = self.env['res.partner']
            if mother_id.id:
                mother = mother_id.id
            else:
                new_mother_id = mother_id.create({'name': rec.mother_name,
                                                  'nid_no': rec.mother_NID,
                                                  'gender': 'female',
                                                  'is_parent': True})
                mother = new_mother_id.id
            if rec.guardian_relation.name=='Father':
                guardian=father
            elif  rec.guardian_relation.name=='Mother':
                guardian=mother
            else:
                guardian_id = self.env['res.partner']
                if guardian_id.id:
                    guardian = guardian_id.id
                else:
                    new_guardian_id = guardian_id.create({'name': rec.guardian_name,
                                                          'nid_no': rec.guardian_NID,
                                                          'gender': rec.guardian_relation.gender,
                                                          'is_parent': True})
                    guardian = new_guardian_id.id
            values = {
                'student_name': rec.student_name,
                'student_name_b': rec.student_name_b,
                'application_id': rec.application_id,
                'father_name': father,
                'mother_name': mother,
                'guardian_relation': rec.guardian_relation.id,
                'guardian_name': guardian,
                'cur_address': rec.cur_address,
                'cur_area': rec.cur_area,
                'cur_police_station': rec.cur_police_station,
                'cur_city': rec.cur_city,
                'country_id': rec.country_id.id,

                'is_same_address': rec.is_same_address,
                'per_address': rec.per_address,
                'per_vill': rec.per_vill,
                'per_po': rec.per_po,
                'per_ps': rec.per_ps,
                'per_district': rec.per_district,
                'per_country_id': rec.per_country_id.id,
                #'student_category':rec.student_category,
                'gender': rec.gender,
                'date_of_birth': rec.date_of_birth,
                'blood_group': rec.blood_group,
                'email': rec.email,
                'mobile': rec.mobile,
                'phone': rec.phone,
                'image': rec.image,
                'is_student': True,
                'religion_id': rec.religion_id.id,
#                'admission_class': rec.register_id.standard.id,
#                'student_id': rec.student_id,
                # 'section_id': rec.section,
                # 'group_id': rec.group,
                # 'import_roll_no': rec.roll_no,
                'application_no': rec.application_no,
                'class_id': rec.class_id.id,
#                'roll_no': rec.roll_no,

            }
            if not rec.is_same_address:
                pass
            else:
                values.update({
                    'per_address': rec.per_address,
                    'per_vill': rec.per_vill,
                    'per_po': rec.per_po,
                    'per_ps': rec.per_ps,
                    'per_dist': rec.per_dist,
                    'per_country_id': rec.country_id.id,
                })

            student = self.env['education.student'].create(values)
            rec.write({
                'state': 'done'
            })
            return {
                'name': _('Student'),
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'education.student',
                'type': 'ir.actions.act_window',
                'res_id': student.id,
                'context': self.env.context
            }
