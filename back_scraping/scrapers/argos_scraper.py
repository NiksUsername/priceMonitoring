import time
from datetime import datetime, timedelta

from curl_cffi import requests
from bs4 import BeautifulSoup

from back_scraping.utils import keepa_manager
from back_scraping.utils import links
from back_scraping.utils.discount_properties import is_big_discount

header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.234 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Connection': 'keep-alive',
    'Cookie': 'analytics_channel=mcomm; _abck=F00624B0353064CB97EE9E72FB0043F3~0~YAAQnzYQYA1hKA+QAQAAFZISSwzZ2/elXTTvlYJkQXwU2Jv+vCnu1r4PsNQSBYK7uoWW+D2SRRH5hGeB6k0u02otP/YGlVQsPgIkWC6y2P69blLlo5XtT1AKwRZKguxpKcNlZVGK4OXVlLdbryWMP960gf80Ej/n5QgNRyugdy+DOeze+pUGLE54ww0RXVNCi0vAgfsZp3g2HZY8p1K6T5mQ4lBDdjYOKa5FIThB9Jl3UZRbbniO4R+l3MKjJW/oDYY01QfXXpVEl84TX3+grLVg086m98+tpvCltlw24p5rvmFL1pbaEjvr09jarM8U5Ggmrqrp/zldNEKKkWurdV6Txr5JsnrILh+eJ6x8LoRckzqXQcOys5UByTtcMJoZTa9rdvIW1n6IJIQDFLZSALXL5tUYTKH5kz1abOCx9g6MiYOEFA==~-1~||0||~-1; utag_main=v_id:018dacfc0c9c004ff4950a12766c05050005700d00bd0$_sn:16$_se:43$_ss:0$_st:1719248227699$vapi_domain:argos.co.uk$dc_visit:16$ses_id:1719246080773%3Bexp-session$_pn:6%3Bexp-session$dc_event:37%3Bexp-session; sessionId=I3D82BBqnKS767BeIxicKX7TsVC0ChWsH5DyemS/TVOpxxZQzQdkHohf+9nW1V+/; cisId=f26450e37dd74c69b4f97d6306b9c289; AMCV_095C467352782EB30A490D45%40AdobeOrg=179643557%7CMCIDTS%7C19899%7CMCMID%7C87286231597634338936380337387751060019%7CMCAID%7CNONE%7CMCOPTOUT-1719253625s%7CNONE%7CvVersion%7C5.5.0; _cls_v=9da0bcf3-1541-4815-b22b-6738aa4b3584; _taggstar_vid=2dca6491-d708-11ee-8214-537a6449f81f; _taggstar_exp=v:3|id:|group:; umdid=NDZmZDA1NTEtZjViYS00ZDlhLTkwYzEtMGEwZTY4N2I1M2YwfGNhM2M1NTJkLWU4MjUtNDE2OS05YTliLTRjZDY3ZWJiZDBjOHww; syte_uuid=20b4f410-fd8d-11ee-829e-9557f3b9dbbe; syte_ab_tests={}; bm_s=YAAQnzYQYHRhKA+QAQAAhpQSSwEHNEr+4Df1opUzpTV5BZSGYhO5m3WWJJGCWvlGuoynVr97vaCvzFKMXBlTl5Zyo0i8on1yQJ4gs/kPCM4kQYGAYCwMmYPcJ5utAyv8RCl8if3DLcn6t6enl1NNMS7p3l0mqcCoQ13tkdu7tciOIm23UJ5+2G8c1dAuFGvzdSy4n30OEFZNw6QpQOxxLVA+gMVbRplPTea/M/244qGVRpI69epAGiXGfKE5n0yUnD5XkbriP1m8wZv6HsKyw2BZf523kXwTpmu+DTx0LqfxXogCVrkKhueuTzc2rYjFZmpAmjZth8BQ3z9ULkotaqAc44N7oXKP; Checkout_Test_Group_2=NEW_HD|NEW_HD_SI|NEW_HD_LI; akaas_arg_uk_global=1727022424~rv=12~id=4d85a4ff3676f113383428adf9c7242b; CONSENTMGR=consent:true%7Cts:1718444037019%7Cid:018dacfc0c9c004ff4950a12766c05050005700d00bd0; PDP_Test_Group_1=2; AWSALB=tGnCy2T3r1pW2M64oiY0x2kmIrZ1qRV9uIU3ZlB/89jXWL/allAv8J2NPNxK1HVFOV+Vj55mfODFKUcLsuXgOJ48GqalSN1TgPju4Xj6vsebSCw/vJ3y6Umpc4As; AWSALBCORS=tGnCy2T3r1pW2M64oiY0x2kmIrZ1qRV9uIU3ZlB/89jXWL/allAv8J2NPNxK1HVFOV+Vj55mfODFKUcLsuXgOJ48GqalSN1TgPju4Xj6vsebSCw/vJ3y6Umpc4As; WC_PERSISTENT=ilvrF6b4eZVFScpcv2tqkAmNX%2Bo%3D%0A%3B2024-06-24+17%3A26%3A18.758_1719246378756-13567_10151; pwd_email=new; UserPersistentSessionCookie=13918363124%3BAster%3BLOGGEDIN%3BloggedIn%3BGIFT_NO%3B10.102.16.99.1718473615020850%3BREMEMBER_NO%3B%3Bfalse%3B; PostCodeSessionCookie=%2CSW1W 0NY%2C; akaas_arg_uk_pm_dxc=100; Content_Test_Group_1=2; prev_vals=ar%3Apdp%3A2289489%3Ajeanpaulgaultierlemaleeaudetoilette-125ml%3A*%7C*ar%3Aproductdetails%3A; AMCVS_095C467352782EB30A490D45%40AdobeOrg=1; ArgosPopUp_customer1In20Chance=false; _cls_s=83163b84-2088-4dce-b68c-dc371616079d:0; Bc=d:1*1_p:0*0.005_r:null*null; akavpau_vpc_gcd=1719246990~id=5712500a39b6209bff81164dedff06ce; akavpau_vpc_pdpcd=1719247024~id=c9eb8c492924f22def110c8d2e2b5120; ufvd=~abTestVariantGroup-B~clp_29203-BG!brands_tommy-hilfiger-e!clp_29949-o!brands_amazon-o!brands_jean-paul%20gaultier-e; Apache=10.102.16.99.1718473615020850; JSESSIONID=0000eNWgKkAFlB-M97D3ZA-l019:1fa25sm9e; WC_SESSION_ESTABLISHED=true; WC_ACTIVEPOINTER=110%2C10151; UserRegistrationType=R; sids=WyI2NjEiXQ%3D%3D; WC_AUTHENTICATION_13918363124=13918363124%2CqICzQrwPpZ%2FNsB0%2B7pHF4zzvrm4%3D; WC_USERACTIVITY_13918363124=13918363124%2C10151%2Cnull%2Cnull%2C1719246378758%2C1719248178758%2Cnull%2Cnull%2Cnull%2Cnull%2CSuhX4mEjgpn7%2BChjgy61ODYCJXkbvRuJdhTvhvBDKV3tfpbU10lm3%2Fj0rD3CEib3cukey9rpjZCLbGKhdxMJNON1pjHteBTJrZDJxQlvsg1bfnSytIBmI1mR7peIzI5mdGoKnXzshZG6l7TVUX%2BIL3LkgYiG97EDRrmRIxo34Bi1WMDb6flahRcao63n8TWcfGDdyyqO21jREAUKVE5Pai8UkZuah2cYVXkBkEC5ewbO67oZ9LVXpPo3J7cDDx%2Bh; mdr_browser=Akamai; AKA_A2=A; bm_ss=ab8e18ef4e; ak_bmsc=BFD761B4A960B3DB7D155ABF8F1E1BA2~000000000000000000000000000000~YAAQnzYQYPJfKA+QAQAA/4gSSxgTT8/RHJHshBgKBIWcS1lEMW9VgUm6ahOxmAhFF7hg2WP+0PpvYQW+/yt83l06gVPiiX+PpAuCSKEgtiWIixYsM59kyf8JRMfUgpyWaP/LhaTOY0lw+MmwmUFgPC4pX+8cqXeAtI+tKigu7C8xswUB9l9V7mOJLLwK3LphguvNXxfRAJkUjHfwbmuoh+CFkhDyW1QoQcJUkirm2vcQ/GxT9LA+7n0j2aWOBgjZPR1xB3M+G6xNu9hEcx9ESbRmjbav9sdgfvCmCfJf9IhIj51aKg0zXtWWNcYmbbBvCS0pHI4GMrwmGJ1z80o0Y5Ip52NzlkGEHDUi8eK3dgwLX9BptUXh4g+VRa+lH5jmgyQulDbkjpjwLV1HupaMq9wAmwROw4yAlG1U3+Pm7H6AT/kCWczNMpppdImZ2cBPtrhhEqr44EEZdvV0deM9yRTYyuf5kaoZNdFdNxtWzLA=; bm_sz=F916C424BADCA96C010D76A1DDA29403~YAAQnzYQYPVfKA+QAQAA/4gSSxhXiY4rqj2++H5vh0D3g7wHnXCkvsJA3S/s+OHBhnVzw1cJZhn69gZu6IWXxIkcGH3T/FPtx1M1GmXun/ouwxyUO6sI6PkVspyVy7UHAWKnwgUAtx28VDUaZ5O4+d0H3MNaURRCzaSMuuhjHZSKH6hTPoSYNgj3IPgboFXgEoDEnT3n265C9RAYBU56VLpYHj1nFl5RCfCOHPocSlHFFZh0dxkF7NekaMCvAxuLtWaKwEJG2FTvWRFVJ9xoqlvynNy5LieJC1ay/E9yZXRyeBcl6resODJZQ0RDfqmhyDIc6VBSqK1q1kg6i+UQxAH48A5kgrGSItwlcEReu/HdvmMIO09pIaGOD1Ss4/ZwhPnND3pf50HTwhNbvC3TOD8ydO+QRd01NWDMfPiujO1UikhfHrfDJDyGC4gDg+rR1RA=~3553090~3551540; bm_sv=8C3DB2CB44EE905C389F384914B335FC~YAAQnzYQYHxhKA+QAQAArJQSSxhOgAXntBupPdIv8vTxfQyQEryKIrmIADsy5du63AAoJmNhusJtArtBCwoGU3JVeTfFkRriJjneEh7e+W+qrPVyVRxkyJ+612hfDBNWU6Sr0icKWvnbMiy1jifFTrBPECgsMHac6iFe3i+fx0zmrCIulpmyNfSOgWhRvQXCs1WSdO+C6uFqOc+GhfIm1LaCFZvi7J+HVlIjPTFSEBLAWpfhWl1RghcvPJl5R2eAl9g=~1; argos_cis_delay_refresh=true; stimgs={%22sessionId%22:63133477%2C%22didReportCameraImpression%22:false%2C%22newUser%22:false}; _taggstar_ses=d033c815-3245-11ef-ae80-337638bd6cbc; bm_mi=7554186C280C1683D4518A3C2A83E941~YAAQnzYQYCdXKA+QAQAA8EkSSxjccFW0MLvI1HbLU0kfJ7uSjosGJojF3KGMOTE+mSnXu2ghZUr+EQU+0S1UI48Q86QIsa0s7T95oB07KySUUDzIwxbsDiiKKcJa59TzMs+tk1wuW/TOExfcmZKSEgfYO3vdfCtY3W5xSW0JQoxV0oiOk7nBQZ6nIn0IiCu8ywG3Q4alS+sJAn4597b5CoMnSL543Pl5Dffuxh1Bkpjv3eotyxYiLhvECGIUzpqDYnpxGwLVLzysv1Dr7vZhy9SyRoh4SUVlBarRM2jGBWDXeWZJuYoGjrYwusMHPViLcAkzTi5jrOP7/Dua/FRQAy17VLqHsVqh5RbjZ4J/rQWW0HKs1yYpT8/M~1'
}

