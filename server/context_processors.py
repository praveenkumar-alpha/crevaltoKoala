
def running_in_demo(request):
    try:
        import server.settings
        return {'running_in_demo': server.settings.DEMO}
    except ImportError:
        return {'running_in_demo': False}
