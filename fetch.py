import json
import os
import requests
import markdown

devices=["NovaPro","NovaPlus","Nova","Nova2","Nova3","Max3","MaxLumi","Note2","NotePro","Note3","Poke3","Poke4","Poke4S","Poke2Color","Poke4Lite","NoteAir","NoteAir2","NoteAir2P","Nova3Color"]
langs=["en_US","zh_CN"]

def fetch(device, lang):
    print(f'Requesting {lang} {device}...')
    req = requests.get(f'http://data.onyx-international.cn/api/firmware/update?where=%7B%22buildNumber%22:0,%22buildType%22:%22user%22,%22deviceMAC%22:%22%22,%22lang%22:%22{lang}%22,%22model%22:%22{device}%22,%22submodel%22:%22%22,%22fingerprint%22:%22%22%7D')
    # Original http string: http://data.onyx-international.cn/api/firmware/update?where={f'"buildNumber":0,"buildType":"user","deviceMAC":"","lang":"{lang}","model":"{device}","submodel":"","fingerprint":""'}
    if (req.status_code != 200):
        return False
    device_info = json.loads(req.text)
    return device_info

def print_to_file():
    for lang in langs:
        if not os.path.exists(f'README-{lang}.md'):
            os.mknod(f'README-{lang}.md')
        f = open(f'README-{lang}.md', "r+")
        f.write("# Onyx Update Urls\n")
        for device in devices:
            info = fetch(device, lang)
            if (info != False):
                upd_create_time = info['createdAt']
                upd_update_time = info['updatedAt']
                upd_changes = info['changeList']
                upd_version = info['buildDisplayId']
                upd_fp = info['fingerprint']
                upd_dlurl_lists = info['downloadUrlList']
            
                upd_changes_formated = str("\n".join(str(e) for e in upd_changes))
                upd_dlurl_formated = str("   - \n".join(str(e) for e in     upd_dlurl_lists))
            
                f.write(f"## Device: {device}\n")
                f.write(f" - Update created time: {upd_create_time}\n")
                f.write(f" - Version: {upd_version}\n")
                f.write(f" - Fingerprint: {upd_fp}\n")
                f.write(f" - Changelog: \n")
                f.write(f"```\n")
                f.write(f"{upd_changes_formated}\n")
                f.write(f"```\n")
                f.write(f" - Download links: \n")
                f.write(f"```\n")
                f.write(f"{upd_dlurl_formated}\n")
                f.write(f"```\n")
        f.close()

if __name__ == "__main__":
    print_to_file()
