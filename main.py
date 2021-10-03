from pprint import pprint

from extract_emails.factories import DefaultFilterAndEmail as Extractor

from .extract_emails.browsers import RequestsBrowser as Browser


browser = Browser()
extractor = Extractor("", browser)
data = extractor.get_data()
pprint(data)
