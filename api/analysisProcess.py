import os

def processInit(msgQueue):
    if os.environ.get("RUN_ANAL") != "true" and os.environ.get("RUN_MAIN") == "true":
        os.environ["RUN_ANAL"] = 'true'
        print("하이")
    for item in range(10000):
        print("하이")
