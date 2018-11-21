from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait  
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
#from selenium.common.exceptions import NoSuchElementException
from time import sleep
#########################################
##### Fill in INTRANET credentials ######
#########################################
user = "aaa.bbb"
password = "xxxxxxxx"
#########################################
browser = webdriver.Firefox()
browser.implicitly_wait(3)
timeout = 5
wait = WebDriverWait(browser, 600)
sleepTimer = 0.1
currentPage = 5
url = "ecm.app.orange.intra/workflows/gsm/SitePages/Home.aspx"
baseUrl="http://" + user + ":" + password +"@" + url
global itemId
def waitForHomePage():
        try:
            element_present = EC.presence_of_element_located((By.ID, 'ctl00_onetidHeadbnnr2'))
            WebDriverWait(browser, timeout).until(element_present)
        except TimeoutException:
            print ("Timed out waiting for page to load")
            return;

# def selectProductByElementId(itemId):
#     ##### Click specific item from list
#     browser.find_element_by_xpath("(//a[@class='wfs-accessrequestbtn'])["+str(itemId)+"]").click()
#     #and contains(@onclick 'selectDevice')
#     return;

def selectPage(currentPage):
    for page in range (currentPage):
        browser.find_element_by_id('pagingWPQ2next').click()
        sleep(sleepTimer)
#        print("Page:"+str(currentPage))
    return;   
        
def selectProductByElementId(itemId):
    ##### Click New GSM Request
    browser.get ('http://ecm.app.orange.intra/workflows/gsm/_layouts/15/bws/orange/wfs/gsm/gsminit.aspx')
    sleep(sleepTimer)
    ##### Click Select Category - SH
    browser.find_element_by_xpath("//a[@class='wfs-accessrequestbtn' and contains (@onclick,'Second hand')]").click()
    sleep(sleepTimer)
  
    try:
        if (currentPage>0):
            selectPage(currentPage)
    # Exception raised when last page is reached
    except NoSuchElementException:
        pass

    sleep(sleepTimer)
    # ##### Click specific item from list
    try:
        browser.find_element_by_xpath("(//a[@class='wfs-accessrequestbtn'])["+str(itemId)+"]").click()
    except NoSuchElementException:
    #Error thrown - No more elements in the list - MEans that we reached the end of itemsId on the last page
        print("Finaly finished :P")
        browser.quit()
        sys.exit(0)
    # Print current page/itemNo
    print("Page:"+str(currentPage)+" - itemId "+str(itemId)+"/50")
    
    try:    # Item already bought ? Increase itemId &moveOn
        browser.find_element_by_id('ctl00_PlaceHolderMain_lblMsg').is_displayed()
        itemId += 1
        return
    except NoSuchElementException:      
        pass
    ##### Select paymentType
    Select(browser.find_element_by_id('WFS_GSM_PaymentType_3eec90ff-b787-41ca-90cb-bff37e875bc0_$LookupField')).select_by_visible_text("Cash/Card")
    ##### Check I confirm
    browser.find_element_by_id('WFS_GSM_SubcategoryConfirmation_7d5e1565-3663-4f0f-b76a-8e9c092e7188_$BooleanField').click()
    ##### Submit page
    browser.find_element_by_xpath("//a[@id='BWS.Orange.WFS.GSM.CustomActionsTab.CustomActionsGroup.StartWorkflow-Large']").click()  
    return;

 


# Login

browser.get(baseUrl + '/')

waitForHomePage()

while True: 
    for currentPage in range (10):
        for itemId in range (1,51):
            selectProductByElementId(itemId)            
        currentPage += 1
sys.exit()