from RedPacket import write_excel
from RedPacket import redpacket
from RedPacket import cal_probability as cp
from RedPacket import config
import time
import os
import xlsxwriter

def run_redpacket(user,pwd,num=None,wm_text=None):
    reporttime = time.strftime('%Y-%m-%d', time.localtime())
    path = "PacketResult" + os.sep + "%s" % reporttime
    if not os.path.exists(path):
        os.makedirs(path)
    rp = redpacket.RedPacket(user,pwd,wm_text)
    if num:
        rp.work_thread_redpacket(int(num))
        invite_pass_list = rp.get_success_inviteuser()
        invite_fail_list = rp.get_fail_inviteuser()
        with open(path + os.sep + '邀请注册成功记录.txt', 'a+') as f1:
            for item in invite_pass_list:
                f1.writelines(item+'\n')
        with open(path + os.sep + '邀请注册失败记录.txt', 'a+') as f2:
            for item in invite_fail_list:
                f2.writelines(item+'\n')

    workbook = xlsxwriter.Workbook(path + os.sep + '红包概率测试结果.xlsx')
    worksheet = workbook.add_worksheet(u"红包统计")
    write_excel.write_packet_result(workbook,worksheet, cp.get_all_packet())
    workbook.close()


if __name__=='__main__':
    run_redpacket(config.user['mobile'],'111111',1)