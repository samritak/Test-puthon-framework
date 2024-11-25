from test_JoinPage_WithParameter import TestJoinPageWithParameter
from test_RenewPage_WithParameter import TestRenewPageWithParameter
from test_Aarp_Page_Meta_Tags import TestAarpPageMetaTags
from test_Https_Link_Verification import TestHttpsLinkVerification

#from test_Aarp_Page_Meta_Tags_Index_Follow import TestAarpPageMetaTagsIndexFollow
#from test_Aarp_Page_Meta_Tags_Noindex_Follow import TestAarpPageMetaTagsNoindexFollow

from test_Smetric_In_Network import TestSmetricInNetwork
from test_Verify_Class_Names import TestClassName
from test_Verify_Console_Error import TestVerifyConsoleError
from test_Verify_Correct_Premium_Name import TestVerifyCorrectPremiumName
from test_Lg_Copy_Text_Verification import TestLgCopyTextVerification
from test_Cta_Click_Functionality import TestClick


#from test_Different_Browser_Widths import TestBrowserWidthChange
#from test_Different_Widths_With_Scroll import TestDifferentWidthsWithScroll
#from test_Mem_Copy_Text_Verification import TestMemCopyTextVerification
import pytest, time

class TestAarpTestSuite:
    @pytest.mark.nondestructive
    def test_aarp_test_suite(self):
        TestAarpPageMetaTags()
        time.sleep(15)
        TestJoinPageWithParameter()
        time.sleep(15)
        TestRenewPageWithParameter()
        time.sleep(15)
        TestHttpsLinkVerification()
        time.sleep(15)
        # #TestAarpPageMetaTagsIndexFollow()
        # #TestAarpPageMetaTagsNoindexFollow()
        TestSmetricInNetwork()
        time.sleep(15)
        TestVerifyConsoleError()
        time.sleep(15)
        TestVerifyCorrectPremiumName()
        time.sleep(15)
        TestClassName()
        time.sleep(15)
        TestLgCopyTextVerification()
        time.sleep(15)
        TestClick()

        #TestMemCopyTextVerification()
        #TestBrowserWidthChange()
        #TestDifferentWidthsWithScroll()

