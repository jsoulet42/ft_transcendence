# backend/management/commands/createdev.py

import getpass
import signal

from django.core.management.base import BaseCommand
from backend.models import CustomUser

class Command(BaseCommand):
	help = 'Creates a development user with staff privileges'

	def handle(self, *args, **options):
		try:
			username = input("Username: ")

			while True:
				password = getpass.getpass(prompt="Password: ")
				password_confirm = getpass.getpass(prompt="Password (again): ")

				if password == password_confirm:
					break
				self.stderr.write(self.style.ERROR("Error: Your passwords didn't match."))

			try:
				dev_user = CustomUser.objects.create_dev(username, 'Non42Users', password=password)
				self.stdout.write(self.style.SUCCESS(f"Dev user '{username}' created successfully!"))
			except ValueError as e:
				self.stderr.write(self.style.ERROR(f"Error creating dev user: {e}"))

		except KeyboardInterrupt as e:
			self.stderr.write(self.style.ERROR(f"\nOperation cancelled."))
