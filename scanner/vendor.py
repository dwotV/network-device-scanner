from mac_vendor_lookup import MacLookup

lookup = MacLookup()
lookup.update_vendors()

def get_vendor(mac):
    try:
        return lookup.lookup(mac)
    except:
        return 'Unknown'
