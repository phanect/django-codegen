from django.core.management.base import BaseCommand, CommandError
from django.db import models

class Command(BaseCommand):
# 	args = '<poll_id poll_id ...>'
	help = 'Closes the specified poll for voting'

	def handle(self, *args, **options):
		if len(args) < 1:
			self.stderr.write("""error: specify a model class to generate form
e.g.
manage.py genform book.models.SampleModel""")
			return
		
		modnames = args[0].split(".")  # e.g. ["book", "models", "MoneyFlowItem"]
		
		for (count, modname) in enumerate(modnames):
			if count == 0:
				model = __import__(modname)  # arg == "book", model == book
			else:
				model = getattr(model, modname)  # model == book, arg == "models" -> model == book.models
		
		html = """<form action="/path/to/nextpage">"""
		script = ""
		script_validate = ""
		
		for field in model._meta.fields:
			
			if isinstance(field, models.DateField):
				input_tag = """<input id="%s" type="text">""" % field.name
				script = script + """$("#%s").datepicker();""" % field.name
			elif isinstance(field, models.IntegerField):
				input_tag = """<input id="%s" type="text">""" % field.name
				script_validate = script_validate + """
$("#%s").validate({
	rules: {
		field: {
			required: true,
			number: true
		}
	}
});
""" % field.name
			else:
				input_tag = """<input id="%s" type="text">"""
			
			html = html + """
	<label for="%s">%s:</label>
	%s
""" % (field.name, field.name.title(), input_tag)

		script = script + """
$("#submit").click(function() {
	$.post($(this).parent.attr("action"), function(data) {
		// Success
	})
	.done(function() {
		// Second Success
	})
	.fail(function() {
		// Error
	})
	.always(function() {
		// Finished
	});
	
	%s
});
""" % script_validate
		html = html + """
	<button id="submit" class="btn">Submit</button>
</form>

<script type="text/javascript">
%s
</script>
""" % script
		self.stdout.write('<!-- Generated from Models -->\n%s' % html)
