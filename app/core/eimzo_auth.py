import base64
from asn1crypto import cms
import re

class EImzoAuth:
    @staticmethod
    def generate_challenge():
        """Generate a random challenge for the client to sign."""
        import secrets
        return secrets.token_hex(32)

    @staticmethod
    def verify_signature(challenge, pkcs7_base64):
        """
        Verify the PKCS#7 signature and extract the signer's TIN (STIR).
        Note: In a production environment, you should also verify the certificate chain 
        and the signature itself against the challenge.
        """
        try:
            pkcs7_data = base64.b64decode(pkcs7_base64)
            content_info = cms.ContentInfo.load(pkcs7_data)
            signed_data = content_info['content']
            
            # Extract certificates
            cert = signed_data['certificates'][0].chosen
            
            # Extract Subject Alternative Name or Subject for TIN
            subject = cert['tbs_certificate']['subject'].native

            # Uzbekistan certificates may store STIR/JSHSHIR in local OIDs such as
            # 1.2.860.3.16.1.1 / 1.2.860.3.16.1.2, or inside textual subject fields.
            tin = None
            candidate_values = []
            for rdn in cert['tbs_certificate']['subject'].chosen:
                for attr in rdn:
                    attr_type = attr['type'].native
                    attr_oid = attr['type'].dotted
                    val = str(attr['value'].native)
                    if (
                        attr_type in ['common_name', 'serial_number', 'userid']
                        or attr_oid.startswith('1.2.860.3.16.1.')
                    ):
                        candidate_values.append(val)

            native_values = subject.values() if isinstance(subject, dict) else []
            candidate_values.extend(str(value) for value in native_values)

            for val in candidate_values:
                for pattern in (r'\d{14}', r'\d{9}'):
                    match = re.search(pattern, val)
                    if match:
                        tin = match.group(0)
                        break
                if tin:
                    break

            if not tin:
                for cert_part in cert.native.values():
                    text = str(cert_part)
                    for pattern in (r'\d{14}', r'\d{9}'):
                        match = re.search(pattern, text)
                        if match:
                            tin = match.group(0)
                            break
                    if tin:
                        break
            
            if not tin:
                raise Exception("TIN (STIR) topilmadi.")
                
            return {
                "success": True,
                "tin": tin,
                "full_name": subject.get('common_name', 'Noma\'lum'),
                "valid_to": cert['tbs_certificate']['validity']['not_after'].native.strftime("%Y-%m-%d")
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

eimzo_auth = EImzoAuth()