cookies = {
    "_abck": "F00624B0353064CB97EE9E72FB0043F3~0~YAAQnzYQYA1hKA+QAQAAFZISSwzZ2/elXTTvlYJkQXwU2Jv+vCnu1r4PsNQSBYK7uoWW+D2SRRH5hGeB6k0u02otP/YGlVQsPgIkWC6y2P69blLlo5XtT1AKwRZKguxpKcNlZVGK4OXVlLdbryWMP960gf80Ej/n5QgNRyugdy+DOeze+pUGLE54ww0RXVNCi0vAgfsZp3g2HZY8p1K6T5mQ4lBDdjYOKa5FIThB9Jl3UZRbbniO4R+l3MKjJW/oDYY01QfXXpVEl84TX3+grLVg086m98+tpvCltlw24p5rvmFL1pbaEjvr09jarM8U5Ggmrqrp/zldNEKKkWurdV6Txr5JsnrILh+eJ6x8LoRckzqXQcOys5UByTtcMJoZTa9rdvIW1n6IJIQDFLZSALXL5tUYTKH5kz1abOCx9g6MiYOEFA==~-1~||0||~-1",
    "_cls_s": "83163b84-2088-4dce-b68c-dc371616079d:0",
    "_cls_v": "9da0bcf3-1541-4815-b22b-6738aa4b3584",
    "_taggstar_exp": "v:3|id:|group:",
    "_taggstar_ses": "d033c815-3245-11ef-ae80-337638bd6cbc",
    "_taggstar_vid": "2dca6491-d708-11ee-8214-537a6449f81f",
    "ak_bmsc": "BFD761B4A960B3DB7D155ABF8F1E1BA2~000000000000000000000000000000~YAAQnzYQYPJfKA+QAQAA/4gSSxgTT8/RHJHshBgKBIWcS1lEMW9VgUm6ahOxmAhFF7hg2WP+0PpvYQW+/yt83l06gVPiiX+PpAuCSKEgtiWIixYsM59kyf8JRMfUgpyWaP/LhaTOY0lw+MmwmUFgPC4pX+8cqXeAtI+tKigu7C8xswUB9l9V7mOJLLwK3LphguvNXxfRAJkUjHfwbmuoh+CFkhDyW1QoQcJUkirm2vcQ/GxT9LA+7n0j2aWOBgjZPR1xB3M+G6xNu9hEcx9ESbRmjbav9sdgfvCmCfJf9IhIj51aKg0zXtWWNcYmbbBvCS0pHI4GMrwmGJ1z80o0Y5Ip52NzlkGEHDUi8eK3dgwLX9BptUXh4g+VRa+lH5jmgyQulDbkjpjwLV1HupaMq9wAmwROw4yAlG1U3+Pm7H6AT/kCWczNMpppdImZ2cBPtrhhEqr44EEZdvV0deM9yRTYyuf5kaoZNdFdNxtWzLA=",
    "AKA_A2": "A",
    "akaas_arg_uk_global": "1727022424~rv=12~id=4d85a4ff3676f113383428adf9c7242b",
    "akaas_arg_uk_pm_dxc": "100",
    "akavpau_vpc_gcd": "1719246990~id=5712500a39b6209bff81164dedff06ce",
    "akavpau_vpc_pdpcd": "1719247024~id=c9eb8c492924f22def110c8d2e2b5120",
    "AMCV_095C467352782EB30A490D45@AdobeOrg": "179643557|MCIDTS|19899|MCMID|87286231597634338936380337387751060019|MCAID|NONE|MCOPTOUT-1719253625s|NONE|vVersion|5.5.0",
    "AMCVS_095C467352782EB30A490D45@AdobeOrg": "1",
    "analytics_channel": "mcomm",
    "Apache": "10.102.16.99.1718473615020850",
    "argos_cis_delay_refresh": "true",
    "ArgosPopUp_customer1In20Chance": "false",
    "AWSALB": "tGnCy2T3r1pW2M64oiY0x2kmIrZ1qRV9uIU3ZlB/89jXWL/allAv8J2NPNxK1HVFOV+Vj55mfODFKUcLsuXgOJ48GqalSN1TgPju4Xj6vsebSCw/vJ3y6Umpc4As",
    "AWSALBCORS": "tGnCy2T3r1pW2M64oiY0x2kmIrZ1qRV9uIU3ZlB/89jXWL/allAv8J2NPNxK1HVFOV+Vj55mfODFKUcLsuXgOJ48GqalSN1TgPju4Xj6vsebSCw/vJ3y6Umpc4As",
    "Bc": "d:1*1_p:0*0.005_r:null*null",
    "bm_mi": "7554186C280C1683D4518A3C2A83E941~YAAQnzYQYCdXKA+QAQAA8EkSSxjccFW0MLvI1HbLU0kfJ7uSjosGJojF3KGMOTE+mSnXu2ghZUr+EQU+0S1UI48Q86QIsa0s7T95oB07KySUUDzIwxbsDiiKKcJa59TzMs+tk1wuW/TOExfcmZKSEgfYO3vdfCtY3W5xSW0JQoxV0oiOk7nBQZ6nIn0IiCu8ywG3Q4alS+sJAn4597b5CoMnSL543Pl5Dffuxh1Bkpjv3eotyxYiLhvECGIUzpqDYnpxGwLVLzysv1Dr7vZhy9SyRoh4SUVlBarRM2jGBWDXeWZJuYoGjrYwusMHPViLcAkzTi5jrOP7/Dua/FRQAy17VLqHsVqh5RbjZ4J/rQWW0HKs1yYpT8/M~1",
    "bm_s": "YAAQnzYQYHRhKA+QAQAAhpQSSwEHNEr+4Df1opUzpTV5BZSGYhO5m3WWJJGCWvlGuoynVr97vaCvzFKMXBlTl5Zyo0i8on1yQJ4gs/kPCM4kQYGAYCwMmYPcJ5utAyv8RCl8if3DLcn6t6enl1NNMS7p3l0mqcCoQ13tkdu7tciOIm23UJ5+2G8c1dAuFGvzdSy4n30OEFZNw6QpQOxxLVA+gMVbRplPTea/M/244qGVRpI69epAGiXGfKE5n0yUnD5XkbriP1m8wZv6HsKyw2BZf523kXwTpmu+DTx0LqfxXogCVrkKhueuTzc2rYjFZmpAmjZth8BQ3z9ULkotaqAc44N7oXKP",
    "bm_ss": "ab8e18ef4e",
    "bm_sv": "8C3DB2CB44EE905C389F384914B335FC~YAAQnzYQYHxhKA+QAQAArJQSSxhOgAXntBupPdIv8vTxfQyQEryKIrmIADsy5du63AAoJmNhusJtArtBCwoGU3JVeTfFkRriJjneEh7e+W+qrPVyVRxkyJ+612hfDBNWU6Sr0icKWvnbMiy1jifFTrBPECgsMHac6iFe3i+fx0zmrCIulpmyNfSOgWhRvQXCs1WSdO+C6uFqOc+GhfIm1LaCFZvi7J+HVlIjPTFSEBLAWpfhWl1RghcvPJl5R2eAl9g=~1",
    "bm_sz": "F916C424BADCA96C010D76A1DDA29403~YAAQnzYQYPVfKA+QAQAA/4gSSxhXiY4rqj2++H5vh0D3g7wHnXCkvsJA3S/s+OHBhnVzw1cJZhn69gZu6IWXxIkcGH3T/FPtx1M1GmXun/ouwxyUO6sI6PkVspyVy7UHAWKnwgUAtx28VDUaZ5O4+d0H3MNaURRCzaSMuuhjHZSKH6hTPoSYNgj3IPgboFXgEoDEnT3n265C9RAYBU56VLpYHj1nFl5RCfCOHPocSlHFFZh0dxkF7NekaMCvAxuLtWaKwEJG2FTvWRFVJ9xoqlvynNy5LieJC1ay/E9yZXRyeBcl6resODJZQ0RDfqmhyDIc6VBSqK1q1kg6i+UQxAH48A5kgrGSItwlcEReu/HdvmMIO09pIaGOD1Ss4/ZwhPnND3pf50HTwhNbvC3TOD8ydO+QRd01NWDMfPiujO1UikhfHrfDJDyGC4gDg+rR1RA=~3553090~3551540",
    "Checkout_Test_Group_2": "NEW_HD|NEW_HD_SI|NEW_HD_LI",
    "cisId": "f26450e37dd74c69b4f97d6306b9c289",
    "CONSENTMGR": "consent:true|ts:1718444037019|id:018dacfc0c9c004ff4950a12766c05050005700d00bd0",
    "Content_Test_Group_1": "2",
    "JSESSIONID": "0000eNWgKkAFlB-M97D3ZA-l019:1fa25sm9e",
    "mdr_browser": "Akamai",
    "PDP_Test_Group_1": "2",
    "PostCodeSessionCookie": ",SW1W 0NY,",
    "prev_vals": "ar:pdp:2289489:jeanpaulgaultierlemaleeaudetoilette-125ml:*|*ar:productdetails:",
    "pwd_email": "new",
    "sessionId": "I3D82BBqnKS767BeIxicKX7TsVC0ChWsH5DyemS/TVOpxxZQzQdkHohf+9nW1V+/",
    "sids": "WyI2NjEiXQ==",
    "stimgs": '{"sessionId":63133477,"didReportCameraImpression":false,"newUser":false}',
    "syte_ab_tests": "{}",
    "syte_uuid": "20b4f410-fd8d-11ee-829e-9557f3b9dbbe",
    "ufvd": "~abTestVariantGroup-B~clp_29203-BG!brands_tommy-hilfiger-e!clp_29949-o!brands_amazon-o!brands_jean-paul gaultier-e",
    "umdid": "NDZmZDA1NTEtZjViYS00ZDlhLTkwYzEtMGEwZTY4N2I1M2YwfGNhM2M1NTJkLWU4MjUtNDE2OS05YTliLTRjZDY3ZWJiZDBjOHww",
    "UserPersistentSessionCookie": "13918363124;Aster;LOGGEDIN;loggedIn;GIFT_NO;10.102.16.99.1718473615020850;REMEMBER_NO;;false;",
    "UserRegistrationType": "R",
    "utag_main": "v_id:018dacfc0c9c004ff4950a12766c05050005700d00bd0$_sn:16$_se:43$_ss:0$_st:1719248227699$vapi_domain:argos.co.uk$dc_visit:16$ses_id:1719246080773;exp-session$_pn:6;exp-session$dc_event:37;exp-session",
    "WC_ACTIVEPOINTER": "110,10151",
    "WC_AUTHENTICATION_13918363124": "13918363124,qICzQrwPpZ/NsB0+7pHF4zzvrm4=",
    "WC_PERSISTENT": "ilvrF6b4eZVFScpcv2tqkAmNX+o=\n;2024-06-24+17:26:18.758_1719246378756-13567_10151",
    "WC_SESSION_ESTABLISHED": "true",
    "WC_USERACTIVITY_13918363124": "13918363124,10151,null,null,1719246378758,1719248178758,null,null,null,null,SuhX4mEjgpn7+Chjgy61ODYCJXkbvRuJdhTvhvBDKV3tfpbU10lm3/j0rD3CEib3cukey9rpjZCLbGKhdxMJNON1pjHteBTJrZDJxQlvsg1bfnSytIBmI1mR7peIzI5mdGoKnXzshZG6l7TVUX+IL3LkgYiG97EDRrmRIxo34Bi1WMDb6flahRcao63n8TWcfGDdyyqO21jREAUKVE5Pai8UkZuah2cYVXkBkEC5ewbO67oZ9LVXpPo3J7cDDx+h"
}

