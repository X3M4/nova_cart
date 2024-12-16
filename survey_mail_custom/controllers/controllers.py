# -*- coding: utf-8 -*-
from odoo import http

# class SurveyMailCustom(http.Controller):
#     @http.route('/survey_mail_custom/survey_mail_custom/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/survey_mail_custom/survey_mail_custom/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('survey_mail_custom.listing', {
#             'root': '/survey_mail_custom/survey_mail_custom',
#             'objects': http.request.env['survey_mail_custom.survey_mail_custom'].search([]),
#         })

#     @http.route('/survey_mail_custom/survey_mail_custom/objects/<model("survey_mail_custom.survey_mail_custom"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('survey_mail_custom.object', {
#             'object': obj
#         })