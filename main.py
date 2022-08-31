import BLBL

up_uid_list = [
    '389328307', '12073864',   '355576491',  '512675827',  '38003425',   '12644002',
    '9094451',   '12677692',   '4089827',    '28703827',   '179753144',  '510555504',
    '429932577', '606465253',  '87091270',   '322721261',  '359960695',  '234381697',
    '381102886', '333935696',  '608863737',  '525661848',  '471763466',  '407280301',
    '341524801', '178690069',  '241360459',  '7683629',    '32517308',   '20051472',
    '488808353', '431342136',  '669983186',  '1108285579', '2717364',    '414702361',
    '144126440', '18697395',   '454422079',  '33817621',   '415470107',  '1791502263',
    '180468957', '873912',     '70557201',   '339820052',  '1708439640', '348478645',
    '166683234', '32703219',   '488099381',  '479003812',  '475270011',  '106450408',
    '170339078', '285315997',  '486500030',  '485601366',  '479929639',  '471266480',
    '99935025',  '43738538',   '56336108',   '526766312',  '401626423',  '395888712',
    '24987178',  '38948508',   '1309466316', '360981055',  '365655050',  '397424026',
    '481201281', '1238377223', '299876758',  '503330085',  '68459731',   '289244434',
    '28531073',  '384514829',  '417449000',  '362755776',  '539548410',  '525560606',
    '398442462', '1083710992', '18218639',   '430179984',  '316348465',  '89388451',
    '265608945', '162145289',  '57290111',   '415472469',  '66415174',   '298061175',
    '28012895',  '25649606',   '27642052',   '354561434'
]

for uid in up_uid_list:
    res = BLBL.up_info(uid)
    print(f'>>>> {uid:>16}: {res.GetUpName:>20}')










