CONSTANCE_CONFIG = {
    "SOME_FIELD": (
        "Some Value",
        "Default values for field",
        str,
    ),
}

CONSTANCE_CONFIG_FIELDSETS = {
    "General Config": {
        "fields": ("SOME_FIELD",),
    },
}
