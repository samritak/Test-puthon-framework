import pytest, time
from test_aarp_join_page_with_parameter import TestAarpJoinPageWithParameter
from test_aarp_renew_page_with_parameter import TestAarpRenewPageWithParameter
from test_aarp_meta_tags import TestAarpMetaTags
from test_aarp_https_link_verification import TestAarpHttpsLinkVerification
from test_aarp_smetric_in_network import TestAarpSmetricInNetwork
from test_aarp_verify_class_name import TestAarpVerifyClassName
from test_aarp_verify_console_error import TestAarpVerifyConsoleError
from test_aarp_verify_correct_premium_name import TestAarpVerifyCorrectPremiumName
from test_aarp_lg_copy_text_verification import TestAarpLgCopyTextVerification
from test_aarp_cta_click import TestAarpCtaClick


class TestAarpMasterChecklist:
    @pytest.mark.nondestructive
    def test_aarp_master_checklist(self):
        TestAarpMetaTags()
        time.sleep(15)
        TestAarpJoinPageWithParameter()
        time.sleep(15)
        TestAarpRenewPageWithParameter()
        time.sleep(15)
        TestAarpHttpsLinkVerification()
        time.sleep(15)
        TestAarpSmetricInNetwork()
        time.sleep(15)
        TestAarpVerifyConsoleError()
        time.sleep(15)
        TestAarpVerifyCorrectPremiumName()
        time.sleep(15)
        TestAarpVerifyClassName()
        time.sleep(15)
        TestAarpLgCopyTextVerification()
        time.sleep(15)
        TestAarpCtaClick()
