import string

SPACES = " \t"
NEW_LINE = "\n"
DIGITS = "0123456789"
LETTERS = string.ascii_letters
LETTERS_DIGITS = LETTERS + DIGITS
IDENTIFIER_CHAR = LETTERS_DIGITS + "_$"
# Assignment ops are "=", "<-", and "be"
ASSIGNMENT_OP_CHAR = "=<-be"
