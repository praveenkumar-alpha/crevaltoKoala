
def running_in_demo(request):
    try:
        import server.settings as settings
        return {'running_in_demo': settings.DEMO}
    except ImportError:
        return {'running_in_demo': False}
