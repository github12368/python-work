# -*- coding: utf-8 -*-
import re
lang="<option value=sq>阿尔巴尼亚语</option><option value=ar>阿拉伯语</option><option value=az>阿塞拜疆语</option><option value=ga>爱尔兰语</option><option value=et>爱沙尼亚语</option><option value=eu>巴斯克语</option><option value=be>白俄罗斯语</option><option value=bg>保加利亚语</option><option value=is>冰岛语</option><option value=pl>波兰语</option><option value=bs>波斯尼亚语</option><option value=fa>波斯语</option><option value=af>布尔语(南非荷兰语)</option><option value=da>丹麦语</option><option value=de>德语</option><option value=ru>俄语</option><option value=fr>法语</option><option value=tl>菲律宾语</option><option value=fi>芬兰语</option><option value=km>高棉语</option><option value=ka>格鲁吉亚语</option><option value=gu>古吉拉特语</option><option value=kk>哈萨克语</option><option value=ht>海地克里奥尔语</option><option value=ko>韩语</option><option value=ha>豪萨语</option><option value=nl>荷兰语</option><option value=gl>加利西亚语</option><option value=ca>加泰罗尼亚语</option><option value=cs>捷克语</option><option value=kn>卡纳达语</option><option value=hr>克罗地亚语</option><option value=la>拉丁语</option><option value=lv>拉脱维亚语</option><option value=lo>老挝语</option><option value=lt>立陶宛语</option><option value=ro>罗马尼亚语</option><option value=mg>马尔加什语</option><option value=mt>马耳他语</option><option value=mr>马拉地语</option><option value=ml>马拉雅拉姆语</option><option value=ms>马来语</option><option value=mk>马其顿语</option><option value=mi>毛利语</option><option value=mn>蒙古语</option><option value=bn>孟加拉语</option><option value=my>缅甸语</option><option value=hmn>苗语</option><option value=zu>南非祖鲁语</option><option value=ne>尼泊尔语</option><option value=no>挪威语</option><option value=pa>旁遮普语</option><option value=pt>葡萄牙语</option><option value=ny>齐切瓦语</option><option value=ja>日语</option><option value=sv>瑞典语</option><option value=sr>塞尔维亚语</option><option value=st>塞索托语</option><option value=si>僧伽罗语</option><option value=eo>世界语</option><option value=sk>斯洛伐克语</option><option value=sl>斯洛文尼亚语</option><option value=sw>斯瓦希里语</option><option value=ceb>宿务语</option><option value=so>索马里语</option><option value=tg>塔吉克语</option><option value=te>泰卢固语</option><option value=ta>泰米尔语</option><option value=th>泰语</option><option value=tr>土耳其语</option><option value=cy>威尔士语</option><option value=ur>乌尔都语</option><option value=uk>乌克兰语</option><option value=uz>乌兹别克语</option><option value=iw>希伯来语</option><option value=el>希腊语</option><option value=es>西班牙语</option><option value=hu>匈牙利语</option><option value=hy>亚美尼亚语</option><option value=ig>伊博语</option><option value=it>意大利语</option><option value=yi>意第绪语</option><option value=hi>印地语</option><option value=su>印尼巽他语</option><option value=id>印尼语</option><option value=jw>印尼爪哇语</option><option value=en>英语</option><option value=yo>约鲁巴语</option><option value=vi>越南语</option><option value=zh-TW>中文(繁体)</option><option SELECTED value=zh-CN>中文(简体)<"
LangChinese=re.findall('>(.*?)<',lang)
while '' in LangChinese:
    LangChinese.remove('')
LangJC=re.findall('value=(.*?)>',lang)
LangDit=dict(zip(LangJC,LangChinese))
print LangDit['en']
