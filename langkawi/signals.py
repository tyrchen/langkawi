from django import dispatch

login = dispatch.Signal(providing_args=["user", "profile", "client", "request"])
connect = dispatch.Signal(providing_args=["user", "profile", "client", "request"])
