import dash_bootstrap_components as dbc

def create_navbar():
    return dbc.NavbarSimple(
                brand="Youtube Analysis Platform",
                brand_href="/",
                color="primary",
                dark=True,
            )