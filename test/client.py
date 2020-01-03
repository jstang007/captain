from captain import settings
import os


token_file = os.path.join(settings.TOKEN_DIR, 'token2.txt')
ca_file = os.path.join(settings.TOKEN_DIR, 'ca.crt')
print(os.path.exists(token_file))
print('{token:%s,ca:%s}' %(token_file, ca_file))