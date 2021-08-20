import os, glob

cwd = os.getcwd()

for x in glob.glob(os.path.join(cwd, "widgets", "*")):
    # print(x)
    os.chdir(x)

    for uiName in os.listdir():
        if not uiName.endswith("Base.ui"):
            continue

        pyName = uiName.replace(".ui", ".py")

        os.system(f"pyuic5 -o {pyName} {uiName}")

        print(f"Updated {pyName}")
