# -*- coding: utf-8 -*-
# (c) Fábio Ramon Lima e Lima - 2012
# framon@monzeu.eti.br

import web
import subprocess

class Printer:
	def __init__ (self, name):
		self.name = name
		self.location = ''
		self.description = ''


class PrintersHandler:
	def GET(self, slash):
		if slash:
			raise web.seeother('/printers')

		print web.ctx.env.get('HTTP_ACCEPT')
		template = web.template.frender('templates/printers.json')
		output = template(web.ctx.home, printers.values())
		web.header('Content-Type', output.content_type)

		return output


class PrinterHandler:
	def GET(self, name):
		printer = printers[name]
		template = web.template.frender('templates/printer.json')
		output = template(web.ctx.home, printer)
		web.header('Content-Type', output.content_type)

		return output


class JobsHandler:
	def POST(self, name):
		printer = printers[name]
		data = web.data()

		print type(data)
		print data[0:10]

		fout = open('job.pdf', 'w')
		fout.write(data)
		fout.close()

		subprocess.call(['lpr', '-H', 'printserver', '-P', name, 'job.pdf'])

		template = web.template.frender('templates/printer.json')
		output = template(web.ctx.home, printer)
		web.header('Content-Type', output.content_type)

		return output


paths = (
	'/printers(/)?', 'PrintersHandler',
	'/printers/([a-z0-9]{4})', 'PrinterHandler',
	'/printers/([a-z0-9]{4})/jobs', 'JobsHandler',
)


app = web.application(paths, globals())


printers = {
	'pt01' : Printer('pt01'), 
	'pt0e' : Printer('pt0e')
}


if __name__ == "__main__":
	app.run()

