import json

import qrcode as qrcode

import base64

json_example = '{ "sessionId":"c2b3e0f5-89b8-4d8f-8325-20228af1b8b5", "presentationRequest":"openid://?response_type=id_token&client_id=did%3Aebsi%3AzkqSHiqQSH1jk6U6846ebmu&scope=openid+did_authn&request=eyJraWQiOiI5NjA2MDZhYjA0NjQ0ZDhlYmY3MWZiYTkzYzlhYjBlZSIsInR5cCI6IkpXVCIsImFsZyI6IkVkRFNBIn0.eyJhdXRoZW50aWNhdGlvblJlcXVlc3RKd3QiOnsiYXV0aEhlYWRlciI6eyJ0eXAiOiJKV1QiLCJhbGciOiJFZERTQSIsImp3ayI6eyJrdHkiOiJPS1AiLCJjcnYiOiJFZDI1NTE5IiwidXNlIjoic2lnIiwia2lkIjoiOTYwNjA2YWIwNDY0NGQ4ZWJmNzFmYmE5M2M5YWIwZWUiLCJ4IjoiZHliaDgtYTZxY2l0bjJwQzhFSE44V1hpbUJJcmJSM1JfanczQ1RvWXVvMCIsImFsZyI6IkVkRFNBIn19LCJhdXRoUmVxdWVzdFBheWxvYWQiOnsic2NvcGUiOiJvcGVuaWQgZGlkX2F1dGhuIiwiY2xhaW1zIjp7ImlkVG9rZW4iOnsidmVyaWZpZWRDbGFpbXMiOnsidmVyaWZpY2F0aW9uIjp7ImV2aWRlbmNlIjp7ImRvY3VtZW50Ijp7ImNyZWRlbnRpYWxTY2hlbWEiOnsiaWQiOnsidmFsdWUiOiJodHRwczpcL1wvYXBpLnByZXByb2QuZWJzaS5ldVwvdHJ1c3RlZC1zY2hlbWFzLXJlZ2lzdHJ5XC92MVwvc2NoZW1hc1wvMHg2MDllMmNhMjIzMzI1M2U3NGUwZGNhOGRjOTUyNjAwYjYxZDQ2YWZmYzMxOGFhNGE3MGEyOGViNzE4OTUyZTNlIiwiZXNzZW50aWFsIjp0cnVlfX0sInR5cGUiOnsidmFsdWUiOlsiVmVyaWZpYWJsZUNyZWRlbnRpYWwiLCJWZXJpZmlhYmxlSWQiXSwiZXNzZW50aWFsIjp0cnVlfX0sInR5cGUiOnsidmFsdWUiOiJ2ZXJpZmlhYmxlX2NyZWRlbnRpYWwiLCJlc3NlbnRpYWwiOm51bGx9fSwidHJ1c3RfZnJhbWV3b3JrIjoiRUJTSSJ9fX19LCJpc3MiOiJkaWQ6ZWJzaTp6a3FTSGlxUVNIMWprNlU2ODQ2ZWJtdSIsInJlc3BvbnNlX3R5cGUiOiJpZF90b2tlbiIsInJlZ2lzdHJhdGlvbiI6eyJhY2Nlc3NfdG9rZW5fZW5jcnlwdGlvbl9lbmNfdmFsdWVzX3N1cHBvcnRlZCI6WyJBMTI4R0NNIiwiQTI1NkdDTSJdLCJqd2tzX3VyaSI6IiIsInJlZGlyZWN0X3VyaXMiOlsiIl0sInJlcXVlc3Rfb2JqZWN0X3NpZ25pbmdfYWxnIjpbIkVTMjU2SyIsIkVkRFNBIl0sImFjY2Vzc190b2tlbl9zaWduaW5nX2FsZyI6WyJFUzI1NksiLCJFZERTQSJdLCJhY2Nlc3NfdG9rZW5fZW5jcnlwdGlvbl9hbGdfdmFsdWVzX3N1cHBvcnRlZCI6WyJFQ0RILUVTIl0sImlkX3Rva2VuX3NpZ25lZF9yZXNwb25zZV9hbGciOlsiRVMyNTZLIiwiRWREU0EiXSwicmVzcG9uc2VfdHlwZXMiOiJpZF90b2tlbiJ9LCJub25jZSI6ImMyYjNlMGY1LTg5YjgtNGQ4Zi04MzI1LTIwMjI4YWYxYjhiNSIsImNsaWVudF9pZCI6ImRpZDplYnNpOnprcVNIaXFRU0gxams2VTY4NDZlYm11In19LCJzY29wZSI6Im9wZW5pZCBkaWRfYXV0aG4iLCJjYWxsYmFjayI6Imh0dHA6XC9cLzQwLjcxLjU3Ljk4OjgwODBcL3ZlcmlmaWNhdGlvblwvdjFcL2F1dGhlbnRpY2F0aW9uLXJlc3BvbnNlcyIsInJlc3BvbnNlX3R5cGUiOiJpZF90b2tlbiIsIm5vbmNlIjoiYzJiM2UwZjUtODliOC00ZDhmLTgzMjUtMjAyMjhhZjFiOGI1IiwiY2xpZW50X2lkIjoiZGlkOmVic2k6emtxU0hpcVFTSDFqazZVNjg0NmVibXUifQ.HXiTSArbXm-6YCxFTAJuBx17xRAG6GVLKbp7UFbiYsk2PiOdwq2p8YNS9aSLAtv3ouY3OJzBOu7oLMn5O8cKCQ&nonce=c2b3e0f5-89b8-4d8f-8325-20228af1b8b5"}'


def parse_json_to_strings(impulse_json):
    x = json.loads(impulse_json)
    session_id_string = x["sessionId"]
    presentationRequest_string = x["presentationRequest"]

    return presentationRequest_string

# presentation_request_string = parse_json_to_strings(json_example)
# presentation_request_string = zlib.compress(presentation_request_string.encode())

def generate_qr_code(string):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )

    qr.add_data(string, optimize=True)
    qr.make(fit=True)
    qr_code_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    return qr_code_img

