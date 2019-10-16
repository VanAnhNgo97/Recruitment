#su dung dich vu translate cua google
from google.cloud import translate

translate_client = translate.Client()
text = """
Join in a product/system design phase with Japan team to analyze system requirements
Suggest, propose creative solutions to solve problems
Design, develop and test high-traffic Web application in Ruby on Rails (sometime do DevOps to deploy to production)
Continuously discover, evaluate, and implement new technologies to maximize development efficiency
"""
target = "vi"
translation = translate_client.translate(
	text, 
	target_language=target)
#print("english text: ", text)
#print(translation)
print("vietnamese text: ", translation["translatedText"])
source_info = translate_client.detect_language(text)
print(source_info)