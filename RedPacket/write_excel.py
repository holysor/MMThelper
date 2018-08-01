import xlsxwriter
import os
import time
from RedPacket import cal_probability as cp
from RedPacket import redpacket

def get_format(wd, option={}):
    return wd.add_format(option)

# 设置居中
def get_format_center(wd,num=1,error=None):
    if error:
        wd.add_format({'align': 'center', 'valign': 'vcenter', 'border': num,'font_color': '#ff0000'})
    return wd.add_format({'align': 'center','valign': 'vcenter','border':num})

def get_format_align(wd,num=1,align='left'):
    return wd.add_format({'bold': True,'align': align,'valign': 'vcenter','border':num})

def set_border_(wd, num=1):
    return wd.add_format({}).set_border(num)

# 写数据
def _write_center(worksheet, cl, data, wd,error=False):

    return worksheet.write(cl, data, get_format_center(wd,error=error))


def _write_left_align(worksheet, cl, data, wd):
    return worksheet.write(cl, data, get_format_align(wd))

#写入红包结果数据
def write_packet_result(workbook,worksheet,data):
    worksheet.set_column("A:A", 15)
    worksheet.set_column("B:B", 15)
    worksheet.set_column("C:C", 15)
    worksheet.set_column("D:D", 15)
    worksheet.set_column("E:E", 15)
    worksheet.set_column("F:F", 10)
    worksheet.set_column("H:H", 15)
    worksheet.set_column("J:J", 15)

    red_packet_str = '200 1%;180 5%;150 15%;120 30%;100 49%'
    worksheet.merge_range('A1:F1', u'红包奖金记账流水', get_format(workbook, {'bold': True, 'font_size': 18, 'align': 'center',
                                                                  'valign': 'vcenter', 'bg_color': 'blue','border':1,
                                                                  'font_color': '#ffffff'}))
    worksheet.merge_range('H3:J3', u'红包统计测试结果', get_format(workbook, {'bold': True, 'font_size': 18, 'align': 'center',
                                                                  'valign': 'vcenter', 'bg_color': 'blue','border':1,
                                                                  'font_color': '#ffffff'}))
    # worksheet.merge_range('J4:J13', u'红包规则:%s'%(red_packet_str), get_format(workbook, {'bold': False, 'font_size': 11, 'align': 'center',
    #                                                               'valign': 'vcenter', 'bg_color': 'green','border':1,'text_wrap':1,
    #                                                               'font_color': '#ffffff'}))
    _write_center(worksheet,'A2','邀请人手机号',workbook)
    _write_center(worksheet,'B2','被邀请人手机号',workbook)
    _write_center(worksheet, 'C2', '邀请流水号', workbook)
    _write_center(worksheet, 'D2', '支付流水号', workbook)
    _write_center(worksheet, 'E2', '支付时间', workbook)
    _write_center(worksheet,'F2','红包金额',workbook)
    _write_left_align(worksheet,'H4','红包总数(个)',workbook)
    _write_left_align(worksheet,'H5','红包总金额(元)',workbook)
    _write_left_align(worksheet,'H6','销售总额(元)',workbook)
    _write_left_align(worksheet,'H7','红包/销售(%)',workbook)
    _write_left_align(worksheet,'H8','100元占比(%)',workbook)
    _write_left_align(worksheet,'H9','120元占比(%)',workbook)
    _write_left_align(worksheet,'H10','150元占比(%)',workbook)
    _write_left_align(worksheet,'H11','180元占比(%)',workbook)
    _write_left_align(worksheet,'H12','200元占比(%)',workbook)
    _write_left_align(worksheet,'H13','其他金额占比(%)',workbook)
    _write_center(worksheet,'J4','\\',workbook)
    _write_center(worksheet,'J5','\\',workbook)
    _write_center(worksheet,'J6','\\',workbook)
    _write_left_align(worksheet,'J7','标准值:20',workbook)
    _write_left_align(worksheet,'J8','标准值:49',workbook)
    _write_left_align(worksheet,'J9','标准值:30',workbook)
    _write_left_align(worksheet,'J10','标准值:15',workbook)
    _write_left_align(worksheet,'J11','标准值:5',workbook)
    _write_left_align(worksheet,'J12','标准值:1',workbook)
    _write_left_align(worksheet,'J13','标准值:0',workbook)
    for i in range(len(data)):

        _write_center(worksheet,"A"+str(i+3),data[i][0],workbook)
        _write_center(worksheet,"B"+str(i+3),data[i][1],workbook)
        _write_center(worksheet,"C"+str(i+3),data[i][3],workbook)
        _write_center(worksheet,"D"+str(i+3),data[i][4],workbook)
        _write_center(worksheet,"E"+str(i+3),str(data[i][5]),workbook)
        _write_center(worksheet,"F"+str(i+3),float(data[i][2]/100.0),workbook)
    packet_statics = cp.packet_statics()
    count = 4
    for item in packet_statics:

        _write_left_align(worksheet,"I"+str(count),item,workbook)
        count+=1

if __name__ == '__main__':
    rp = redpacket.RedPacket()
    # rp.work_thread_redpacket(500)
    reporttime = time.strftime('%Y-%m-%d', time.localtime())
    path = "PacketResult" + os.sep + "%s" % reporttime
    if not os.path.exists(path):
        os.makedirs(path)
    workbook = xlsxwriter.Workbook(path + os.sep + '红包概率测试结果.xlsx')
    worksheet = workbook.add_worksheet(u"红包统计")
    write_packet_result(workbook,worksheet,cp.get_all_packet())
    workbook.close()