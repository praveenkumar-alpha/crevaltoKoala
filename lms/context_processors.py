
def running_in_demo(request):
    try:
        import lms.settings as settings
        return {'running_in_demo': settings.DEMO}
    except (ImportError, AttributeError):
        return {'running_in_demo': False}
