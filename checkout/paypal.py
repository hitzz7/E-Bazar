import sys

from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment


class PayPalClient:
    def __init__(self):
        self.client_id = "AfxnTzqKY36NDpY3IoIHldUSii9roAAFMCDYciALSif36xlMWA5v2UTINVYXr4vwolMJGdAbyh1SrFB_"
        self.client_secret = "EMV4AcmyOYDuOqV1OEnlP7FgdeWxuiGINFSt22XRmZ7rLA_qVPD7U7_dKcn3x8RxdXtY1BePceIIsLbC"
        self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)
        self.client = PayPalHttpClient(self.environment)