prices = {}

temporary_discounts = {}

def get_links():
    return links.argos_links


def get_new_prices(url, page_number=1):
    response = requests.get(url+f"opt/page:{page_number}/", headers=header)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        items = soup.find_all('div', class_='ProductCardstyles__ContentBlock-h52kot-5')

        discounts_list = []
        for item in items:
            name = item.find('div', class_='ProductCardstyles__Title-h52kot-12').text.strip()
            price = float(item.find('div', class_='ProductCardstyles__PriceText-h52kot-16').text.strip().replace("£", ""))
            old_price = item.find("div", class_="ProductCardstyles__WasText-h52kot-20")
            if old_price:
                old_price = float(old_price.text.replace("Was", "").strip().replace("£", ""))
            else:
                old_price = price
            link = "https://www.argos.co.uk" + item.find('a', class_='ProductCardstyles__Link-h52kot-13')['href'].split("?")[0]
            image = f"https://media.4rgos.it/s/Argos/{link.split('/')[4].split('?')[0]}_R_SET?w=270&h=270&qlt=75&fmt.jpeg.interlaced=true"

            item_data = {
                "name": name,
                "price": price,
                "link": link,
                "old_price": old_price,
                "image": image
            }
            if link in prices:
                item_data["old_price"] = prices[link]["old_price"]
                if prices[link]["old_price"] > price and price != prices[link]["price"] and link not in temporary_discounts:
                    item_data["old_price"] = prices[link]["old_price"]
                    item_data["previous_price"] = prices[link]["price"]
                    prices[link]["price"] = price
                    discounts_list.append(item_data)
                    temporary_discounts[link] = datetime.now()
                elif link not in temporary_discounts:
                    if prices[link]["old_price"] < old_price:
                        prices[link]["old_price"] = old_price
                    prices[link]["price"] = price
            else:
                prices[link] = item_data.copy()
                item_data["old_price"] = 0
                discounts_list.append(item_data)

        item_count = int(soup.find("span", class_="styles__ResultsCount-sc-1hkcas-11")["data-search-results"])
        if 60*page_number < item_count:
            time.sleep(1)
            for discount in get_new_prices(url,page_number+1):
                discounts_list.append(discount)

        temp = temporary_discounts.items()
        for key, value in temp:
            if value < datetime.now() - timedelta(hours=12):
                temporary_discounts.pop(key)
        return discounts_list

    else:
        print("Failed to retrieve argos page")
        return []


