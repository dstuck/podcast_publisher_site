import datetime as dt
from ftplib import FTP, error_perm
import os
import xlrd

from pod_config import get_conf

CONF = get_conf()


def download_sermon_info(local_info_name='sermon_info.xlsx'):
    ftp_params = {
        'host': CONF['FTP']['host'],
        'user': CONF['FTP']['user'],
        'passwd': CONF['FTP']['password']
    }
    fcc_ftp = FTP(**ftp_params)
    fcc_ftp.cwd('/SEB/Audio')
    info_name = fcc_ftp.nlst()[-1]
    if 'sermons' not in info_name:
        raise ValueError('Bad info name: {}'.format(info_name))
    if os.path.exists(local_info_name):
        os.rename(local_info_name, 'old_' + local_info_name)
    with open(local_info_name, 'wb') as ofile:
        fcc_ftp.retrbinary('RETR %s' % info_name, ofile.write)
    workbook = xlrd.open_workbook(local_info_name)
    sheet = workbook.sheet_by_index(0)
    sermons = [sheet.row_values(n) for n in range(5, sheet.nrows)]
    columns = [x.lower().replace(' ', '_') for x in sheet.row_values(4)]
    sermon_info = [
        {key: v for key, v in zip(columns, sermon)} for sermon in sermons
    ]
    for sermon in sermon_info:
        sermon['date'] = xlrd.xldate.xldate_as_datetime(
            sermon['date'], workbook.datemode
        )
    # Add whether audio files exist
    ftp_files = []
    for year in range(2016, dt.datetime.now().year + 1):
        try:
            fcc_ftp.cwd(
                '/SEB/Audio/{0}/Processed {0} Sermons'.format(year)
            )
        except error_perm:
            continue
        ftp_files.extend(fcc_ftp.nlst())
    for sermon in sermon_info:
        for f in ftp_files:
            sermon['has_ftp_file'] = False
            if sermon['date'].strftime('%Y%m%d') in f:
                sermon['has_ftp_file'] = True
                break
    return sermon_info


def download_sermon_audio(service_date):
    tmp_local = os.path.join(
        CONF['general']['tmp_dir'], 'tmp_sermon{}.mp3'.format(
            service_date.strftime('%Y%m%d')
        )
    )
    ftp_params = {
        'host': CONF['FTP']['host'],
        'user': CONF['FTP']['user'],
        'passwd': CONF['FTP']['password']
    }
    fcc_ftp = FTP(**ftp_params)
    fcc_ftp.cwd(
        '/SEB/Audio/{0}/Processed {0} Sermons'.format(service_date.year)
    )
    files = fcc_ftp.nlst()
    cp_file = None
    for f in reversed(files):
        if service_date.strftime('%Y%m%d') in f:
            cp_file = f
            break
    if cp_file is None:
        raise IOError('No file found for ' + service_date.strftime('%Y%m%d'))
    with open(tmp_local, 'wb') as ofile:
        fcc_ftp.retrbinary('RETR %s' % cp_file, ofile.write)
    return tmp_local
