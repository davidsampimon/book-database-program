import re

regex = r"[\d]+.\d{2}"

print(re.match(regex, '99.99'))