def get_keepa_results(price_drops):
    keepa_drops = []
    for price_drop in price_drops:
        if price_drop["old_price"] == 0 or price_drop["price"]/price_drop["previous_price"] <= 0.85:
            bar_code = get_bar_code(price_drop["link"])
            if not bar_code:
                compare_price, fee, fee_percentage, asin, avg90, graph, sales_rank_drop_30, monthly_sold, percentage = keepa_manager.get_from_title(price_drop["name"])
            else:
                compare_price, fee, fee_percentage, asin, avg90, graph, sales_rank_drop_30, monthly_sold, percentage = keepa_manager.get_from_bar_code(bar_code)

            if not compare_price:
                continue
            profit = compare_price-price_drop["price"]-0.5-(compare_price/6 - price_drop["price"]/6) - fee - (compare_price*fee_percentage)
            profit_margin = profit/compare_price
            if profit_margin >= 0.15:
                margin_ping = {
                    "keepa_price": compare_price,
                    "price": price_drop["price"],
                    "name": price_drop["name"],
                    "link": price_drop["link"],
                    "margin": profit_margin,
                    "ASIN":asin,
                    "avg": avg90,
                    "image": price_drop["image"],
                    "graph": graph,
                    "rank_drop": sales_rank_drop_30,
                    "monthly_sold": monthly_sold,
                    "match_percentage": percentage
                }
                keepa_drops.append(margin_ping)
    return keepa_drops


def get_bar_code(link):
    response = requests.get(link, headers=header, cookies=cookies, impersonate="chrome120")
    soup = BeautifulSoup(response.content, 'html.parser')
    description = soup.find("div", class_="product-description-content-text")
    lines = description.find_all("li")
    if len(lines) > 0 and "EAN:" in lines[len(lines)-1].text:
        return lines[len(lines)-1].text.replace("EAN:", "").replace(".", "").strip()
    return None

