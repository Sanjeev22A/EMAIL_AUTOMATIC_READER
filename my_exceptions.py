class IMAP_CONNECTOR_FAIL_EXCEPTION(Exception):
    ##When the imap connector fails to create or when authentication to imap_connector fails
    pass

class MAIL_READ_FAILED_EXCEPTION(Exception):
    ##when reading mail fails
    pass