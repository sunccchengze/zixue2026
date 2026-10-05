import requests, re, json

COOKIE = (
    'EDUWEBDEVICE=438424fddf914627a6a53048bc24bafd; '
    'WM_TID=tKN693wAIONFVVUFQRadBYnYa%2FsWhqmh; '
    'hasVolume=true; videoVolume=0.8; '
    'WM_NI=kpGSn%2FLR5I2oYtfMqDOceeJCvnHBO96qYMLIePKKi0dOxrCsORyo5ZWNxdx5dVQi2ySOyjUlsMCRArVFc%2Fii%2FrGna%2B3Eo17i3cFBzDA%2FnKaRyAhDBxzC0boY9myXYVjTVEI%3D; '
    'WM_NIKE=9ca17ae2e6ffcda170e2e6eeaeee54b288aa89dc3495b08aa7d84e979f9e86e75fb59889d2c661ba938f8ef82af0fea7c3b92aa9b089b4ed25908efbaab1659bacaaaef4508dbdab86c949b6b288a3ce33f6af97aecf43a79085acec3ca891b893c2798d8eb790b8529592b885fb3fa88a9f8ab1739191b78bd868b1938db3c47a969aadd0ec63edae898fe421f19ba1d2b663f1bd8aa3f95083f1a2ace45abb9fa8a5c174ba9d0083ee53fbb3b7b9dc5eaa8c9aa6cc37e2a3; '
    'NTESSTUDYSI=9778371d40004721a72a7f3cbd0f4603; '
    'STUDY_INFO="yd.257ab665226f482a8@163.com|8|1478967543|1791173094626"; '
    'STUDY_SESS="uKrFzQzGuXczHcXr0h6l2xAOoK/ecrb3SrFPJ6oP2UIM+06ByPnctsM+7ghAV9V3OFh1yDwLU8LX/VINIkbdQ8FyVxh7rKMXb3lbDtWFfloRilI5jhaqyNzNnlIFEAVg/mTZMRYYzDDTFddmSdgvXGI2XHDPKUvjnyBtFJJ0ZJ4Lhur2Nm2wEb9HcEikV+3FTI8+lZKyHhiycNQo+g+/oA=="; '
    'STUDY_PERSIST="vejNrljP3sWq4DqD7oG4MjA5muVMOxpkCCxKRow/l4WrtDFgWPNG7mh0Sv3d3k4zJ7lkhnGYWlGrAkQKv3MMSazgtm4th2ysDk3TqUjBmny1onkeWf9uZ2uNccF80HAHW9cWT2Ihj6KIxdMigqNpZZL3G9MWkUwLl0xPTB+nqk4/9VzZUAYIVDVHViOC5JRCLoPj3Ag+JrbswAxoqvg97Hwfx5Vepjs3MW07qYRGHvZgpjCC7Iso4RP9U87vJE8LtaQzUT1ovP2MqtW5+L3Hw+PvH8+tZRDonbf7gEH7JU="; '
    'NETEASE_WDA_UID=1478967543#|#1628386399907; '
    'videoRate=1.5'
)

COURSE_ID = '1461171171'
TERM_ID = '1461946452'
COURSE_PATH = 'NJTU-1461171171'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'Cookie': COOKIE,
    'Referer': f'https://www.icourse163.org/learn/{COURSE_PATH}?tid={TERM_ID}',
    'Origin': 'https://www.icourse163.org',
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

SESSION = requests.Session()
SESSION.headers.update(HEADERS)
