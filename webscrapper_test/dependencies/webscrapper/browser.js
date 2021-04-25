function checkingBrowser() {
    let userAgent = navigator.userAgent;

    const browser = {
        'Chrome' : false, 
        'Firefox' : false, 
        'MSIE' : false, 
        'Safari' : false, 
        'OP' : false, 
        'Edg' : false, 
        'Edge' : false, 
        'rv:' : false
    }
    const browserKeys = Object.keys(browser)

    for(index = 0; index < browserKeys.length; index++) {
        if(userAgent.indexOf(browserKeys[index]) > -1) {
            browser[index] = true
        }
    }

    // if both Chrome & Edge exist, the browser is then Edge //
    if(browser['Chrome'] && (browser['Edg'] || browser['Edge'])) {
        browser['Chrome'] = false
    }

    // if both Safari & Chrome exist, the browser is then Chrome //
    if(browser['Safari'] && browser['Chrome']) {
        browser['Safari'] = false
    }

    // if both Opera & Chrome exist, the browser is then Opera //
    if(browser['OP'] && browser['Chrome']) {
        browser['Chrome'] = false
    }
}

checkingBrowser()