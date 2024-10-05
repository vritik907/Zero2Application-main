from kivy.utils import platform

if platform == "android":
    from auth_files.android.androidAuth import (
        initialize_google,
        login_google,
        logout_google,
    )

elif platform != "ios":
    from auth_files.desktop.desktopAuth import (
        initialize_google,
        login_google,
        logout_google,
    )
