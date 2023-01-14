CONSTANCE_CONFIG = {
    "SEND_LATE_CONTACT_ATTEMPT_3_EMAIL_TO_CLIENT_DELTA_IN_DAYS": (
        7,
        "Send late contact attempt 3 email to client after number of days",
        int,
    ),
    "CONTACT_ATTEMPT_BROKER_FOLLOW_UP_ETA_IN_SECONDS": (
        60 * 60 * 24,
        "ETA to create follow up notification and task for contact attempt statuses for brokers.",
        int,
    ),
    "CONTACT_ATTEMPT_COMPANY_OWNER_FOLLOW_UP_ETA_IN_SECONDS": (
        60 * 60 * 24,
        "ETA to create follow up notification and task for contact attempt statuses for company owners.",
        int,
    ),
    "CASE_PRODUCTS_EXPIRING_SOON_ETA_IN_MONTHS": (
        3,
        "ETA to create notifications for case products expiring soon.",
        int,
    ),
    "REGISTRATION_UUID_EXPIRATION_DELTA_IN_DAYS": (
        1,
        "Number of days after which Signup Request for registration UUID token will expire.",
        int,
    ),
    "CANCEL_SUBSCRIPTION_ADDITIONAL_MONTHS_AFTER_CYCLE_END_DELTA_IN_MONTHS": (
        1,
        "Number of months to cancel subscription after the subscription's current cycle's end.",
        int,
    ),
    "LOCK_COMPANY_AFTER_UNPAID_REGISTRATION_DELTA_IN_DAYS": (
        5,
        "Number of days after to lock the company brokers due to their unpaid subscription.",
        int,
    ),
    "DUPLICATE_LEADS_DELTA_IN_SECONDS": (
        3600,
        "Create new lead after number of seconds, else update the existing lead.",
        int,
    ),
    "CREDITS_BUNDLE_EXPIRING_REMINDER_DELTA_IN_SECONDS": (
        60 * 60 * 24,
        "Number of seconds before bundle expiration to send reminder email to company owner.",
        int,
    ),
    "REDUCE_LEAD_PRICE_DELTA_IN_SECONDS": (
        60 * 60 * 24,
        "Number of hours after which lead credits will be reduced",
        int,
    ),
    "MAX_UPLOAD_SIZE_IMAGE_IN_BYTES": (
        5 * 1024 * 1024,
        "Max file upload size in bytes. Max can be 10 MB.",  # to extend this, client_max_body_size in nginx config
        int,
    ),
    "MINIMUM_CREDITS_REMAINING_TO_ALLOW_CREDITS_BUNDLE_PURCHASE": (
        1.0,
        "Minimum number of credits which will allow user to purchase another credit bundle.",
        float,
    ),
    "LEAD_PRICE_REDUCTION_FACTOR": (
        0.5,
        "Lead credits will be reduced by some factor",
        float,
    ),
    "project_name_ACCOUNT_COMPANY_ID": (
        "",
        "Company ID from which credits will be deducted.",
        str,
    ),
    "DATE_FORMAT": (
        "%B %-d, %Y",
        "Date format (e.g. September 30, 2022)",
        str,
    ),
    "DATETIME_FORMAT": (
        "%-d %B %Y at %H:%M",
        "Date time format (e.g. 30 September 2022 at 07:30)",
        str,
    ),
    "DATETIME_DETAILED_FORMAT": (
        "%Y-%m-%dT%H:%M:%S.%f",
        "Date time detailed format (e.g. 2022-09-30 07:30:45)",
        str,
    ),
    "PHONE_NUMBER_REGION": (
        "GB",
        "Region used used to convert local phone numbers to internation format.",
        str,
    ),
    "DEFAULT_MEMBERSHIP_TYPE": (
        "SUBSCRIPTION_ONLY",
        "Default membership for company which have just been registered. Valid options: SUBSCRIPTION_ONLY, "
        "SUBSCRIPTION_AND_CREDITS",
        str,
    ),
    "UPDATES_EMAIL_ADDRESS": (
        "updates@expertmortgageadvisor.co.uk",
        "Email address for sending updates related emails.",
        str,
    ),
    "INFO_EMAIL_ADDRESS": (
        "info@project_name.co.uk",
        "Email address for sending info related emails.",
        str,
    ),
    "NO_REPLY_EMAIL_ADDRESS": (
        "no-reply@project_name.co.uk",
        "Email address for sending no-reply related emails.",
        str,
    ),
    "BILLINGS_EMAIL_ADDRESS": (
        "billings@project_name.co.uk",
        "Email address for sending billings related emails.",
        str,
    ),
    "LEADS_EMAIL_ADDRESS": (
        "leads@project_name.co.uk",
        "Email address for sending new leads emails.",
        str,
    ),
}
