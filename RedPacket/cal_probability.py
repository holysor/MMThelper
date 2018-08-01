from RedPacket import connect_sql as sql
from RedPacket import api
from RedPacket import config

def get_all_packet():
    '''查询数据库，获取邀请人所有红包金额及被邀请人的记录'''
    os = sql.OperationSQL('sysdb')
    compid = api.get_company_id(config.user['mobile'],config.user['password'])
    os.execute_sql('SELECT invite_person_mobile,register_person_mobile,gold,invite_no,\
    gold_pay_no,gold_pay_time FROM sysdb.sys_invite_gold_detail WHERE invite_comp_id=%s'%compid)
    os.close()
    return os.get_all_data()

def packet_statics():
    '''红包统计数据'''
    packetall = get_all_packet()
    amount= 0
    packet_100_count = 0
    packet_120_count = 0
    packet_150_count = 0
    packet_180_count = 0
    packet_200_count = 0
    packet_other_count=0

    for item in packetall:
        amount+=item[2]
        if item[2]==10000:
            packet_100_count+=1
        elif item[2]==12000:
            packet_120_count+=1
        elif item[2]==15000:
            packet_150_count+=1
        elif item[2]==18000:
            packet_180_count+=1
        elif item[2]== 20000:
            packet_200_count+=1
        else:
            packet_other_count+=1
    packet_total = len(packetall)
    packet_amount = amount
    sell_amount = 58800*packet_total
    packet_amount_percent = round(100*packet_amount/sell_amount,2)
    packer_100_percent = round(100*packet_100_count/packet_total,2)
    packer_120_percent = round(100*packet_120_count/packet_total,2)
    packer_150_percent = round(100*packet_150_count/packet_total,2)
    packer_180_percent = round(100*packet_180_count/packet_total,2)
    packer_200_percent = round(100*packet_200_count/packet_total,2)
    packer_other_percent = round(100*packet_other_count/packet_total,2)
    return len(packetall),amount/100,sell_amount/100,packet_amount_percent,packer_100_percent,\
           packer_120_percent,packer_150_percent,packer_180_percent,packer_200_percent,packer_other_percent

