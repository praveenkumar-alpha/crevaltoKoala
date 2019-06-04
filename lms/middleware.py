#
# Copyright (C) 2019 Guillaume Bernard <guillaume.bernard@loria.fr>
#
# This file is part of Koala LMS (Learning Management system)

# Koala LMS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# We make an extensive use of the Django framework, https://www.djangoproject.com/
#

from django.conf import settings
from django.contrib.auth import authenticate, login

from lms import logger


class AutoAuthenticationOnDemonstration:
    """
    Automatically login the demonstration user, if any
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.demo = getattr(settings, 'DEMO', False)
        if self.demo and hasattr(settings, 'DEMONSTRATION_LOGIN') and hasattr(settings, 'DEMONSTRATION_PASSWORD'):
            self.login = getattr(settings, 'DEMONSTRATION_LOGIN')
            self.password = getattr(settings, 'DEMONSTRATION_PASSWORD')
        else:
            raise ValueError("When you enable the demonstration server, you must provide "
                             "credentials of a user that will be connected automatically."
                             "You have to provide the login using the DEMONSTRATION_LOGIN "
                             "key in your settings and DEMONSTRATION_PASSWORD for the password.")

    def __call__(self, request):
        response = self.get_response(request)
        # This works only when running a demonstration server
        if self.demo:
            # If the user is already connected, it is not necessary to go further
            if request.user.is_anonymous:
                logger.debug("The demonstration user is set and will be logged in.")
                # noinspection PyBroadException
                try:
                    user = authenticate(request, username=self.login, password=self.password)
                    if user is not None:
                        login(request, user)
                        logger.info("User identified by %s is now connected.", self.login)
                    else:
                        logger.error(
                            "Unable to connect the demo user identified by %s, %s.",
                            self.login, self.password
                        )
                except Exception as ex:
                    logger.error(
                        "Unable to connect the demo user identified by %s, %s. Reason is %s.",
                        self.login, self.password, str(ex)
                    )
                    raise
        else:
            logger.warning("Automatic login works only when running the demonstration mode.")
        return response
