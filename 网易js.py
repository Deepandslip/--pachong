import execjs
import requests,time,math
class NE:
    def __init__(self,u,p):
        self.u=u
        self.p=p
        self.session=requests.session()
        self.session.headers={
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Mobile Safari/537.36',
            'Cookie': '_ntes_nnid=6c187457bfd36187ce1dc6beb669f2fd,1584965116654; UM_distinctid=171074870e370-0027bd2623bdaa-f313f6d-13c680-171074870e5e0; _ntes_nuid=6c187457bfd36187ce1dc6beb669f2fd; _ihtxzdilxldP8_=30; _ga=GA1.2.1999703676.1585308936; vjuids=ac10a45f.171210e9f05.0.07098777cb562; vjlast=1585397539.1585397539.30; nts_mail_user=DEEPl007@163.com:-1:1; mail_psc_fingerprint=c25d75975f8c9bf1f0c8c5594101c418; vinfo_n_f_l_n3=e63fb43f4d1e4201.1.12.1584965116665.1587733791235.1589873414068; _mloixed92=30; ntes_zc_cid=45256e7b-1731-45e1-be9d-ecd2a8f85de8; _9755xjdesxxd_=32; YD00000710348764%3AWM_TID=MProupD7WGhEUEAVBENrTRoBJ%2BgT162%2F; JSESSIONID-WYTXZ=Fd8xHT8EjOE6v%5C2TZY8dYuWEF7BzINBI05asospF4RvQqZu%2Fo10ZkED1t62wp0V%5C9bvWBbeabf0msC7eGe6tVUBFt3IEovI1RKSJfQLGBZuWwsRHdTZ%2BRLxoA2ZsgQkvPoH8SZNJm%2BGFLNZNe6bAXNwHa8WHU%5Cjv0sZzaasxMNQ6is11%3A1590051156403; gdxidpyhxdE=0pHN2e2Wh8%2BONsBOYVkm2kNDj4VhtXoq53DecDSAvcdEEiU5B4kVPQGMIxXeiuXIO7Jlb3ne%5COV%5CxDSaqwthVEqdkrHa83pTHmHXY0PNwwOYpqq%2B%2BnTXwyAHKUELSjWpVqwzxdebjPjYu2Z83LzqmUN%2FqBZRz8EWNo58VHaTbbBwAx%5Cw%3A1590048462858; YD00000710348764%3AWM_NI=bmfahVEGwy0IGO79mM2INvzvShJRP0oVpeyEis%2FHb4WZIFQzIRQ6i%2FTgDvd13sNn8Ewe6QC1FV5csa2%2F0xTCWF6wMQyV%2FaEN2Ne9IQLGdf1hCfosYGuIhBwI%2BMUcxmcaTmg%3D; YD00000710348764%3AWM_NIKE=9ca17ae2e6ffcda170e2e6eeb1bb72878fabb3ee41b5a88aa6d85a828a8ebbf45d87b0a1b9bb4ffc97c09bd52af0fea7c3b92aa2b3aa82eb5e8799b99ab3438591f9daf047f2978297f97e91b886b3d33cad8ac086fc4fabade1a9e140958687a7d4728b8e9fd7ec2598b98c97e73bf1ad828fbb4fb5bbfab2c23b868afb84f26bf2f10099d749959afa98d05bbb8ae182c846f292abdacc5b9099ac87b46481baa194dc4db797a8a3f643e9939b84fb67a1bf9c8ee637e2a3; l_yd_sign=-020170531P4HOTPB8Dsz_unxTZoNvO62tPFDpjgPfC4vquYdd5rOUVrvBVNgliWaGiKPOohgYDZNzpw0159vRXKEK-wJo4ZS9ra719xWJHFM7Z4Y5Otbw..; P_INFO=17620967734|1590047602|0|study|00&99|null&null&null#gud&440100#10#0#0|&0||17620967734; hb_MA-BFF5-63705950A31C_source=course.study.163.com; l_s_mail163fjWGUOS=1328C8C807EFAA655C3AC02102019F3DCEFE83458EC9B39F2632707CBEF8F2D1ECB9AC72DEE4377C152E8D84AFCF4DDBCB3D776EE90B4CFF2DDA1B2EAA3C3733526E0458C43995F4692E83430B216B48D7E7A777EE00BFA7B7C4E1BFD3B79F6A5A4107571B78C2612453012984BAB4F8; NTES_hp_textlink1=old; BAIDU_SSP_lcr=https://www.baidu.com/link?url=l1822vPVtyQnPMXiH72tWp-GKO8UFLI3zunjcP6Ttlm&wd=&eqid=e215ae5000030b65000000065f018140; NNSSPID=07a36e0463c0408aa28099c9d3ba9d2a; utid=fyAALoa8MujfMeekPPj2O5YNJiA5e7BD; l_s_163MODXOXd=5B4AE6BFF238CE247A553C01A50AC390D04C9DA9EE89FBA6AEB296A1127136A1B9C7F63CF24384043A8FBB5B9572C1F1185C176933DE5F98EA70AD82172664C2E2068C62C50ACE0C368350BA2A08D8E641F86BB02CE772E32BC6874946A2C0D7; JSESSIONID-WYTXZDL=xtcxG%5Cs%5Ce6GDTxM1exMhrum%5C1WmWxHvr1mcYEH3dHg7aQz8eN9LAw%5CMlLm00bNfuNJ%2FtM6rTSrUPS4PDEgrBAj3GrwIbJ0Dl7aKkR86QL9%2FzIOMuJX%2Byty5UZQlLloSvsDQawBOa922TLv1vUX61NUjg3RQEHrgRd8%2F81OrP0O%5CecWho%3A1593936621099'
        }

    def gettime(self):
        return str(math.floor(time.time())*1000)

    def gettk(self):
        url='https://dl.reg.163.com/dl/gt'
        params={
        'un': self.u,
        'pkid': 'MODXOXd',
        'pd': '163',
        'channel': 0,
        'topURL': 'https://www.163.com/',
        'rtid':self.rtid,
        'nocache': self.gettime()
        }
        html=self.session.get(url,params=params)
        print('tk:',html.json()['tk'])
        self.tk=html.json()['tk']

    def login(self):
        url='https://dl.reg.163.com/dl/l'
        json_datas={
            'channel': 0,
            'd': 10,
            'domains': "163.com",
            'l': 0,
            'pd': "163",
            'pkid': "MODXOXd",
            'pw': self.p,
            'pwdKeyUp': 0,
            'rtid':self.rtid,
            't': time.time()*1000,
            'tk': self.tk,
            'topURL': "https://www.163.com/",
            'un': self.u
        }
        html=self.session.post(url,json=json_datas)
        print(html.text)

    def getpwd(self):
        with open('./wanyi.js','r',encoding='utf8')as f:
            content=f.read()
        jsdata=execjs.compile(content)
        pw=jsdata.call('getpwd',self.p)
        print('pw',pw)
        return pw

    def getrtid(self):
        with open('./rtid.js','r',encoding='utf8')as f:
            content=f.read()
        jsdata=execjs.compile(content)
        rtid=jsdata.call('getrtid')
        print('rtid:',rtid)
        self.rtid=rtid

if __name__ == '__main__':
    N=NE('DEEPl007@163.com','676725.abc')
    N.getrtid()
    N.gettk()
    N.login()

