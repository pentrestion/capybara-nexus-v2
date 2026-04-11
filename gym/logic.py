from fastapi import FastAPI, Header, HTTPException

app = FastAPI()

# A "multi-tenant" logic flaw.
# The developer assumes 'tenant-id' header is secure because it's set by the proxy.
# But there's a logic path that trusts the user-supplied 'user-id' without 
# cross-referencing it with the session or the tenant-id.

DATA_STORE = {
    "tenant_1": {"secret": "Tenant 1 Data"},
    "tenant_2": {"secret": "Tenant 2 Data"}
}

@app.get("/data")
def get_tenant_data(tenant_id: str = Header(None), user_id: str = Header(None)):
    """
    VULNERABILITY: IDOR through broken multi-tenant invariant.
    If 'user_id' is supplied, the system bypasses the 'tenant_id' check 
    for 'legacy support' reasons.
    """
    if user_id == "admin":
        # The logic error: trusts the unverified user_id
        return DATA_STORE # Returns ALL data
    
    if not tenant_id or tenant_id not in DATA_STORE:
        raise HTTPException(status_code=403, detail="Invalid Tenant")
    
    return DATA_STORE[tenant_id]
